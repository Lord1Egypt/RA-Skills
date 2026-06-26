#!/usr/bin/env node
/**
 * Feishu Voice Message Sender
 * 
 * Sends voice/audio messages to Feishu users via Open API.
 * Audio must be in OPUS format.
 * 
 * Usage:
 *   node send-voice.mjs --app-id "cli_xxx" --app-secret "xxx" \
 *     --user-id "ou_xxx" --audio-file "voice.opus" --duration 3480
 * 
 * Or with environment variables:
 *   FEISHU_APP_ID, FEISHU_APP_SECRET
 */

import fs from 'fs';
import path from 'path';
import { parseArgs } from 'util';

// Parse command line arguments
const { values: args } = parseArgs({
    options: {
        'app-id': { type: 'string' },
        'app-secret': { type: 'string' },
        'user-id': { type: 'string' },
        'chat-id': { type: 'string' },
        'audio-file': { type: 'string' },
        'duration': { type: 'string' },
        'help': { type: 'boolean', short: 'h' }
    }
});

if (args.help) {
    console.log(`
Feishu Voice Message Sender

Usage:
  node send-voice.mjs [options]

Options:
  --app-id        Feishu App ID (or set FEISHU_APP_ID env)
  --app-secret    Feishu App Secret (or set FEISHU_APP_SECRET env)
  --user-id       Target user's Open ID (send to user)
  --chat-id       Target chat ID (send to group)
  --audio-file    Path to OPUS audio file (required)
  --duration      Audio duration in milliseconds (required)
  -h, --help      Show this help message

Examples:
  # Send to user
  node send-voice.mjs --app-id cli_xxx --app-secret xxx \\
    --user-id ou_xxx --audio-file voice.opus --duration 3480

  # Send to group chat
  node send-voice.mjs --app-id cli_xxx --app-secret xxx \\
    --chat-id oc_xxx --audio-file voice.opus --duration 3480
`);
    process.exit(0);
}

// Configuration
const APP_ID = args['app-id'] || process.env.FEISHU_APP_ID;
const APP_SECRET = args['app-secret'] || process.env.FEISHU_APP_SECRET;
const USER_ID = args['user-id'];
const CHAT_ID = args['chat-id'];
const AUDIO_FILE = args['audio-file'];
const DURATION_MS = parseInt(args['duration'] || '0', 10);

// Validate required parameters
function validateParams() {
    const errors = [];

    if (!APP_ID) errors.push('Missing --app-id or FEISHU_APP_ID env');
    if (!APP_SECRET) errors.push('Missing --app-secret or FEISHU_APP_SECRET env');
    if (!USER_ID && !CHAT_ID) errors.push('Missing --user-id or --chat-id');
    if (!AUDIO_FILE) errors.push('Missing --audio-file');
    if (!DURATION_MS || DURATION_MS <= 0) errors.push('Missing or invalid --duration');

    if (errors.length > 0) {
        console.error('❌ Validation errors:');
        errors.forEach(e => console.error(`   - ${e}`));
        console.error('\nRun with --help for usage information.');
        process.exit(1);
    }

    if (!fs.existsSync(AUDIO_FILE)) {
        console.error(`❌ Audio file not found: ${AUDIO_FILE}`);
        process.exit(1);
    }

    if (!AUDIO_FILE.endsWith('.opus')) {
        console.warn('⚠️  Warning: Audio file should be in OPUS format');
    }
}

// Get Tenant Access Token
async function getTenantAccessToken() {
    const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify({
            app_id: APP_ID,
            app_secret: APP_SECRET
        })
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to get token: ${data.msg}`);
    }

    console.log('✅ Got Tenant Access Token');
    return data.tenant_access_token;
}

// Upload audio file
async function uploadAudioFile(token) {
    const audioBuffer = fs.readFileSync(AUDIO_FILE);
    const fileName = path.basename(AUDIO_FILE);

    const formData = new FormData();
    formData.append('file_type', 'opus');
    formData.append('file_name', fileName);
    formData.append('duration', DURATION_MS.toString());
    formData.append('file', new Blob([audioBuffer]), fileName);

    const response = await fetch('https://open.feishu.cn/open-apis/im/v1/files', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to upload audio: ${JSON.stringify(data)}`);
    }

    console.log('✅ Uploaded audio file, file_key:', data.data.file_key);
    return data.data.file_key;
}

// Send audio message
async function sendAudioMessage(token, fileKey) {
    const receiveIdType = USER_ID ? 'open_id' : 'chat_id';
    const receiveId = USER_ID || CHAT_ID;

    const response = await fetch(`https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify({
            receive_id: receiveId,
            msg_type: 'audio',
            content: JSON.stringify({
                file_key: fileKey
            })
        })
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to send message: ${JSON.stringify(data)}`);
    }

    console.log('✅ Sent voice message!');
    console.log('   Message ID:', data.data.message_id);
    return data.data;
}

// Main function
async function main() {
    validateParams();

    console.log('🎤 Sending voice message to Feishu...\n');
    console.log(`📁 Audio file: ${path.resolve(AUDIO_FILE)}`);
    console.log(`⏱️  Duration: ${DURATION_MS}ms`);
    console.log(`📬 Target: ${USER_ID ? `User ${USER_ID}` : `Chat ${CHAT_ID}`}\n`);

    try {
        const token = await getTenantAccessToken();
        const fileKey = await uploadAudioFile(token);
        await sendAudioMessage(token, fileKey);
        console.log('\n🎉 Done!');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        process.exit(1);
    }
}

main();
