#!/usr/bin/env node
const path = require('path');
const args = require('minimist')(process.argv.slice(2));
const action = args._[0];
if (!action) {
    console.error('No action specified. Use one of: list, upload, download, delete, rename');
    process.exit(1);
}
const scriptMap = {
    list: path.join(__dirname, 'list.js'),
    upload: path.join(__dirname, 'upload.js'),
    download: path.join(__dirname, 'download.js'),
    delete: path.join(__dirname, 'delete.js'),
    rename: path.join(__dirname, 'rename.js')
};
const script = scriptMap[action];
if (!script) {
    console.error(`Unknown action: ${action}`);
    process.exit(1);
}
require('child_process').spawnSync('node', [script, ...process.argv.slice(3)], { stdio: 'inherit' });