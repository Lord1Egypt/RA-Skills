'use strict';
/**
 * jackal-client.js — standalone Jackal client for subprocess use
 *
 * A thin client that client.py (or any caller) can spawn as a subprocess to
 * perform client-side Jackal operations under the USER's own wallet — giving
 * true VFS sovereignty rather than sidecar-mediated storage.
 *
 * Commands:
 *   node jackal-client.js upload <key>
 *     Reads base64-encoded data from stdin.
 *     Uploads to Home/jackal-memory/<safe_key> in the user's own Jackal VFS.
 *     Stdout: {"ok":true,"cid":"Home/jackal-memory/<safe_key>"}
 *
 *   node jackal-client.js download <cid>
 *     Downloads file from Jackal by full VFS path (cid).
 *     Stdout: {"ok":true,"data_b64":"<base64>"}
 *
 * Required env vars:
 *   JACKAL_MNEMONIC  — BIP39 mnemonic for the user's wallet (never pass via argv)
 *   JACKAL_ADDRESS   — jkl1... address (required for download only)
 *
 * All SDK/progress logs go to stderr. Stdout is reserved for the single JSON
 * result line so callers can parse it cleanly.
 *
 * Exit 0 on success, 1 on failure (also writes {"ok":false,"error":"..."} to stdout).
 */

global.WebSocket = require('ws').WebSocket;

// ── Redirect console.log to stderr ───────────────────────────────────────────
// jackal.js emits progress logs via console.log (e.g. "progress: 100 {...}").
// Redirecting to stderr keeps stdout clean for our single JSON result line.
// BigInt-safe serialiser — tx responses from Jackal contain BigInt values that
// JSON.stringify() rejects by default.
const safeStringify = v => JSON.stringify(v, (_, val) =>
    typeof val === 'bigint' ? val.toString() : val
);
console.log = (...args) => process.stderr.write(
    args.map(a => typeof a === 'object' && a !== null ? safeStringify(a) : String(a)).join(' ') + '\n'
);
// NOTE: No fetch polyfill. Node 20's native fetch (undici) handles File/Blob
// bodies correctly for multi-provider upload retries. node-fetch v2 treats them
// as one-time-use streams, causing "body used already" errors on retry.
// Downloads bypass fetch entirely via nodeHttpGet (require('https')), which is
// the proven fix for SSL renegotiation issues on Windows.

// ── Load .env ─────────────────────────────────────────────────────────────────
const fs   = require('fs');
const path = require('path');
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
    for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
        const m = line.match(/^\s*([\w]+)\s*=\s*(.*)\s*$/);
        if (m) process.env[m[1]] ??= m[2].replace(/^['"]|['"]$/g, '');
    }
}

const { ClientHandler, StorageHandler } = require('@jackallabs/jackal.js');

const CHAIN_ID          = 'jackal-1';
// Ordered fallback list — tried in sequence, first successful connection wins.
// Verified live 2026-03-06: rpc.jackalprotocol.com, jackal-rpc.polkachu.com
const RPCS              = [
    'https://rpc.jackalprotocol.com',
    'https://jackal-rpc.polkachu.com',
];
const RPC_TIMEOUT_MS    = 15_000;
const BROADCAST_OPTS    = { monitorTimeout: 15 };
const JKL_FOLDER        = 'jackal-memory';
const JKL_PATH          = `Home/${JKL_FOLDER}`;
const PREFERRED_DOMAINS = ['squirrellogic.com'];

const MNEMONIC = process.env.JACKAL_MNEMONIC || '';
const ADDRESS  = process.env.JACKAL_ADDRESS  || '';

// ── Logging ───────────────────────────────────────────────────────────────────

const log = (...args) => process.stderr.write('[jackal-client] ' + args.join(' ') + '\n');

// Write the single JSON result to stdout and flush.
function result(obj) {
    process.stdout.write(JSON.stringify(obj) + '\n');
}

// ── Error helpers ─────────────────────────────────────────────────────────────

function isEventTimeout(err) {
    return err?.errorText === 'Event Timeout' && err?.txResponse?.code === 0;
}

function isCosmjsTimeout(err) {
    return typeof err?.txId === 'string' && err?.message?.includes('was not yet found on the chain');
}

function isNonFatalTimeout(err) {
    return isEventTimeout(err) || isCosmjsTimeout(err);
}

// jackal.js errors are plain objects with errorText, not Error instances.
// Using err?.message alone produces "[object Object]" for these.
function errMsg(err) {
    return err?.message || err?.errorText || safeStringify(err);
}

function isSequenceMismatch(err) {
    const msg = errMsg(err);
    return typeof msg === 'string' && msg.includes('account sequence mismatch');
}

// ── Native HTTP download ──────────────────────────────────────────────────────
// Uses require('https') directly — same path as nodeHttpGet in index.js which is
// proven reliable on Windows. Avoids fetch() entirely for provider downloads.

function nodeHttpGet(url) {
    return new Promise((resolve, reject) => {
        const lib = url.startsWith('https') ? require('https') : require('http');
        const req = lib.get(url, (res) => {
            if (res.statusCode !== 200) {
                reject(new Error(`HTTP ${res.statusCode} from ${url}`));
                return;
            }
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end',  () => resolve(Buffer.concat(chunks)));
            res.on('error', reject);
        });
        req.on('error', reject);
        req.setTimeout(30000, () => req.destroy(new Error('Request timeout')));
    });
}

// ── Client init ───────────────────────────────────────────────────────────────
// Connects wallet, inits storage handler, creates working folder if needed,
// loads provider pool. Returns { storage, address, providerUrls }.

async function initClient() {
    log('Connecting...');
    let client = null;
    let lastErr = null;
    for (const rpc of RPCS) {
        try {
            log(`Trying RPC: ${rpc}`);
            client = await Promise.race([
                ClientHandler.connect({
                    selectedWallet: 'mnemonic',
                    mnemonic:       MNEMONIC,
                    chainId:        CHAIN_ID,
                    endpoint:       rpc,
                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error(`RPC timeout after ${RPC_TIMEOUT_MS}ms: ${rpc}`)), RPC_TIMEOUT_MS)
                ),
            ]);
            log(`Connected via ${rpc}`);
            break;
        } catch (e) {
            log(`RPC failed (${rpc}): ${errMsg(e)}`);
            lastErr = e;
        }
    }
    if (!client) throw lastErr || new Error('All RPC endpoints failed');
    const address = client.getJackalAddress();
    log(`Wallet — ${address}`);

    const storage = await StorageHandler.init(client, { setFullSigner: true });

    // Load Home/; create it on first use.
    log('Loading Home directory...');
    try {
        await storage.loadDirectory();
    } catch (_) {
        log('First-time setup — calling initStorage()...');
        try {
            await storage.initStorage({ broadcastOptions: BROADCAST_OPTS });
        } catch (initErr) {
            if (!isNonFatalTimeout(initErr)) throw initErr;
            log('initStorage() timeout — tx confirmed, continuing');
        }
        await storage.loadDirectory();
    }

    // Create working subfolder if this is the first run.
    if (!storage.listChildFolders().includes(JKL_FOLDER)) {
        log(`Creating folder ${JKL_FOLDER}...`);
        try {
            await storage.createFolders({ names: JKL_FOLDER, broadcastOptions: BROADCAST_OPTS });
        } catch (folderErr) {
            if (!isNonFatalTimeout(folderErr)) throw folderErr;
            log('createFolders() timeout — tx confirmed, continuing');
        }
        // Reload Home to refresh VFS cache — the SDK's in-memory tree doesn't
        // update after a timed-out createFolders(), so the subfolder path won't
        // resolve until we force a fresh load.
        log('Reloading Home after folder creation...');
        await storage.loadDirectory();
    }

    // Navigate into the working folder.
    await storage.loadDirectory({ path: JKL_PATH });
    log(`Working directory: ${JKL_PATH}`);

    // Load provider pool — parallel IP resolution, preferred providers sorted first.
    log('Resolving provider pool...');
    const addresses = await storage.getAvailableProviders();
    const settled   = await Promise.allSettled(
        addresses.map(addr =>
            Promise.race([
                storage.findProviderIps([addr]),
                new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 10_000)),
            ])
        )
    );

    const ips = {};
    for (const r of settled) {
        if (r.status === 'fulfilled') Object.assign(ips, r.value);
    }
    const providerCount = Object.keys(ips).length;
    if (providerCount === 0) throw new Error('No providers available');

    await storage.loadProviderPool(ips);

    const providerUrls = Object.values(ips).sort((a, b) => {
        const aP = PREFERRED_DOMAINS.some(d => a.includes(d)) ? 0 : 1;
        const bP = PREFERRED_DOMAINS.some(d => b.includes(d)) ? 0 : 1;
        return aP - bP;
    });

    const uploadIps = Object.fromEntries(
        Object.entries(ips).filter(([, url]) => PREFERRED_DOMAINS.some(d => url.includes(d)))
    );
    const uploadIpCount = Object.keys(uploadIps).length;

    log(`Provider pool ready — ${providerUrls.length} providers (${uploadIpCount} preferred for upload)`);

    return { storage, address, providerUrls, uploadIps, uploadIpCount };
}

// ── Upload ────────────────────────────────────────────────────────────────────

async function upload(key) {
    if (!MNEMONIC) throw new Error('JACKAL_MNEMONIC env var is required');

    // Read base64 data from stdin.
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const data_b64 = Buffer.concat(chunks).toString('utf8').trim();
    if (!data_b64) throw new Error('No data received on stdin');

    const { storage, uploadIps, uploadIpCount } = await initClient();

    if (uploadIpCount > 0) {
        log(`Using preferred upload pool (${uploadIpCount} providers)`);
        await storage.loadProviderPool(uploadIps);
    } else {
        log('No preferred upload providers found — using full pool');
    }

    const safeName = key.replace(/[^a-zA-Z0-9._-]/g, '_');
    const bytes    = Buffer.from(data_b64, 'base64');
    const file     = new File([bytes], safeName, { type: 'application/octet-stream' });

    log(`Uploading ${safeName} (${bytes.length} bytes)...`);
    await storage.queuePublic(file);

    try {
        await storage.processAllQueues(BROADCAST_OPTS);
    } catch (uploadErr) {
        if (!isNonFatalTimeout(uploadErr)) throw uploadErr;
        // Tx confirmed but listener timed out — processAllQueues didn't call
        // loadDirectory() internally. Reload manually so getFileParticulars works.
        log('Upload timeout — tx confirmed, reloading directory...');
        await storage.loadDirectory({ path: JKL_PATH });
    }

    const cid = `${JKL_PATH}/${safeName}`;
    log(`Upload complete — ${cid}`);
    result({ ok: true, cid });
}

// ── Download ──────────────────────────────────────────────────────────────────

async function download(cid) {
    if (!MNEMONIC) throw new Error('JACKAL_MNEMONIC env var is required');
    if (!ADDRESS)  throw new Error('JACKAL_ADDRESS env var is required for download');

    const { storage, providerUrls } = await initClient();

    // Always reload directory before getFileParticulars — VFS cache may be stale.
    log(`Reloading directory for download...`);
    await storage.loadDirectory({ path: JKL_PATH });

    log(`Getting file particulars: ${cid} (owner: ${ADDRESS})`);
    const particulars    = await storage.getFileParticulars(cid, ADDRESS);
    if (!particulars) throw new Error(`File not found in VFS: ${cid}`);
    const { merkleLocation } = particulars;

    if (!merkleLocation) throw new Error('getFileParticulars returned no merkleLocation');
    log(`merkleLocation: ${merkleLocation}`);

    // Brute-force all providers in parallel — 5 attempts × 12s for propagation.
    for (let attempt = 0; attempt < 5; attempt++) {
        if (attempt > 0) {
            log(`Waiting 12s (propagation delay) — attempt ${attempt + 1}/5...`);
            await new Promise(r => setTimeout(r, 12_000));
        }

        log(`Attempt ${attempt + 1}/5 — ${providerUrls.length} providers in parallel...`);

        try {
            const data = await Promise.any(
                providerUrls.map(provider =>
                    nodeHttpGet(`${provider}/download/${merkleLocation}`)
                        .then(buf => { log(`Provider hit: ${provider}`); return buf; })
                )
            );
            log(`Download complete — ${data.length} bytes`);
            result({ ok: true, data_b64: data.toString('base64') });
            return;
        } catch (aggErr) {
            const errors = aggErr.errors
                ? aggErr.errors.map((e, i) => `  [${i}] ${providerUrls[i] || '?'}: ${e.message}`).join('\n')
                : String(aggErr);
            log(`All providers failed attempt ${attempt + 1}/5:\n${errors}`);
        }
    }

    throw new Error('File not found on any provider after 5 attempts');
}

// ── Entry point ───────────────────────────────────────────────────────────────

async function main() {
    const [,, command, arg] = process.argv;

    if (!command || !['upload', 'download'].includes(command)) {
        process.stderr.write('Usage:\n');
        process.stderr.write('  node jackal-client.js upload <key>     # reads base64 from stdin\n');
        process.stderr.write('  node jackal-client.js download <cid>   # writes base64 to stdout\n');
        process.exit(1);
    }
    if (!arg) {
        process.stderr.write(`Error: ${command} requires an argument\n`);
        process.exit(1);
    }

    if (command === 'upload')   await upload(arg);
    if (command === 'download') await download(arg);

    // jackal.js holds open WebSocket connections for tx monitoring that keep the
    // event loop alive indefinitely. Force exit once our work is done.
    process.exit(0);
}

main().catch(err => {
    const msg = errMsg(err);
    if (isSequenceMismatch(err)) {
        process.stderr.write(`[jackal-client] Fatal: sequence mismatch — ${msg}\n`);
        process.stderr.write(`[jackal-client] Hint: mempool may have stale txs. Retry after a delay.\n`);
    } else {
        process.stderr.write(`[jackal-client] Fatal: ${msg}\n`);
    }
    result({ ok: false, error: msg });
    process.exit(1);
});
