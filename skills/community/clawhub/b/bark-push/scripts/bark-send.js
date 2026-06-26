#!/usr/bin/env node
/**
 * Bark Push Notification Script (Node.js)
 * 
 * Usage: node bark-send.js [options]
 * 
 * Options:
 *   -t, --title     Push title (required)
 *   -b, --body     Push body/content (required)
 *   -k, --key      Device key (optional, uses process.env.BARK_KEY if not provided)
 *   -s, --sound    Sound name (optional, default: default)
 *   -B, --badge    Badge number (optional)
 *   -u, --url      Click跳转URL (optional)
 *   -g, --group    Group name (optional)
 *   -l, --level    Notification level: critical/active/timeSensitive/passive (optional)
 *   -i, --image    Image URL (optional)
 *   -S, --subtitle Subtitle (optional)
 *   -h, --help     Show help
 * 
 * Examples:
 *   node bark-send.js -t "标题" -b "内容"
 *   node bark-send.js --title "提醒" --body "时间到了" --sound alarm
 *   BARK_KEY=your_key node bark-send.js -t "测试" -b "推送测试"
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {
    title: '',
    body: '',
    key: process.env.BARK_KEY || process.env.BARK_DEVICE_KEY || '',
    sound: 'default',
    badge: null,
    url: '',
    group: '',
    level: '',
    image: '',
    subtitle: ''
};

for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
        case '-t':
        case '--title':
            options.title = args[++i];
            break;
        case '-b':
        case '--body':
            options.body = args[++i];
            break;
        case '-k':
        case '--key':
            options.key = args[++i];
            break;
        case '-s':
        case '--sound':
            options.sound = args[++i];
            break;
        case '-B':
        case '--badge':
            options.badge = parseInt(args[++i], 10);
            break;
        case '-u':
        case '--url':
            options.url = args[++i];
            break;
        case '-g':
        case '--group':
            options.group = args[++i];
            break;
        case '-l':
        case '--level':
            options.level = args[++i];
            break;
        case '-i':
        case '--image':
            options.image = args[++i];
            break;
        case '-S':
        case '--subtitle':
            options.subtitle = args[++i];
            break;
        case '-h':
        case '--help':
            showHelp();
            process.exit(0);
        default:
            console.error(`Unknown option: ${args[i]}`);
            showHelp();
            process.exit(1);
    }
}

function showHelp() {
    const helpText = `
Bark Push Notification Script

Usage: node bark-send.js [options]

Options:
  -t, --title     Push title (required)
  -b, --body     Push body/content (required)
  -k, --key      Device key (optional, uses BARK_KEY env if not provided)
  -s, --sound    Sound name (optional, default: default)
  -B, --badge    Badge number (optional)
  -u, --url      Click跳转URL (optional)
  -g, --group    Group name (optional)
  -l, --level    Notification level: critical/active/timeSensitive/passive (optional)
  -i, --image    Image URL (optional)
  -S, --subtitle Subtitle (optional)
  -h, --help     Show help

Examples:
  node bark-send.js -t "标题" -b "内容"
  node bark-send.js --title "提醒" --body "时间到了" --sound alarm
  BARK_KEY=your_key node bark-send.js -t "测试" -b "推送测试"
`;
    console.log(helpText);
}

// Validate required parameters
if (!options.title) {
    console.error('Error: Title is required');
    process.exit(1);
}

if (!options.body) {
    console.error('Error: Body is required');
    process.exit(1);
}

if (!options.key) {
    console.error('Error: Device key is required. Set BARK_KEY env or use -k option');
    process.exit(1);
}

// Build request payload
const payload = {
    title: options.title,
    body: options.body
};

if (options.subtitle) payload.subtitle = options.subtitle;
if (options.sound) payload.sound = options.sound;
if (options.badge !== null) payload.badge = options.badge;
if (options.url) payload.url = options.url;
if (options.group) payload.group = options.group;
if (options.level) payload.level = options.level;
if (options.image) payload.image = options.image;

// Build API URL
const apiUrl = new URL(`https://api.day.app/${options.key}`);

// Send request
const postData = JSON.stringify(payload);

const requestOptions = {
    hostname: apiUrl.hostname,
    port: 443,
    path: apiUrl.pathname + apiUrl.search,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
    }
};

const req = https.request(requestOptions, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            const result = JSON.parse(data);
            if (result.code === 200) {
                console.log('✓ Push notification sent successfully!');
                console.log(`  Title: ${options.title}`);
                console.log(`  Body: ${options.body}`);
                process.exit(0);
            } else {
                console.error('✗ Failed to send push notification');
                console.error(`  Response: ${data}`);
                process.exit(1);
            }
        } catch (e) {
            console.error('✗ Failed to parse response');
            console.error(`  Response: ${data}`);
            process.exit(1);
        }
    });
});

req.on('error', (error) => {
    console.error('✗ Request error:', error.message);
    process.exit(1);
});

req.write(postData);
req.end();
