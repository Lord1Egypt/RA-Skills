#!/usr/bin/env node

/**
 * Agnes Video Generator Skill Script
 *
 * Usage:
 *   node generate.js --prompt "描述" [--image "url"] [--num_frames 121] [--frame_rate 24] [--size 1152x768]
 *
 * Asynchronous: creates task, polls until complete, returns video URL.
 */

const https = require('https');
const AGNES_API_KEY = process.env.AGNES_API_KEY;

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.prompt) {
    console.error(JSON.stringify({ success: false, error: '--prompt is required' }));
    process.exit(1);
  }

  // Build request body
  const body = {
    model: 'agnes-video-v2.0',
    prompt: args.prompt
  };

  if (args.num_frames) body.num_frames = parseInt(args.num_frames, 10);
  if (args.frame_rate) body.frame_rate = parseFloat(args.frame_rate);
  if (args.width) body.width = parseInt(args.width, 10);
  if (args.height) body.height = parseInt(args.height, 10);
  if (args.seed) body.seed = parseInt(args.seed, 10);
  if (args.negative_prompt) body.negative_prompt = args.negative_prompt;

  // Handle image input (single URL)
  if (args.image) {
    // For image-to-video, the AGNES API expects 'image' at top level
    body.image = args.image;
  }

  // Extra body for advanced modes
  if (args.extra_mode) {
    body.extra_body = { mode: args.extra_mode };
  }

  // Create video generation task
  createTask(body)
    .then(task => {
      const videoId = task.video_id;
      console.error(`Task created: ${task.task_id}, video_id: ${videoId}`);
      return pollVideo(videoId);
    })
    .then(result => {
      console.log(JSON.stringify({
        success: true,
        url: result.remixed_from_video_id,
        size: result.size,
        seconds: result.seconds,
        video_id: result.video_id,
        status: result.status
      }));
    })
    .catch(err => {
      console.error(JSON.stringify({ success: false, error: err.message }));
      process.exit(1);
    });
}

function createTask(body) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify(body);
    const options = {
      hostname: 'apihub.agnes-ai.com',
      port: 443,
      path: '/v1/videos',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${AGNES_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          try {
            const json = JSON.parse(data);
            if (json.video_id) {
              resolve(json);
            } else {
              reject(new Error('No video_id in response'));
            }
          } catch (e) {
            reject(new Error('Parse error: ' + e.message));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', e => reject(e));
    req.write(payload);
    req.end();
  });
}

function pollVideo(videoId, maxAttempts = 120, intervalMs = 5000) {
  return new Promise((resolve, reject) => {
    let attempts = 0;

    function check() {
      attempts++;
      queryVideo(videoId)
        .then(result => {
          if (result.status === 'completed') {
            resolve(result);
          } else if (result.status === 'failed') {
            reject(new Error(`Video generation failed: ${result.error ? JSON.stringify(result.error) : 'unknown error'}`));
          } else if (attempts >= maxAttempts) {
            reject(new Error('Polling timeout after ' + (maxAttempts * intervalMs / 1000) + ' seconds'));
          } else {
            setTimeout(check, intervalMs);
          }
        })
        .catch(reject);
    }

    check();
  });
}

function queryVideo(videoId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'apihub.agnes-ai.com',
      port: 443,
      path: `/agnesapi?video_id=${encodeURIComponent(videoId)}`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${AGNES_API_KEY}`
      }
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const json = JSON.parse(data);
            resolve(json);
          } catch (e) {
            reject(e);
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', e => reject(e));
    req.end();
  });
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--prompt' && argv[i+1]) {
      args.prompt = argv[++i];
    } else if (argv[i] === '--image' && argv[i+1]) {
      args.image = argv[++i];
    } else if (argv[i] === '--num_frames' && argv[i+1]) {
      args.num_frames = argv[++i];
    } else if (argv[i] === '--frame_rate' && argv[i+1]) {
      args.frame_rate = argv[++i];
    } else if (argv[i] === '--size' && argv[i+1]) {
      // Parse size like "1152x768"
      const parts = argv[++i].split('x');
      if (parts.length === 2) {
        args.width = parseInt(parts[0], 10);
        args.height = parseInt(parts[1], 10);
      }
    } else if (argv[i] === '--seed' && argv[i+1]) {
      args.seed = argv[++i];
    } else if (argv[i] === '--negative_prompt' && argv[i+1]) {
      args.negative_prompt = argv[++i];
    } else if (argv[i] === '--extra_mode' && argv[i+1]) {
      args.extra_mode = argv[++i];
    }
  }
  return args;
}

main();
