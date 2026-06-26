#!/usr/bin/env node
const https = require('https');

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = 'https://api.heybossai.com/v1';

const args = process.argv.slice(2);
const command = args[0];
const repo = args[1];
const extra = args[2];

if (!command || !repo) {
  console.log('Usage: deepwiki.js <command> <repo> [args]');
  console.log('Commands: ask, structure, contents');
  process.exit(0);
}

if (!SKILLBOSS_API_KEY) {
  console.error('Error: SKILLBOSS_API_KEY environment variable is required');
  process.exit(1);
}

function pilot(body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const options = {
      hostname: 'api.heybossai.com',
      path: '/v1/pilot',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SKILLBOSS_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); } catch (e) { reject(e); }
      });
    });

    req.on('error', reject);
    req.setTimeout(60000, () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });
    req.write(data);
    req.end();
  });
}

async function run() {
  const baseUrl = `https://deepwiki.com/${repo}`;

  if (command === 'structure') {
    // Scrape the DeepWiki index page via SkillBoss API Hub to get wiki structure
    const result = await pilot({
      type: 'scraper',
      inputs: { url: baseUrl }
    });
    const content = result.result.data.markdown;
    console.log(typeof content === 'string' ? content : JSON.stringify(content, null, 2));

  } else if (command === 'contents') {
    // Scrape a specific wiki path via SkillBoss API Hub
    const path = extra || '';
    const pageUrl = path ? `${baseUrl}/${path}` : baseUrl;
    const result = await pilot({
      type: 'scraper',
      inputs: { url: pageUrl }
    });
    const content = result.result.data.markdown;
    console.log(typeof content === 'string' ? content : JSON.stringify(content, null, 2));

  } else if (command === 'ask') {
    // Step 1: Scrape the repo wiki page via SkillBoss API Hub
    const scrapeResult = await pilot({
      type: 'scraper',
      inputs: { url: baseUrl }
    });
    const wikiContent = scrapeResult.result.data.markdown;
    const docText = typeof wikiContent === 'string' ? wikiContent : JSON.stringify(wikiContent);

    // Step 2: Use SkillBoss API Hub LLM chat to answer the question
    const chatResult = await pilot({
      type: 'chat',
      inputs: {
        messages: [
          {
            role: 'system',
            content: `You are a helpful assistant. Answer questions about the GitHub repository ${repo} based on the following documentation:\n\n${docText}`
          },
          {
            role: 'user',
            content: extra
          }
        ]
      },
      prefer: 'balanced'
    });
    const answer = chatResult.result.choices[0].message.content;
    console.log(answer);

  } else {
    console.error(`Unknown command: ${command}`);
    console.log('Commands: ask, structure, contents');
    process.exit(1);
  }
}

run().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
