#!/usr/bin/env node
/**
 * content-repackage.js
 * 
 * Read a markdown file, generate multi-platform content:
 *   - Twitter/X thread (280-char threads)
 *   - HTML landing page (standalone, clean)
 *   - Email digest (plain text)
 * 
 * Usage:
 *   node content-repackage.js <input.md> [output-dir]
 * 
 * Example:
 *   node content-repackage.js meeting-note-template.md ./output
 */

const fs = require('fs');
const path = require('path');

const { isMarkdownFile, readMarkdown, extractFrontmatter, stripMarkdown } = require('./libs/md-parser');
const { generateThread, generateEmail, generateLanding } = require('./libs/generators');

const OUTPUT_DIR = process.argv[3] || './repackage-output';

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 50) || 'untitled';
}

function getBasename(inputPath) {
  return path.basename(inputPath, path.extname(inputPath));
}

async function main() {
  const inputPath = process.argv[2];

  if (!inputPath) {
    console.error('\n❌  Usage: node content-repackage.js <input.md> [output-dir]\n');
    console.error('   Example: node content-repackage.js my-article.md ./out\n');
    process.exit(1);
  }

  if (!isMarkdownFile(inputPath)) {
    console.error(`\n❌  Not a .md file: ${inputPath}\n`);
    process.exit(1);
  }

  if (!fs.existsSync(inputPath)) {
    console.error(`\n❌  File not found: ${inputPath}\n`);
    process.exit(1);
  }

  const raw = fs.readFileSync(inputPath, 'utf-8');
  const { frontmatter, content } = extractFrontmatter(raw);
  const stripped = stripMarkdown(content);

  console.log(`\n📄  Input:  ${inputPath}`);
  console.log(`📁  Output: ${OUTPUT_DIR}/\n`);

  ensureDir(OUTPUT_DIR);
  const base = getBasename(inputPath);
  const slug = slugify(frontmatter.title || base);

  // ── Twitter Thread ──────────────────────────────────────────
  const thread = generateThread(stripped, { title: frontmatter.title });
  const threadPath = path.join(OUTPUT_DIR, `${slug}-thread.txt`);
  fs.writeFileSync(threadPath, thread, 'utf-8');
  console.log(`✅  Twitter thread → ${threadPath}`);
  console.log(`   (${thread.split('\n---\n').length - 1} tweets)\n`);

  // ── Email Digest ─────────────────────────────────────────────
  const email = generateEmail(stripped, { title: frontmatter.title });
  const emailPath = path.join(OUTPUT_DIR, `${slug}-email.txt`);
  fs.writeFileSync(emailPath, email, 'utf-8');
  console.log(`✅  Email digest  → ${emailPath}\n`);

  // ── HTML Landing Page ────────────────────────────────────────
  const landing = generateLanding(stripped, { title: frontmatter.title, date: frontmatter.date });
  const landingPath = path.join(OUTPUT_DIR, `${slug}-landing.html`);
  fs.writeFileSync(landingPath, landing, 'utf-8');
  console.log(`✅  HTML landing  → ${landingPath}\n`);

  // ── Summary ──────────────────────────────────────────────────
  console.log('─────────────────────────────────');
  console.log('✨  Done! Files generated:');
  console.log(`   ${threadPath}`);
  console.log(`   ${emailPath}`);
  console.log(`   ${landingPath}`);
  console.log('');
}

main().catch(err => {
  console.error('❌  Error:', err.message);
  process.exit(1);
});
