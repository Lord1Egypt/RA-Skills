#!/usr/bin/env node
/**
 * site.js — 3-layer site launcher (zero dependencies except cloudflared/wrangler)
 *
 * Layer 1 — Tunnel (no account needed, temporary public URL):
 *   node site.js tunnel <dir|port>
 *       → stderr: live URL printed in real-time
 *
 * Layer 2 — Pages (permanent hosting, Cloudflare account required):
 *   node site.js deploy <project-name> <dir> --token <CF_API_TOKEN> --account <CF_ACCOUNT_ID>
 *       → {url, project, subdomain}
 *
 * Layer 3 — Domain (custom domain linked to Pages):
 *   node site.js zone <domain> --token <CF_API_TOKEN>
 *       → {zone_id, name, status}
 *   node site.js dns-link <zone-id> <project-name> --token <CF_API_TOKEN>
 *       → {name, content, proxied}
 *   node site.js pages-domain <project-name> <domain> --token <CF_API_TOKEN> --account <CF_ACCOUNT_ID>
 *       → {domain, status}
 *   node site.js domain-check <domain> --token <CF_API_TOKEN> --account <CF_ACCOUNT_ID>
 *       → {available, name}
 */

import { execSync, spawn } from 'node:child_process';

const BASE = 'https://api.cloudflare.com/client/v4';

function parseFlags(args) {
  const flags = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      flags[key] = val;
    } else { flags._.push(args[i]); }
  }
  return flags;
}

const [,, cmd, ...rawArgs] = process.argv;
const flags = parseFlags(rawArgs);

const TOKEN   = flags.token   ?? process.env.CF_API_TOKEN;
const ACCOUNT = flags.account ?? process.env.CF_ACCOUNT_ID;

const log = msg => process.stderr.write(msg + '\n');
const out = data => console.log(JSON.stringify(data));

async function api(method, path, body) {
  if (!TOKEN) throw new Error('--token <CF_API_TOKEN> required');
  const res = await fetch(BASE + path, {
    method,
    headers: { 'Authorization': `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const json = await res.json();
  if (!json.success) throw new Error(JSON.stringify(json.errors));
  return json.result;
}

// ══ LAYER 1: TUNNEL ══════════════════════════════════════════════════════════
if (cmd === 'tunnel') {
  const target = flags._[0];
  if (!target) throw new Error('Usage: site.js tunnel <dir|port>');

  // Check cloudflared is installed
  try { execSync('which cloudflared', { stdio: 'ignore' }); }
  catch { log('Installing cloudflared...'); execSync('brew install cloudflared', { stdio: 'inherit' }); }

  const isPort = /^\d+$/.test(target);
  log(`🚇 Starting tunnel for ${isPort ? 'port ' + target : target}...`);
  log('⏳ URL will appear below — share it for instant access. Ctrl+C to stop.\n');

  if (isPort) {
    // Port tunnel
    const proc = spawn('cloudflared', ['tunnel', '--url', `http://localhost:${target}`], { stdio: ['ignore', 'pipe', 'pipe'] });
    proc.stderr.on('data', d => process.stderr.write(d));
    proc.stdout.on('data', d => process.stdout.write(d));
  } else {
    // Static directory — serve via npx serve then tunnel
    const serveProc = spawn('npx', ['-y', 'serve', target, '-p', '8080', '-s'], { stdio: 'ignore' });
    await new Promise(r => setTimeout(r, 1500));
    const proc = spawn('cloudflared', ['tunnel', '--url', 'http://localhost:8080'], { stdio: ['ignore', 'pipe', 'pipe'] });
    proc.stderr.on('data', d => process.stderr.write(d));
    proc.stdout.on('data', d => process.stdout.write(d));
    process.on('SIGINT', () => { serveProc.kill(); proc.kill(); process.exit(0); });
  }
}

// ══ LAYER 2: DEPLOY TO PAGES ══════════════════════════════════════════════════
else if (cmd === 'deploy') {
  const [projectName, dir] = flags._;
  if (!projectName || !dir) throw new Error('Usage: site.js deploy <project-name> <dir> --token ... --account ...');
  if (!ACCOUNT) throw new Error('--account <CF_ACCOUNT_ID> required');

  // Create project if it doesn't exist
  log(`📁 Creating Pages project "${projectName}"...`);
  try {
    await api('POST', `/accounts/${ACCOUNT}/pages/projects`, { name: projectName, production_branch: 'main' });
    log('✅ Project created');
  } catch (e) {
    if (e.message.includes('already exists') || e.message.includes('8000007')) { log('ℹ️  Project already exists, deploying...'); }
    else throw e;
  }

  // Deploy via wrangler
  log(`🚀 Deploying ${dir}...`);
  const env = { ...process.env, CLOUDFLARE_API_TOKEN: TOKEN, CLOUDFLARE_ACCOUNT_ID: ACCOUNT };
  const result = execSync(
    `wrangler pages deploy "${dir}" --project-name "${projectName}" --branch main 2>&1`,
    { env }
  ).toString();

  const urlMatch = result.match(/https:\/\/[a-z0-9]+\.${projectName}\.pages\.dev/) || result.match(/https:\/\/[^\s]+\.pages\.dev/);
  const url = urlMatch ? urlMatch[0] : `https://${projectName}.pages.dev`;
  log(result);
  out({ url, project: projectName, subdomain: `${projectName}.pages.dev` });
}

// ══ LAYER 3: DOMAIN TOOLS ══════════════════════════════════════════════════════
else if (cmd === 'zone') {
  const domain = flags._[0];
  if (!domain) throw new Error('Usage: site.js zone <domain>');
  log(`🔍 Looking up zone for ${domain}...`);
  const zones = await api('GET', `/zones?name=${encodeURIComponent(domain)}`);
  if (!zones.length) { out({ zone_id: null, error: 'Zone not found — domain may not be active yet' }); process.exit(0); }
  const z = zones[0];
  out({ zone_id: z.id, name: z.name, status: z.status });
}

else if (cmd === 'dns-link') {
  const [zoneId, projectName] = flags._;
  if (!zoneId || !projectName) throw new Error('Usage: site.js dns-link <zone-id> <project-name>');
  log(`📡 Adding CNAME: @ → ${projectName}.pages.dev...`);
  const result = await api('POST', `/zones/${zoneId}/dns_records`, {
    type: 'CNAME', name: '@', content: `${projectName}.pages.dev`, proxied: true,
  });
  out({ id: result.id, name: result.name, content: result.content, proxied: result.proxied });
}

else if (cmd === 'pages-domain') {
  const [projectName, domain] = flags._;
  if (!projectName || !domain) throw new Error('Usage: site.js pages-domain <project-name> <domain>');
  if (!ACCOUNT) throw new Error('--account <CF_ACCOUNT_ID> required');
  log(`🔗 Attaching ${domain} to ${projectName}...`);
  const result = await api('POST', `/accounts/${ACCOUNT}/pages/projects/${projectName}/domains`, { name: domain });
  out({ domain: result.name, status: result.status });
}

else if (cmd === 'domain-check') {
  const domain = flags._[0];
  if (!domain) throw new Error('Usage: site.js domain-check <domain>');
  if (!ACCOUNT) throw new Error('--account <CF_ACCOUNT_ID> required');
  log(`🔍 Checking availability of ${domain}...`);
  try {
    const result = await api('GET', `/accounts/${ACCOUNT}/registrar/domains/${domain}`);
    out({ available: result.available, name: result.name });
  } catch {
    out({ available: null, error: 'Could not check — domain may not be a supported TLD for Cloudflare Registrar' });
  }
}

else {
  process.stderr.write(`Unknown command: ${cmd}\nCommands: tunnel, deploy, zone, dns-link, pages-domain, domain-check\n`);
  process.exit(1);
}
