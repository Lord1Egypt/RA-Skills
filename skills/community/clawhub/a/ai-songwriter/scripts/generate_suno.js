#!/usr/bin/env node
/**
 * Suno Music Generator via kie.ai API
 * 
 * Usage:
 *   generate:  node generate_suno.js "歌名" "歌词+元标签" "风格标签"
 *   extend:    node generate_suno.js --extend <audioId> <continueAt_sec> "续写歌词" [model]
 *   cover:     node generate_suno.js --cover <audioUrl> [model]
 *   upload-ext: node generate_suno.js --upload-extend <audioUrl> "续写歌词" [model]
 */

const https = require('https');
const API_KEY = process.env.KIE_API_KEY || process.env.SUNO_API_KEY;
if (!API_KEY) {
  console.error("Error: KIE_API_KEY or SUNO_API_KEY environment variable is missing.");
  process.exit(1);
}
const HOST = 'api.kie.ai';
const DEFAULT_MODEL = 'V5';

// ─── HTTP helper ───
function request(method, path, body) {
  const data = body ? JSON.stringify(body) : null;
  const headers = { 'Authorization': `Bearer ${API_KEY}` };
  if (data) { headers['Content-Type'] = 'application/json'; headers['Content-Length'] = Buffer.byteLength(data); }
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname: HOST, port: 443, path, method, headers }, (res) => {
      let buf = '';
      res.on('data', c => buf += c);
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch(e) { reject(e); }});
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─── Polling ───
async function waitForTask(taskId) {
  console.log(`[Task ${taskId}] Generating via Suno ${DEFAULT_MODEL}... Polling every 10s.`);
  while (true) {
    process.stdout.write('.');
    const res = await request('GET', `/api/v1/generate/record-info?taskId=${taskId}`);
    if (res.code !== 200) throw new Error(`API Error: ${res.msg}`);
    
    // Status enum usually: SUCCESS, FAILED, RUNNING/PENDING
    const status = res.data.status;
    if (status === 'SUCCESS') {
      console.log('\n--- GENERATION COMPLETE ---');
      res.data.sunoData.forEach((song, i) => {
        console.log(`\nTrack ${i+1}: ${song.title}`);
        console.log(`Audio URL: ${song.audioUrl}`);
        console.log(`Video URL: ${song.videoUrl}`);
        console.log(`Duration: ${song.duration}s`);
        console.log(`Audio ID (for extension): ${song.id}`);
      });
      return res.data;
    } else if (status === 'FAILED') {
      console.log('\nTask failed.');
      console.log(JSON.stringify(res.data, null, 2));
      process.exit(1);
    }
    await sleep(10000);
  }
}

// ─── Main ───
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Missing arguments.");
    process.exit(1);
  }

  try {
    let res;
    if (args[0] === '--extend') {
      // [audioId] [continueAt] [prompt] [model]
      const body = {
        audioId: args[1],
        continueAt: parseInt(args[2], 10),
        prompt: args[3],
        model: args[4] || DEFAULT_MODEL,
        defaultParamFlag: true,
        callBackUrl: "https://example.com/callback"
      };
      res = await request('POST', '/api/v1/generate/extend', body);
    } else if (args[0] === '--cover') {
      // [audioUrl] [model]
      const body = { audioUrl: args[1], model: args[2] || DEFAULT_MODEL, callBackUrl: "https://example.com/callback" };
      res = await request('POST', '/api/v1/generate/cover', body);
    } else if (args[0] === '--upload-extend') {
      // [audioUrl] [prompt] [model]
      const body = { audioUrl: args[1], prompt: args[2], model: args[3] || DEFAULT_MODEL, callBackUrl: "https://example.com/callback" };
      res = await request('POST', '/api/v1/generate/upload-extend', body);
    } else {
      // Normal generate: [title] [prompt] [tags]
      const body = {
        title: args[0],
        prompt: args[1],
        tags: args[2],
        model: DEFAULT_MODEL,
        customMode: true,
        instrumental: false,
        callBackUrl: "https://example.com/callback"
      };
      res = await request('POST', '/api/v1/generate', body);
    }

    if (res.code !== 200) {
      console.error("API request failed:", res);
      process.exit(1);
    }
    await waitForTask(res.data.taskId);
  } catch (err) {
    console.error("\nExecution error:", err);
    process.exit(1);
  }
}

main();
