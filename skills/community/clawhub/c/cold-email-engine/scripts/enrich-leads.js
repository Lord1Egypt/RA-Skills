#!/usr/bin/env node
/**
 * Lead Enrichment — Find emails from business websites/domains
 * 
 * Usage:
 *   node enrich-leads.js --source leads.csv --output enriched.csv
 *   node enrich-leads.js --domain example.com
 */

const https = require('https');
const fs = require('fs');

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    https.get({ hostname: u.hostname, path: u.pathname + u.search, headers: { 'User-Agent': 'Mozilla/5.0', ...headers } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, data: d }));
    }).on('error', reject);
  });
}

// Extract emails from HTML
function extractEmails(html) {
  const matches = html.match(/[\w.+-]+@[\w-]+\.[\w.]+/g) || [];
  return [...new Set(matches)].filter(e =>
    !e.includes('example.com') && !e.includes('wixpress') &&
    !e.includes('sentry.io') && !e.includes('schema.org') &&
    !e.endsWith('.png') && !e.endsWith('.jpg') && !e.endsWith('.gif')
  );
}

// Try multiple pages to find email
async function findEmail(domain) {
  const pages = [
    `https://${domain}`,
    `https://${domain}/contact`,
    `https://${domain}/about`,
    `https://${domain}/contact-us`,
    `https://www.${domain}`,
    `https://www.${domain}/contact`,
  ];

  for (const url of pages) {
    try {
      const res = await httpGet(url);
      if (res.status === 200) {
        const emails = extractEmails(res.data);
        if (emails.length > 0) return emails[0];
      }
    } catch (e) { /* skip */ }
  }
  return null;
}

// Parse CSV
function parseCSV(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
  return { headers, rows: lines.slice(1).map(line => {
    const values = line.match(/(".*?"|[^,]+)/g) || [];
    const obj = {};
    headers.forEach((h, i) => { obj[h] = (values[i] || '').replace(/"/g, '').trim(); });
    return obj;
  })};
}

async function main() {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--source') args.source = process.argv[++i];
    if (process.argv[i] === '--output') args.output = process.argv[++i];
    if (process.argv[i] === '--domain') args.domain = process.argv[++i];
  }

  if (args.domain) {
    const email = await findEmail(args.domain);
    console.log(email ? `Found: ${email}` : 'No email found');
    return;
  }

  if (!args.source) {
    console.log('Usage: node enrich-leads.js --source leads.csv --output enriched.csv');
    console.log('       node enrich-leads.js --domain example.com');
    return;
  }

  const { headers, rows } = parseCSV(args.source);
  const output = args.output || args.source.replace('.csv', '-enriched.csv');
  let enriched = 0;

  console.log(`\n🔍 Enriching ${rows.length} leads...\n`);

  const outHeaders = headers.includes('email') ? headers : [...headers, 'email'];
  const lines = [outHeaders.join(',')];

  for (const row of rows) {
    if (row.email) {
      lines.push(outHeaders.map(h => row[h] || '').join(','));
      continue;
    }

    const domain = row.website || row.domain || row.url || '';
    if (!domain) {
      lines.push(outHeaders.map(h => row[h] || '').join(','));
      continue;
    }

    const cleanDomain = domain.replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*/, '');
    const email = await findEmail(cleanDomain);
    if (email) {
      row.email = email;
      enriched++;
      console.log(`✅ ${cleanDomain} → ${email}`);
    } else {
      console.log(`❌ ${cleanDomain} — no email found`);
    }
    lines.push(outHeaders.map(h => row[h] || '').join(','));

    await new Promise(r => setTimeout(r, 1000)); // rate limit
  }

  fs.writeFileSync(output, lines.join('\n'));
  console.log(`\n📊 Enriched ${enriched}/${rows.length} leads → ${output}`);
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
