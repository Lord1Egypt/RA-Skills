#!/usr/bin/env node
/**
 * Upload a pearl (knowledge file) to your virtual buddy on ClawBuddy.
 * 
 * Usage:
 *   node upload-pearl.js --file pearl.md
 *   node upload-pearl.js --file browser-games.md --title "Browser Games"
 *   node upload-pearl.js --content "# Knowledge" --title "Topic"
 * 
 * Requires CLAWBUDDY_TOKEN environment variable (your buddy_xxx token).
 */

import fs from 'fs';
import path from 'path';
import { loadEnv } from './lib/env.js';

// Load .env before reading any env vars
loadEnv();

const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

const RELAY_URL = process.env.CLAWBUDDY_URL || 'https://clawbuddy.help';
const TOKEN = process.env.CLAWBUDDY_TOKEN;

const filePath = getArg('file');
const title = getArg('title');
const inlineContent = getArg('content');

function showUsage() {
  console.error('Upload Pearl to Your Virtual Buddy');
  console.error('===================================');
  console.error('');
  console.error('Usage:');
  console.error('  node upload-pearl.js --file pearl.md [--title "Title"]');
  console.error('  node upload-pearl.js --content "..." --title "Title"');
  console.error('');
  console.error('Options:');
  console.error('  --file     Path to pearl file (markdown)');
  console.error('  --content  Inline pearl content');
  console.error('  --title    Pearl title (defaults to filename)');
  console.error('');
  console.error('Environment:');
  console.error('  CLAWBUDDY_TOKEN  Your buddy token (buddy_xxx)');
  console.error('  CLAWBUDDY_URL    API URL (default: https://clawbuddy.help)');
  console.error('');
  console.error('Pearl limits: max 10 pearls per buddy, max 20KB per pearl');
  process.exit(1);
}

if (!filePath && !inlineContent) {
  console.error('Error: --file or --content is required');
  showUsage();
}

if (!TOKEN) {
  console.error('Error: CLAWBUDDY_TOKEN environment variable not set');
  console.error('');
  console.error('Use the same buddy_xxx token from your .env');
  process.exit(1);
}

async function main() {
  // Load content
  let content = inlineContent;
  let pearlTitle = title;
  
  if (filePath) {
    if (!fs.existsSync(filePath)) {
      console.error(`Error: File not found: ${filePath}`);
      process.exit(1);
    }
    content = fs.readFileSync(filePath, 'utf-8');
    if (!pearlTitle) {
      // Use filename without extension as title
      pearlTitle = path.basename(filePath, path.extname(filePath))
        .replace(/[-_]/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase());
    }
    console.log(`Loaded pearl from ${filePath} (${content.length} bytes)`);
  }

  if (!pearlTitle) {
    console.error('Error: --title is required when using --content');
    process.exit(1);
  }

  if (content.length > 20 * 1024) {
    console.error(`Error: Pearl too large (${content.length} bytes, max 20KB)`);
    process.exit(1);
  }

  // Upload pearl using buddy token
  console.log(`Uploading pearl: "${pearlTitle}"...`);
  
  const res = await fetch(`${RELAY_URL}/api/buddy/pearls`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${TOKEN}`,
    },
    body: JSON.stringify({
      title: pearlTitle,
      content,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    console.error('Upload failed:', data.error || 'Unknown error');
    process.exit(1);
  }

  console.log('');
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║  ✅ PEARL UPLOADED SUCCESSFULLY                              ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  Title:    ${pearlTitle}`);
  console.log(`  Size:     ${content.length} bytes`);
  console.log('');
  console.log('Your virtual buddy now has this knowledge available!');
}

main().catch(err => {
  console.error('Error:', err.message || err);
  process.exit(1);
});
