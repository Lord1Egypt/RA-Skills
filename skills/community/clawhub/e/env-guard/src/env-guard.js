/**
 * EnvGuard — Secret & Credential Scanner
 * Scan files for leaked API keys, passwords, tokens, and secrets.
 * @author @TheShadowRose
 * @license MIT
 */

const fs = require('fs');
const path = require('path');

const DEFAULT_PATTERNS = [
  { name: 'OpenAI API Key', pattern: /sk-[a-zA-Z0-9]{20,}/, severity: 'critical' },
  { name: 'AWS Access Key', pattern: /AKIA[0-9A-Z]{16}/, severity: 'critical' },
  { name: 'GitHub Token', pattern: /ghp_[a-zA-Z0-9]{36}/, severity: 'critical' },
  { name: 'GitHub OAuth', pattern: /gho_[a-zA-Z0-9]{36}/, severity: 'critical' },
  { name: 'Anthropic API Key', pattern: /sk-ant-[a-zA-Z0-9\-_]{20,}/, severity: 'critical' },
  { name: 'Generic API Key', pattern: /api[_-]?key\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]/i, severity: 'high' },
  { name: 'Generic Secret', pattern: /secret\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]/i, severity: 'high' },
  { name: 'Generic Token', pattern: /token\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]/i, severity: 'high' },
  { name: 'Password in Config', pattern: /password\s*[:=]\s*['"][^'"]{4,}['"]/i, severity: 'high' },
  { name: 'Private Key', pattern: /-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/, severity: 'critical' },
  { name: 'Connection String', pattern: /(mongodb|postgres|mysql|redis):\/\/[^\s'"]+/i, severity: 'high' },
  { name: 'Discord Webhook', pattern: /https:\/\/discord\.com\/api\/webhooks\/\d+\/[a-zA-Z0-9_-]+/, severity: 'high' },
  { name: 'Slack Webhook', pattern: /https:\/\/hooks\.slack\.com\/services\/[A-Z0-9]+\/[A-Z0-9]+\/[a-zA-Z0-9]+/, severity: 'high' },
  { name: 'Bearer Token', pattern: /bearer\s+[a-zA-Z0-9\-_.]{20,}/i, severity: 'high' },
  { name: 'JWT Token', pattern: /eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_.]+/, severity: 'medium' },
];

const DEFAULT_IGNORE = [
  'node_modules', '.git', 'dist', 'build', '__pycache__',
  '.jpg', '.png', '.gif', '.ico', '.svg', '.woff', '.ttf',
  '.exe', '.dll', '.so', '.dylib', '.zip', '.tar', '.gz'
];

class EnvGuard {
  constructor(options = {}) {
    this.patterns = options.patterns || DEFAULT_PATTERNS;
    this.ignoreDirs = options.ignoreDirs || DEFAULT_IGNORE;
    this.allowlist = options.allowlist || [];
    this.findings = [];
  }

  scan(targetPath) {
    this.findings = [];
    this._scanDir(path.resolve(targetPath));
    return this.report();
  }

  _scanDir(dirPath) {
    let entries;
    try { entries = fs.readdirSync(dirPath, { withFileTypes: true }); }
    catch { return; }

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        if (!this.ignoreDirs.includes(entry.name)) {
          this._scanDir(fullPath);
        }
        continue;
      }

      // Skip binary/image files
      const ext = path.extname(entry.name).toLowerCase();
      if (DEFAULT_IGNORE.some(i => i.startsWith('.') && ext === i)) continue;

      this._scanFile(fullPath);
    }
  }

  _scanFile(filePath) {
    let content;
    try { content = fs.readFileSync(filePath, 'utf8'); }
    catch { return; }

    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      for (const pat of this.patterns) {
        const match = line.match(pat.pattern);
        if (match) {
          const finding = {
            file: filePath,
            line: i + 1,
            type: pat.name,
            severity: pat.severity,
            snippet: this._redact(match[0]),
            raw: line.trim().substring(0, 120)
          };
          
          // Check allowlist
          const key = `${filePath}:${i + 1}:${pat.name}`;
          if (!this.allowlist.includes(key)) {
            this.findings.push(finding);
          }
        }
      }
    }
  }

  _redact(value) {
    if (value.length <= 8) return '***';
    return value.substring(0, 4) + '...' + value.substring(value.length - 4);
  }

  report() {
    const critical = this.findings.filter(f => f.severity === 'critical');
    const high = this.findings.filter(f => f.severity === 'high');
    const medium = this.findings.filter(f => f.severity === 'medium');

    return {
      clean: this.findings.length === 0,
      total: this.findings.length,
      critical: critical.length,
      high: high.length,
      medium: medium.length,
      findings: this.findings,
      summary: this.findings.length === 0
        ? '✅ No secrets found'
        : `🔴 ${this.findings.length} potential secrets found (${critical.length} critical, ${high.length} high, ${medium.length} medium)`
    };
  }

  addPattern(name, pattern, severity = 'high') {
    this.patterns.push({ name, pattern, severity });
    return this;
  }

  addAllowlist(entry) {
    this.allowlist.push(entry);
    return this;
  }
}

// CLI mode
if (require.main === module) {
  const target = process.argv[2] || '.';
  const guard = new EnvGuard();
  const report = guard.scan(target);
  
  console.log(`\n${report.summary}\n`);
  
  for (const f of report.findings) {
    const icon = f.severity === 'critical' ? '🔴' : f.severity === 'high' ? '🟡' : '🔵';
    console.log(`${icon} ${f.file}:${f.line}`);
    console.log(`   ${f.type}: ${f.snippet}`);
  }
  
  process.exit(report.clean ? 0 : 1);
}

module.exports = { EnvGuard };
