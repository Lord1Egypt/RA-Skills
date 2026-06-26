const ftp = require('basic-ftp');
const path = require('path');

async function loadCreds() {
    // Try OpenClaw secret store first
    try {
        const { execSync } = require('child_process');
        const out = execSync('openclaw secrets get ftp-client-zc/cred', { encoding: 'utf8' }).trim();
        if (out) {
            return JSON.parse(out);
        }
    } catch (_) {}
    // Fallback to local creds.json
    try {
        const creds = require(path.join(__dirname, '..', 'creds.json'));
        return creds;
    } catch (e) {
        console.error('Unable to load stored credentials. Provide host/user/password as args.');
        process.exit(1);
    }
}

async function main() {
    const args = require('minimist')(process.argv.slice(2));
    const host = args.host || (await loadCreds()).host;
    const user = args.user || (await loadCreds()).user;
    const password = args.password || (await loadCreds()).password;
    const remotePath = args.path || '/';

    const client = new ftp.Client();
    client.ftp.verbose = false;
    try {
        await client.access({ host, user, password, secure: false });
        const list = await client.list(remotePath);
        console.log(JSON.stringify(list, null, 2));
    } catch (err) {
        console.error('FTP list error:', err.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();