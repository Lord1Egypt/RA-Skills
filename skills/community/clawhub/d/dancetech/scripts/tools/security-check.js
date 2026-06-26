#!/usr/bin/env node
/**
 * Pre-commit hook: Security Railcard
 * Blocks commits that contain exposed API keys or secrets
 *
 * Install: ln -sf ../../tools/security-check.js .git/hooks/pre-commit
 */

const { execSync } = require('child_process');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const HOOK_PATH = path.join(WORKSPACE, 'tools', 'security_railcard.js');

try {
  // Get staged files (excluding those that would be ignored anyway)
  const stdout = execSync('git diff --cached --name-only --diff-filter=ACMR', {
    cwd: WORKSPACE,
    encoding: 'utf8'
  });
  const stagedFiles = stdout.split('\n').filter(f => f.trim());

  if (stagedFiles.length === 0) {
    process.exit(0);
  }

  console.log(`\n🛡️  Security Railcard: Checking ${stagedFiles.length} staged file(s)...\n`);

  // Scan only staged files (not whole directory) for speed
  const fs = require('fs');
  const SECRET_PATTERNS = [
    /sk-or-v1-[a-zA-Z0-9]{50,}/i,
    /ghp_[a-zA-Z0-9]{36,}/i,
    /gho_[a-zA-Z0-9]{36,}/i,
    /(?:api[_-]?key|apikey|secret|token|password|passwd|credentials)\s*[:=]\s*['"]?([a-zA-Z0-9_\-]{20,})['"]?/i,
    /0x[a-fA-F0-9]{64}/,
    /Bearer\s+[a-zA-Z0-9_\-]{20,}/i,
    /moltbook_[a-zA-Z0-9]{30,}/i,
    /privy_app_secret_[a-zA-Z0-9]{30,}/i
  ];

  const EXCLUDED = /(node_modules|\.git|dist|build|coverage|\.env\.example|README|CHANGELOG|SECURITY|docs|examples|tests|\.png|\.jpg|\.jpeg|\.gif|\.svg|\.ico)$/i;

  let found = false;

  stagedFiles.forEach(file => {
    if (EXCLUDED.test(file)) return;
    const fullPath = path.join(WORKSPACE, file);
    if (!fs.existsSync(fullPath)) return;
    const content = fs.readFileSync(fullPath, 'utf8');
    const lines = content.split('\n');

    lines.forEach((line, idx) => {
      SECRET_PATTERNS.forEach(pattern => {
        const match = line.match(pattern);
        if (match) {
          const val = match[0] || match[1] || '';
          const isPlaceholder = /(your_|example|placeholder|changeme|xxx+|replace|test_|dummy)/i.test(val);
          if (!isPlaceholder) {
            console.log(`  ❌ ${file}:${idx + 1} — Possible secret detected`);
            console.log(`     ${line.trim().substring(0, 70)}...`);
            found = true;
          }
        }
      });
    });
  });

  if (found) {
    console.log('\n🚨 Commit blocked: Secrets detected in staged files.');
    console.log('Move sensitive data to .env (already gitignored) and use placeholders.\n');
    process.exit(1);
  } else {
    console.log('✅ No secrets in staged files. Commit allowed.\n');
    process.exit(0);
  }

} catch (err) {
  console.error('Security railcard error:', err.message);
  // Fail safe: block commit if hook errors
  process.exit(1);
}
