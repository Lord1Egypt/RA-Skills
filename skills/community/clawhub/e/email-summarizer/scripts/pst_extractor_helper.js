#!/usr/bin/env node
/**
 * pst_extractor_helper.js
 *
 * Native PST parser using the `pst-extractor` npm package.
 * Called by parse_local.py when readpst is unavailable.
 *
 * Usage:
 *   node pst_extractor_helper.js <pst_file> [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--max N]
 *
 * Output: JSON array of email records (stdout), log messages on stderr.
 *
 * Prerequisites (install once before first use):
 *   cd email-summarizer/scripts && npm install
 *
 * The script resolves pst-extractor using Node's standard require() resolution:
 *   - node_modules/ sibling to this script  (preferred, after `npm install`)
 *   - Any parent node_modules/ up the directory tree (standard Node.js behaviour)
 *
 * NOTE: This script does NOT execute any shell commands or spawn child processes.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Module resolution (pure Node.js, no shell execution) ─────────────────────

// Prepend the script's own directory to the module search path so that
// `npm install` run inside scripts/ is found automatically, without any
// shell calls or child_process usage.
const scriptDir = __dirname;
const localModules = path.join(scriptDir, 'node_modules');

if (fs.existsSync(localModules)) {
  // Insert at front so local node_modules takes priority over any global install
  require('module').globalPaths.unshift(localModules);
}

let PSTFile, PSTFolder, PSTMessage;

try {
  ({ PSTFile, PSTFolder, PSTMessage } = require('pst-extractor'));
} catch (e) {
  process.stderr.write(
    '[pst-helper] ERROR: pst-extractor not found.\n' +
    'Please install it first by running:\n' +
    '  cd email-summarizer/scripts && npm install\n'
  );
  process.exit(1);
}

// ── Argument parsing ──────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help') {
  process.stderr.write('Usage: node pst_extractor_helper.js <file.pst> [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--max N]\n');
  process.exit(0);
}

const pstPath = args[0];
let sinceMs = null;
let untilMs = null;
let maxCount = 2000;

for (let i = 1; i < args.length; i++) {
  if (args[i] === '--since' && args[i + 1]) { sinceMs = new Date(args[++i]).getTime(); }
  else if (args[i] === '--until' && args[i + 1]) { untilMs = new Date(args[++i]).getTime(); }
  else if (args[i] === '--max'   && args[i + 1]) { maxCount = parseInt(args[++i], 10); }
}

if (!fs.existsSync(pstPath)) {
  process.stderr.write(`[pst-helper] File not found: ${pstPath}\n`);
  process.exit(1);
}

// ── Recipient SMTP address extraction ────────────────────────────────────────

function _getRecipientAddrs(item) {
  const addrs = [];
  try {
    const n = item.numberOfRecipients || 0;
    for (let i = 0; i < n; i++) {
      const r = item.getRecipient(i);
      const addr = (r.smtpAddress || r.emailAddress || '').trim();
      // Skip Exchange internal DN addresses (start with /o= or /O=)
      if (addr && !addr.startsWith('/') && addr.includes('@')) {
        addrs.push(addr.toLowerCase());
      }
    }
  } catch (_) {}
  return addrs;
}

// ── HTML → plain text (lightweight) ──────────────────────────────────────────

function htmlToText(html) {
  if (!html) return '';
  return html
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s{3,}/g, '  ')
    .trim();
}

// ── Date helpers ──────────────────────────────────────────────────────────────

function toIso(dateObj) {
  if (!dateObj) return '';
  try { return new Date(dateObj).toISOString(); } catch (_) { return String(dateObj); }
}

function inRange(dateObj) {
  if (!dateObj) return true;
  const ms = new Date(dateObj).getTime();
  if (isNaN(ms)) return true;
  if (sinceMs !== null && ms < sinceMs) return false;
  if (untilMs !== null && ms >= untilMs) return false;
  return true;
}

// ── Folder name → direction heuristic ────────────────────────────────────────

const SENT_HINTS = ['sent', '已发送', '发件箱', 'outbox', 'outgoing'];

function isSentFolder(name) {
  if (!name) return false;
  const lower = name.toLowerCase();
  return SENT_HINTS.some(h => lower.includes(h));
}

// ── PST traversal ─────────────────────────────────────────────────────────────

const results = [];
let totalSkipped = 0;
let idCounter = 0;

function processFolder(folder, folderPath) {
  const name = folder.displayName || '';
  const currentPath = folderPath ? `${folderPath}/${name}` : name;
  const direction = isSentFolder(name) ? 'sent' : 'received';

  // Process emails in this folder
  if (folder.emailCount > 0 && results.length < maxCount) {
    let item;
    try { item = folder.getNextChild(); } catch (_) { item = null; }

    while (item !== null && results.length < maxCount) {
      if (item instanceof PSTMessage) {
        const dateObj = item.messageDeliveryTime || item.creationTime;
        if (!inRange(dateObj)) {
          totalSkipped++;
        } else {
          // Body: prefer plain text, fall back to HTML→text
          let body = (item.body || '').trim();
          if (!body && item.bodyHTML) {
            body = htmlToText(item.bodyHTML);
          }
          body = body.slice(0, 2000);

          // Attachments
          const attachmentNames = [];
          for (let ai = 0; ai < item.numberOfAttachments; ai++) {
            try {
              const att = item.getAttachment(ai);
              if (att && att.displayName) attachmentNames.push(att.displayName);
            } catch (_) {}
          }

          results.push({
            id:          String(++idCounter),
            direction,
            folder:      currentPath,
            date:        toIso(dateObj),
            from:        item.senderName
                           ? `${item.senderName} <${item.senderEmailAddress || ''}>`
                           : (item.senderEmailAddress || ''),
            to:          item.displayTo  || '',
            to_addrs:    _getRecipientAddrs(item),   // real SMTP addresses for owner inference
            cc:          item.displayCC  || '',
            subject:     item.subject    || '(no subject)',
            body,
            attachments: attachmentNames,
          });
        }
      }

      try { item = folder.getNextChild(); } catch (_) { break; }
    }
  }

  // Recurse into subfolders
  let subfolders;
  try { subfolders = folder.getSubFolders(); } catch (_) { return; }
  for (const sub of subfolders) {
    if (results.length >= maxCount) break;
    processFolder(sub, currentPath);
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

try {
  process.stderr.write(`[pst-helper] Opening ${pstPath} ...\n`);
  const pstFile = new PSTFile(pstPath);
  const root = pstFile.getRootFolder();
  processFolder(root, '');
  process.stderr.write(`[pst-helper] Done. ${results.length} emails loaded, ${totalSkipped} skipped by date filter.\n`);
  process.stdout.write(JSON.stringify(results, null, 2));
} catch (e) {
  process.stderr.write(`[pst-helper] Error: ${e.message}\n${e.stack}\n`);
  process.exit(1);
}
