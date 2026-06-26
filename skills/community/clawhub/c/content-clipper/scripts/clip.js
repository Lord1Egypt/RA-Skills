/**
 * content-clipper — Extract web content and clip to flomo or markdown
 * Usage: node clip.js --url <url> [--target flomo|markdown] [--output path] [--summary] [--tags tag1,tag2]
 */
const https = require('https');
const http = require('http');
const fs = require('fs');
const { execSync } = require('child_process');
const { URL } = require('url');

const FLOMO_WEBHOOK = process.env.FLOMO_WEBHOOK || 'https://flomoapp.com/iwh/MTg4MTA/c6fceb66258d3cc5c527d82f283ba06a/';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { target: 'flomo', summary: false, tags: [] };
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--url': opts.url = args[++i]; break;
      case '--target': opts.target = args[++i]; break;
      case '--output': opts.output = args[++i]; break;
      case '--summary': opts.summary = true; break;
      case '--tags': opts.tags = args[++i].split(',').map(t => t.trim()); break;
    }
  }
  return opts;
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' } }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetch(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractText(html) {
  // Remove scripts, styles, nav, footer
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '');
  
  // Extract title
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1].replace(/\s+/g, ' ').trim() : '';
  
  // Extract article or main content
  const articleMatch = text.match(/<article[\s\S]*?>([\s\S]*?)<\/article>/i)
    || text.match(/<main[\s\S]*?>([\s\S]*?)<\/main>/i)
    || text.match(/<div[^>]*class="[^"]*content[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
  
  const content = articleMatch ? articleMatch[1] : text;
  
  // Strip tags, decode entities, clean whitespace
  const cleaned = content
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/h[1-6]>/gi, '\n\n')
    .replace(/<li[^>]*>/gi, '• ')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n))
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\s+|\s+$/gm, '')
    .trim();
  
  return { title, content: cleaned };
}

function postToFlomo(content, tags) {
  const tagStr = tags.map(t => `#${t}`).join(' ');
  const body = JSON.stringify({ content: tagStr ? `${tagStr}\n\n${content}` : content });
  
  try {
    const result = execSync(
      `curl.exe --noproxy "*" -s -X POST "${FLOMO_WEBHOOK}" -H "Content-Type: application/json" -d ${JSON.stringify(body).replace(/"/g, '\\"')}`,
      { encoding: 'utf8', timeout: 15000 }
    );
    return JSON.parse(result);
  } catch (e) {
    // Fallback: use Node https
    return new Promise((resolve, reject) => {
      const url = new URL(FLOMO_WEBHOOK);
      const req = https.request({
        hostname: url.hostname,
        path: url.pathname,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }, res => {
        let data = '';
        res.on('data', c => data += c);
        res.on('end', () => { try { resolve(JSON.parse(data)); } catch { resolve(data); } });
      });
      req.on('error', reject);
      req.write(body);
      req.end();
    });
  }
}

function saveMarkdown(title, content, url, tags, outputPath) {
  const tagStr = tags.map(t => `#${t}`).join(' ');
  const md = `# ${title}\n\n> Source: ${url}\n> Clipped: ${new Date().toISOString()}\n${tagStr ? `> Tags: ${tagStr}\n` : ''}\n---\n\n${content}\n`;
  fs.writeFileSync(outputPath, md, 'utf8');
  return outputPath;
}

async function main() {
  const opts = parseArgs();
  if (!opts.url) {
    console.error('Usage: node clip.js --url <url> [--target flomo|markdown] [--output path] [--tags t1,t2]');
    process.exit(1);
  }
  
  console.error(`Fetching: ${opts.url}`);
  const html = await fetch(opts.url);
  const { title, content } = extractText(html);
  
  if (!content || content.length < 50) {
    console.error('Warning: extracted content is very short, page may require JavaScript rendering');
  }
  
  const clipContent = `**${title}**\n\n${content.slice(0, 3000)}${content.length > 3000 ? '\n\n...(truncated)' : ''}\n\nSource: ${opts.url}`;
  
  if (opts.target === 'flomo') {
    console.error('Posting to flomo...');
    const result = await postToFlomo(clipContent, opts.tags);
    console.log(JSON.stringify({ ok: true, target: 'flomo', title, contentLength: content.length, result }));
  } else if (opts.target === 'markdown') {
    const outPath = opts.output || `clip_${Date.now()}.md`;
    saveMarkdown(title, content, opts.url, opts.tags, outPath);
    console.log(JSON.stringify({ ok: true, target: 'markdown', title, contentLength: content.length, path: outPath }));
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
