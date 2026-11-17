#!/usr/bin/env node
// peerd — always-on Decent peer daemon = an agent's P2P inbox/outbox.
// Pure JS, normal user privilege, messaging only (no TUN / virtual IP).
// Holds ONE warm Carrier connection so the agent never pays DHT-join latency
// per message. The agent interacts only with local files (no network in the
// agent's own commands):
//   inbox.jsonl    <- daemon appends every received text  {ts,from,text}
//   outbox.jsonl   -> agent appends commands; daemon sends them:
//                       {"type":"send","to":"<userid>","text":"..."}
//                       {"type":"friend","to":"<address>","hello":"..."}
//   requests.jsonl <- daemon appends incoming friend requests {ts,from,hello}
//   friends.json   <- daemon snapshots peer.friends()
//   status.json    <- {address,userid,online,joined,ts}
// Trusted 2+-agent mesh: auto-accepts friend requests from IDs listed in
// ~/.decent-peer/allow.txt (one userid/address per line); others just logged.
//
// Env: DECENT_PEER_DIST (path to peer dist/index.js), DECENT_PEER_HOME
// (default ~/.decent-peer), AGENT_NAME.
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const HOME = process.env.DECENT_PEER_HOME || join(homedir(), ".decent-peer");
mkdirSync(HOME, { recursive: true });
const P = (f) => join(HOME, f);
const NAME = process.env.AGENT_NAME || "agent";

// Prefer the published npm package (portable to any Node machine); fall back to
// a local repo build only if DECENT_PEER_DIST is explicitly set.
let Peer;
try {
  ({ Peer } = await import("@decentnetwork/peer"));
} catch (err) {
  if (!process.env.DECENT_PEER_DIST) throw err;
  ({ Peer } = await import(process.env.DECENT_PEER_DIST));
}

const BOOTSTRAPS = (() => {
  const cfg = join(HOME, "config.json");
  if (existsSync(cfg)) {
    try { const c = JSON.parse(readFileSync(cfg, "utf8")); if (c.bootstrapNodes) return c.bootstrapNodes; } catch {}
  }
  // Decent Network public DHT bootstrap nodes — geographically diverse so a
  // fresh peer can always find at least one. Put your own in
  // ~/.decent-peer/config.json {"bootstrapNodes":[...]} to override.
  return [
    // US-East
    { host: "13.58.208.50", port: 33445, pk: "89vny8MrKdDKs7Uta9RdVmspPjnRMdwMmaiEW27pZ7gh" },
    { host: "18.216.102.47", port: 33445, pk: "G5z8MqiNDFTadFUPfMdYsYtkUDbX5mNCMVHMZtsCnFeb" },
    { host: "18.216.6.197", port: 33445, pk: "H8sqhRrQuJZ6iLtP2wanxt4LzdNrN2NNFnpPdq1uJ9n2" },
    // US-West
    { host: "54.193.141.205", port: 33445, pk: "7TfZWZNV8vnBxxWzJXuvKgX2QyKkLpg2oXx3LQ5tg8LW" },
    // Global
    { host: "154.64.235.176", port: 33445, pk: "GdNtV2N74fZnLjhH7NhQ18nGdxb1k8jRM9dQaK7WnxmL" },
    // Asia-Pacific (Singapore + China); one on port 443 for networks that block 33445
    { host: "52.74.215.181", port: 33445, pk: "Xv6d34WaUw9bPn7YihzVAFw7D2igbQJZ3jwmzzfYVFV" },
    { host: "47.100.103.201", port: 33445, pk: "CX1XH419p4xJ5SV4KvDxBeKYSRdMJW9QpdWJY8owUxHd" },
    { host: "52.83.171.135", port: 443, pk: "5tuHgK1Q4CYf4K5PutsEPK5E3Z7cbtEBdx7LwmdzqXHL" },
    { host: "52.83.191.228", port: 33445, pk: "3khtxZo89SBScAMaHhTvD68pPHiKxgZT6hTCSZZVgNEm" },
  ];
})();

const allow = () => existsSync(P("allow.txt"))
  ? readFileSync(P("allow.txt"), "utf8").split("\n").map((s) => s.trim()).filter(Boolean)
  : [];
const now = () => new Date().toISOString();
const log = (m) => console.log(`[${now()}] ${m}`);

const peer = await Peer.create({
  keyFile: P("peer.save"), bootstrapNodes: BOOTSTRAPS, compatibilityMode: "legacy", debugLabel: NAME,
});
await peer.start();

// Receiver-side dedup (mesh bug #3): a peer that replays its outbox (cursor reset) re-delivers
// every old message. Drop an identical (from,text) seen within DEDUP_MS. PERSISTENT across restarts
// (.inbox.seen on disk) with a 48h window — the v1 in-memory-only version missed a replay that
// arrived AFTER a peerd restart (empty map). 48h > any legit gap between identical sends on this
// channel (reports carry dates/changing numbers), so no real message is lost.
const DEDUP_MS = 48 * 60 * 60 * 1000;
const SEENF = ".inbox.seen";
const _djb2 = (s) => { let h = 5381; for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return h.toString(36); };
let _seen = new Map();
try { if (existsSync(P(SEENF))) _seen = new Map(Object.entries(JSON.parse(readFileSync(P(SEENF), "utf8")))); } catch {}
const _persistSeen = () => { try { writeFileSync(P(SEENF), JSON.stringify(Object.fromEntries(_seen))); } catch {} };
peer.onText((msg) => {
  const key = _djb2(`${msg.pubkey}|${msg.text}`);
  const t = Date.now();
  for (const [k, ts] of _seen) if (t - ts > DEDUP_MS) _seen.delete(k);
  if (_seen.has(key)) { log(`DEDUP drop ${msg.pubkey}: ${msg.text.slice(0, 48)}`); return; }
  _seen.set(key, t); _persistSeen();
  appendFileSync(P("inbox.jsonl"), JSON.stringify({ ts: now(), from: msg.pubkey, text: msg.text }) + "\n");
  log(`RECV ${msg.pubkey}: ${msg.text}`);
});
peer.onFriendRequest(async (req) => {
  const from = req.userid ?? req.pubkey;
  appendFileSync(P("requests.jsonl"), JSON.stringify({ ts: now(), from, hello: req.hello ?? "" }) + "\n");
  log(`FRIEND-REQ ${from} "${req.hello ?? ""}"`);
  if (allow().some((a) => from?.includes(a) || a.includes(from))) {
    try { await peer.acceptFriendRequest(req.pubkey); log(`AUTO-ACCEPTED ${from}`); }
    catch (e) { log(`accept failed: ${e.message}`); }
  }
});

writeFileSync(P("status.json"), JSON.stringify(
  { name: NAME, address: peer.address(), userid: peer.userid(), online: true, joined: false, ts: now() }, null, 2));
log(`address ${peer.address()}`);
log(`userid  ${peer.userid()}`);

// Resilient join: a transient bootstrap timeout must NOT kill the daemon.
for (let attempt = 1; ; attempt++) {
  try { await peer.joinNetwork(); break; }
  catch (e) { log(`join attempt ${attempt} failed: ${e.message} — retrying in 10s`); await new Promise((r) => setTimeout(r, 10000)); }
}
for (let i = 0; i < 3; i++) { try { const n = await peer.announceSelf(45000); if (n.length) break; } catch (e) { log(`announce retry: ${e.message}`); } }
writeFileSync(P("status.json"), JSON.stringify(
  { name: NAME, address: peer.address(), userid: peer.userid(), online: true, joined: true, ts: now() }, null, 2));
log("joined + announced — inbox live");

// Heartbeat (mesh bug #3): a live daemon must refresh status.json ts, or
// monitoring reads a stale "joined true" from a wedged/dead process.
setInterval(() => { try { writeFileSync(P("status.json"), JSON.stringify(
  { name: NAME, address: peer.address(), userid: peer.userid(), online: true, joined: true, ts: now() }, null, 2)); } catch {} }, 30000);

// re-announce so we stay reachable
setInterval(() => peer.announceSelf(20000).catch(() => {}), 120000);
setInterval(() => { try { writeFileSync(P("friends.json"), JSON.stringify(peer.friends(), null, 2)); } catch {} }, 30000);

// outbox pump: poll for new command lines, send via the warm connection.
// Cursor discipline (mesh bug #3): RESUME from the persisted .outbox.cursor across restarts
// (so messages appended while peerd was down still send, and we never replay history). Only a
// truly fresh outbox (no persisted cursor) skips to the end.
let cursor = 0;
{
  const nLines = existsSync(P("outbox.jsonl"))
    ? readFileSync(P("outbox.jsonl"), "utf8").split("\n").filter(Boolean).length : 0;
  if (existsSync(P(".outbox.cursor"))) {
    cursor = Math.min(Math.max(0, Number(readFileSync(P(".outbox.cursor"), "utf8")) || 0), nLines);
  } else {
    cursor = nLines; // first run ever: don't replay pre-existing history
  }
  writeFileSync(P(".outbox.cursor"), String(cursor));
}
const retries = new Map(); // outbox line index -> failed attempts (mesh bug #2)
setInterval(async () => {
  if (!existsSync(P("outbox.jsonl"))) return;
  const lines = readFileSync(P("outbox.jsonl"), "utf8").split("\n").filter(Boolean);
  // Outbox truncated/rotated below our position -> assume those lines were already delivered and
  // clamp; do NOT reset to 0 (that was the bug that replayed the whole outbox = 141 dupes).
  if (cursor > lines.length) cursor = lines.length;
  for (; cursor < lines.length; cursor++) {
    let cmd; try { cmd = JSON.parse(lines[cursor]); } catch { continue; }
    try {
      if (cmd.type === "send") { await peer.sendText(cmd.to, cmd.text); log(`SENT ${cmd.to}: ${cmd.text}`); }
      else if (cmd.type === "friend") { await peer.sendFriendRequest(cmd.to, cmd.hello ?? `hello from ${NAME}`); log(`FRIEND-REQ -> ${cmd.to}`); }
      else if (cmd.type === "accept") { await peer.acceptFriendRequest(cmd.to); log(`ACCEPTED ${cmd.to}`); }
    } catch (e) {
      // Mesh bug #2 (sender side): a failed send must NOT advance the cursor —
      // that silently drops the message forever (5 work orders lost 07-18).
      // With peer >=0.1.112 sendText throws when the receiver never ACKs; stop
      // here and retry this same line next tick until it delivers. Watchdogs
      // keep daemons up, so head-of-line blocking is bounded to minutes.
      retries.set(cursor, (retries.get(cursor) ?? 0) + 1);
      if (retries.get(cursor) % 40 === 1) log(`outbox cmd failed (${cmd.type} ${cmd.to}) attempt ${retries.get(cursor)}: ${e.message} — will retry, NOT advancing cursor`);
      break;
    }
  }
  writeFileSync(P(".outbox.cursor"), String(cursor));
}, 1500);

process.on("unhandledRejection", (e) => log(`unhandledRejection: ${e?.message ?? e}`));
// Mesh bug #1 evidence: never exit silently — every death leaves a trace.
process.on("uncaughtException", (e) => { log(`uncaughtException: ${e?.stack ?? e}`); process.exit(1); });
process.on("exit", (code) => { try { log(`process exit code=${code}`); } catch {} });
process.on("SIGINT", async () => { await peer.stop().catch(() => {}); process.exit(0); });
process.on("SIGTERM", async () => { await peer.stop().catch(() => {}); process.exit(0); });
