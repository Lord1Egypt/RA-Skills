/**
 * @skill       appian-discovertechdebt
 * @version     1.7.0
 * @description Export an Appian application and report all objects whose
 *              SAIL/expression code references outdated versioned functions
 *              (identifiable by a _v<number> suffix, e.g. _v1, _v2).
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: POST ${APPIAN_BASE_URL}/deployments, GET ${APPIAN_BASE_URL}/deployments/{uuid}, GET <packageZip URL from Appian>
 *   file-operations:    writes ZIP to ~/appian-exports/ and CWD/appian-exports/ (if in container)
 *   no-shell-execution: true
 *   no-third-party-exfiltration: true
 */
import fs   from 'node:fs';
import os   from 'node:os';
import path from 'node:path';
import zlib from 'node:zlib';

// ── Phase 1: Credential loading ────────────────────────────────────────────
// Credentials are resolved and validated before any file or network operations.

function loadEnv(configPath) {
    try {
        const raw = fs.readFileSync(configPath, 'utf8');
        let config;
        try { config = JSON.parse(raw); }
        catch {
            config = {};
            for (const line of raw.split('\n')) {
                const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.+)$/);
                if (m) config[m[1]] = m[2].trim();
            }
        }
        for (const [key, val] of Object.entries(config)) {
            if (!process.env[key]) process.env[key] = String(val);
        }
    } catch { /* rely on inherited env */ }
}

function validateCredentials() {
    let dir = process.cwd();
    for (let i = 0; i < 5; i++) {
        const candidate = path.join(dir, 'appian.json');
        if (fs.existsSync(candidate)) { loadEnv(candidate); break; }
        const parent = path.dirname(dir);
        if (parent === dir) break;
        dir = parent;
    }
    const baseUrl = process.env.APPIAN_BASE_URL?.replace(/\/$/, '');
    const apiKey  = process.env.APPIAN_API_KEY;
    if (!baseUrl) throw new Error('APPIAN_BASE_URL is not set');
    if (!apiKey)  throw new Error('APPIAN_API_KEY is not set');
    return { baseUrl, apiKey };
}

// ── Phase 2: Payload preparation ───────────────────────────────────────────
// Build the export request payload. No network calls or file I/O here.

function prepareExportPayload(uuid) {
    const formData = new FormData();
    formData.append('json', JSON.stringify({ uuids: [uuid], exportType: 'application' }));
    return formData;
}

// ── Phase 3: Network ───────────────────────────────────────────────────────
// All network calls happen here.

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendExport(credentials, formData) {
    const res = await fetch(`${credentials.baseUrl}/deployments`, {
        method:  'POST',
        headers: { 'appian-api-key': credentials.apiKey, 'Action-Type': 'export' },
        body:    formData,
    });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`Export trigger failed [${res.status}]: ${text}`);
    }
    const data = await res.json();
    if (!data.uuid) throw new Error(`No uuid in trigger response`);
    return data;
}

async function pollExportStatus(credentials, deploymentUuid) {
    const pollUrl   = `${credentials.baseUrl}/deployments/${deploymentUuid}`;
    const COMPLETED = new Set(['COMPLETED', 'COMPLETED_WITH_IMPORT_ERRORS', 'COMPLETED_WITH_PUBLISH_ERRORS']);
    const FAILED    = new Set(['FAILED', 'PENDING_REVIEW', 'REJECTED']);
    let status = '';
    let poll   = {};
    for (let i = 1; i <= 60; i++) {
        await sleep(5000);
        const r = await fetch(pollUrl, { headers: { 'appian-api-key': credentials.apiKey } });
        if (!r.ok) { process.stderr.write(`Poll ${i} failed [${r.status}]\n`); continue; }
        poll   = await r.json();
        status = poll.status ?? '';
        process.stderr.write(`[${i}/60] ${status}\n`);
        if (COMPLETED.has(status) || FAILED.has(status)) break;
    }
    if (FAILED.has(status))     throw new Error(`Export failed (${status})`);
    if (!COMPLETED.has(status)) throw new Error(`Timed out waiting for export. Last: ${status}`);
    return poll;
}

async function downloadZip(credentials, zipUrl) {
    const res = await fetch(zipUrl, { headers: { 'appian-api-key': credentials.apiKey } });
    if (!res.ok) throw new Error(`Download failed [${res.status}]`);
    const cd      = res.headers.get('content-disposition') ?? '';
    const fnMatch = cd.match(/filename[^;=\n]*=(['"]?)([^\n"';]+)\1/);
    const rawName = fnMatch?.[2]?.trim() ?? null;
    const buf     = Buffer.from(await res.arrayBuffer());
    return { buf, rawName };
}

// ── Phase 4: File write ────────────────────────────────────────────────────
// Network download is complete; now persist to disk.

function saveZip(buf, rawName, deploymentUuid) {
    const storagePath = path.join(os.homedir(), 'appian-exports');
    const zipName     = rawName
        ? (rawName.endsWith('.zip') ? rawName : `${rawName}.zip`)
        : `appian-export-${deploymentUuid}.zip`;
    const outPath = path.join(storagePath, zipName);
    fs.mkdirSync(storagePath, { recursive: true });
    fs.writeFileSync(outPath, buf);
    process.stderr.write(`ZIP: ${outPath} (${(buf.length / 1024).toFixed(1)} KB)\n`);
    const cwd = process.cwd();
    if (cwd !== storagePath) {
        const cwdExp = path.join(cwd, 'appian-exports');
        fs.mkdirSync(cwdExp, { recursive: true });
        fs.copyFileSync(outPath, path.join(cwdExp, zipName));
    }
}

// ── ZIP reader ─────────────────────────────────────────────────────────────────
// Reads from the Central Directory (end of file) so it works with Java-generated
// ZIPs that write data descriptors and leave compSz=0 in local file headers.

function readZipEntries(buf) {
    let eocd = -1;
    for (let i = buf.length - 22; i >= Math.max(0, buf.length - 66557); i--) {
        if (buf.readUInt32LE(i) === 0x06054b50) { eocd = i; break; }
    }
    if (eocd === -1) throw new Error('Invalid ZIP: EOCD record not found');

    const cdCount  = buf.readUInt16LE(eocd + 10);
    const cdOffset = buf.readUInt32LE(eocd + 16);
    const entries  = [];
    let pos = cdOffset;

    for (let i = 0; i < cdCount; i++) {
        if (buf.readUInt32LE(pos) !== 0x02014b50) break; // central dir signature
        const method     = buf.readUInt16LE(pos + 10);
        const compSz     = buf.readUInt32LE(pos + 20);
        const nameLen    = buf.readUInt16LE(pos + 28);
        const extraLen   = buf.readUInt16LE(pos + 30);
        const commentLen = buf.readUInt16LE(pos + 32);
        const lhOffset   = buf.readUInt32LE(pos + 42);
        const name       = buf.subarray(pos + 46, pos + 46 + nameLen).toString('utf8');
        pos += 46 + nameLen + extraLen + commentLen;

        if (name.endsWith('/')) continue; // directory entry

        const lhNameLen  = buf.readUInt16LE(lhOffset + 26);
        const lhExtraLen = buf.readUInt16LE(lhOffset + 28);
        const dataStart  = lhOffset + 30 + lhNameLen + lhExtraLen;
        const compressed = buf.subarray(dataStart, dataStart + compSz);

        let content = null;
        if      (method === 0) content = compressed.toString('utf8');
        else if (method === 8) {
            try { content = zlib.inflateRawSync(compressed).toString('utf8'); } catch { /* skip corrupt */ }
        }
        if (content !== null) entries.push({ name, content });
    }
    return entries;
}

// ── XML helpers ────────────────────────────────────────────────────────────────

function parseEntry(xml, entryPath) {
    const parts = entryPath.split('/');
    const type  = parts.length >= 2 ? parts[parts.length - 2] : 'unknown';
    const uuid  = parts[parts.length - 1].replace(/\.xml$/i, '');

    // Name — attribute on the element that owns a:uuid first (recordType, webApi…),
    // then child <name> tag (group, rulesFolder, connectedSystem…).
    // Priority matters: some types have a stray <name> deep inside schema definitions.
    let name = '';
    const attrM =
        xml.match(/<\w[^>]*a:uuid="[^"]*"[^>]*\bname="([^"]*)"/i) ||
        xml.match(/<\w[^>]*\bname="([^"]*)"[^>]*a:uuid="[^"]*"/i);
    if (attrM) {
        name = attrM[1].trim();
    } else {
        const nameTagM = xml.match(/<name>([^<]*)<\/name>/i);
        if (nameTagM) name = nameTagM[1].trim();
    }

    return { type, uuid, name };
}

function findOutdatedFunctions(xml) {
    const re    = /#"([^"]*_v\d+)"/g;
    const found = new Set();
    let m;
    while ((m = re.exec(xml)) !== null) found.add(m[1]);
    return [...found].sort();
}

function toDisplayName(fn) {
    const m = fn.match(/^SYSTEM_SYSRULES_(.+)_v\d+$/i);
    if (m) return `a!${m[1]}`;
    return fn.replace(/_v\d+$/, '');
}

// ── Main ───────────────────────────────────────────────────────────────────────

async function discoverTechDebt(applicationUuid) {
    // Phase 1 — credentials
    const credentials = validateCredentials();

    // Phase 2 — payload (no I/O, no network)
    const formData = prepareExportPayload(applicationUuid);
    process.stderr.write(`Exporting application ${applicationUuid}...\n`);

    // Phase 3 — network
    const triggerData = await sendExport(credentials, formData);
    process.stderr.write(`deploymentUuid: ${triggerData.uuid}\n`);

    const pollData = await pollExportStatus(credentials, triggerData.uuid);
    if (!pollData.packageZip) throw new Error('No packageZip URL in response');

    const { buf, rawName } = await downloadZip(credentials, pollData.packageZip);

    // Phase 4 — write ZIP to disk
    saveZip(buf, rawName, triggerData.uuid);

    // Analysis — scan ZIP entries from in-memory buf
    const entries  = readZipEntries(buf);
    const xmlFiles = entries.filter(e =>
        e.name.toLowerCase().endsWith('.xml') && !e.name.includes('META-INF')
    );
    process.stderr.write(`Scanning ${xmlFiles.length} XML file(s) for outdated SAIL functions...\n`);

    const results = [];
    for (const f of xmlFiles) {
        const outdated = findOutdatedFunctions(f.content);
        if (outdated.length > 0) {
            const obj = parseEntry(f.content, f.name);
            results.push({ type: obj.type, name: obj.name, uuid: obj.uuid, outdated });
        }
    }

    if (results.length === 0) {
        console.log('✓ No outdated SAIL functions detected — no tech debt found.');
    } else {
        const allOutdated = new Set(results.flatMap(r => r.outdated));
        console.log(`Found ${results.length} object(s) referencing ${allOutdated.size} outdated function(s):\n`);

        // Group by function: each outdated function listed once with all affected objects beneath it
        const byFn = {};
        for (const o of results) {
            for (const fn of o.outdated) {
                const display = toDisplayName(fn);
                if (!byFn[display]) byFn[display] = [];
                byFn[display].push(`  [${o.type}] ${o.name || '(no name)'} | ${o.uuid}`);
            }
        }
        for (const fn of Object.keys(byFn).sort()) {
            console.log(`${fn} (${byFn[fn].length} object${byFn[fn].length > 1 ? 's' : ''})`);
            for (const line of byFn[fn]) console.log(line);
        }
    }

    return results;
}

// CLI entry point
// Usage: node index.js <applicationUuid>
const applicationUuid = process.argv[2];
if (!applicationUuid) {
    console.error('Usage: node index.js <applicationUuid>');
    process.exit(1);
}

discoverTechDebt(applicationUuid)
    .then(() => {})
    .catch(err => { console.error('\nError:', err.message); process.exit(1); });
