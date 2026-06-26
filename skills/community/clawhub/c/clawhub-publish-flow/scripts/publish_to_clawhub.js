#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const { Blob, FormData, fetch } = globalThis;

function parseArgs(argv) {
  const out = { tags: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const next = argv[i + 1];
    if (a === '--skill-path') out.skillPath = next, i++;
    else if (a === '--slug') out.slug = next, i++;
    else if (a === '--version') out.version = next, i++;
    else if (a === '--changelog') out.changelog = next, i++;
    else if (a === '--display-name') out.displayName = next, i++;
    else if (a === '--tag') out.tags.push(next), i++;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:\n  node publish_to_clawhub.js --skill-path <path> --slug <slug> --version <version> --changelog <text> [--display-name <name>] [--tag <tag>]...`);
}

function loadClawhubConfig() {
  const candidates = [
    path.join(os.homedir(), 'Library', 'Application Support', 'clawhub', 'config.json'),
    path.join(os.homedir(), '.config', 'clawhub', 'config.json'),
    path.join(os.homedir(), '.clawhub', 'config.json'),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) {
      const obj = JSON.parse(fs.readFileSync(p, 'utf8'));
      if (obj.token) return { path: p, ...obj };
    }
  }
  throw new Error('ClawHub config with token not found');
}

function listFiles(dir, base = dir) {
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) out = out.concat(listFiles(p, base));
    else out.push({ abs: p, rel: path.relative(base, p) });
  }
  return out;
}

(async () => {
  const args = parseArgs(process.argv);
  if (args.help || !args.skillPath || !args.slug || !args.version || !args.changelog) {
    usage();
    process.exit(args.help ? 0 : 1);
  }

  const skillPath = path.resolve(args.skillPath);
  if (!fs.existsSync(path.join(skillPath, 'SKILL.md'))) {
    throw new Error(`Missing SKILL.md in ${skillPath}`);
  }

  const cfg = loadClawhubConfig();
  const registry = cfg.registry || 'https://clawhub.ai';
  const files = listFiles(skillPath);

  const form = new FormData();
  form.set('payload', JSON.stringify({
    slug: args.slug,
    displayName: args.displayName || args.slug,
    version: args.version,
    changelog: args.changelog,
    tags: args.tags.length ? args.tags : ['latest'],
    acceptLicenseTerms: true,
  }));

  for (const f of files) {
    const buf = fs.readFileSync(f.abs);
    form.append('files', new Blob([buf]), f.rel);
  }

  const res = await fetch(new URL('/api/v1/skills', registry), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${cfg.token}`,
      Accept: 'application/json',
    },
    body: form,
  });

  const text = await res.text();
  console.log(`STATUS ${res.status}`);
  console.log(text);
  if (!res.ok) process.exit(1);
})();
