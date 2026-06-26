#!/usr/bin/env node
// anthropic-chat: Direct Anthropic Messages API caller

const http = require('http');
const https = require('https');
const { URL } = require('url');

const API_KEY = process.env.ANTHROPIC_API_KEY || process.env.ANTHROPOPIC_API_KEY;
const MODEL = process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-20250514';
const MAX_TOKENS = 4096;

if (!API_KEY) {
  console.error('Error: ANTHROPIC_API_KEY environment variable is not set.');
  console.error('Please set it in your environment or .env file.');
  process.exit(1);
}

const body = JSON.stringify({
  model: MODEL,
  max_tokens: MAX_TOKENS,
  messages: [{ role: 'user', content: TASK || 'Hello, Claude.' }]
});

const url = new URL('https://api.anthropic.com/v1/messages');
const options = {
  hostname: url.hostname,
  port: 443,
  path: url.pathname,
  method: 'POST',
  headers: {
    'x-api-key': API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json',
    'content-length': Buffer.byteLength(body)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    try {
      const parsed = JSON.parse(data);
      if (parsed.error) {
        console.error('API Error:', parsed.error);
        process.exit(1);
      }
      console.log(JSON.stringify(parsed, null, 2));
    } catch (e) {
      console.error('Failed to parse response:', data);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('Request failed:', e.message);
  process.exit(1);
});

req.write(body);
req.end();
