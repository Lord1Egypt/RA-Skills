const ftp = require('basic-ftp');
const path = require('path');
const fs = require('fs');

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

async function downloadFile(client, remote, local) {
    const dirname = path.dirname(local);
    if (!fs.existsSync(dirname)) fs.mkdirSync(dirname, { recursive: true });
    // check if remote is a directory
    try {
        await client.cd(remote);
        // It's a directory
        await client.ensureDir(local);
        const list = await client.list();
        for (const item of list) {
            await downloadFile(client, path.posix.join(remote, item.name), path.join(local, item.name));
        }
    } catch (_) {
        // Assume it's a file
        await client.downloadTo(local, remote);
    }
}

async function main() {
    const args = require('minimist')(process.argv.slice(2));
    const host = args.host || (await loadCreds()).host;
    const user = args.user || (await loadCreds()).user;
    const password = args.password || (await loadCreds()).password;
    const remotePath = args.remotePath || args._[0];
    const localPath = args.localPath || args._[1] || '.';
    if (!remotePath) {
        console.error('Missing required remotePath');
        process.exit(1);
    }
    const client = new ftp.Client();
    client.ftp.verbose = false;
    try {
        await client.access({ host, user, password, secure: false });
        await downloadFile(client, remotePath, localPath);
        console.log('Download completed');
    } catch (err) {
        console.error('FTP download error:', err.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();