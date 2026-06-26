#!/usr/bin/env node
/**
 * Web Scraper via SkillBoss API Hub
 *
 * Usage: node crawl4ai.js "url" [--json]
 *
 * Output: Markdown content from the page
 */

const https = require('https');

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;

if (!SKILLBOSS_API_KEY) {
  console.error('SKILLBOSS_API_KEY environment variable is required');
  process.exit(1);
}

async function scrape(url) {
  const body = JSON.stringify({
    type: 'scraper',
    inputs: { url }
  });

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.heybossai.com',
      path: '/v1/pilot',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SKILLBOSS_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log('Web Scraper via SkillBoss API Hub');
    console.log('');
    console.log('Usage: node crawl4ai.js "url" [--json]');
    console.log('');
    console.log('Options:');
    console.log('  --json    Output full JSON response');
    console.log('');
    console.log('Environment:');
    console.log('  SKILLBOSS_API_KEY  SkillBoss API Hub key');
    process.exit(0);
  }

  const url = args.find(a => !a.startsWith('--'));
  const jsonOutput = args.includes('--json');

  try {
    const result = await scrape(url);

    if (jsonOutput) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      // Output content from SkillBoss scraping result
      const content = result?.result?.data;
      const md = (typeof content === 'string') ? content : (content?.markdown || content?.text || JSON.stringify(content));
      console.log(md);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
