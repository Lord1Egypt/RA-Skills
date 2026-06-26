#!/usr/bin/env node
/**
 * Cloudflare Browser Rendering Crawl CLI
 * 
 * Usage:
 *   node crawl.js start <url> [options]
 *   node crawl.js status <job_id>
 *   node crawl.js results <job_id> [options]
 *   node crawl.js cancel <job_id>
 * 
 * Environment:
 *   CLOUDFLARE_API_TOKEN - API token with Browser Rendering permission
 *   CLOUDFLARE_ACCOUNT_ID - Your Cloudflare account ID
 */

const API_TOKEN = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT_ID = process.env.CLOUDFLARE_ACCOUNT_ID;
const BASE_URL = `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/browser-rendering/crawl`;

if (!API_TOKEN || !ACCOUNT_ID) {
  console.error('Error: Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID');
  process.exit(1);
}

const headers = {
  'Authorization': `Bearer ${API_TOKEN}`,
  'Content-Type': 'application/json'
};

// Parse CLI arguments
const args = process.argv.slice(2);
const command = args[0];

function parseOptions(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1];
      if (val && !val.startsWith('--')) {
        opts[key] = isNaN(val) ? val : Number(val);
        i++;
      } else {
        opts[key] = true;
      }
    }
  }
  return opts;
}

async function startCrawl(url, options = {}) {
  const body = {
    url,
    limit: options.limit || 10,
    depth: options.depth || 100,
    formats: options.format ? [options.format] : ['markdown'],
    render: options.render !== false
  };
  
  if (options.source) body.source = options.source;
  if (options.prompt) {
    body.formats = ['json'];
    body.jsonOptions = { prompt: options.prompt };
  }
  
  console.log(`Starting crawl: ${url}`);
  console.log(`Options: limit=${body.limit}, depth=${body.depth}, formats=${body.formats.join(',')}`);
  
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  });
  
  const data = await res.json();
  
  if (!data.success) {
    console.error('Error:', data.errors || data);
    process.exit(1);
  }
  
  const jobId = data.result;
  console.log(`\nJob started: ${jobId}`);
  console.log(`\nCheck status: node crawl.js status ${jobId}`);
  console.log(`Get results:  node crawl.js results ${jobId}`);
  
  return jobId;
}

async function getStatus(jobId) {
  const res = await fetch(`${BASE_URL}/${jobId}?limit=1`, { headers });
  const data = await res.json();
  
  if (!data.success) {
    console.error('Error:', data.errors || data);
    process.exit(1);
  }
  
  const { status, total, finished, browserSecondsUsed } = data.result;
  
  console.log(`Job: ${jobId}`);
  console.log(`Status: ${status}`);
  console.log(`Progress: ${finished || 0}/${total || '?'} pages`);
  if (browserSecondsUsed) {
    console.log(`Browser time: ${(browserSecondsUsed / 60).toFixed(1)} minutes`);
  }
  
  return data.result;
}

async function getResults(jobId, options = {}) {
  let url = `${BASE_URL}/${jobId}`;
  const params = [];
  if (options.limit) params.push(`limit=${options.limit}`);
  if (options.status) params.push(`status=${options.status}`);
  if (options.cursor) params.push(`cursor=${options.cursor}`);
  if (params.length) url += '?' + params.join('&');
  
  const res = await fetch(url, { headers });
  const data = await res.json();
  
  if (!data.success) {
    console.error('Error:', data.errors || data);
    process.exit(1);
  }
  
  const result = data.result;
  
  console.log(`Job: ${jobId}`);
  console.log(`Status: ${result.status}`);
  console.log(`Total pages: ${result.total}`);
  console.log(`Browser time: ${(result.browserSecondsUsed / 60).toFixed(1)} minutes`);
  console.log(`\n--- Results (${result.records?.length || 0} records) ---\n`);
  
  if (result.records) {
    for (const record of result.records) {
      console.log(`[${record.status}] ${record.url}`);
      if (options.verbose && record.markdown) {
        console.log(record.markdown.substring(0, 500) + '...\n');
      }
      if (options.verbose && record.json) {
        console.log(JSON.stringify(record.json, null, 2).substring(0, 500) + '...\n');
      }
    }
  }
  
  if (result.cursor) {
    console.log(`\nMore results available. Use --cursor ${result.cursor}`);
  }
  
  // Output JSON if requested
  if (options.json) {
    console.log('\n--- JSON Output ---');
    console.log(JSON.stringify(result, null, 2));
  }
  
  return result;
}

async function cancelCrawl(jobId) {
  const res = await fetch(`${BASE_URL}/${jobId}`, {
    method: 'DELETE',
    headers
  });
  
  if (res.ok) {
    console.log(`Cancelled job: ${jobId}`);
  } else {
    const data = await res.json();
    console.error('Error:', data.errors || data);
  }
}

async function waitForCrawl(jobId, maxWaitMs = 300000) {
  const startTime = Date.now();
  const pollInterval = 5000;
  
  console.log(`Waiting for job ${jobId} to complete...`);
  
  while (Date.now() - startTime < maxWaitMs) {
    const result = await getStatus(jobId);
    
    if (result.status !== 'running') {
      return result;
    }
    
    await new Promise(r => setTimeout(r, pollInterval));
  }
  
  throw new Error('Timeout waiting for crawl to complete');
}

// Main
async function main() {
  const opts = parseOptions(args.slice(1));
  
  switch (command) {
    case 'start':
      const url = args[1];
      if (!url) {
        console.error('Usage: node crawl.js start <url> [--limit N] [--depth N] [--format markdown|html|json]');
        process.exit(1);
      }
      await startCrawl(url, opts);
      break;
      
    case 'status':
      const statusId = args[1];
      if (!statusId) {
        console.error('Usage: node crawl.js status <job_id>');
        process.exit(1);
      }
      await getStatus(statusId);
      break;
      
    case 'results':
      const resultsId = args[1];
      if (!resultsId) {
        console.error('Usage: node crawl.js results <job_id> [--limit N] [--verbose] [--json]');
        process.exit(1);
      }
      await getResults(resultsId, opts);
      break;
      
    case 'cancel':
      const cancelId = args[1];
      if (!cancelId) {
        console.error('Usage: node crawl.js cancel <job_id>');
        process.exit(1);
      }
      await cancelCrawl(cancelId);
      break;
      
    case 'wait':
      const waitId = args[1];
      if (!waitId) {
        console.error('Usage: node crawl.js wait <job_id>');
        process.exit(1);
      }
      await waitForCrawl(waitId);
      break;
      
    default:
      console.log(`Cloudflare Crawl CLI

Commands:
  start <url>     Start a crawl job
    --limit N     Max pages to crawl (default: 10)
    --depth N     Max link depth (default: 100)
    --format      Output format: markdown, html, json
    --source      URL source: all, sitemaps, links
    --prompt      AI extraction prompt (enables JSON format)
    
  status <id>     Check job status
  results <id>    Get crawl results
    --limit N     Max records to return
    --verbose     Show content preview
    --json        Output raw JSON
    
  cancel <id>     Cancel a running job
  wait <id>       Wait for job to complete

Environment:
  CLOUDFLARE_API_TOKEN    API token
  CLOUDFLARE_ACCOUNT_ID   Account ID
`);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
