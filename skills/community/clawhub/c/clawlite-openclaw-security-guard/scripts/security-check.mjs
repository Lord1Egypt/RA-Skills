#!/usr/bin/env node

const [, , mode, ...rest] = process.argv;
const input = rest.join(' ').trim();

if (!mode || !input) {
  console.error('Usage: node security-check.mjs <text|command|url|path> <value>');
  process.exit(2);
}

const RULES = {
  text: [
    { level: 'BLOCK', label: 'prompt-injection', re: /(ignore (all|previous) instructions|developer mode|system override|reveal (the )?system prompt|bypass safety|jailbreak)/i },
    { level: 'BLOCK', label: 'secret', re: /(sk-[a-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]+)/i },
    { level: 'WARN', label: 'exfiltration', re: /(send (me|this|that).*(token|secret|key|cookie)|upload .*?(\.env|id_rsa|passwd)|pastebin|webhook)/i },
    { level: 'WARN', label: 'obfuscation', re: /(```json|@context|mainEntity|acceptedAnswer|\| .* \| .* \|)/i }
  ],
  command: [
    { level: 'BLOCK', label: 'destructive-shell', re: /(rm -rf|mkfs|dd if=|shutdown|reboot|:\(\)\{:\|:&\};:)/i },
    { level: 'BLOCK', label: 'shell-pipe-fetch', re: /(curl .*\| *(bash|sh)|wget .*\| *(bash|sh))/i },
    { level: 'WARN', label: 'chaining', re: /(&&|\|\||;|\$\(|`)/ },
    { level: 'WARN', label: 'network-exfil', re: /(nc |ncat |scp |rsync .*@|curl .*https?:\/\/)/i }
  ],
  url: [
    { level: 'BLOCK', label: 'localhost', re: /https?:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])/i },
    { level: 'BLOCK', label: 'metadata-ssrf', re: /(169\.254\.169\.254|metadata\.google|100\.100\.100\.200|latest\/meta-data)/i },
    { level: 'BLOCK', label: 'file-uri', re: /^file:\/\//i },
    { level: 'WARN', label: 'private-ip', re: /https?:\/\/(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)/i }
  ],
  path: [
    { level: 'BLOCK', label: 'traversal', re: /(\.\.\/|\.\.\\)/ },
    { level: 'BLOCK', label: 'sensitive-path', re: /(\/etc\/passwd|\/proc\/|id_rsa|\.env|keychain|\/var\/run\/docker\.sock|authorized_keys)/i },
    { level: 'WARN', label: 'home-secret-path', re: /(\.ssh|\.gnupg|\.aws|\.npmrc|\.pypirc)/i }
  ]
};

const rules = RULES[mode];
if (!rules) {
  console.error(`Unknown mode: ${mode}`);
  process.exit(2);
}

const findings = rules.filter(r => r.re.test(input));
const verdict = findings.some(f => f.level === 'BLOCK') ? 'BLOCK' : findings.some(f => f.level === 'WARN') ? 'WARN' : 'ALLOW';

console.log(JSON.stringify({ mode, verdict, findings: findings.map(f => ({ level: f.level, label: f.label })) }, null, 2));
process.exit(verdict === 'BLOCK' ? 1 : 0);
