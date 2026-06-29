#!/usr/bin/env node

/**
 * Agnes Image-to-Image Wrapper
 * Accepts a local image file path, converts to base64, and sends image edit request.
 *
 * Usage:
 *   node img2img.js --prompt "description" --image "/path/to/file.jpg" [--size 720x1280]
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const AGNES_API_KEY = process.env.AGNES_API_KEY || process.env.AGNES_APIKEY;

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.prompt) {
    console.error(JSON.stringify({ success: false, error: '--prompt is required' }));
    process.exit(1);
  }
  if (!args.image) {
    console.error(JSON.stringify({ success: false, error: '--image (local file path) is required for img2img' }));
    process.exit(1);
  }

  // Read image file and convert to base64 Data URI
  let imagePath = args.image;
  if (!fs.existsSync(imagePath)) {
    console.error(JSON.stringify({ success: false, error: `Image file not found: ${imagePath}` }));
    process.exit(1);
  }

  const imgData = fs.readFileSync(imagePath);
  const base64 = imgData.toString('base64');

  // Determine MIME type from extension (simplified)
  const ext = path.extname(imagePath).toLowerCase();
  let mime = 'image/jpeg';
  if (ext === '.png') mime = 'image/png';
  else if (ext === '.gif') mime = 'image/gif';
  else if (ext === '.webp') mime = 'image/webp';

  const dataUri = `data:${mime};base64,${base64}`;

  const body = {
    model: 'agnes-image-2.1-flash',
    prompt: args.prompt,
    size: args.size || '1024x1024',
    extra_body: {
      image: [dataUri],
      response_format: 'url'
    }
  };

  const payload = JSON.stringify(body);

  const options = {
    hostname: 'apihub.agnes-ai.com',
    port: 443,
    path: '/v1/images/generations',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${AGNES_API_KEY}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  };

  const req = https.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      if (res.statusCode === 200) {
        try {
          const json = JSON.parse(data);
          const imageUrl = json.data && json.data[0] && json.data[0].url;
          if (imageUrl) {
            console.log(JSON.stringify({ success: true, url: imageUrl }));
          } else {
            console.error(JSON.stringify({ success: false, error: 'No image URL in response', raw: json }));
            process.exit(1);
          }
        } catch (e) {
          console.error(JSON.stringify({ success: false, error: 'Parse error: ' + e.message, raw: data }));
          process.exit(1);
        }
      } else {
        console.error(JSON.stringify({ success: false, error: `HTTP ${res.statusCode}: ${data}` }));
        process.exit(1);
      }
    });
  });

  req.on('error', (e) => {
    console.error(JSON.stringify({ success: false, error: 'Request failed: ' + e.message }));
    process.exit(1);
  });

  req.write(payload);
  req.end();
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--prompt' && argv[i+1]) {
      args.prompt = argv[++i];
    } else if (argv[i] === '--size' && argv[i+1]) {
      args.size = argv[++i];
    } else if (argv[i] === '--image' && argv[i+1]) {
      args.image = argv[++i];
    }
  }
  return args;
}

main();
