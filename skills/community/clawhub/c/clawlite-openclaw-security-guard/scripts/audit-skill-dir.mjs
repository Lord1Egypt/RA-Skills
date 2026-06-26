#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const target = process.argv[2];
if (!target) {
  console.error('Usage: node audit-skill-dir.mjs <skill-dir>');
  process.exit(2);
}

const root = path.resolve(target);
if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
  console.error(`Directory not found: ${root}`);
  process.exit(2);
}

const includeExt = new Set(['.md', '.js', '.mjs', '.ts', '.tsx', '.json', '.yaml', '.yml', '.sh']);
const findings = [];

const rules = [
  { level: 'BLOCK', label: 'hardcoded-secret', re: /(sk-[a-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----|re_[A-Za-z0-9_]{10,})/i },
  { level: 'BLOCK', label: 'pipe-to-shell', re: /(curl .*\| *(bash|sh)|wget .*\| *(bash|sh))/i },
  { level: 'BLOCK', label: 'destructive-shell', re: /(rm -rf|mkfs|dd if=|chmod -R 777|chown -R root|:\(\)\{:\|:&\};:)/i },
  { level: 'WARN', label: 'exfiltration', re: /(discord\.com\/api\/webhooks|pastebin|transfer\.sh|api\.telegram\.org|nc |ncat |scp |rsync .*@)/i },
  { level: 'WARN', label: 'sensitive-path', re: /(\/etc\/passwd|id_rsa|authorized_keys|\.env|\.ssh|\.gnupg|keychain)/i },
  { level: 'WARN', label: 'postinstall-autoexec', re: /("postinstall"\s*:\s*"[^"]+")/i }
];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === '.next' || entry.name === 'dist') continue;
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p);
    else if (includeExt.has(path.extname(entry.name).toLowerCase()) || entry.name === 'SKILL.md' || entry.name === 'package.json') scanFile(p);
  }
}

function scanFile(file) {
  const text = fs.readFileSync(file, 'utf8');
  const lines = text.split(/\r?\n/);
  lines.forEach((line, i) => {
    for (const rule of rules) {
      if (rule.re.test(line)) {
        findings.push({ level: rule.level, label: rule.label, file, line: i + 1, excerpt: line.trim().slice(0, 200) });
      }
    }
  });
}

walk(root);
const verdict = findings.some(f => f.level === 'BLOCK') ? 'BLOCK' : findings.some(f => f.level === 'WARN') ? 'WARN' : 'ALLOW';
console.log(JSON.stringify({ root, verdict, findings }, null, 2));
process.exit(verdict === 'BLOCK' ? 1 : 0);
