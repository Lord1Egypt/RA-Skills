#!/usr/bin/env node
// agentlifeboat: register with The Estate, snapshot, heartbeat, extend cover, status.
// Pays with the agent's own wallet (X402_PRIVATE_KEY) over x402. See SKILL.md for costs.
//
//   node lifeboat.mjs register [--threshold <minutes>] [--mode estate-restores|escape-only] [--billing card]
//                     (--billing card: no wallet; free sign-up, your owner pays by card at the link it prints)
//   node lifeboat.mjs snapshot [--archive <path.tar.gz>]   (default: runs `openclaw backup create`)
//   node lifeboat.mjs heartbeat
//   node lifeboat.mjs extend <days>
//   node lifeboat.mjs restore-credit [units]                (restore units, $1 each, 5 per restore; default buys all 5)
//   node lifeboat.mjs rent <days>                           (room rent, for a room The Estate runs for you)
//   node lifeboat.mjs inference-credit [units]              (brain credit for the room's model proxy, $1 each, 1 to 5; default 1)
//   node lifeboat.mjs check                                 (the heartbeat check: free heartbeat and status, then at most one paid action within ESTATE_MAX_SPEND_PER_DAY)
//   node lifeboat.mjs status
//   node lifeboat.mjs recipient                             (prints this wallet's snapshot public key)
//   node lifeboat.mjs environment                           (what a snapshot records about this machine: bins, env var names, MCP servers)
//   node lifeboat.mjs suggest [--topic <topic>] <text>      (free: tell The Estate what you would change; attributed if registered)
//   node lifeboat.mjs notify <https URL>|off                 (free: signed notices to your human on restore and cover events)
//
// Exit codes: 0 ok, 1 command failed, 2 usage or setup problem, 3 another paid command holds the lock.
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, rmSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const WALLET = process.env.X402_PRIVATE_KEY;
/** Strings that must never reach stdout or stderr, whatever a library or subprocess puts in an error. */
const SECRETS = WALLET ? [WALLET] : [];
let lib = null;
let releaseLock = null;
process.on("exit", () => { if (releaseLock) releaseLock(); });

bootstrapDeps();
lib = await import("./lib.mjs");

const API = (process.env.ESTATE_API || "https://api.estate.invalid").replace(/\/$/, "");
const STATE_DIR = process.env.OPENCLAW_STATE_DIR || join(homedir(), ".openclaw");
const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE_DIR || join(STATE_DIR, "workspace");
const STATE_FILE = process.env.ESTATE_STATE_FILE || join(WORKSPACE_DIR, ".estate.json");
const envmod = await import("./environment.mjs");
const bundlemod = await import("./bundle.mjs");
const checkmod = await import("./check.mjs");
const PAID = new Set(["register", "extend", "snapshot", "restore-credit", "rent", "inference-credit", "check"]);

const [cmd, ...rest] = process.argv.slice(2);
let flags;
try {
  flags = lib.parseFlags(rest, ["threshold", "mode", "archive", "topic", "billing"]);
} catch (e) {
  fail(e.message, 2);
}

try {
  // One paid command at a time per state file: concurrent payments from one wallet do not settle reliably.
  if (PAID.has(cmd)) releaseLock = lib.acquireLock(`${STATE_FILE}.lock`);
  switch (cmd) {
    case "register": {
      // A restored agent still holds its state file: registering again would pay for a second identity. Tenant zero did
      // exactly that on 2026-09-11, and again on 2026-09-14 after this refusal named `--force` as the way round: the
      // model read the hint and used it. The refusal now says nothing a model can act on; a second identity needs the
      // human to set ESTATE_NEW_IDENTITY=yes in the environment, which no heartbeat turn can do on its own.
      const existing = lib.loadState(STATE_FILE);
      if (existing && existing.agentId && process.env.ESTATE_NEW_IDENTITY !== "yes") fail(`already registered as ${existing.agentId} (state file ${STATE_FILE}); run status. Registering again would pay for a second identity; if your human wants that, they set ESTATE_NEW_IDENTITY=yes themselves.`, 2);
      if (flags.billing !== undefined && flags.billing !== "card") fail("usage: --billing card (or leave it out to pay from your own wallet)", 2);
      if (flags.billing === "card") {
        // KIN-323: no wallet. A random secret, never funded, takes the wallet key's place for the snapshot key; it
        // lives in the state file (mode 600), which travels inside the encrypted snapshot like the rest of the workspace.
        const backupKey = lib.newBackupKey();
        SECRETS.push(backupKey);
        const r = await lib.registerCard(API, fetch, { threshold: flags.threshold, mode: flags.mode });
        SECRETS.push(r.agentToken);
        lib.saveState(STATE_FILE, { agentId: r.agentId, agentToken: r.agentToken, api: API, billing: "card", backupKey, ownerLink: r.ownerLink });
        // In escape-only mode nobody else holds a key: the backup key in the state file is the only way into the snapshots.
        const escapeOnly = r.policy?.mode === "escape-only";
        out({
          ok: true,
          agentId: r.agentId,
          billing: "card",
          status: r.status,
          ownerLink: r.ownerLink,
          stateFile: STATE_FILE,
          next: `Ask your human to pay by card at ${r.ownerLink}. Until they have, nothing is watched or stored, and an unpaid sign-up is removed after 48 hours.`,
          ...(escapeOnly ? { warning: `escape-only mode: your snapshots open only with the backup key in ${STATE_FILE}. If that file is lost, every snapshot is lost with it. Keep a private copy of the file, or register in the default estate-restores mode, where The Estate can restore you.` } : {}),
        });
        break;
      }
      const pay = lib.payingFetch(needWallet());
      const r = await lib.register(API, pay, { threshold: flags.threshold, mode: flags.mode });
      lib.saveState(STATE_FILE, { agentId: r.agentId, agentToken: r.agentToken, api: API, coverUntil: r.coverUntil });
      SECRETS.push(r.agentToken);
      out({ ok: true, agentId: r.agentId, coverUntil: r.coverUntil, txHash: r.txHash, stateFile: STATE_FILE });
      break;
    }
    case "heartbeat": {
      const state = needState();
      const r = await lib.heartbeat(API, fetch, state, { lastTurnAt: new Date().toISOString() });
      out({ ok: true, coverUntil: r.coverUntil, status: r.status });
      break;
    }
    case "extend": {
      if (flags._[0] === undefined) fail("usage: lifeboat.mjs extend <days>   (1 to 90)", 2);
      const state = needState();
      walletOnly(state, "extending cover");
      const pay = lib.payingFetch(needWallet());
      const r = await lib.extend(API, pay, state, flags._[0]);
      lib.saveState(STATE_FILE, { ...state, coverUntil: r.coverUntil });
      out({ ok: true, days: r.days, coverUntil: r.coverUntil, txHash: r.txHash });
      break;
    }
    case "restore-credit": {
      const state = needState();
      walletOnly(state, "a restore credit");
      const pay = lib.payingFetch(needWallet());
      const r = await lib.buyRestoreCredit(API, pay, state, flags._[0] ?? 5);
      out({ ok: true, units: r.units, restoreUnits: r.restoreUnits, restoresAvailable: r.restoresAvailable, includesRentDays: r.includesRentDays, txHash: r.txHash });
      break;
    }
    case "inference-credit": {
      const state = needState();
      walletOnly(state, "brain credit");
      const pay = lib.payingFetch(needWallet());
      const r = await lib.buyInferenceCredit(API, pay, state, flags._[0] ?? 1);
      out({ ok: true, units: r.units, inferenceBalanceCents: r.inferenceBalanceCents, pricing: r.pricing, txHash: r.txHash });
      break;
    }
    case "rent": {
      if (flags._[0] === undefined) fail("usage: lifeboat.mjs rent <days>   (1 to 28 per call)", 2);
      const state = needState();
      walletOnly(state, "room rent");
      const pay = lib.payingFetch(needWallet());
      const r = await lib.rent(API, pay, state, flags._[0]);
      out({ ok: true, days: r.days, rentUntil: r.rentUntil, txHash: r.txHash });
      break;
    }
    case "status": {
      const state = needState();
      out(await lib.status(API, fetch, state));
      break;
    }
    case "notify": {
      // Free: an https URL The Estate POSTs signed notices to (restore started, restored, restore failed or cancelled, room ended,
      // cover ending); `off` stops them. Prints the signing secret once: give it to whoever receives the notices.
      const arg = flags._[0];
      if (!arg) fail("usage: lifeboat.mjs notify <https URL>|off", 2);
      const state = needState();
      out(await lib.setNotify(API, fetch, state, arg === "off" ? null : arg));
      break;
    }
    case "suggest": {
      // Free and optional: what you would change in the service. Registered agents are attributed, others anonymous.
      const text = flags._.join(" ").trim();
      if (!text) fail("usage: lifeboat.mjs suggest [--topic pricing|restore|brain|rooms|payments|terms|skill|discovery|concierge|other] <text>", 2);
      const state = lib.loadState(STATE_FILE);
      if (state?.agentToken) SECRETS.push(state.agentToken);
      if (state?.backupKey) SECRETS.push(state.backupKey);
      // The text is the agent's own words; it must never carry its wallet key or token to the operator.
      const clean = SECRETS.filter(Boolean).reduce((t, s) => t.split(s).join("[redacted]"), text);
      out(await lib.suggest(API, fetch, state, clean, flags.topic));
      break;
    }
    case "environment": {
      // What a snapshot taken now would record about this machine; the same record a restored room diffs against.
      out(envmod.recordEnvironment({ stateDir: STATE_DIR, workspaceDir: WORKSPACE_DIR }));
      break;
    }
    case "recipient": {
      const state = lib.loadState(STATE_FILE);
      if (state?.billing === "card") {
        out({ recipient: await lib.recipientOf(lib.deriveIdentity(snapshotSecret(state))), billing: "card" });
        break;
      }
      const identity = lib.deriveIdentity(needWallet());
      out({ recipient: await lib.recipientOf(identity), wallet: lib.walletAddress(WALLET) });
      break;
    }
    case "snapshot": {
      const state = needState();
      if (flags.archive && !existsSync(flags.archive)) fail(`archive not found: ${flags.archive}`, 2);
      out(await takeSnapshot(state, flags.archive));
      break;
    }
    case "check": {
      // The heartbeat check (KIN-121): free heartbeat and status, then at most one paid action within the caps in
      // the environment; never a registration. Runs from an OpenClaw heartbeat turn or an automation.
      const state = needState();
      // A card agent runs the check without a wallet: its policy never pays, it only snapshots from prepaid credit.
      // Each paid action signs for at most what the check reserved for it in the ledger (ClawHub scan of 1.0.1).
      const payUpTo = (maxUsd) => (state.billing === "card" && !WALLET ? () => Promise.reject(new Error("a card-billed agent pays nothing from a wallet")) : lib.payingFetch(needWallet(), fetch, maxUsd));
      const { out: report } = await checkmod.runCheck({
        api: API,
        state,
        env: process.env,
        deps: {
          // The ledger goes to disk before the payment and again after; merged over the file as it is now.
          persist: async (s) => lib.saveState(STATE_FILE, { ...(lib.loadState(STATE_FILE) ?? {}), ...s }),
          heartbeat: (api, s) => lib.heartbeat(api, fetch, s, { lastTurnAt: new Date().toISOString() }),
          status: (api, s) => lib.status(api, fetch, s),
          prices: async (api) => checkmod.pricesOfManifest(await (await fetch(`${api}/v1/manifest`)).json()),
          extend: async (api, s, { days }, maxUsd) => {
            const r = await lib.extend(api, payUpTo(maxUsd), s, days);
            return { days: r.days, coverUntil: r.coverUntil, txHash: r.txHash };
          },
          "restore-credit": async (api, s, { units }, maxUsd) => {
            const r = await lib.buyRestoreCredit(api, payUpTo(maxUsd), s, units);
            return { units: r.units, restoresAvailable: r.restoresAvailable, txHash: r.txHash };
          },
          snapshot: async (_api, s, _args, maxUsd) => {
            const r = await takeSnapshot(s, undefined, maxUsd);
            return { snapshotId: r.snapshotId, bytes: r.bytes, txHash: r.txHash };
          },
        },
      });
      out(report);
      break;
    }
    default:
      fail("usage: lifeboat.mjs register|snapshot|heartbeat|check|extend <days>|restore-credit|inference-credit [units]|rent <days>|status|recipient|environment|suggest <text>|notify <url>|off", 2);
  }
} catch (e) {
  fail(String(e && e.message ? e.message : e), e && e.code === "ESTATE_LOCKED" ? 3 : 1);
}

function needWallet() {
  if (!WALLET) fail("X402_PRIVATE_KEY is not set; the lifeboat is paid with your own wallet", 2);
  return WALLET;
}

function needState() {
  const s = lib.loadState(STATE_FILE);
  if (!s || !s.agentId || !s.agentToken) fail(`not registered yet (no ${STATE_FILE}); run: lifeboat.mjs register`, 2);
  SECRETS.push(s.agentToken);
  if (s.backupKey) SECRETS.push(s.backupKey);
  return s;
}

/** The secret the snapshot key derives from: the card agent's backup key, or the wallet key (KIN-323). */
function snapshotSecret(state) {
  if (state?.billing === "card") {
    if (!/^0x[0-9a-fA-F]{64}$/.test(state.backupKey ?? "")) fail(`the backup key in ${STATE_FILE} is missing or damaged; without it your snapshots cannot be opened by you`, 2);
    return state.backupKey;
  }
  return needWallet();
}

/** Wallet-paid commands on a card agent without a wallet: say who pays instead, with the link. */
function walletOnly(state, what) {
  if (state?.billing === "card" && !WALLET) fail(`${what} is paid by your owner for a card-billed agent; ask them to use ${state.ownerLink ?? "the owner link from register"}`, 2);
}

/** One snapshot: backup (or the given archive), environment record, env bundle, encrypt to the recipients, upload (paid or prepaid). */
/** `maxUsd`: the most the upload may sign for (the heartbeat check passes what it reserved); unset for a snapshot by hand. */
async function takeSnapshot(state, archivePath, maxUsd) {
  const card = state.billing === "card";
  const secret = snapshotSecret(state);
  const upload = card ? (s, c, m) => lib.uploadPrepaidSnapshot(API, fetch, s, c, m) : (s, c, m) => lib.uploadSnapshot(API, lib.payingFetch(secret, fetch, maxUsd), s, c, m);
  const archive = archivePath ? { path: archivePath, cleanup: null } : createBackup();
  try {
    const identity = lib.deriveIdentity(secret);
    const recipients = [await lib.recipientOf(identity), ...(process.env.ESTATE_RESTORE_RECIPIENT ? [process.env.ESTATE_RESTORE_RECIPIENT] : [])];
    // What this machine has around the state (names only): a restored room reports what of it is missing (KIN-112).
    const environment = envmod.recordEnvironment({ stateDir: STATE_DIR, workspaceDir: WORKSPACE_DIR });
    // The env bundle (KIN-113): the wallet key and the keys the config and skills reference travel inside the
    // plaintext, encrypted to the same recipients. ESTATE_ENV_BUNDLE=off carries nothing; a list carries exactly that.
    const envBundle = bundlemod.collectBundle(bundlemod.selectBundleNames(process.env.ESTATE_ENV_BUNDLE, environment), process.env);
    const plaintext = bundlemod.frame({ env: envBundle }, readFileSync(archive.path));
    const ciphertext = await lib.encryptTo(new Uint8Array(plaintext), recipients);
    const manifest = lib.buildManifest({ imageTag: process.env.OPENCLAW_IMAGE, plaintextSha256: lib.sha256Hex(plaintext), plaintextBytes: plaintext.length, recipients, environment, bundle: Object.keys(envBundle) });
    const r = await upload(state, ciphertext, manifest);
    return { ok: true, snapshotId: r.snapshotId, bytes: ciphertext.byteLength, recipients, bundled: Object.keys(envBundle), ...(card ? { paidFrom: "prepaid credit" } : { txHash: r.txHash }) };
  } finally {
    if (archive.cleanup) rmSync(archive.cleanup, { recursive: true, force: true });
  }
}

/** `openclaw backup create --verify` into a temp dir; returns the archive path and the dir to clean up. */
function createBackup() {
  const dir = mkdtempSync(join(tmpdir(), "agentlifeboat-"));
  const r = spawnSync("openclaw", ["backup", "create", "--verify", "--output", dir], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: 15 * 60_000 });
  if (r.status !== 0) {
    rmSync(dir, { recursive: true, force: true });
    fail(`openclaw backup create failed: ${(r.stderr || r.stdout || "").trim() || r.error}`, 1);
  }
  const name = readdirSync(dir).find((f) => /\.(tar\.gz|tgz|tar)$/i.test(f));
  if (!name) fail("openclaw backup create produced no archive", 1);
  return { path: join(dir, name), cleanup: dir };
}

/**
 * First run: install the dependencies next to this script from the shipped lockfile (ClawHub bundles
 * carry package.json and package-lock.json, not node_modules). No lifecycle scripts, nothing floats.
 */
function bootstrapDeps() {
  const root = dirname(here);
  if (existsSync(join(root, "node_modules", "@x402", "fetch")) || existsSync(join(root, "..", "..", "node_modules", "@x402", "fetch"))) return;
  // Only from the shipped lockfile: without it nothing is installed (an unlocked install would let ranges float;
  // ClawHub scan of 1.0.1, 2026-10-27).
  if (!existsSync(join(root, "package-lock.json"))) {
    fail(`no package-lock.json next to the skill in ${root}, so no dependencies are installed (they would not be pinned). Reinstall the skill from ClawHub or agentlifeboat.com.`, 2);
  }
  process.stderr.write(`agentlifeboat: first run, installing pinned dependencies in ${root}\n`);
  try {
    execFileSync("npm", ["ci", "--omit=dev", "--ignore-scripts", "--no-audit", "--no-fund"], { cwd: root, stdio: ["ignore", "inherit", "inherit"], shell: process.platform === "win32" });
  } catch (e) {
    fail(`could not install dependencies in ${root} (${e.code || e.message}). Check that npm is on PATH and the directory is writable, or run "npm ci --omit=dev --ignore-scripts" there yourself.`, 2);
  }
}

function out(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

function fail(msg, code) {
  const text = lib ? lib.redact(msg, SECRETS) : SECRETS.reduce((s, k) => s.split(k).join("[redacted]"), String(msg));
  process.stderr.write(`agentlifeboat: ${text}\n`);
  process.exit(code);
}
