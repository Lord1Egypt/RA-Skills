#!/usr/bin/env node
/**
 * Cold Email Campaign Sender
 * 
 * Usage:
 *   node send-campaign.js --list leads.csv --template templates/intro.txt --from "hello@domain.com"
 *   node send-campaign.js --list leads.csv --template templates/intro.txt --dry-run
 *
 * CSV format: email,first_name,business_name,city,industry,specific_issue
 * Template format: First line = Subject, rest = body. Uses {variable} placeholders.
 */

const fs = require('fs');
const https = require('https');
const path = require('path');

const RESEND_KEY = process.env.RESEND_API_KEY;
const RATE_LIMIT = 25; // emails per run
const DELAY_MS = 2000; // 2 seconds between emails

function parseArgs() {
  const args = { dryRun: process.argv.includes('--dry-run') };
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--list') args.list = process.argv[++i];
    if (process.argv[i] === '--template') args.template = process.argv[++i];
    if (process.argv[i] === '--from') args.from = process.argv[++i];
    if (process.argv[i] === '--limit') args.limit = parseInt(process.argv[++i]);
  }
  return args;
}

function parseCSV(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim());
    const obj = {};
    headers.forEach((h, i) => obj[h] = values[i] || '');
    return obj;
  });
}

function parseTemplate(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  const subject = lines[0].replace(/^Subject:\s*/i, '').trim();
  const body = lines.slice(1).join('\n').trim();
  return { subject, body };
}

function fillTemplate(template, vars) {
  let text = template;
  for (const [key, value] of Object.entries(vars)) {
    text = text.replace(new RegExp(`\\{${key}\\}`, 'g'), value || '');
  }
  return text;
}

function sendEmail(from, to, subject, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ from, to: [to], subject, text: body });
    const req = https.request({
      hostname: 'api.resend.com', path: '/emails', method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + RESEND_KEY,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(d);
          resolve({ ok: !!parsed.id, id: parsed.id, error: parsed.message });
        } catch(e) { resolve({ ok: false, error: d }); }
      });
    });
    req.on('error', reject);
    req.write(data); req.end();
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Track sent emails for suppression
function loadSent(campaignId) {
  const file = `campaign-${campaignId}-sent.json`;
  if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8'));
  return [];
}

function saveSent(campaignId, sent) {
  fs.writeFileSync(`campaign-${campaignId}-sent.json`, JSON.stringify(sent, null, 2));
}

async function main() {
  const args = parseArgs();
  if (!args.list || !args.template) {
    console.log('Usage: node send-campaign.js --list leads.csv --template template.txt --from "Name <email>" [--dry-run] [--limit 25]');
    process.exit(1);
  }
  if (!RESEND_KEY && !args.dryRun) { console.error('Missing RESEND_API_KEY'); process.exit(1); }

  const leads = parseCSV(args.list);
  const { subject: subjectTpl, body: bodyTpl } = parseTemplate(args.template);
  const from = args.from || 'hello@yourdomain.com';
  const limit = Math.min(args.limit || RATE_LIMIT, RATE_LIMIT);
  const campaignId = new Date().toISOString().split('T')[0];
  const alreadySent = loadSent(campaignId);
  const sentEmails = new Set(alreadySent.map(s => s.email));

  console.log(`📧 Campaign: ${leads.length} leads, limit ${limit}/run, from: ${from}`);
  if (args.dryRun) console.log('🏃 DRY RUN — no emails will be sent\n');

  let sent = 0, skipped = 0, failed = 0;
  const results = [...alreadySent];

  for (const lead of leads) {
    if (sent >= limit) break;
    if (!lead.email || sentEmails.has(lead.email)) { skipped++; continue; }

    const vars = { ...lead, sender_name: from.split('<')[0].trim() };
    const subject = fillTemplate(subjectTpl, vars);
    const body = fillTemplate(bodyTpl, vars);

    if (args.dryRun) {
      console.log(`[DRY] To: ${lead.email} | Subject: ${subject}`);
      sent++;
      continue;
    }

    const result = await sendEmail(from, lead.email, subject, body);
    if (result.ok) {
      console.log(`✅ Sent to ${lead.email} (${result.id})`);
      results.push({ email: lead.email, subject, sentAt: new Date().toISOString(), id: result.id });
      sent++;
    } else {
      console.log(`❌ Failed: ${lead.email} — ${result.error}`);
      failed++;
    }

    await sleep(DELAY_MS);
  }

  if (!args.dryRun) saveSent(campaignId, results);
  console.log(`\n📊 Results: ${sent} sent, ${skipped} skipped, ${failed} failed`);
}

main().catch(e => { console.error('Campaign error:', e.message); process.exit(1); });
