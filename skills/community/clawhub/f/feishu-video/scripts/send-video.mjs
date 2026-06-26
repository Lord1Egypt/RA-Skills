#!/usr/bin/env node
/**
 * Feishu Video Message Sender
 *
 * Sends video messages to Feishu users via Open API.
 * Video must be in MP4 format.
 *
 * Usage:
 *   node send-video.mjs --app-id "cli_xxx" --app-secret "xxx" \
 *     --user-id "ou_xxx" --video-file "video.mp4"
 *
 * Or with environment variables:
 *   FEISHU_APP_ID, FEISHU_APP_SECRET
 */

import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFileSync } from 'child_process';
import { parseArgs } from 'util';

// Parse command line arguments
const { values: args } = parseArgs({
    options: {
        'app-id': { type: 'string' },
        'app-secret': { type: 'string' },
        'user-id': { type: 'string' },
        'chat-id': { type: 'string' },
        'video-file': { type: 'string' },
        'duration': { type: 'string' },
        'segment-seconds': { type: 'string' },
        'max-size-mb': { type: 'string' },
        'no-cover': { type: 'boolean' },
        'help': { type: 'boolean', short: 'h' }
    }
});

if (args.help) {
    console.log(`
Feishu Video Message Sender

Usage:
  node send-video.mjs [options]

Options:
  --app-id        Feishu App ID (or set FEISHU_APP_ID env)
  --app-secret    Feishu App Secret (or set FEISHU_APP_SECRET env)
  --user-id       Target user's Open ID (send to user)
  --chat-id       Target chat ID (send to group)
  --video-file    Path to MP4 video file (required)
  --duration      Video duration in milliseconds (optional)
  --segment-seconds  Segment length in seconds (optional)
  --max-size-mb   Max upload size per segment in MB (default: 30)
  --no-cover      Skip auto cover extraction
  -h, --help      Show this help message

Examples:
  # Send to user
  node send-video.mjs --app-id cli_xxx --app-secret xxx \
    --user-id ou_xxx --video-file video.mp4

  # Send to group chat
  node send-video.mjs --app-id cli_xxx --app-secret xxx \
    --chat-id oc_xxx --video-file video.mp4
`);
    process.exit(0);
}

// Configuration
const APP_ID = args['app-id'] || process.env.FEISHU_APP_ID;
const APP_SECRET = args['app-secret'] || process.env.FEISHU_APP_SECRET;
const USER_ID = args['user-id'];
const CHAT_ID = args['chat-id'];
const VIDEO_FILE = args['video-file'];
const DURATION_MS = parseInt(args['duration'] || '0', 10);
const SKIP_COVER = Boolean(args['no-cover']);
const MAX_UPLOAD_MB = parseFloat(args['max-size-mb'] || '30');
const MAX_UPLOAD_BYTES = Math.floor(MAX_UPLOAD_MB * 1024 * 1024);
const SEGMENT_SECONDS = parseInt(args['segment-seconds'] || '0', 10);

// Validate required parameters
function validateParams() {
    const errors = [];

    if (!APP_ID) errors.push('Missing --app-id or FEISHU_APP_ID env');
    if (!APP_SECRET) errors.push('Missing --app-secret or FEISHU_APP_SECRET env');
    if (!USER_ID && !CHAT_ID) errors.push('Missing --user-id or --chat-id');
    if (!VIDEO_FILE) errors.push('Missing --video-file');
    if (args.duration && (!DURATION_MS || DURATION_MS <= 0)) {
        errors.push('Invalid --duration');
    }
    if (args['max-size-mb'] && (!MAX_UPLOAD_MB || MAX_UPLOAD_MB <= 0)) {
        errors.push('Invalid --max-size-mb');
    }
    if (args['segment-seconds'] && (!SEGMENT_SECONDS || SEGMENT_SECONDS <= 0)) {
        errors.push('Invalid --segment-seconds');
    }

    if (errors.length > 0) {
        console.error('❌ Validation errors:');
        errors.forEach(e => console.error(`   - ${e}`));
        console.error('\nRun with --help for usage information.');
        process.exit(1);
    }

    if (!fs.existsSync(VIDEO_FILE)) {
        console.error(`❌ Video file not found: ${VIDEO_FILE}`);
        process.exit(1);
    }

    if (!VIDEO_FILE.endsWith('.mp4')) {
        console.warn('⚠️  Warning: Video file should be in MP4 format');
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

// Upload video file
async function uploadVideoFile(token, filePath, durationMs) {
    const videoBuffer = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);

    const formData = new FormData();
    formData.append('file_type', 'mp4');
    formData.append('file_name', fileName);
    if (durationMs && durationMs > 0) {
        formData.append('duration', durationMs.toString());
    }
    formData.append('file', new Blob([videoBuffer]), fileName);

    const response = await fetch('https://open.feishu.cn/open-apis/im/v1/files', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to upload video: ${JSON.stringify(data)}`);
    }

    console.log('✅ Uploaded video file, file_key:', data.data.file_key);
    return data.data.file_key;
}

// Extract cover image using ffmpeg
function extractCoverImage(filePath) {
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'feishu-video-'));
    const coverPath = path.join(tempDir, 'cover.jpg');

    execFileSync('ffmpeg', [
        '-y',
        '-i', filePath,
        '-frames:v', '1',
        '-q:v', '2',
        coverPath
    ], { stdio: 'ignore' });

    return coverPath;
}

// Upload cover image
async function uploadCoverImage(token, coverPath) {
    const coverBuffer = fs.readFileSync(coverPath);
    const formData = new FormData();
    formData.append('image_type', 'message');
    formData.append('image', new Blob([coverBuffer]), 'cover.jpg');

    const response = await fetch('https://open.feishu.cn/open-apis/im/v1/images', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to upload cover: ${JSON.stringify(data)}`);
    }

    console.log('✅ Uploaded cover image, image_key:', data.data.image_key);
    return data.data.image_key;
}

function getVideoInfo(filePath) {
    const output = execFileSync('ffprobe', [
        '-v', 'error',
        '-show_entries', 'format=duration,bit_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        filePath
    ], { encoding: 'utf8' }).trim();

    const [durationStr, bitRateStr] = output.split('\n');
    const durationSeconds = parseFloat(durationStr || '0');
    const bitRate = parseInt(bitRateStr || '0', 10);
    return { durationSeconds, bitRate };
}

function splitVideoIntoSegments(filePath) {
    const { durationSeconds, bitRate } = getVideoInfo(filePath);
    if (!durationSeconds || !bitRate) {
        throw new Error('Unable to read video metadata for segmentation');
    }

    const targetBytes = Math.floor(MAX_UPLOAD_BYTES * 0.95);
    const autoSegmentSeconds = Math.max(1, Math.floor((targetBytes * 8) / bitRate));
    const segmentSeconds = SEGMENT_SECONDS > 0 ? SEGMENT_SECONDS : autoSegmentSeconds;
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'feishu-video-seg-'));
    const outputPattern = path.join(tempDir, 'segment-%03d.mp4');

    execFileSync('ffmpeg', [
        '-y',
        '-i', filePath,
        '-c', 'copy',
        '-f', 'segment',
        '-segment_time', `${segmentSeconds}`,
        '-reset_timestamps', '1',
        outputPattern
    ], { stdio: 'ignore' });

    const segments = fs.readdirSync(tempDir)
        .filter(name => name.endsWith('.mp4'))
        .sort()
        .map(name => path.join(tempDir, name));

    return { segments, tempDir };
}

// Send video message
async function sendVideoMessage(token, fileKey, imageKey) {
    const receiveIdType = USER_ID ? 'open_id' : 'chat_id';
    const receiveId = USER_ID || CHAT_ID;

    const content = {
        file_key: fileKey
    };
    if (imageKey) {
        content.image_key = imageKey;
    }

    const response = await fetch(`https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify({
            receive_id: receiveId,
            msg_type: 'media',
            content: JSON.stringify(content)
        })
    });

    const data = await response.json();
    if (data.code !== 0) {
        throw new Error(`Failed to send message: ${JSON.stringify(data)}`);
    }

    console.log('✅ Sent video message!');
    console.log('   Message ID:', data.data.message_id);
    return data.data;
}

// Main function
async function main() {
    validateParams();

    console.log('🎬 Sending video message to Feishu...\n');
    console.log(`📁 Video file: ${path.resolve(VIDEO_FILE)}`);
    if (args.duration) {
        console.log(`⏱️  Duration: ${DURATION_MS}ms`);
    }
    console.log(`📬 Target: ${USER_ID ? `User ${USER_ID}` : `Chat ${CHAT_ID}`}\n`);

    try {
        const token = await getTenantAccessToken();
        const fileSize = fs.statSync(VIDEO_FILE).size;
        let segments = [VIDEO_FILE];
        let segmentTempDir = null;

        if (fileSize > MAX_UPLOAD_BYTES) {
            console.warn(`⚠️  File larger than ${MAX_UPLOAD_MB}MB (${(fileSize / 1024 / 1024).toFixed(2)}MB), splitting...`);
            const splitResult = splitVideoIntoSegments(VIDEO_FILE);
            segments = splitResult.segments;
            segmentTempDir = splitResult.tempDir;
            console.log(`✅ Split into ${segments.length} segments`);
        }

        for (let i = 0; i < segments.length; i += 1) {
            const segmentPath = segments[i];
            const segmentLabel = segments.length > 1 ? `(${i + 1}/${segments.length}) ` : '';
            let segmentDuration = null;

            if (args.duration && segments.length === 1) {
                segmentDuration = DURATION_MS;
            } else {
                try {
                    const info = getVideoInfo(segmentPath);
                    if (info.durationSeconds) {
                        segmentDuration = Math.round(info.durationSeconds * 1000);
                    }
                } catch {
                    segmentDuration = null;
                }
            }

            const fileKey = await uploadVideoFile(token, segmentPath, segmentDuration);
            let imageKey = null;

            if (!SKIP_COVER) {
                try {
                    const coverPath = extractCoverImage(segmentPath);
                    imageKey = await uploadCoverImage(token, coverPath);
                    fs.rmSync(path.dirname(coverPath), { recursive: true, force: true });
                } catch (error) {
                    console.warn(`⚠️  ${segmentLabel}Failed to generate cover image, sending without cover`);
                    console.warn(`   ${error.message}`);
                }
            }

            await sendVideoMessage(token, fileKey, imageKey);
            if (segments.length > 1) {
                console.log(`✅ ${segmentLabel}Sent`);
            }
        }

        if (segmentTempDir) {
            fs.rmSync(segmentTempDir, { recursive: true, force: true });
        }
        console.log('\n🎉 Done!');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        process.exit(1);
    }
}

main();
