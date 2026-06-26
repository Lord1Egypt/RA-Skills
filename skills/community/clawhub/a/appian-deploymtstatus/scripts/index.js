/**
 * @skill       appian-deploymtstatus
 * @version     1.2.0
 * @description Check the status of an Appian deployment and optionally download artifacts.
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: GET ${APPIAN_BASE_URL}/deployments/{uuid}, artifact URLs from Appian response
 *   file-operations:    optionally writes log/ZIP to ~/appian-exports/ (only when --download-* flags passed)
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

// ── Phase 2: File I/O ──────────────────────────────────────────────────────
// Prepare output directory if downloads requested. No network calls here.

function prepareOutputDir(needsDir) {
    const destDir = path.join(os.homedir(), 'appian-exports');
    if (needsDir) fs.mkdirSync(destDir, { recursive: true });
    return destDir;
}

// ── Phase 3: Network ───────────────────────────────────────────────────────
// All network calls and artifact writes happen here.

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchStatus(credentials, deploymentUuid, wait) {
    const pollUrl   = `${credentials.baseUrl}/deployments/${deploymentUuid}`;
    const TERMINAL  = new Set([
        'COMPLETED', 'COMPLETED_WITH_IMPORT_ERRORS', 'COMPLETED_WITH_PUBLISH_ERRORS',
        'FAILED', 'PENDING_REVIEW', 'REJECTED',
    ]);
    let data;
    let attempt       = 0;
    const maxAttempts = wait ? 72 : 1;

    do {
        if (attempt > 0) await sleep(5000);
        const res = await fetch(pollUrl, { headers: { 'appian-api-key': credentials.apiKey } });
        if (!res.ok) {
            const text = await res.text().catch(() => '');
            throw new Error(`Status fetch failed [${res.status}]: ${text}`);
        }
        data = await res.json();
        const status = data.status ?? '';
        if (wait && attempt > 0) process.stderr.write(`[${attempt}/${maxAttempts}] status: ${status}\n`);
        attempt++;
        if (TERMINAL.has(status)) break;
    } while (attempt < maxAttempts);

    return data;
}

async function downloadArtifact(url, apiKey, destDir, fallbackName) {
    const res = await fetch(url, { headers: { 'appian-api-key': apiKey } });
    if (!res.ok) {
        process.stderr.write(`  Download failed [${res.status}]: ${url}\n`);
        return null;
    }
    const cd        = res.headers.get('content-disposition') ?? '';
    const nameMatch = cd.match(/filename[^;=\n]*=(['"]?)([^\n"';]+)\1/);
    const fileName  = nameMatch?.[2]?.trim() ?? fallbackName;
    const outPath   = path.join(destDir, fileName);
    fs.writeFileSync(outPath, Buffer.from(await res.arrayBuffer()));
    console.log(`  Saved: ${outPath} (${(fs.statSync(outPath).size / 1024).toFixed(1)} KB)`);
    return outPath;
}

async function getDeploymentStatus(deploymentUuid, opts = {}) {
    // Phase 1 — credentials
    const credentials = validateCredentials();

    // Phase 2 — prepare output dir (no network)
    const destDir = prepareOutputDir(opts.downloadLog || opts.downloadZip);

    // Phase 3 — network
    const data    = await fetchStatus(credentials, deploymentUuid, opts.wait);
    const status  = data.status ?? 'UNKNOWN';
    const summary = data.summary ?? {};
    const objects = summary.objects ?? {};

    console.log(`\n=== Deployment ${deploymentUuid} ===`);
    console.log(`Status: ${status}`);
    if (objects.total !== undefined) {
        console.log(`Objects — total: ${objects.total}, imported: ${objects.imported}, failed: ${objects.failed}, skipped: ${objects.skipped}`);
    }
    if (data.deploymentLogUrl)          console.log(`Log URL:     ${data.deploymentLogUrl}`);
    if (data.packageZip)                console.log(`Package ZIP: ${data.packageZip}`);
    if (data.pluginsZip)                console.log(`Plugins ZIP: ${data.pluginsZip}`);
    if (data.customizationFile)         console.log(`Cust. File:  ${data.customizationFile}`);
    if (data.customizationFileTemplate) console.log(`Cust. Tmpl:  ${data.customizationFileTemplate}`);
    if (data.databaseScripts?.length)   console.log(`DB Scripts:  ${data.databaseScripts.length} file(s)`);

    const downloads = [];
    if (opts.downloadLog && data.deploymentLogUrl) {
        process.stderr.write('\nDownloading log...\n');
        const f = await downloadArtifact(data.deploymentLogUrl, credentials.apiKey, destDir, `${deploymentUuid}-log.txt`);
        if (f) downloads.push(f);
    }
    if (opts.downloadZip && data.packageZip) {
        process.stderr.write('\nDownloading package ZIP...\n');
        const f = await downloadArtifact(data.packageZip, credentials.apiKey, destDir, `${deploymentUuid}.zip`);
        if (f) downloads.push(f);
    }

    return { deploymentUuid, status, summary, downloads };
}

// CLI entry point
// Usage: node index.js <deploymentUuid> [--wait] [--download-log] [--download-zip]
const args           = process.argv.slice(2);
const deploymentUuid = args.find(a => !a.startsWith('--'));
const wait           = args.includes('--wait');
const downloadLog    = args.includes('--download-log');
const downloadZip    = args.includes('--download-zip');

if (!deploymentUuid) {
    console.error('Usage: node index.js <deploymentUuid> [--wait] [--download-log] [--download-zip]');
    process.exit(1);
}

getDeploymentStatus(deploymentUuid, { wait, downloadLog, downloadZip })
    .then(() => {})
    .catch(err => { console.error('\nError:', err.message); process.exit(1); });
