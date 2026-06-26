#!/usr/bin/env node
/**
 * Draft Router - Telegram Inline Button Handler
 * Receives forwarded messages and presents routing options
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const MEMORY_DIR = '/home/node/.openclaw/workspace/memory';
const ARCHIVE_DIR = '/home/node/.openclaw/workspace/memory/drafts-archive';

// Ensure archive directory exists
if (!fs.existsSync(ARCHIVE_DIR)) {
  fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
}

/**
 * Detect if message is a draft based on header pattern
 * Pattern: DRAFTS | YYYY-MM-DD HH:MM ---
 */
function isDraftMessage(content) {
  const draftPattern = /^DRAFTS\s*\|\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}/m;
  return draftPattern.test(content);
}

/**
 * Extract clean content from draft (remove header)
 */
function extractDraftContent(content) {
  // Remove the DRAFTS | date header and separator line
  return content.replace(/^DRAFTS\s*\|\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s*\n---\s*\n/m, '').trim();
}

/**
 * Main handler - called when a draft message is received
 * Returns button configuration for OpenClaw message tool
 */
function handleDraft(content, source) {
  // Generate unique ID for this draft
  const draftId = `draft-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  
  // Clean the content (remove header for storage)
  const cleanContent = extractDraftContent(content);
  
  // Store draft temporarily for callback handling
  const draftPath = path.join(ARCHIVE_DIR, `${draftId}.json`);
  fs.writeFileSync(draftPath, JSON.stringify({
    id: draftId,
    content: cleanContent,
    originalContent: content,
    source: source,
    receivedAt: new Date().toISOString()
  }, null, 2));

  // Return button configuration
  return {
    text: `📄 Draft received\n\nPreview: ${cleanContent.substring(0, 100)}${cleanContent.length > 100 ? '...' : ''}\n\nWhat would you like to do?`,
    buttons: [
      [
        { text: '🧠 Knowledge', callback_data: `draft:${draftId}:knowledge` },
        { text: '📦 Archive', callback_data: `draft:${draftId}:archive` },
        { text: '✅ Tasks', callback_data: `draft:${draftId}:tasks` }
      ],
      [
        { text: '▶️ Run as Prompt', callback_data: `draft:${draftId}:prompt` }
      ]
    ]
  };
}

/**
 * Handle button callback
 */
function handleCallback(draftId, action) {
  const draftPath = path.join(ARCHIVE_DIR, `${draftId}.json`);
  
  if (!fs.existsSync(draftPath)) {
    return { error: 'Draft not found or already processed' };
  }

  const draft = JSON.parse(fs.readFileSync(draftPath, 'utf8'));

  switch (action) {
    case 'knowledge':
      return addToKnowledge(draft);
    case 'archive':
      return archiveDraft(draft);
    case 'tasks':
      return addToTasks(draft);
    case 'prompt':
      return runAsPrompt(draft);
    default:
      return { error: `Unknown action: ${action}` };
  }
}

/**
 * Add draft content to MEMORY.md
 */
function addToKnowledge(draft) {
  const memoryPath = '/home/node/.openclaw/workspace/MEMORY.md';
  const entry = `

## Draft Entry - ${new Date().toISOString().split('T')[0]}

**Source:** ${draft.source || 'Unknown'}  
**Added:** ${new Date().toLocaleString('en-NZ', { timeZone: 'Pacific/Auckland' })}

${draft.content}

---
`;

  fs.appendFileSync(memoryPath, entry);
  
  // Move draft to processed
  const processedPath = path.join(ARCHIVE_DIR, 'processed', `${draft.id}-knowledge.md`);
  if (!fs.existsSync(path.dirname(processedPath))) {
    fs.mkdirSync(path.dirname(processedPath), { recursive: true });
  }
  fs.renameSync(
    path.join(ARCHIVE_DIR, `${draft.id}.json`),
    path.join(ARCHIVE_DIR, 'processed', `${draft.id}-knowledge.json`)
  );
  fs.writeFileSync(processedPath, draft.content);

  return { 
    success: true, 
    message: '✅ Added to MEMORY.md',
    action: 'knowledge'
  };
}

/**
 * Archive draft to storage
 */
function archiveDraft(draft) {
  const archivePath = path.join(ARCHIVE_DIR, 'archived', `${draft.id}.md`);
  if (!fs.existsSync(path.dirname(archivePath))) {
    fs.mkdirSync(path.dirname(archivePath), { recursive: true });
  }

  const content = `# Archived Draft - ${new Date().toISOString().split('T')[0]}

**Source:** ${draft.source || 'Unknown'}  
**Received:** ${draft.receivedAt}

---

${draft.content}
`;

  fs.writeFileSync(archivePath, content);
  
  // Remove temp file
  fs.unlinkSync(path.join(ARCHIVE_DIR, `${draft.id}.json`));

  return { 
    success: true, 
    message: '✅ Archived to memory/drafts-archive/archived/',
    action: 'archive'
  };
}

/**
 * Add draft as a task to SESSION-STATE.md
 */
function addToTasks(draft) {
  const sessionStatePath = '/home/node/.openclaw/workspace/SESSION-STATE.md';
  
  // Read current SESSION-STATE.md
  let content = '';
  if (fs.existsSync(sessionStatePath)) {
    content = fs.readFileSync(sessionStatePath, 'utf8');
  }
  
  // Create task entry
  const today = new Date().toISOString().split('T')[0];
  const taskEntry = `- [ ] **Draft Task ${today}:** ${draft.content.substring(0, 80)}${draft.content.length > 80 ? '...' : ''}`;
  
  // Find the Active Tasks section and add the task
  if (content.includes('### Active Tasks')) {
    // Insert after "### Active Tasks"
    const sectionIndex = content.indexOf('### Active Tasks');
    const insertIndex = content.indexOf('\n', sectionIndex) + 1;
    content = content.slice(0, insertIndex) + `${taskEntry}\n` + content.slice(insertIndex);
  } else {
    // Add Active Tasks section if not exists
    content += `\n\n### Active Tasks\n${taskEntry}\n`;
  }
  
  // Update last updated date
  const dateMatch = content.match(/\*\*Last Updated:\*\* \d{4}-\d{2}-\d{2}/);
  if (dateMatch) {
    content = content.replace(dateMatch[0], `**Last Updated:** ${today}`);
  }
  
  fs.writeFileSync(sessionStatePath, content);
  
  // Move draft to processed
  const processedPath = path.join(ARCHIVE_DIR, 'processed', `${draft.id}-tasks.md`);
  if (!fs.existsSync(path.dirname(processedPath))) {
    fs.mkdirSync(path.dirname(processedPath), { recursive: true });
  }
  fs.renameSync(
    path.join(ARCHIVE_DIR, `${draft.id}.json`),
    path.join(ARCHIVE_DIR, 'processed', `${draft.id}-tasks.json`)
  );
  fs.writeFileSync(processedPath, draft.content);

  return { 
    success: true, 
    message: '✅ Added to SESSION-STATE.md as a task',
    action: 'tasks'
  };
}

/**
 * Prepare draft to run as prompt
 */
function runAsPrompt(draft) {
  // Keep the draft file but mark it as prompt mode
  const promptPath = path.join(ARCHIVE_DIR, 'prompts', `${draft.id}.md`);
  if (!fs.existsSync(path.dirname(promptPath))) {
    fs.mkdirSync(path.dirname(promptPath), { recursive: true });
  }

  fs.writeFileSync(promptPath, draft.content);
  
  // Update draft status
  const draftPath = path.join(ARCHIVE_DIR, `${draft.id}.json`);
  const updated = JSON.parse(fs.readFileSync(draftPath, 'utf8'));
  updated.status = 'prompt-ready';
  fs.writeFileSync(draftPath, JSON.stringify(updated, null, 2));

  return { 
    success: true, 
    message: '📝 Ready to run as prompt. I\'ll now ask qualifying questions one at a time.',
    action: 'prompt',
    content: draft.content
  };
}

// CLI interface for OpenClaw integration
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'handle' && args[1]) {
    const content = args.slice(1).join(' ');
    const result = handleDraft(content, 'telegram-forward');
    console.log(JSON.stringify(result));
  } else if (command === 'callback' && args[1] && args[2]) {
    const result = handleCallback(args[1], args[2]);
    console.log(JSON.stringify(result));
  } else {
    console.log('Usage:');
    console.log('  node draft-router.js handle "<content>"');
    console.log('  node draft-router.js callback <draft-id> <action>');
  }
}

module.exports = { handleDraft, handleCallback, isDraftMessage, extractDraftContent };
