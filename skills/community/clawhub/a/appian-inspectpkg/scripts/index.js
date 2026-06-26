/**
 * @skill       appian-inspectpkg
 * @version     1.1.0
 * @description Inspect an Appian package ZIP before deploying via the v2 Deployment Management API.
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: POST ${APPIAN_BASE_URL}/inspections, GET ${APPIAN_BASE_URL}/inspections/{uuid}
 *   file-operations:    reads package ZIP from user-supplied path (upload only, no writes)
 *   no-shell-execution: true
 *   no-third-party-exfiltration: true
 */
import fs   from 'node:fs';
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

// ── Phase 2: File I/O ──────────────────────────────────────────────────────
// All disk reads happen here, before any network calls.

function readPackageFile(zipPath) {
    if (!fs.existsSync(zipPath)) throw new Error(`Package file not found: ${zipPath}`);
    return { name: path.basename(zipPath), buf: fs.readFileSync(zipPath), size: fs.statSync(zipPath).size };
}

function readCustomizationFile(custFilePath) {
    if (!fs.existsSync(custFilePath)) throw new Error(`Customization file not found: ${custFilePath}`);
    return { name: path.basename(custFilePath), buf: fs.readFileSync(custFilePath) };
}

function prepareInspectionPayload(zipFile, custFile) {
    const jsonPayload = { packageFileName: zipFile.name };
    if (custFile) jsonPayload.customizationFileName = custFile.name;

    const formData = new FormData();
    formData.append('json', JSON.stringify(jsonPayload));
    formData.append(zipFile.name,
        new Blob([zipFile.buf], { type: 'application/zip' }),
        zipFile.name
    );
    if (custFile) {
        formData.append(custFile.name,
            new Blob([custFile.buf], { type: 'text/plain' }),
            custFile.name
        );
    }
    return { formData, jsonPayload };
}

// ── Phase 3: Network ───────────────────────────────────────────────────────
// All network calls happen here. No file reads from this point onward.

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendInspection(credentials, formData) {
    const res = await fetch(`${credentials.baseUrl}/inspections`, {
        method:  'POST',
        headers: { 'appian-api-key': credentials.apiKey },
        body:    formData,
    });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`Inspection trigger failed [${res.status}]: ${text}`);
    }
    const data = await res.json();
    if (!data.uuid) throw new Error(`No uuid in response: ${JSON.stringify(data)}`);
    return data;
}

async function pollInspectionStatus(credentials, inspectionUuid) {
    const pollUrl     = `${credentials.baseUrl}/inspections/${inspectionUuid}`;
    let data;
    let status        = '';
    let attempt       = 0;
    const maxAttempts = 24; // 2 minutes

    while (status !== 'COMPLETED' && status !== 'FAILED' && attempt < maxAttempts) {
        await sleep(5000);
        attempt++;
        const res = await fetch(pollUrl, { headers: { 'appian-api-key': credentials.apiKey } });
        if (!res.ok) { process.stderr.write(`Poll ${attempt} failed [${res.status}]\n`); continue; }
        data   = await res.json();
        status = data.status ?? '';
        process.stderr.write(`[${attempt}/${maxAttempts}] status: ${status}\n`);
    }

    if (!data)               throw new Error('No inspection result received');
    if (status === 'FAILED') throw new Error(`Inspection system error: ${JSON.stringify(data)}`);
    return data;
}

async function inspectPackage(zipPath, custFilePath) {
    // Phase 1 — credentials
    const credentials = validateCredentials();

    // Phase 2 — file I/O (all disk reads before any network call)
    const zipFile  = readPackageFile(zipPath);
    const custFile = custFilePath ? readCustomizationFile(custFilePath) : null;
    const { formData, jsonPayload } = prepareInspectionPayload(zipFile, custFile);

    process.stderr.write(`Inspecting: ${zipFile.name} (${(zipFile.size / 1024).toFixed(1)} KB)\n`);
    process.stderr.write(`Payload: ${JSON.stringify(jsonPayload)}\n`);

    // Phase 3 — network (no file reads from here onward)
    const triggerData    = await sendInspection(credentials, formData);
    const inspectionUuid = triggerData.uuid;
    process.stderr.write(`inspectionUuid: ${inspectionUuid}\n`);

    const data = await pollInspectionStatus(credentials, inspectionUuid);

    const summary  = data.summary ?? {};
    const expected = summary.objectsExpected ?? {};
    const problems = summary.problems ?? {};
    const errors   = problems.errors   ?? [];
    const warnings = problems.warnings ?? [];

    console.log(`\n=== Inspection Results ===`);
    console.log(`Objects expected — total: ${expected.total ?? '?'}, imported: ${expected.imported ?? '?'}, skipped: ${expected.skipped ?? '?'}, failed: ${expected.failed ?? '?'}`);

    if (errors.length > 0) {
        console.log(`\nErrors (${errors.length}):`);
        for (const e of errors) console.log(`  [${e.objectName ?? e.objectUuid ?? 'unknown'}] ${e.errorMessage}`);
    } else {
        console.log('\nNo errors.');
    }

    if (warnings.length > 0) {
        console.log(`\nWarnings (${warnings.length}):`);
        for (const w of warnings) console.log(`  [${w.objectName ?? w.objectUuid ?? 'unknown'}] ${w.warningMessage}`);
    } else {
        console.log('No warnings.');
    }

    return { inspectionUuid, status: data.status, expected, errors, warnings };
}

// CLI entry point
// Usage: node index.js <zipPath> [customizationFilePath]
const zipPath      = process.argv[2];
const custFilePath = process.argv[3] && process.argv[3] !== 'null' ? process.argv[3] : null;

if (!zipPath) {
    console.error('Usage: node index.js <zipPath> [customizationFilePath]');
    process.exit(1);
}

inspectPackage(zipPath, custFilePath)
    .then(() => {})
    .catch(err => { console.error('\nError:', err.message); process.exit(1); });
