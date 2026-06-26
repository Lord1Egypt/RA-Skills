/**
 * @skill       appian-listpkg
 * @version     1.1.0
 * @description List all packages for an Appian application via the v2 Deployment Management API.
 *
 * @security-manifest
 *   env-accessed:       APPIAN_BASE_URL, APPIAN_API_KEY
 *   external-endpoints: GET ${APPIAN_BASE_URL}/applications/{uuid}/packages
 *   file-operations:    none
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

// ── Phase 2: No file I/O ───────────────────────────────────────────────────
// This skill performs no disk reads or writes.

// ── Phase 3: Network ───────────────────────────────────────────────────────

async function listPackages(applicationUuid) {
    // Phase 1 — credentials
    const credentials = validateCredentials();

    // Phase 3 — network (no file I/O for this skill)
    const url = `${credentials.baseUrl}/applications/${applicationUuid}/packages`;
    process.stderr.write(`GET ${url}\n`);

    const res = await fetch(url, { headers: { 'appian-api-key': credentials.apiKey } });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`Request failed [${res.status}]: ${text}`);
    }

    const data     = await res.json();
    const packages = data.packages ?? [];

    if (packages.length === 0) {
        console.log('No packages found for this application.');
        return data;
    }

    console.log(`Found ${data.totalPackageCount} package(s):\n`);
    for (const pkg of packages) {
        console.log(`  Name:     ${pkg.name}`);
        console.log(`  UUID:     ${pkg.uuid}`);
        console.log(`  Objects:  ${pkg.objectCount}${pkg.databaseScriptCount ? ` + ${pkg.databaseScriptCount} DB scripts` : ''}`);
        console.log(`  Created:  ${pkg.createdTimestamp}`);
        console.log(`  Modified: ${pkg.lastModifiedTimestamp}`);
        if (pkg.description)           console.log(`  Desc:     ${pkg.description}`);
        if (pkg.ticketLink)            console.log(`  Ticket:   ${pkg.ticketLink}`);
        if (pkg.hasCustomizationFile)  console.log(`  Has customization file: yes`);
        console.log('');
    }

    return data;
}

// CLI entry point
// Usage: node index.js <applicationUuid>
const applicationUuid = process.argv[2];
if (!applicationUuid) {
    console.error('Usage: node index.js <applicationUuid>');
    process.exit(1);
}

listPackages(applicationUuid)
    .then(() => {})
    .catch(err => { console.error('Error:', err.message); process.exit(1); });
