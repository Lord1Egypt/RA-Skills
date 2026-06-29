#!/usr/bin/env node

/**
 * Agnes Image Generator Skill Script
 *
 * Usage:
 *   node generate.js --prompt "A cute puppy" [--size 1024x1024] [--image "url or data-uri"]
 *
 * Returns JSON: { success: true, url: "https://..." } or { success: false, error: "..." }
 */

const https = require('https');

const AGNES_API_KEY = process.env.AGNES_API_KEY || process.env.AGNES_APIKEY;

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.prompt) {
    console.error('Error: --prompt is required');
    process.exit(1);
  }

  const body = {
    model: 'agnes-image-2.1-flash',
    prompt: args.prompt,
    size: args.size || '1024x1024'
  };

  if (args.image) {
    // For img2img, extra_body contains image array
    body.extra_body = {
      image: [args.image],
      response_format: 'url'
    };
  } else {
    // For text2image, ensure response format is url
    body.extra_body = {
      response_format: 'url'
    };
  }

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
