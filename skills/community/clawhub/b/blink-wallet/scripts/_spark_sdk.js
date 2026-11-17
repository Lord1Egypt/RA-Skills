/**
 * Blink Claw Skill — Breez Spark SDK wrapper (OPTIONAL, non-custodial)
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * SPIKE / PROOF-OF-CONCEPT. This is the client-side path for NON-CUSTODIAL
 * (Spark) account operations that require signing — most importantly SEND, but
 * also balance/history reads straight from the wallet.
 *
 * It wraps the standalone Node.js build of the Breez Spark SDK,
 *   `@breeztech/breez-sdk-spark`
 * which is a WASM package that runs headless in Node (no React Native, no
 * browser `init()`). This is DISTINCT from `@breeztech/breez-sdk-spark-react-native`
 * that blink-mobile uses.
 *
 * WHY THIS IS DIFFERENT FROM THE REST OF blink-skills
 * ---------------------------------------------------
 *  - It requires the account's 12/24-word SEED (`SPARK_MNEMONIC`). Whoever runs
 *    it can spend the funds. This is a genuine custody shift: the whole point of
 *    a non-custodial account is that the user holds the keys. Handle with care.
 *  - It pulls a large (~63 MB) optional native/WASM dependency, breaking the
 *    project's "zero runtime dependencies" invariant. It is therefore an
 *    OPTIONAL dependency and lazy-loaded — nothing here runs unless a
 *    `spark-*` command is invoked.
 *  - It needs Node.js 22+ (WASM requirements of the SDK).
 *
 * SECURITY RULES (enforced/observed here):
 *  - The seed is read ONLY from the `SPARK_MNEMONIC` environment variable.
 *    Unlike BLINK_API_KEY, we do NOT scan shell rc files for a seed.
 *  - The seed is never logged, echoed, or written anywhere by this module.
 *  - No API change to Blink is involved — this is a pure client capability.
 * ─────────────────────────────────────────────────────────────────────────────
 */

const os = require('os');
const path = require('path');
const crypto = require('crypto');

const SPARK_PACKAGE = '@breeztech/breez-sdk-spark';
const DEFAULT_NETWORK = 'mainnet';

/**
 * Lazily load the Breez Spark SDK. Throws a clear, actionable error if the
 * optional dependency is not installed.
 * @returns {object} The SDK module (connect, defaultConfig, ...).
 */
function loadSdkModule() {
  // The SDK package probes for optional MySQL storage backends at require() time
  // and prints several noisy "mysql2 not found" warnings to the console before
  // any of our code runs. We use file storage (storageDir), so this is harmless
  // — silence console during the require, then restore it. This is the only way
  // to suppress it: the messages predate the SDK logger (initLogging).
  const saved = { log: console.log, warn: console.warn, error: console.error };
  const noop = () => {};
  console.log = noop;
  console.warn = noop;
  console.error = noop;
  try {
    // Logging is silenced in connect() (awaited, before the SDK connects) —
    // loadSdkModule is sync and must stay so.
    return require(SPARK_PACKAGE);
  } catch (err) {
    // Restore before throwing so the error is actually visible.
    console.log = saved.log;
    console.warn = saved.warn;
    console.error = saved.error;
    throw new Error(
      `The Breez Spark SDK (${SPARK_PACKAGE}) is not installed.\n` +
        `Non-custodial send/balance/history requires it. Install with:\n` +
        `    npm install ${SPARK_PACKAGE}\n` +
        `and ensure you are on Node.js 22+.\n` +
        `Original load error: ${err.message}`,
    );
  } finally {
    console.log = saved.log;
    console.warn = saved.warn;
    console.error = saved.error;
  }
}

/**
 * Route every SDK log entry to a noop sink. This covers only entries that
 * flow through the SDK's Rust/WASM logger (initLogging). It does NOT cover
 * the Node-side storage chatter — "Skipping redundant payment event: …" is
 * a direct console.debug call (see suppressSdkStdoutNoise) — so both
 * mechanisms are applied for the full connection lifetime. Best-effort:
 * older SDK builds without initLogging are left as-is, and a rejection here
 * must never break connecting.
 * @param {object} mod  the loaded SDK module
 */
async function silenceSdkLogger(mod) {
  try {
    if (mod && typeof mod.initLogging === 'function') {
      await mod.initLogging({ log: () => {} });
    }
  } catch {
    // Never let log silencing interfere with SDK availability.
  }
}

/**
 * Require Node 22+ (SDK constraint).
 */
function requireNode22() {
  const major = parseInt(process.versions.node.split('.')[0], 10);
  if (major < 22) {
    throw new Error(`The Breez Spark SDK requires Node.js 22+. Current version: ${process.versions.node}.`);
  }
}

/**
 * Validate a mnemonic's BIP39 checksum.
 *
 * A word count alone is not validation: twelve arbitrary dictionary words pass
 * it, and a single mistyped word then derives a DIFFERENT, valid, empty wallet.
 * The user sees a zero balance and no error, which looks like fund loss.
 *
 * FAILS CLOSED. This function has exactly two outcomes: it returns true because
 * the checksum verified, or it throws. It must never return false, and it must
 * never conflate "the validator could not run" with "the seed is fine" — that
 * conflation IS the vulnerability, because it silently disables the very
 * control that prevents deriving the wrong wallet. A missing validator is
 * therefore a hard error, distinguishable by `e.code`:
 *
 *   MNEMONIC_VALIDATOR_UNAVAILABLE — `bip39` is not installed.
 *   MNEMONIC_INVALID_CHECKSUM      — the phrase is not a valid BIP39 mnemonic.
 *
 * @param {string} mnemonic
 * @returns {true}
 * @throws {Error} If the validator is unavailable or the checksum is invalid.
 */
function validateMnemonicChecksum(mnemonic) {
  let bip39;
  try {
    bip39 = require('bip39');
  } catch (err) {
    const e = new Error(
      'Cannot verify SPARK_MNEMONIC: the `bip39` package is not installed, so the BIP39 ' +
        'checksum check cannot run. Refusing to continue unverified — an unnoticed typo in ' +
        'the seed derives a different, valid, EMPTY wallet, which looks exactly like losing ' +
        'your funds. Install it with:\n' +
        '    npm install bip39\n' +
        'Note that `npm install --omit=optional` and `--omit=dev` both skip it.\n' +
        `Original load error: ${err.message}`,
    );
    e.code = 'MNEMONIC_VALIDATOR_UNAVAILABLE';
    throw e;
  }
  if (!bip39.validateMnemonic(mnemonic)) {
    // Deliberately does not echo the mnemonic or name the offending word.
    const e = new Error(
      'SPARK_MNEMONIC failed BIP39 checksum validation. The word count is right but the ' +
        'phrase is not a valid BIP39 mnemonic — usually a mistyped or transposed word. ' +
        'Connecting anyway would silently derive a different, empty wallet.',
    );
    e.code = 'MNEMONIC_INVALID_CHECKSUM';
    throw e;
  }
  return true;
}

/**
 * Read the non-custodial account seed from the environment.
 *
 * SECURITY: env var only — no rc-file scanning for seeds. Never logged.
 *
 * Fails closed: the BIP39 checksum MUST verify before the seed is returned. If
 * the validator cannot run, this throws rather than proceeding unverified.
 *
 * @returns {string} The BIP39 mnemonic.
 * @throws {Error} If unset, the wrong length, or the checksum cannot be verified.
 */
function getMnemonic() {
  const mnemonic = process.env.SPARK_MNEMONIC;
  if (!mnemonic || !mnemonic.trim()) {
    throw new Error(
      'SPARK_MNEMONIC not set. Non-custodial operations that sign transactions require the ' +
        'account seed (12/24 BIP39 words) in the SPARK_MNEMONIC environment variable. ' +
        'This grants spend authority — never share or log it.',
    );
  }
  const words = mnemonic.trim().split(/\s+/);
  if (words.length !== 12 && words.length !== 24) {
    throw new Error('SPARK_MNEMONIC must be a 12 or 24 word BIP39 mnemonic.');
  }
  const normalized = words.join(' ');
  validateMnemonicChecksum(normalized);
  return normalized;
}

/**
 * Resolve the Breez API key (required by the SDK to reach the Spark service).
 * @returns {string}
 */
function getBreezApiKey() {
  const key = process.env.BREEZ_API_KEY;
  if (!key || !key.trim()) {
    throw new Error('BREEZ_API_KEY not set. The Breez Spark SDK requires a Breez API key to connect.');
  }
  return key.trim();
}

/**
 * Compute a stable, per-seed storage directory for the SDK's local state.
 * We derive a non-reversible id from the mnemonic so different accounts get
 * different dirs, without writing the seed to disk in any readable form.
 * @param {string} mnemonic
 * @param {string} network
 * @returns {string}
 */
function storageDirFor(mnemonic, network) {
  const id = crypto.createHash('sha256').update(mnemonic).digest('hex').slice(0, 16);
  return path.join(os.homedir(), '.blink', 'spark', `${network}-${id}`);
}

/**
 * Verify the SDK's SQLite storage backend can actually be opened.
 *
 * The Node build of the Spark SDK stores wallet state in SQLite via
 * `better-sqlite3`, a NATIVE module that must be compiled at install time. When
 * npm runs with `--ignore-scripts` (common in CI, sandboxes and locked-down
 * corporate installs) the package is unpacked but never built, and the SDK
 * SUPPRESSES the resulting warning. `require()` of the SDK then succeeds, so
 * everything looks installed — and each `spark-*` command instead fails deep
 * inside `connect()` with `Could not locate the bindings file`.
 *
 * We do NOT probe the SDK's own `defaultStorage()` factory: in 0.23.1 that
 * factory is lazy — it returns an object without opening a database, so the
 * probe passes even when the native binding is absent, which is exactly the
 * failure this preflight exists to catch. Instead we require `better-sqlite3`
 * directly and open a database ourselves. `better-sqlite3` is already the
 * SDK's own dependency, so this adds nothing new to the install.
 *
 * @throws {Error} If the native binding cannot be required or a database cannot
 *         be opened.
 */
function assertStorageAvailable() {
  let betterSqlite3;
  try {
    // Resolve from the SDK's own tree so we test the SAME copy the SDK will
    // load, not a possibly-different hoisted one.
    const sdkPath = require.resolve(SPARK_PACKAGE);
    betterSqlite3 = require(require.resolve('better-sqlite3', { paths: [sdkPath] }));
  } catch (err) {
    // If we cannot even resolve the SDK package, the problem is the SDK install
    // layout, not better-sqlite3's compilation — name it differently so the
    // remediation isn't a rebuild that can't help.
    if (err && err.code === 'MODULE_NOT_FOUND' && /breez-sdk-spark/.test(String(err.message))) {
      const e = new Error(
        `Could not resolve the Breez Spark SDK (${SPARK_PACKAGE}) to probe its storage backend. ` +
          `Reinstall it: npm install ${SPARK_PACKAGE}. Original error: ${err.message}`,
      );
      e.code = 'SPARK_STORAGE_UNAVAILABLE';
      throw e;
    }
    throw storageUnavailableError(err);
  }

  try {
    const probe = new betterSqlite3(':memory:');
    try {
      probe.prepare('SELECT 1 AS ok').get();
    } finally {
      probe.close();
    }
  } catch (err) {
    // The bindings file is missing or unloadable: present, but not compiled.
    throw storageUnavailableError(err);
  }
}

/**
 * Build the actionable SPARK_STORAGE_UNAVAILABLE error. The remediation names
 * the package-manager build-script approval step, because on pnpm/yarn and on
 * npm with an install-scripts allowlist, a bare `npm rebuild` exits 0 while
 * still not producing a usable binding — verify by opening a database, not by
 * trusting the rebuild exit code.
 *
 * @param {Error} err
 * @returns {Error}
 */
function storageUnavailableError(err) {
  const e = new Error(
    `The Breez Spark SDK is installed but its SQLite storage backend is not usable.\n` +
      `${SPARK_PACKAGE} stores wallet state through the native module \`better-sqlite3\`,\n` +
      `which must be COMPILED during install.\n\n` +
      `This usually means the install ran without build scripts enabled. Approve and\n` +
      `run the build for your package manager, then VERIFY it by opening a database —\n` +
      `a rebuild can exit 0 while still not producing a working binding:\n` +
      `    npm:    npm rebuild better-sqlite3   (if scripts were blocked, allow them)\n` +
      `    pnpm:   pnpm approve-builds  then  pnpm rebuild better-sqlite3\n` +
      `    yarn:   yarn rebuild better-sqlite3\n` +
      `Building requires python3, make and a C++ compiler (build-essential).\n` +
      `Original storage error: ${err.message}`,
  );
  e.code = 'SPARK_STORAGE_UNAVAILABLE';
  return e;
}

/**
 * Create the wallet-state dir owner-only and FAIL CLOSED if that cannot be
 * established.
 *
 * Without `mode`, mkdirSync honours the umask (0775 under a typical 022), so
 * group users could traverse or modify state belonging to a seed-controlled
 * Bitcoin wallet. We therefore:
 *   1. reject a symlink (or any non-directory) at the target — a pre-placed
 *      symlink could redirect the wallet state somewhere an attacker controls;
 *   2. create with mode 0700 and chmod unconditionally so a permissively
 *      created dir from an earlier run is repaired;
 *   3. VERIFY the postcondition — no group or world bits may remain — and throw
 *      if they do. A swallowed chmod failure that left the dir at 0777 must be
 *      a hard error, not a silent pass, because connect() is about to write
 *      seed-controlled wallet state there.
 *
 * @param {string} dir
 * @throws {Error} SPARK_STORAGE_PERMISSIONS if owner-only cannot be established.
 */
function ensureOwnerOnlyDir(dir) {
  const fs = require('fs');
  const path = require('path');

  const refuse = (message) => {
    const e = new Error(message);
    e.code = 'SPARK_STORAGE_PERMISSIONS';
    return e;
  };

  // Reject symlinks at the target and within the MANAGED ancestor chain —
  // ~/.blink and ~/.blink/spark — but no higher. Two boundaries matter:
  //
  //   - Do NOT walk above the Blink-owned root (~/.blink). Ancestors above it
  //     (the home dir, /home -> /usr/home, managed /Users on macOS) are not
  //     attacker-controlled wallet state, so their being symlinks is legitimate
  //     and must not refuse the command.
  //   - For a path OUTSIDE home (a custom storage path, or a tmpdir-based test),
  //     the tool owns nothing above the leaf. Walking such a path to the root
  //     would hit legitimately-symlinked system dirs — macOS's /var ->
  //     /private/var makes os.tmpdir() itself unreachable this way — so for
  //     out-of-home paths we scan only the leaf.
  //
  // (TOCTOU note: a symlink swapped in AFTER these lstat checks but before chmod
  // is an advisory-only gap against an active local attacker — closing it needs
  // fd-based O_NOFOLLOW, which is out of scope here.)
  const managedRoot = path.join(os.homedir(), '.blink');
  const resolved = path.resolve(dir);
  const managed = [resolved];
  if (resolved.startsWith(managedRoot + path.sep) || resolved === managedRoot) {
    // Under the Blink root: walk up to and including ~/.blink, then stop.
    let cur = resolved;
    while (cur !== managedRoot) {
      cur = path.dirname(cur);
      managed.push(cur);
    }
  }
  // else: out-of-home path — scan only the leaf.
  // The leaf is `managed[0]`; for an in-home path the rest are the managed
  // ancestors (~/.blink/spark, ~/.blink). Reject a symlink at any of them.
  for (const p of managed) {
    let lst;
    try {
      lst = fs.lstatSync(p);
    } catch (err) {
      if (err && err.code === 'ENOENT') continue; // not created yet
      throw err;
    }
    if (lst.isSymbolicLink()) {
      const isLeaf = p === managed[0];
      throw refuse(
        `Refusing to use wallet-state path '${dir}': ${isLeaf ? 'the path' : `ancestor '${p}'`} is a symlink, which could redirect seed-controlled wallet state. Remove it or point storage elsewhere.`,
      );
    }
  }

  // Reject a non-directory AT the target.
  try {
    const lst = fs.lstatSync(dir);
    if (!lst.isDirectory()) {
      throw refuse(
        `Refusing to use wallet-state path '${dir}': it exists but is not a directory. Remove it or point the storage elsewhere.`,
      );
    }
  } catch (err) {
    if (err && err.code === 'SPARK_STORAGE_PERMISSIONS') throw err;
    if (!err || err.code !== 'ENOENT') throw err;
  }

  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(dir, 0o700);
  } catch (err) {
    // A chmod failure is only fatal if the dir is NOT already owner-only. On
    // filesystems where chmod is unsupported (some network FS) an already-0700
    // dir must be usable; a permissive one must still fail closed.
    let mode = null;
    try {
      mode = fs.statSync(dir).mode & 0o777;
    } catch {
      /* fall through to the throw below */
    }
    if (mode !== null && (mode & 0o077) === 0) return; // already secure
    throw refuse(
      `Could not make the wallet-state dir owner-only at '${dir}': ${err.message}. ` +
        'Wallet state belongs to a seed-controlled account and must not be group/world accessible.',
    );
  }

  // Verify the postcondition rather than trusting the calls above.
  const mode = fs.statSync(dir).mode & 0o777;
  if ((mode & 0o077) !== 0) {
    throw refuse(
      `Wallet-state dir '${dir}' has mode ${mode.toString(8)} after hardening; group/world bits must be 0. ` +
        'Refusing to write seed-controlled wallet state there.',
    );
  }
}

/**
 * Canonicalize an operator-supplied LNURL domain to a bare lowercase hostname
 * with an optional explicit port ("host" or "host:port"). DNS hostnames are
 * case-insensitive, a trailing root dot is equivalent, and :443 is the HTTPS
 * default — so byte-equality against a refused name is NOT a real guard:
 * "BREEZ.TIPS", "breez.tips.", and "breez.tips:443" all target the same
 * service. This normalizes those spellings and rejects anything that is not
 * a bare hostname (URLs with scheme/path/query/fragment, embedded whitespace,
 * malformed labels, empty input).
 *
 * @param {string} raw
 * @returns {{ host: string, port: string|null, canonical: string }}
 */
function canonicalizeLnurlDomain(raw) {
  const domainError = (why) => {
    const err = new Error(
      `SPARK_LNURL_DOMAIN is invalid (${why}) — expected a bare hostname like 'blink.sv', optionally with an explicit port.`,
    );
    err.code = 'SPARK_LNURL_DOMAIN_INVALID';
    return err;
  };

  const trimmed = String(raw ?? '').trim();
  if (!trimmed) throw domainError('empty');
  if (/\s/.test(trimmed)) throw domainError('embedded whitespace');
  if (/[/?#%]/.test(trimmed)) throw domainError('URL path/query/fragment characters');
  if (trimmed.includes('://')) throw domainError('a scheme — supply the hostname only');

  let host = trimmed.toLowerCase();
  let port = null;
  const portMatch = host.match(/^(.*):(\d{1,5})$/);
  if (portMatch) {
    host = portMatch[1];
    port = portMatch[2];
    if (!host) throw domainError('missing hostname before the port');
    // TCP ports are 1-65535 — the regex alone would let :0, :65536 and :99999
    // through (review round 1 nit, PR #13; hardened here in v2.6.0).
    const portNum = Number(port);
    if (portNum < 1 || portNum > 65535) throw domainError('port must be 1-65535');
  }
  // Exactly one trailing root dot is the canonical FQDN form — strip it.
  if (host.endsWith('.')) host = host.slice(0, -1);
  if (!host) throw domainError('hostname only a root dot');
  if (host.includes(':')) throw domainError('more than one colon');
  // DNS-label grammar: labels of [a-z0-9]([a-z0-9-]*[a-z0-9])?, joined by dots.
  if (!/^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*$/.test(host)) {
    throw domainError('malformed hostname');
  }
  return { host, port, canonical: port ? `${host}:${port}` : host };
}

/**
 * The Lightning-address domain for a Spark wallet connection. blink-skills is
 * a BLINK skill: Lightning addresses are always registered on Blink domains —
 * 'breez.tips' (the Breez SDK's own default) is deliberately refused IN ANY
 * EQUIVALENT SPELLING (case, root dot, explicit port), because a
 * registration landing there would create an address this skill's ecosystem
 * (blink.sv LNURL routing, resolve-receiver) can never see.
 *
 * The SDK's defaultConfig('mainnet').lnurlDomain is 'breez.tips' and regtest
 * has none — which is why every connect() MUST set this explicitly, exactly
 * as blink-mobile does (config.lnurlDomain = 'blink.sv').
 *
 * Precedence: SPARK_LNURL_DOMAIN env (other Blink domains / private
 * deployments; canonicalized + validated) > per-network default.
 *
 * @param {string} network  'mainnet' | 'regtest'
 * @returns {string}
 */
function lnurlDomainFor(network) {
  const fromEnv = process.env.SPARK_LNURL_DOMAIN;
  if (fromEnv) {
    const { host, canonical } = canonicalizeLnurlDomain(fromEnv);
    if (host === 'breez.tips') {
      throw new Error(
        `SPARK_LNURL_DOMAIN='${canonical}' is not permitted: blink-skills registers Lightning addresses on Blink domains only (blink.sv / staging.blink.sv), never on the Breez default domain.`,
      );
    }
    return canonical;
  }
  return network === 'mainnet' ? 'blink.sv' : 'staging.blink.sv';
}

/**
 * Cross-check that the LNURL management service is actually reachable.
 *
 * getLightningAddress() reads a cache filled by the SDK's recovery-on-connect,
 * and that recovery fails SILENTLY — observed live (2026-09-12, blink.sv):
 * the management endpoints 404'd while a registered address existed, so
 * getLightningAddress() returned null and callers reported `registered: false`
 * as a verified fact (a false negative; the address really was registered and
 * routable). This probe distinguishes "no address" from "cannot know":
 *
 * A null cache is only trustworthy when the service answers a benign lookup
 * for a username that can never collide with a real claim (fresh random
 * `zz<digits>` passes both client and server username rules). If even that
 * throws, the service is unreachable and any "not registered" answer is
 * unverified.
 *
 * Epistemic limit (deliberate): the probe proves the LNURL SERVICE is
 * reachable — a necessary, not sufficient, condition for the SDK's
 * identity-keyed recovery route having run. They are distinct service
 * operations, and a deployment could serve availability checks while the
 * recovery route is broken (the reverse of the observed outage). The
 * definitive client-side fix is a server-side pubkey→address lookup
 * (blink-lnurl-server#43); until then, 'verified' means "service reachable",
 * which is the strongest claim available without it.
 *
 *
 * @param {object} sdk  connected SDK instance
 * @returns {Promise<{ healthy: boolean, error: string|null }>}
 */
async function probeLnLookupHealthy(sdk) {
  const probeUsername = 'zz' + String(Math.floor(Math.random() * 1e10)).padStart(10, '0');
  try {
    await sdk.checkLightningAddressAvailable({ username: probeUsername });
    return { healthy: true, error: null };
  } catch (e) {
    return { healthy: false, error: safeErrorDetail(e) };
  }
}

/**
 * SDK stdout-noise suppression — a reference-counted lease around a single
 * process-global filtering wrapper (review round 2, PR #16: per-connection
 * save/restore corrupted overlapping lifecycles — closing connection A
 * restored the original console.debug while B still needed suppression, and
 * closing B then restored A's noop, leaving debug permanently muted).
 *
 * What is suppressed and why: the pinned SDK's Node storage emits
 * "Skipping redundant payment event: …" DIRECTLY via console.debug
 * (nodejs/storage/index.cjs:362-364 — same in the mysql/postgres storage
 * variants) whenever a duplicate payment update is applied, i.e. whenever
 * cached events replay after recent payment activity (observed live in
 * field tests 2/3: spark_balance and spark_send emitted SDK lines into
 * stdout, breaking the all-JSON contract). console.debug is an alias of
 * console.log in Node — stdout. The message does not flow through the
 * Rust/WASM logger that initLogging configures.
 *
 * Lease semantics: the FIRST active connection installs ONE wrapper that
 * forwards unrelated console.debug calls untouched and drops only the known
 * noise prefix; the LAST lease to close restores the original — and only if
 * console.debug is still our wrapper, so a third-party replacement that
 * appeared meanwhile is never clobbered. Releases are idempotent (duplicate
 * disconnect is a no-op), so overlapping connections in any close order keep
 * stdout protected exactly while at least one is active.
 *
 * @returns {() => void} release function — call when the connection ends
 *   (or fails to open); safe to call more than once.
 */
const SDK_STDOUT_NOISE_PREFIX = 'Skipping redundant payment event';
let stdoutNoiseLease = null; // { count, savedDebug, wrapper } | null

function suppressSdkStdoutNoise() {
  if (typeof console.debug !== 'function') return () => {};
  if (!stdoutNoiseLease) {
    const savedDebug = console.debug;
    const wrapper = (...args) => {
      const first = args.length > 0 ? String(args[0]) : '';
      if (first.startsWith(SDK_STDOUT_NOISE_PREFIX)) return; // known SDK noise
      return savedDebug.apply(console, args); // everything else flows through
    };
    console.debug = wrapper;
    stdoutNoiseLease = { count: 0, savedDebug, wrapper };
  }
  stdoutNoiseLease.count += 1;
  let released = false;
  return () => {
    if (released || !stdoutNoiseLease) return; // idempotent / already drained
    released = true;
    stdoutNoiseLease.count -= 1;
    if (stdoutNoiseLease.count === 0) {
      // Restore only OUR wrapper — if a third party replaced console.debug
      // while we were active, theirs stays (ours comes off with it anyway).
      if (console.debug === stdoutNoiseLease.wrapper) {
        console.debug = stdoutNoiseLease.savedDebug;
      }
      stdoutNoiseLease = null;
    }
  };
}

/**
 * Connect to the Breez Spark SDK using the seed from SPARK_MNEMONIC.
 *
 * Setting lnurlDomain makes the SDK's automatic recover_lightning_address
 * (run on connect against config.lnurlDomain, keyed by the seed-derived
 * identity pubkey) query the Blink server — so a seed imported from
 * blink-mobile with a registered user@blink.sv address has that address
 * recovered into the local cache, where getLightningAddress() returns it.
 *
 * @param {object} [opts]
 * @param {string} [opts.network]  "mainnet" (default) or "regtest".
 * @param {number} [opts.disconnectTimeoutMs]  How long the returned
 *   disconnect() waits for the SDK before returning (default 5000). The
 *   stdout-noise lease is NOT bound to this timeout — it releases only when
 *   the SDK's real disconnect settles. Injectable for tests.
 * @returns {Promise<{ sdk: object, disconnect: () => Promise<void> }>}
 */
async function connect({ network = DEFAULT_NETWORK, disconnectTimeoutMs = 5000 } = {}) {
  requireNode22();
  const mod = loadSdkModule();
  const mnemonic = getMnemonic();
  const apiKey = getBreezApiKey();

  const config = mod.defaultConfig(network);
  config.apiKey = apiKey;
  config.lnurlDomain = lnurlDomainFor(network);

  const storageDir = storageDirFor(mnemonic, network);
  ensureOwnerOnlyDir(storageDir);

  // Fail fast with a build-tools message rather than an opaque bindings error.
  assertStorageAvailable();

  // Silence SDK logging (awaited — no race with the first payment) and hold
  // the stdout guard for the ENTIRE connection lifetime: the duplicate-event
  // replay that pollutes stdout happens any time after connect, not just at
  // load (see suppressSdkStdoutNoise).
  await silenceSdkLogger(mod);
  const restoreQuiet = suppressSdkStdoutNoise();

  let sdk;
  try {
    sdk = await mod.connect({
      config,
      seed: { type: 'mnemonic', mnemonic, passphrase: undefined },
      storageDir,
    });
  } catch (err) {
    restoreQuiet();
    throw err;
  }

  // The lease is owned by the SDK's ACTUAL shutdown, not by the caller's
  // wait (review round 3, PR #16): on a hung sdk.disconnect(), the old code
  // released the noise guard when the 5s race timed out — while the SDK's
  // still-pending storage/event workers could emit "Skipping redundant
  // payment event" to stdout after the command's JSON. The real disconnect
  // is memoized ONCE, kept non-rejecting, and releases the lease only when
  // IT settles; the public disconnect() merely bounds how long the CALLER
  // waits. disconnectTimeoutMs is injectable so tests can exercise the
  // timeout path without a real 5-second stall.
  let rawDisconnect = null;
  const startDisconnect = () => {
    if (!rawDisconnect) {
      rawDisconnect = Promise.resolve()
        .then(() => sdk.disconnect())
        .catch(() => {}) // non-rejecting by contract — callers rely on this
        .finally(restoreQuiet); // the lease follows the REAL settlement
    }
    return rawDisconnect;
  };
  const disconnect = async () => {
    // Bounded AND non-rejecting by contract: the SDK's disconnect can hang or
    // reject; cleanup must never block the caller or mask a payment outcome.
    // Callers that inject alternate connectors (tests) still guard at their
    // own layer — see the comments in spark_send.js and l402_pay_spark.js.
    await Promise.race([startDisconnect(), new Promise((resolve) => setTimeout(resolve, disconnectTimeoutMs))]);
  };

  return { sdk, disconnect };
}

/**
 * Normalize the SDK's getInfo() response into a stable shape.
 * The SDK exposes balance as `balanceSats` (a BigInt in some builds).
 * @param {object} info
 * @returns {{ balanceSats: number }}
 */
function normalizeInfo(info) {
  const raw = info && info.balanceSats !== null && info.balanceSats !== undefined ? info.balanceSats : 0;
  return { balanceSats: Number(raw) };
}

const MAX_SAFE = BigInt(Number.MAX_SAFE_INTEGER);
const MIN_SAFE = BigInt(-Number.MAX_SAFE_INTEGER);

/**
 * Recursively normalize an SDK value for JSON output.
 *
 * JSON.stringify cannot represent two SDK shapes:
 *   - BigInt (throws)        → Number when safe, String when it would round
 *     unsafely (large token balances must never silently lose precision).
 *   - Map (always "{}")      → plain object with recursively normalized
 *     values. The pinned SDK returns tokenBalances as Map<string,
 *     TokenBalance>; a JSON round-trip would report a wallet WITH tokens
 *     as holding none.
 * Arrays and plain objects are normalized recursively; primitives pass through.
 *
 * Shared SDK-to-CLI adapter: any command printing raw SDK payloads should use
 * this rather than a JSON round-trip.
 */
function normalizeSdkValue(value) {
  if (typeof value === 'bigint') {
    return value <= MAX_SAFE && value >= MIN_SAFE ? Number(value) : value.toString();
  }
  if (value instanceof Map) {
    const out = {};
    for (const [k, v] of value) out[String(k)] = normalizeSdkValue(v);
    return out;
  }
  if (Array.isArray(value)) return value.map(normalizeSdkValue);
  if (value && typeof value === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(value)) out[k] = normalizeSdkValue(v);
    return out;
  }
  return value;
}

/**
 * Read a balance that is stable, not a mid-sync transient.
 *
 * Right after an incoming Spark payment, `getInfo({ ensureSynced: true })` can
 * return before the payment finishes claiming, so a naive read can be
 * transiently low (observed live: 2000 -> 1176 -> 2200). This polls until the
 * balance repeats across two consecutive reads, or a bounded timeout elapses,
 * whichever comes first.
 *
 * The deadline starts AFTER the first read, not before it. The first read
 * carries the sync and can cost more than the entire polling budget (measured
 * 6.35s against SDK 0.23.1, versus a 5s default budget); timing from before it
 * meant the loop never ran, `prev` stayed null, and the final `cur === prev`
 * compared against null — reporting `stable: false` for a balance that had not
 * moved. Subsequent reads are effectively free (~0-1ms) once synced.
 *
 * @param {object} sdk
 * @param {object} [opts]
 * @param {number} [opts.maxWaitMs]   Cap on the comparison window, excluding
 *                                    the initial sync read (default 5000).
 * @param {number} [opts.intervalMs]  Poll interval (default 1000).
 * @returns {Promise<{ balanceSats: number, stable: boolean }>}
 */
async function waitForStableBalance(sdk, { maxWaitMs = 5000, intervalMs = 1000 } = {}) {
  let prev = null;
  // First read — carries the sync, so it is timed separately from the window.
  let cur = normalizeInfo(await sdk.getInfo({ ensureSynced: true })).balanceSats;
  const deadline = Date.now() + maxWaitMs;
  while (Date.now() < deadline) {
    if (prev !== null && cur === prev) {
      return { balanceSats: cur, stable: true };
    }
    await new Promise((r) => setTimeout(r, intervalMs));
    prev = cur;
    cur = normalizeInfo(await sdk.getInfo({ ensureSynced: true })).balanceSats;
  }
  // Timed out — return the last read, flagged as not confirmed-stable. `prev`
  // is null when only one read was taken, which is unconfirmed, not equal.
  return { balanceSats: cur, stable: prev !== null && cur === prev };
}

/**
 * Normalize a single Payment record from listPayments() defensively across
 * SDK versions.
 *
 * Token payments (method 'token' / details.type 'token') carry amounts in
 * TOKEN BASE UNITS, not sats — funnelling them into amountSats mislabels a
 * $0.999 USDB receive as "999,001 sats" (~$770 at 1293 sats/$; observed in
 * live field test 3). Token rows therefore emit amountSats/feeSats: null and
 * carry the base-unit amount as a precision string plus token metadata,
 * mirroring the tokenBalances shape (balance string + decimals + formatted).
 * @param {object} p
 * @returns {object}
 */
function normalizePayment(p) {
  if (!p || typeof p !== 'object') return { raw: p };
  const has = (v) => v !== null && v !== undefined;

  // The SDK `Payment` shape (v0.18) uses `amount` and `fees` (both bigint).
  // Fall back to older/alt field names defensively.
  const amount = has(p.amount) ? p.amount : p.amountSats;
  let fee = null;
  if (has(p.fees)) fee = p.fees;
  else if (has(p.feesSats)) fee = p.feesSats;
  else if (has(p.feeSats)) fee = p.feeSats;

  const base = {
    id: p.id || p.paymentHash || p.txId || null,
    type: p.paymentType || p.type || null, // "send" | "receive"
    status: p.status || null,
    timestamp: has(p.timestamp) ? Number(p.timestamp) : null,
  };

  const details = p.details && typeof p.details === 'object' ? p.details : null;
  if (p.method === 'token' || (details && details.type === 'token')) {
    const meta = (details && details.metadata && typeof details.metadata === 'object' && details.metadata) || {};
    const decimals = has(meta.decimals) ? meta.decimals : null;
    return {
      ...base,
      asset: 'token',
      amountSats: null,
      feeSats: null,
      amountBaseUnits: has(amount) ? String(amount) : null,
      feeBaseUnits: has(fee) ? String(fee) : null,
      amountFormatted: has(amount) && decimals !== null ? formatTokenAmount(amount, decimals) : null,
      token: {
        ticker: meta.ticker || null,
        name: meta.name || null,
        decimals,
        identifier: meta.identifier || meta.tokenIdentifier || null,
      },
    };
  }

  return {
    ...base,
    asset: 'btc',
    amountSats: has(amount) ? Number(amount) : null,
    feeSats: has(fee) ? Number(fee) : null,
  };
}

function feeFromPrepare(prepareResponse) {
  // Fee location varies by destination type / SDK version:
  //  - LNURL-pay prepare response:      top-level `feeSats`
  //  - bolt11Invoice send method:       `lightningFeeSats` (+ optional `sparkTransferFeeSats`)
  //  - sparkAddress send method:        `fee` (string)
  //  - older builds:                    `feeSats` on paymentMethod
  const has = (v) => v !== null && v !== undefined;
  // Non-finite results (NaN/Infinity from a malformed SDK value) read as
  // "unknown" (null), never as a fee an agent might quote or budget with.
  const num = (v) => {
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };
  if (!has(prepareResponse)) return null;

  // LNURL: top-level feeSats.
  if (has(prepareResponse.feeSats)) return num(prepareResponse.feeSats);

  const pm = prepareResponse.paymentMethod;
  if (!pm) return null;

  if (has(pm.feeSats)) return num(pm.feeSats);

  // bolt11Invoice: lightning fee (+ spark transfer fee if the route uses Spark).
  // A composite with one non-finite PRESENT component is an unknowable total —
  // return null (unknown) rather than a deceptively valid partial sum.
  if (has(pm.lightningFeeSats)) {
    const fee = num(pm.lightningFeeSats);
    if (fee === null) return null;
    if (has(pm.sparkTransferFeeSats)) {
      const transfer = num(pm.sparkTransferFeeSats);
      if (transfer === null) return null;
      return fee + transfer;
    }
    return fee;
  }
  if (has(pm.sparkTransferFeeSats)) return num(pm.sparkTransferFeeSats);

  // sparkAddress: `fee` (may be a string).
  if (has(pm.fee)) return num(pm.fee);
  return null;
}

/**
 * Safely extract a human-readable detail from ANY thrown/rejected value.
 * Property access and string coercion can both throw — a null-prototype
 * object has no toString, and a Proxy may have throwing traps — so a warning
 * built from `${e.message}` would itself throw and replace the real outcome
 * (see l402_pay_spark.js's dispatch catch). Use this in every catch that
 * must not throw.
 *
 * @param {*} value
 * @returns {string}
 */
function safeErrorDetail(value) {
  try {
    return value && typeof value.message === 'string' ? value.message : String(value);
  } catch {
    return '(non-coercible error value)';
  }
}

// ── Token (BTKN) helpers ─────────────────────────────────────────────────────

/**
 * USDB token identifier on Spark MAINNET (issued by Brale; 6 decimals).
 * Override for other networks (regtest has its own identifier) or testing
 * with the SPARK_USDB_TOKEN env var.
 */
const USDB_TOKEN_MAINNET = 'btkn1xgrvjwey5ngcagvap2dzzvsy4uk8ua9x69k82dwvt5e7ef9drm9qztux87';

/**
 * Resolve a --token argument to a concrete token identifier.
 * 'usdb' resolves per-network: SPARK_USDB_TOKEN env var wins, then the
 * mainnet constant (only valid on mainnet — regtest must set the env var
 * or pass the identifier explicitly). Anything else passes through as-is.
 *
 * @param {string} token  'usdb' or a concrete token identifier
 * @param {string} network
 * @returns {string}
 */
function resolveTokenIdentifier(token, network) {
  if (token !== 'usdb') return token;
  const fromEnv = process.env.SPARK_USDB_TOKEN;
  if (fromEnv) return fromEnv;
  if (network !== 'mainnet') {
    throw new Error(
      "The 'usdb' alias has no known identifier on this network — set SPARK_USDB_TOKEN or pass the token identifier explicitly with --token.",
    );
  }
  return USDB_TOKEN_MAINNET;
}

/**
 * Convert a human-readable decimal amount to base units.
 * '10.5' with 6 decimals -> 10500000n. Rejects negative/garbage input and
 * more fractional digits than the token supports.
 *
 * @param {string} input
 * @param {number} decimals
 * @returns {bigint}
 */
function parseTokenAmount(input, decimals) {
  const m = String(input)
    .trim()
    .match(/^(\d+)(?:\.(\d+))?$/);
  if (!m) throw new Error(`Invalid token amount '${input}' — expected a non-negative decimal like 10.5`);
  const frac = m[2] || '';
  if (frac.length > decimals) {
    throw new Error(`Amount '${input}' has more than ${decimals} decimal places for this token`);
  }
  const padded = (frac + '0'.repeat(decimals)).slice(0, decimals);
  return BigInt(m[1] + padded);
}

/**
 * Format base units for display: 10500000n with 6 decimals -> '10.500000'.
 * @param {bigint|number} units
 * @param {number} decimals
 * @returns {string}
 */
function formatTokenAmount(units, decimals) {
  const n = BigInt(units);
  const negative = n < 0n;
  const abs = negative ? -n : n;
  const base = 10n ** BigInt(decimals);
  const whole = abs / base;
  const frac = (abs % base).toString().padStart(decimals, '0');
  return `${negative ? '-' : ''}${whole}${decimals > 0 ? '.' + frac : ''}`;
}

/**
 * Normalize a tokenBalances Map (SDK shape) into a plain JSON-safe object:
 *   { [identifier]: { balance: string, decimals, name, ticker, issuerPublicKey } }
 * The balance is a STRING (BigInt) — token supplies can exceed the safe
 * integer range and precision must never be silently lost.
 *
 * @param {Map<string, {balance: bigint, tokenMetadata: object}>|undefined} tokenBalances
 * @returns {object}
 */
function normalizeTokenBalances(tokenBalances) {
  if (!tokenBalances || typeof tokenBalances[Symbol.iterator] !== 'function') return {};
  const out = {};
  for (const [id, tb] of tokenBalances) {
    const meta = tb && tb.tokenMetadata ? tb.tokenMetadata : {};
    out[String(id)] = {
      balance: String(tb.balance),
      decimals: meta.decimals,
      name: meta.name,
      ticker: meta.ticker,
      issuerPublicKey: meta.issuerPublicKey,
      balanceFormatted: formatTokenAmount(tb.balance, meta.decimals || 0),
    };
  }
  return out;
}

module.exports = {
  SPARK_PACKAGE,
  DEFAULT_NETWORK,
  loadSdkModule,
  requireNode22,
  validateMnemonicChecksum,
  getMnemonic,
  getBreezApiKey,
  storageDirFor,
  ensureOwnerOnlyDir,
  assertStorageAvailable,
  connect,
  normalizeInfo,
  normalizeSdkValue,
  feeFromPrepare,
  safeErrorDetail,
  waitForStableBalance,
  normalizePayment,
  USDB_TOKEN_MAINNET,
  resolveTokenIdentifier,
  parseTokenAmount,
  formatTokenAmount,
  normalizeTokenBalances,
  lnurlDomainFor,
  canonicalizeLnurlDomain,
  probeLnLookupHealthy,
  suppressSdkStdoutNoise,
};
