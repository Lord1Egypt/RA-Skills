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

async function uploadFile(client, local, remote) {
    const stat = fs.statSync(local);
    if (stat.isDirectory()) {
        // ensure remote directory exists
        await client.ensureDir(remote);
        const files = fs.readdirSync(local);
        for (const f of files) {
            await uploadFile(client, path.join(local, f), path.posix.join(remote, f));
        }
    } else {
        await client.uploadFrom(local, remote);
    }
}

async function main() {
    const args = require('minimist')(process.argv.slice(2));
    const host = args.host || (await loadCreds()).host;
    const user = args.user || (await loadCreds()).user;
    const password = args.password || (await loadCreds()).password;
    const localPath = args.localPath || args._[0];
    const remotePath = args.remotePath || args._[1] || '/';
    if (!localPath) {
        console.error('Missing required --localPath');
        process.exit(1);
    }
    const client = new ftp.Client();
    client.ftp.verbose = false;
    try {
        await client.access({ host, user, password, secure: false });
        await uploadFile(client, localPath, remotePath);
        console.log('Upload completed');
    } catch (err) {
        console.error('FTP upload error:', err.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();