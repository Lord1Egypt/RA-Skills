#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Get the script directory
const scriptDir = __dirname;

// Get arguments
const args = process.argv.slice(2);

if (args.length === 0) {
    console.log('Facebook Advanced CLI');
    console.log('');
    console.log('Usage: facebook-advanced <command> [options]');
    console.log('');
    console.log('Commands:');
    console.log('  fb-post-list <page_id> [--fields fields] [--limit N]     List posts from a page');
    console.log('  fb-post-create <page_id> --message "text" [--link "url"] Create a post');
    console.log('  fb-post-read <post_id>                                   Read a specific post');
    console.log('  fb-post-hide <post_id>                                   Hide a post');
    console.log('  fb-post-delete <post_id> [--force]                       Delete a post');
    console.log('  fb-comment-list <post_id> [--limit N]                    List comments');
    console.log('  fb-comment-create <post_id> --message "text"             Create a comment');
    console.log('  fb-comment-delete <comment_id> [--force]                 Delete a comment');
    console.log('  fb-page-info <page_id>                                   Get page info');
    console.log('');
    console.log('See SKILL.md for full documentation.');
    process.exit(0);
}

const command = args[0];
const commandArgs = args.slice(1);

// Map commands to PowerShell scripts
const commandMap = {
    'fb-post-list': 'fb-post-list.ps1',
    'fb-post-create': 'fb-post-create.ps1',
    'fb-post-read': 'fb-post-read.ps1',
    'fb-post-hide': 'fb-post-hide.ps1',
    'fb-post-delete': 'fb-post-delete.ps1',
    'fb-comment-list': 'fb-comment-list.ps1',
    'fb-comment-create': 'fb-comment-create.ps1',
    'fb-comment-delete': 'fb-comment-delete.ps1',
    'fb-page-info': 'fb-page-info.ps1'
};

const scriptFile = commandMap[command];

if (!scriptFile) {
    console.error(`Unknown command: ${command}`);
    console.error('Available commands:', Object.keys(commandMap).join(', '));
    process.exit(1);
}

const scriptPath = path.join(scriptDir, scriptFile);

// Check if PowerShell is available
const isWindows = process.platform === 'win32';
const pwsh = isWindows ? 'powershell.exe' : 'pwsh';

// Run the PowerShell script
const ps = spawn(pwsh, ['-ExecutionPolicy', 'Bypass', '-File', scriptPath, ...commandArgs], {
    stdio: 'inherit',
    cwd: scriptDir
});

ps.on('error', (err) => {
    console.error(`Failed to start PowerShell: ${err.message}`);
    console.error('Make sure PowerShell is installed and in your PATH.');
    process.exit(1);
});

ps.on('close', (code) => {
    process.exit(code);
});
