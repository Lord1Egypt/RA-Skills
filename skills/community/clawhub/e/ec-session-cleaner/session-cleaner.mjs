#!/usr/bin/env node
/**
 * Session Cleaner - Converts session JSONL to readable markdown
 * 
 * Usage:
 *   node session-cleaner.mjs <session-file.jsonl>
 *   node session-cleaner.mjs --all              # Process all sessions
 *   node session-cleaner.mjs --yesterday        # Process yesterday's sessions
 *   node session-cleaner.mjs --date 2026-01-30  # Process specific date
 * 
 * Output: memory/sessions/<session-id>_clean.md
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSIONS_DIR = process.env.SESSIONS_DIR || path.join(process.env.HOME, '.openclaw/agents/main/sessions');
const OUTPUT_DIR = process.env.OUTPUT_DIR || path.join(__dirname, '../memory/sessions');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

function parseSessionFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.trim().split('\n').filter(l => l.trim());
  const entries = [];
  
  for (const line of lines) {
    try {
      entries.push(JSON.parse(line));
    } catch (e) {
      // Skip malformed lines
    }
  }
  return entries;
}

function extractNarrative(entries) {
  const narrative = [];
  let sessionMeta = {
    id: null,
    startTime: null,
    endTime: null,
    channel: null,
    model: null,
  };

  for (const entry of entries) {
    // Extract metadata
    if (entry.timestamp && !sessionMeta.startTime) {
      sessionMeta.startTime = entry.timestamp;
    }
    if (entry.timestamp) {
      sessionMeta.endTime = entry.timestamp;
    }
    if (entry.id && !sessionMeta.id) {
      sessionMeta.id = entry.id;
    }

    // Process messages
    if (entry.type === 'message' && entry.message) {
      const msg = entry.message;
      const timestamp = entry.timestamp ? new Date(entry.timestamp).toISOString().slice(11, 16) : '';
      
      if (msg.role === 'user') {
        // User messages - extract text content
        let text = '';
        if (typeof msg.content === 'string') {
          text = msg.content;
        } else if (Array.isArray(msg.content)) {
          text = msg.content
            .filter(c => c.type === 'text')
            .map(c => c.text)
            .join('\n');
        }
        
        if (text && text.trim() && !text.includes('HEARTBEAT')) {
          // Clean up Telegram/channel prefixes
          const cleanText = text.replace(/^\[Telegram.*?\]\s*/s, '').trim();
          if (cleanText) {
            narrative.push({
              type: 'user',
              time: timestamp,
              content: cleanText.slice(0, 500) + (cleanText.length > 500 ? '...' : '')
            });
          }
        }
      } else if (msg.role === 'assistant') {
        // Assistant messages - extract text only (no tool calls)
        let text = '';
        if (typeof msg.content === 'string') {
          text = msg.content;
        } else if (Array.isArray(msg.content)) {
          text = msg.content
            .filter(c => c.type === 'text')
            .map(c => c.text)
            .join('\n');
        }
        
        // Skip empty or tool-only responses
        if (text && text.trim() && text !== 'NO_REPLY' && text !== 'HEARTBEAT_OK') {
          // Extract model if available
          if (msg.model) sessionMeta.model = msg.model;
          
          narrative.push({
            type: 'assistant',
            time: timestamp,
            content: text.slice(0, 1000) + (text.length > 1000 ? '...' : ''),
            model: msg.model
          });
        }
      }
    }

    // Track tool usage (summary only)
    if (entry.type === 'message' && entry.message?.content) {
      const content = entry.message.content;
      if (Array.isArray(content)) {
        for (const item of content) {
          if (item.type === 'toolCall') {
            narrative.push({
              type: 'tool',
              time: entry.timestamp ? new Date(entry.timestamp).toISOString().slice(11, 16) : '',
              name: item.name,
              summary: `Used ${item.name}`
            });
          }
        }
      }
    }
  }

  return { narrative, meta: sessionMeta };
}

function formatMarkdown(narrative, meta, originalFile) {
  const date = meta.startTime ? new Date(meta.startTime).toISOString().slice(0, 10) : 'unknown';
  const startTime = meta.startTime ? new Date(meta.startTime).toISOString().slice(11, 16) : '';
  const endTime = meta.endTime ? new Date(meta.endTime).toISOString().slice(11, 16) : '';
  
  // Group tools together
  const toolsUsed = [...new Set(narrative.filter(n => n.type === 'tool').map(n => n.name))];
  
  // Filter to just user/assistant exchanges
  const exchanges = narrative.filter(n => n.type === 'user' || n.type === 'assistant');
  
  // Generate summary (first user message + key topics)
  const firstUserMsg = exchanges.find(e => e.type === 'user')?.content || 'No user messages';
  
  let md = `# Session ${path.basename(originalFile, '.jsonl').slice(0, 8)}

**Date:** ${date}  
**Time:** ${startTime} - ${endTime} UTC  
**Model:** ${meta.model || 'unknown'}  
**Tools used:** ${toolsUsed.length > 0 ? toolsUsed.join(', ') : 'none'}

---

## Summary
${firstUserMsg.slice(0, 200)}${firstUserMsg.length > 200 ? '...' : ''}

---

## Conversation

`;

  for (const item of exchanges) {
    if (item.type === 'user') {
      md += `### 👤 User (${item.time})\n${item.content}\n\n`;
    } else if (item.type === 'assistant') {
      md += `### 🤖 Assistant (${item.time})\n${item.content}\n\n`;
    }
  }

  md += `---
*Generated by session-cleaner.mjs from ${path.basename(originalFile)}*
`;

  return md;
}

function processSession(filePath) {
  const filename = path.basename(filePath);
  const sessionId = filename.replace('.jsonl', '').replace('.deleted', '').slice(0, 8);
  const outputPath = path.join(OUTPUT_DIR, `${sessionId}_clean.md`);
  
  // Skip if already processed
  if (fs.existsSync(outputPath)) {
    console.log(`⏭️  Skipping ${sessionId} (already exists)`);
    return null;
  }

  try {
    const entries = parseSessionFile(filePath);
    const { narrative, meta } = extractNarrative(entries);
    
    // Skip noisy cron sessions, keep valuable ones
    const SKIP_CRONS = [
      'fireflies-sync',
      'crewlink-',
      'collect-activitywatch',
      'collect-screentime', 
      'collect-git-stats',
      'gmail-push-check',
      'Check Gmail',
      'activitywatch-collect',
      
      'sync-sessions',
      'mc-session-sync',
    ];
    
    const firstUserMsg = narrative.find(n => n.type === 'user');
    if (firstUserMsg && firstUserMsg.content.includes('[cron:')) {
      const shouldSkip = SKIP_CRONS.some(skip => firstUserMsg.content.includes(skip));
      if (shouldSkip) {
        console.log(`⏭️  Skipping ${sessionId} (noise cron)`);
        return null;
      }
      // Keep valuable crons: daily-brief, daily-review, moltbot-business-loop, 
      // strategic-review, overnight-proactive, etc.
    }
    
    // Skip empty sessions or heartbeat-only sessions
    const exchanges = narrative.filter(n => n.type === 'user' || n.type === 'assistant');
    if (exchanges.length < 2) {
      console.log(`⏭️  Skipping ${sessionId} (too few exchanges: ${exchanges.length})`);
      return null;
    }
    
    const markdown = formatMarkdown(narrative, meta, filePath);
    fs.writeFileSync(outputPath, markdown);
    console.log(`✅ Created ${outputPath}`);
    return outputPath;
  } catch (e) {
    console.error(`❌ Error processing ${filePath}: ${e.message}`);
    return null;
  }
}

function getSessionsForDate(dateStr) {
  const files = fs.readdirSync(SESSIONS_DIR);
  return files
    .filter(f => f.includes(dateStr) || f.endsWith('.jsonl'))
    .map(f => path.join(SESSIONS_DIR, f))
    .filter(f => {
      const stat = fs.statSync(f);
      const fileDate = stat.mtime.toISOString().slice(0, 10);
      return dateStr ? fileDate === dateStr : true;
    });
}

function getYesterdaysSessions() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const dateStr = yesterday.toISOString().slice(0, 10);
  
  const files = fs.readdirSync(SESSIONS_DIR);
  return files
    .filter(f => f.includes(dateStr) || f.endsWith('.jsonl'))
    .map(f => path.join(SESSIONS_DIR, f))
    .filter(f => {
      const stat = fs.statSync(f);
      const fileDate = stat.mtime.toISOString().slice(0, 10);
      return fileDate === dateStr;
    });
}

// Main
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(`
Session Cleaner - Convert session JSONL to readable markdown

Usage:
  node session-cleaner.mjs <session-file.jsonl>
  node session-cleaner.mjs --all
  node session-cleaner.mjs --yesterday
  node session-cleaner.mjs --date 2026-01-30

Output: ${OUTPUT_DIR}
`);
  process.exit(0);
}

let sessions = [];

if (args[0] === '--all') {
  sessions = fs.readdirSync(SESSIONS_DIR)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => path.join(SESSIONS_DIR, f));
} else if (args[0] === '--yesterday') {
  sessions = getYesterdaysSessions();
} else if (args[0] === '--date' && args[1]) {
  sessions = getSessionsForDate(args[1]);
} else {
  sessions = [args[0]];
}

console.log(`\n📁 Processing ${sessions.length} session(s)...\n`);

let processed = 0;
for (const session of sessions) {
  const result = processSession(session);
  if (result) processed++;
}

console.log(`\n✅ Done! Created ${processed} clean markdown files in ${OUTPUT_DIR}\n`);
