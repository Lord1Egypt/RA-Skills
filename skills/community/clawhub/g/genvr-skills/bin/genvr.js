#!/usr/bin/env node

/**
 * GenVR CLI Toolkit (Pure Node.js Edition)
 * A standalone, zero-dependency CLI for the GenVR API.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { pipeline } = require('stream/promises');

// Helper: Minimal zero-dependency .env loader
function loadEnv() {
    const envPath = path.join(process.cwd(), '.env');
    if (fs.existsSync(envPath)) {
        const content = fs.readFileSync(envPath, 'utf8');
        content.split('\n').forEach(line => {
            const [key, ...value] = line.split('=');
            if (key && value.length > 0) {
                const k = key.trim();
                if (!process.env[k]) {
                    process.env[k] = value.join('=').trim().replace(/^["']|["']$/g, '');
                }
            }
        });
    }
}
loadEnv();

// Configuration
const BASE_URL = 'https://api.genvrresearch.com';

// Helper: Parse CLI arguments
function parseArgs(args) {
    const parsed = { _: [], params: {} };
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--')) {
            const key = arg.slice(2);
            if (i + 1 < args.length && !args[i + 1].startsWith('--') && args[i + 1].includes('=')) {
                // If next is a parameter like prompt=...
                parsed[key] = args[++i];
            } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
                parsed[key] = args[++i];
            } else {
                parsed[key] = true;
            }
        } else if (arg.includes('=')) {
            const [k, ...v] = arg.split('=');
            parsed.params[k] = v.join('=');
        } else {
            parsed._.push(arg);
        }
    }
    return parsed;
}

// Helper: Make API requests
async function request(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };

    if (process.env.GENVR_API_KEY) {
        headers['Authorization'] = `Bearer ${process.env.GENVR_API_KEY}`;
    }

    return new Promise((resolve, reject) => {
        const req = https.request(url, {
            method: options.method || 'GET',
            headers
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    try {
                        resolve(JSON.parse(body));
                    } catch (e) {
                        resolve(body);
                    }
                } else {
                    reject(new Error(`API Error (${res.statusCode}): ${body}`));
                }
            });
        });

        req.on('error', reject);
        if (options.body) {
            req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
        }
        req.end();
    });
}

// Helper: Download file
async function downloadFile(url, dest) {
    console.log(`Downloading result to ${path.basename(dest)}...`);
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            if (res.statusCode !== 200) {
                reject(new Error(`Failed to download: ${res.statusCode}`));
                return;
            }
            const fileStream = fs.createWriteStream(dest);
            res.pipe(fileStream);
            fileStream.on('finish', () => {
                fileStream.close();
                console.log(`Saved to ${path.resolve(dest)}`);
                resolve();
            });
        }).on('error', reject);
    });
}

// Commands
const commands = {
    async list(args) {
        const resp = await request('/api/models');
        const models = resp.data || [];
        
        if (args.json) {
            console.log(JSON.stringify(models, null, 2));
            return;
        }

        console.log('Available GenVR Models:');
        console.log('-----------------------');
        models.forEach(m => {
            console.log(`${m.name.padEnd(30)} | ${m.category.padEnd(15)} | ${m.subcategory}`);
        });
    },

    async generate(args) {
        const uid = args.uid || process.env.GENVR_UID;
        if (!uid) throw new Error('GENVR_UID is required. Use --uid or set environment variable.');

        const payload = {
            uid,
            category: args.category,
            subcategory: args.subcategory,
            ...args.params
        };

        console.log(`Starting task: ${args.category}/${args.subcategory}...`);
        const startResp = await request('/v2/generate', { method: 'POST', body: payload });
        const taskId = startResp.taskId || (startResp.data && startResp.data.id);

        if (!taskId) throw new Error(`Failed to start task: ${JSON.stringify(startResp)}`);
        console.log(`Task started. ID: ${taskId}`);

        if (args['no-wait']) return;

        // Polling
        while (true) {
            process.stdout.write('.');
            const statusResp = await request('/v2/status', {
                method: 'POST',
                body: { id: taskId, uid, category: args.category, subcategory: args.subcategory }
            });
            
            const data = statusResp.data || {};
            const status = data.status;

            if (status === 'completed') {
                console.log('\nTask completed!');
                const resultResp = await request('/v2/response', {
                    method: 'POST',
                    body: { id: taskId, uid, category: args.category, subcategory: args.subcategory }
                });
                
                const resultData = resultResp.data || {};
                const output = resultData.output;
                const url = Array.isArray(output) ? output[0] : output;

                if (!url) {
                    console.log('Result data:', JSON.stringify(resultData, null, 2));
                    return;
                }

                // Generate filename
                const cleanUrl = url.split('?')[0];
                const ext = path.extname(cleanUrl) || '.png';
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
                const filename = args.filename || `${timestamp}-${args.category}${ext}`;

                await downloadFile(url, filename);
                break;
            }

            if (status === 'failed') {
                console.log('\nTask failed.');
                throw new Error(data.error || data.message || 'Unknown error');
            }

            await new Promise(r => setTimeout(r, 2000));
        }
    },

    async status(args) {
        const uid = args.uid || process.env.GENVR_UID;
        const resp = await request('/v2/status', {
            method: 'POST',
            body: { id: args['job-id'], uid, category: args.category, subcategory: args.subcategory }
        });
        console.log(JSON.stringify(resp, null, 2));
    }
};

async function main() {
    const argv = parseArgs(process.argv.slice(2));
    const cmd = argv._[0];

    if (!cmd || cmd === 'help') {
        console.log(`
GenVR CLI Toolkit
Usage: npx genvr <command> [options]

Commands:
  list        List available models
  generate    Generate content (image, video, etc.)
  status      Check job status

Options for generate:
  --category <name>       e.g., imagegen
  --subcategory <name>    e.g., google_nano_banana_2
  --filename <name>       Output filename
  --no-wait               Return immediately
  key=value               Model parameters (e.g., prompt="A forest")

Options for status:
  --job-id <id>           Task ID to check
  --category <name>       Category of the task
  --subcategory <name>    Subcategory of the task

Authentication:
  Set GENVR_API_KEY and GENVR_UID environment variables.
        `);
        return;
    }

    if (!commands[cmd]) {
        console.error(`Unknown command: ${cmd}`);
        process.exit(1);
    }

    try {
        await commands[cmd](argv);
    } catch (e) {
        console.error(`Error: ${e.message}`);
        process.exit(1);
    }
}

main();
