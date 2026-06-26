/**
 * @skill       appian-export
 * @version     1.3.0
 * @description Export an Appian application or package as a ZIP via the v2 Deployment Management API.
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: ${APPIAN_BASE_URL}/deployments, ${APPIAN_BASE_URL}/deployments/{uuid}, <packageZip URL from Appian>
 *   file-operations:    writes ZIP to ~/appian-exports/ (created if absent)
 *   no-shell-execution: true
 *   no-third-party-exfiltration: true
 */
import fs   from 'node:fs';
import os   from 'node:os';
import path from 'node:path';

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
// Build the export request payload. No network calls here.

function prepareExportPayload(uuids, exportType, exportName) {
    const jsonPayload = { uuids: Array.isArray(uuids) ? uuids : [uuids], exportType };
    if (exportName) jsonPayload.name = exportName;
    const formData = new FormData();
    formData.append('json', JSON.stringify(jsonPayload));
    return { formData, jsonPayload };
}

// ── Phase 3: Network ───────────────────────────────────────────────────────
// All network calls happen here. File writes (saving the ZIP) follow after download.

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
    if (!data.uuid) throw new Error(`No uuid in response: ${JSON.stringify(data)}`);
    return data;
}

async function pollExportStatus(credentials, deploymentUuid) {
    const pollUrl   = `${credentials.baseUrl}/deployments/${deploymentUuid}`;
    const COMPLETED = new Set(['COMPLETED', 'COMPLETED_WITH_IMPORT_ERRORS', 'COMPLETED_WITH_PUBLISH_ERRORS']);
    const FAILED    = new Set(['FAILED', 'PENDING_REVIEW', 'REJECTED']);
    let status = '';
    let data   = {};
    const maxAttempts = 60;

    for (let i = 1; i <= maxAttempts; i++) {
        await sleep(5000);
        const res = await fetch(pollUrl, { headers: { 'appian-api-key': credentials.apiKey } });
        if (!res.ok) { process.stderr.write(`Poll ${i} failed [${res.status}]\n`); continue; }
        data   = await res.json();
        status = data.status ?? '';
        process.stderr.write(`[${i}/${maxAttempts}] ${status}\n`);
        if (COMPLETED.has(status) || FAILED.has(status)) break;
    }

    if (FAILED.has(status)) {
        const detail = data.errorMessage ?? data.message ?? data.error ?? '';
        throw new Error(`Export failed (${status})${detail ? ` — ${detail}` : ''}`);
    }
    if (!COMPLETED.has(status)) throw new Error(`Timed out. Last status: ${status}`);
    return data;
}

async function downloadZip(credentials, zipUrl) {
    const res = await fetch(zipUrl, { headers: { 'appian-api-key': credentials.apiKey } });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`Download failed [${res.status}]: ${text}`);
    }
    const cd        = res.headers.get('content-disposition') ?? '';
    const nameMatch = cd.match(/filename[^;=\n]*=(['"]?)([^\n"';]+)\1/);
    const rawName   = nameMatch?.[2]?.trim() ?? null;
    const buf       = Buffer.from(await res.arrayBuffer());
    return { buf, rawName };
}

// ── Phase 4: File write ────────────────────────────────────────────────────
// Network download is complete; now persist to disk.

function saveZip(buf, rawName, deploymentUuid, exportName, storagePath, cwd) {
    const fileName = rawName ?? exportName
        ?? `appian-export-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.zip`;
    const zipName  = fileName.endsWith('.zip') ? fileName : `${fileName}.zip`;
    const outPath  = path.join(storagePath, zipName);

    fs.mkdirSync(storagePath, { recursive: true });
    fs.writeFileSync(outPath, buf);

    const sizeKb = (buf.length / 1024).toFixed(1);
    console.log(`\n✓ Export complete`);
    console.log(`  ZIP path: ${outPath}`);
    console.log(`  Size:     ${sizeKb} KB`);

    if (cwd !== storagePath) {
        const cwdExports = path.join(cwd, 'appian-exports');
        fs.mkdirSync(cwdExports, { recursive: true });
        const cwdPath = path.join(cwdExports, zipName);
        fs.copyFileSync(outPath, cwdPath);
        console.log(`  Copied to: ${cwdPath}`);
    }

    return { outPath, sizeKb };
}

// ── Main ───────────────────────────────────────────────────────────────────

async function exportAppianObjects(uuids, exportName, exportType) {
    // Phase 1 — credentials
    const credentials = validateCredentials();
    const storagePath = path.join(os.homedir(), 'appian-exports');
    const cwd         = process.cwd();

    // Phase 2 — payload (no I/O, no network)
    const { formData, jsonPayload } = prepareExportPayload(uuids, exportType, exportName);
    process.stderr.write(`Exporting: ${JSON.stringify(jsonPayload)}\n`);

    // Phase 3 — network
    const triggerData = await sendExport(credentials, formData);
    process.stderr.write(`deploymentUuid: ${triggerData.uuid}\n`);

    const pollData = await pollExportStatus(credentials, triggerData.uuid);

    if (!pollData.packageZip) throw new Error(`No packageZip URL in response`);
    const { buf, rawName } = await downloadZip(credentials, pollData.packageZip);

    // Phase 4 — write to disk
    saveZip(buf, rawName, triggerData.uuid, exportName, storagePath, cwd);

    return { deploymentUuid: triggerData.uuid, status: pollData.status };
}

// ---------------------------------------------------------------------------
// CLI entry point
//
// Export an application:
//   node index.js <applicationUuid> [exportName]
//
// Export a specific package under an application:
//   node index.js <applicationUuid> --package <packageUuid> [exportName]
// ---------------------------------------------------------------------------
const args       = process.argv.slice(2);
const pkgFlagIdx = args.indexOf('--package');
const hasPkgFlag = pkgFlagIdx !== -1;

let uuidsToExport, exportName, exportType;

if (hasPkgFlag) {
    const applicationUuid = args[0];
    const packageUuid     = args[pkgFlagIdx + 1];
    exportName  = args.find((a, i) => !a.startsWith('--') && i !== 0 && i !== pkgFlagIdx + 1) ?? null;
    exportType  = 'package';
    uuidsToExport = [packageUuid];
    if (!applicationUuid || !packageUuid) {
        console.error('Usage: node index.js <applicationUuid> --package <packageUuid> [exportName]');
        process.exit(1);
    }
} else {
    const applicationUuid = args[0];
    exportName    = args[1] && args[1] !== 'null' ? args[1] : null;
    exportType    = 'application';
    uuidsToExport = [applicationUuid];
    if (!applicationUuid) {
        console.error('Usage:');
        console.error('  Export application: node index.js <applicationUuid> [exportName]');
        console.error('  Export package:     node index.js <applicationUuid> --package <packageUuid> [exportName]');
        process.exit(1);
    }
}

exportAppianObjects(uuidsToExport, exportName, exportType)
    .then(() => {})
    .catch(err => { console.error('\nError:', err.message); process.exit(1); });
