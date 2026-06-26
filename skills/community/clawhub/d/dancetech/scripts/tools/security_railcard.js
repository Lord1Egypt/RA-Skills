#!/usr/bin/env node
/**
 * Security Railcard - Prevents API key exposure in automated workflows
 * Scans files for common secret patterns before they are committed or deployed
 */

const fs = require('fs');
const path = require('path');

// Patterns that indicate potential secrets (API keys, tokens, private keys)
const SECRET_PATTERNS = [
  // OpenRouter keys
  /sk-or-v1-[a-zA-Z0-9]{50,}/i,
  // GitHub tokens
  /ghp_[a-zA-Z0-9]{36,}/i,
  /gho_[a-zA-Z0-9]{36,}/i,
  /ghu_[a-zA-Z0-9]{36,}/i,
  /ghs_[a-zA-Z0-9]{36,}/i,
  /ghr_[a-zA-Z0-9]{36,}/i,
  // Generic API keys
  /(?:api[_-]?key|apikey|secret|token|password|passwd|credentials)\s*[:=]\s*['"]?([a-zA-Z0-9_\-]{20,})['"]?/i,
  // Private keys (hex)
  /0x[a-fA-F0-9]{64}/,
  // Bearer tokens
  /Bearer\s+[a-zA-Z0-9_\-]{20,}/i,
  // Basic auth
  /Basic\s+[a-zA-Z0-9=]{20,}/i,
  // JWT-ish (three base64 parts separated by dots)
  /eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/i,
  // Moltbook keys
  /moltbook_[a-zA-Z0-9]{30,}/i,
  // Privy keys
  /privy_app_secret_[a-zA-Z0-9]{30,}/i
];

const EXCLUDED_PATHS = [
  /node_modules/,
  /\.git/,
  /dist/,
  /build/,
  /coverage/,
  /\.env\.example/,
  /README\.md/,
  /CHANGELOG\.md/,
  /SECURITY\.md/,
  /docs\//,
  /examples\//,
  /tests\//,
  /\.png$/,
  /\.jpg$/,
  /\.jpeg$/,
  /\.gif$/,
  /\.svg$/,
  /\.ico$/
];

function shouldExclude(filePath) {
  return EXCLUDED_PATHS.some(pattern => pattern.test(filePath));
}

function scanFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const findings = [];

    lines.forEach((line, lineNum) => {
      SECRET_PATTERNS.forEach(pattern => {
        const match = line.match(pattern);
        if (match) {
          // Skip if it's clearly a placeholder
          const matchedValue = match[0] || match[1] || '';
          const isPlaceholder = /(?:your_|example|placeholder|changeme|xxx+|replace|test_|dummy)/i.test(matchedValue);
          if (!isPlaceholder) {
            findings.push({
              line: lineNum + 1,
              content: line.trim().substring(0, 80),
              pattern: pattern.toString().substring(0, 40) + '...'
            });
          }
        }
      });
    });

    return findings;
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    throw err;
  }
}

function scanDirectory(dirPath, options = {}) {
  const findings = [];
  const files = [];

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relPath = path.relative(dirPath, fullPath);

      if (shouldExclude(relPath)) continue;

      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()) {
        files.push(fullPath);
      }
    }
  }

  walk(dirPath);

  console.log(`\n🔍 Scanning ${files.length} files for exposed secrets...\n`);

  let totalFindings = 0;
  files.forEach(file => {
    const fileFindings = scanFile(file);
    if (fileFindings && fileFindings.length > 0) {
      findings.push({ file, findings: fileFindings });
      totalFindings += fileFindings.length;
    }
  });

  return { findings, totalFindings };
}

function report(findings, totalFindings) {
  if (totalFindings === 0) {
    console.log('✅ No secrets detected. Safe to commit.\n');
    return true;
  }

  console.log(`\n🚨 SECURITY ALERT: ${totalFindings} potential secret(s) found!\n`);
  findings.forEach(({ file, findings }) => {
    const relFile = path.relative(process.cwd(), file);
    console.log(`  📁 ${relFile}`);
    findings.forEach(f => {
      console.log(`    Line ${f.line}: ${f.content}...`);
    });
  });

  console.log('\n❌ Commit blocked. Please remove secrets before committing.\n');
  console.log('Next steps:');
  console.log('  1. Move secrets to .env files (already gitignored)');
  console.log('  2. Use environment variables in your code: process.env.YOUR_KEY');
  console.log('  3. Rotate any exposed keys immediately');
  console.log('  4. If placeholders were flagged, adjust naming to use common placeholders\n');

  return false;
}

// Main execution
function main() {
  const targetDir = process.argv[2] || process.cwd();
  const { findings, totalFindings } = scanDirectory(targetDir);
  const safe = report(findings, totalFindings);
  process.exit(safe ? 0 : 1);
}

main();
