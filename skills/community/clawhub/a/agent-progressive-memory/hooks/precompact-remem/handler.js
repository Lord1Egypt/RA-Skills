/**
 * precompact-remem hook handler
 * Intercepts session:compact:before and triggers a memory flush.
 * 
 * Events: session:compact:before
 * Install: local hook at hooks/precompact-remem/
 */

'use strict';

const FS = require('fs');
const PATH = require('path');

/**
 * Check if session has meaningful context to flush
 */
function hasMeaningfulContext(event) {
  // Only flush if session has actual conversation history
  const msgCount = event.context?.messageCount || 0;
  const tokenCount = event.context?.tokenCount || 0;
  // Flush if >= 10 messages or >= 1000 tokens
  return msgCount >= 10 || tokenCount >= 1000;
}

/**
 * Get list of memory group directories
 */
function getMemoryGroups(memoryDir) {
  const groupsDir = PATH.join(memoryDir, 'groups');
  if (!FS.existsSync(groupsDir)) return [];
  try {
    return FS.readdirSync(groupsDir).filter(f => {
      const stat = FS.statSync(PATH.join(groupsDir, f));
      return stat.isDirectory();
    });
  } catch (e) {
    return [];
  }
}

/**
 * Get last modified time of a file
 */
function getFileMtime(filePath) {
  try {
    if (!FS.existsSync(filePath)) return null;
    return FS.statSync(filePath).mtime;
  } catch (e) {
    return null;
  }
}

/**
 * Read a JSON file safely
 */
function readJSON(filePath) {
  try {
    if (!FS.existsSync(filePath)) return null;
    return JSON.parse(FS.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return null;
  }
}

/**
 * Write a JSON file safely
 */
function writeJSON(filePath, data) {
  FS.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Main handler
 * @param {object} event - OpenClaw hook event
 */
async function handler(event) {
  if (event.type !== 'session' || event.action !== 'compact:before') {
    return;
  }

  const workspaceDir = event.context?.workspaceDir;
  if (!workspaceDir) {
    console.log('[precompact-remem] workspace.dir not configured, skipping');
    return;
  }

  const memoryDir = PATH.join(workspaceDir, 'memory');
  const flushStatePath = PATH.join(memoryDir, 'flush-state.json');

  // Step 1: Check if session has meaningful context
  if (!hasMeaningfulContext(event)) {
    console.log('[precompact-remem] Session too small to flush, skipping');
    return;
  }

  const sessionKey = event.sessionKey || 'unknown';
  const messageCount = event.context?.messageCount || 0;
  const tokenCount = event.context?.tokenCount || 0;

  console.log(`[precompact-remem] Triggering flush before compaction. Session: ${sessionKey}, Messages: ${messageCount}, Tokens: ${tokenCount}`);

  // Step 2: Discover memory groups
  const groups = getMemoryGroups(memoryDir);
  if (groups.length === 0) {
    console.log('[precompact-remem] No memory groups found, skipping');
    return;
  }

  // Step 3: Read old flush state
  const oldState = readJSON(flushStatePath) || {};

  // Step 4: Compute deltas
  const deltas = [];
  for (const group of groups) {
    const groupDir = PATH.join(memoryDir, 'groups', group);
    const files = ['attention.md', 'experience.md', 'project.md', 'people.md'];
    
    for (const file of files) {
      const filePath = PATH.join(groupDir, file);
      const mtime = getFileMtime(filePath);
      if (!mtime) continue;
      
      const lastFlush = oldState[`${group}/${file}_mtime`];
      if (!lastFlush || new Date(mtime) > new Date(lastFlush)) {
        deltas.push({ group, file, path: filePath, mtime: mtime.toISOString() });
      }
    }
  }

  // Step 5: Update flush state
  const newState = {
    last_flush_time: new Date().toISOString(),
    trigger: 'precompact',
    session_key: sessionKey,
    message_count: messageCount,
    token_count: tokenCount,
    groups_found: groups.length,
    deltas_detected: deltas.length,
    deltas: deltas.slice(0, 10),
    // Preserve old timestamps
    ...Object.fromEntries(
      Object.entries(oldState).filter(([k]) => k.endsWith('_mtime'))
    )
  };

  for (const delta of deltas) {
    newState[`${delta.group}/${delta.file}_mtime`] = delta.mtime;
  }

  writeJSON(flushStatePath, newState);

  console.log(`[precompact-remem] Flush complete. Groups: ${groups.length}, Deltas: ${deltas.length}`);

  // Step 6: Optionally notify via messages
  // Note: We can't easily inject into the session here since we're
  // in the compaction pipeline. The flush is best-effort.
}

module.exports = { handler };
