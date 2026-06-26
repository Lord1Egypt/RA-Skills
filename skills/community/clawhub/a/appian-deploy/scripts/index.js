/**
 * @skill       appian-deploy
 * @version     1.2.3
 * @description Deploy (import) an Appian package ZIP via the v2 Deployment Management API.
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: POST ${APPIAN_BASE_URL}/deployments, GET ${APPIAN_BASE_URL}/deployments/{uuid}
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
// All disk reads happen here, isolated from network operations.

function readPackageFile(zipPath) {
    if (!fs.existsSync(zipPath)) throw new Error(`Package file not found: ${zipPath}`);
    return { name: path.basename(zipPath), buf: fs.readFileSync(zipPath) };
}

function readCustomizationFile(custFilePath) {
    if (!fs.existsSync(custFilePath)) throw new Error(`Customization file not found: ${custFilePath}`);
    return { name: path.basename(custFilePath), buf: fs.readFileSync(custFilePath) };
}

function prepareDeploymentPayload(zipFile, custFile, deploymentName, description) {
    const jsonPayload = { name: deploymentName, packageFileName: zipFile.name };
    if (description) jsonPayload.description = description;
    if (custFile)    jsonPayload.customizationFileName = custFile.name;

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
// All network calls happen here. No file reads occur in this phase.

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendDeployment(credentials, formData) {
    const res = await fetch(`${credentials.baseUrl}/deployments`, {
        method:  'POST',
        headers: { 'appian-api-key': credentials.apiKey, 'Action-Type': 'import' },
        body:    formData,
    });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`Deploy trigger failed [${res.status}]: ${text}`);
    }
    const data = await res.json();
    if (!data.uuid) throw new Error(`No uuid in response: ${JSON.stringify(data)}`);
    return data;
}

async function pollStatus(credentials, deploymentUuid) {
    const pollUrl = `${credentials.baseUrl}/deployments/${deploymentUuid}`;
    const TERMINAL = new Set([
        'COMPLETED', 'COMPLETED_WITH_IMPORT_ERRORS', 'COMPLETED_WITH_PUBLISH_ERRORS',
        'FAILED', 'PENDING_REVIEW', 'REJECTED',
    ]);
    let status = '';
    let data   = {};
    const maxAttempts = 72;

    for (let i = 1; i <= maxAttempts; i++) {
        await sleep(5000);
        const res = await fetch(pollUrl, { headers: { 'appian-api-key': credentials.apiKey } });
        if (!res.ok) { process.stderr.write(`Poll ${i} failed [${res.status}]\n`); continue; }
        data   = await res.json();
        status = data.status ?? '';
        process.stderr.write(`[${i}/${maxAttempts}] ${status}\n`);
        if (TERMINAL.has(status)) break;
    }
    if (!TERMINAL.has(status)) throw new Error(`Timed out. Last status: ${status}`);
    return { status, data };
}

// ── Main ───────────────────────────────────────────────────────────────────

async function deployPackage(zipPath, deploymentName, description, custFilePath) {
    // Phase 1 — credentials
    const credentials = validateCredentials();

    // Phase 2 — file I/O (all disk reads before any network call)
    const zipFile  = readPackageFile(zipPath);
    const custFile = custFilePath ? readCustomizationFile(custFilePath) : null;
    const { formData, jsonPayload } = prepareDeploymentPayload(zipFile, custFile, deploymentName, description);

    console.log(`Uploading: ${zipFile.name} (${(zipFile.buf.length / 1024).toFixed(1)} KB)`);
    console.log('Payload:', JSON.stringify(jsonPayload, null, 2));

    // Phase 3 — network (no file reads from here onward)
    const triggerData = await sendDeployment(credentials, formData);
    process.stderr.write(`deploymentUuid: ${triggerData.uuid}\n`);

    const { status, data: pollData } = await pollStatus(credentials, triggerData.uuid);

    const objects = pollData.summary?.objects ?? {};
    console.log(`\n=== Deployment ${status} ===`);
    if (objects.total !== undefined) {
        console.log(`Objects — total: ${objects.total}, imported: ${objects.imported}, failed: ${objects.failed}, skipped: ${objects.skipped}`);
    }
    if (pollData.deploymentLogUrl) console.log(`Log: ${pollData.deploymentLogUrl}`);

    return { deploymentUuid: triggerData.uuid, status, summary: pollData.summary, logUrl: pollData.deploymentLogUrl };
}

// CLI entry point
// Usage: node index.js <zipPath> <deploymentName> [description] [customizationFilePath]
const zipPath        = process.argv[2];
const deploymentName = process.argv[3];
const description    = process.argv[4] && process.argv[4] !== 'null' ? process.argv[4] : null;
const custFilePath   = process.argv[5] && process.argv[5] !== 'null' ? process.argv[5] : null;

if (!zipPath || !deploymentName) {
    console.error('Usage: node index.js <zipPath> <deploymentName> [description] [customizationFilePath]');
    process.exit(1);
}

deployPackage(zipPath, deploymentName, description, custFilePath)
    .then(() => {})
    .catch(err => { console.error('\nError:', err.message); process.exit(1); });
