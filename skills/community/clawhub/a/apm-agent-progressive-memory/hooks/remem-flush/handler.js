/**
 * remem-flush hook handler
 * Intercepts /remem commands and triggers a 6-step memory flush.
 * 
 * Events: message:received
 * Install: local hook at hooks/remem-flush/
 */

'use strict';

const HOOK_DIR = __dirname;
const FS = require('fs');
const PATH = require('path');

/**
 * Check if a message is a /remem command
 * @param {string} content - message content
 * @returns {boolean}
 */
function isRememCommand(content) {
  if (!content || typeof content !== 'string') return false;
  return content.trim() === '/remem' || content.trim().startsWith('/remem ');
}

/**
 * Get list of memory group directories
 * @param {string} memoryDir - path to memory directory
 * @returns {string[]} group names
 */
function getMemoryGroups(memoryDir) {
  const groupsDir = PATH.join(memoryDir, 'groups');
  if (!FS.existsSync(groupsDir)) return [];
  
  try {
    return FS.readdirSync(groupsDir)
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace(/\.md$/, ''))
      .filter(name => {
        if (name === 'flush-state' || name === 'group_names') return false;
        const dirPath = PATH.join(groupsDir, name);
        const filePath = PATH.join(groupsDir, `${name}.md`);
        if (FS.existsSync(dirPath) && FS.statSync(dirPath).isDirectory()) return true;
        return FS.existsSync(filePath);
      });
  } catch (e) {
    return [];
  }
}

/**
 * Read a JSON file safely
 * @param {string} filePath 
 * @returns {object|null}
 */
function readJSON(filePath) {
  try {
    if (!FS.existsSync(filePath)) return null;
    const content = FS.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (e) {
    return null;
  }
}

/**
 * Write a JSON file safely
 * @param {string} filePath 
 * @param {object} data 
 */
function writeJSON(filePath, data) {
  FS.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Get last modified time of a file
 * @param {string} filePath
 * @returns {Date|null}
 */
function getFileMtime(filePath) {
  try {
    if (!FS.existsSync(filePath)) return null;
    const stat = FS.statSync(filePath);
    return stat.mtime;
  } catch (e) {
    return null;
  }
}

/**
 * Main handler
 * @param {object} event - OpenClaw hook event
 * @param {object} ctx - OpenClaw hook context
 */
async function handler(event, ctx) {
  // Handle both message:received (manual /remem) and systemEvent (cron /remem)
  let content = '';
  let sessionId = event.sessionId || 'unknown';
  let contextUsage = 0;

  if (event.type === 'message' && event.action === 'received') {
    // Manual /remem from user message
    content = event.context?.content || '';
    if (!isRememCommand(content)) {
      return; // Not a /remem command, skip
    }
    contextUsage = event.context?.usagePercent || 0;
  } else if (event.type === 'system' && event.action === 'event') {
    // Cron-triggered /remem systemEvent
    content = event.context?.content || '';
    if (!isRememCommand(content)) {
      return; // Not a /remem command, skip
    }
    // For systemEvent, try to get context from event.session
    contextUsage = event.session?.context?.usagePercent || 0;
    sessionId = event.sessionId || sessionId;
  } else {
    return; // Unsupported event type
  }

  const workspaceDir = ctx.config?.workspace?.dir;
  if (!workspaceDir) {
    console.error('[remem-flush] workspace.dir not configured');
    return;
  }

  const memoryDir = PATH.join(workspaceDir, 'memory');
  const flushStatePath = PATH.join(memoryDir, 'flush-state.json');

  // Step 2: Discover memory groups
  const groups = getMemoryGroups(memoryDir);

  // Step 3: Read old memory timestamps from flush-state
  const oldState = readJSON(flushStatePath) || {};

  // Step 4: Compute deltas (compare current file mtimes with last flush)
  const deltas = [];
  for (const group of groups) {
    const groupDir = PATH.join(memoryDir, 'groups', group);
    const attentionFile = PATH.join(groupDir, 'attention.md');
    const experienceFile = PATH.join(groupDir, 'experience.md');
    const projectFile = PATH.join(groupDir, 'project.md');
    const peopleFile = PATH.join(groupDir, 'people.md');

    for (const [fileName, filePath] of [
      ['attention.md', attentionFile],
      ['experience.md', experienceFile],
      ['project.md', projectFile],
      ['people.md', peopleFile]
    ]) {
      const mtime = getFileMtime(filePath);
      if (!mtime) continue;

      const lastFlush = oldState[`${group}/${fileName}_mtime`];
      if (!lastFlush || new Date(mtime) > new Date(lastFlush)) {
        deltas.push({ group, file: fileName, path: filePath, mtime: mtime.toISOString() });
      }
    }
  }

  // Step 5: Update flush state
  const newState = {
    last_flush_time: new Date().toISOString(),
    context_usage_at_flush: contextUsage,
    session_id: sessionId,
    groups_found: groups.length,
    deltas_detected: deltas.length,
    deltas: deltas.slice(0, 10), // cap at 10 for storage
    // Preserve old timestamps for unchanged files
    ...Object.fromEntries(
      Object.entries(oldState).filter(([k]) => k.endsWith('_mtime'))
    )
  };

  // Update mtime records for all files we just checked
  for (const delta of deltas) {
    newState[`${delta.group}/${delta.file}_mtime`] = delta.mtime;
  }

  writeJSON(flushStatePath, newState);

  // Step 6: Log for debugging
  console.log(`[remem-flush] Flush complete. Groups: ${groups.length}, Deltas: ${deltas.length}, Session: ${sessionId}`);

  // Return undefined to let the AI handle the response normally
  // The hook just does the background flush work
  return;
}

module.exports = { handler };
