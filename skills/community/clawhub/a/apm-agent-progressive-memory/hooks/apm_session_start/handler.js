'use strict';

/**
 * apm_session_start hook handler (chat-type aware)
 *
 * Auto-loads the right memory context per chat type:
 *   - DM (sessionKey has ':direct:')           → APM DM protocol from memory/main/*
 *   - Group chat (sessionKey has ':channel:'   → group APM from memory/groups/{name}.md
 *                     or ':group:')
 *   - Subagent / cron                         → skip (renderer filters anyway)
 *
 * Injects a synthetic bootstrap file:
 *   - APM_SESSION_START.md         (DM)
 *   - APM_GROUP_SESSION_START.md   (group chat)
 *
 * Event: agent:bootstrap
 * Install: local hook at hooks/apm_session_start/
 *
 * NOTE: OpenClaw's agent:bootstrap event context does NOT include chatType.
 * We must parse sessionKey to detect chat type.
 *
 * CHANNEL SUPPORT:
 *   - Matrix    : sessionKey = agent:<id>:matrix:{direct|channel}:<room>[:<domain>]
 *                 room id format = !opaque:domain (room-only fallback strips domain)
 *   - Telegram  : sessionKey = agent:<id>:telegram:{group|direct}:<chat_id>
 *                 chat_id is a number (negative for groups); no domain separator
 *   - Slack     : sessionKey = agent:<id>:slack:{channel|direct}:<channel_id>
 *                 channel_id is a snowflake; no domain separator
 *   - Discord   : sessionKey = agent:<id>:discord:{channel|direct}:<channel_id>
 *                 channel_id is a snowflake; no domain separator
 *
 * The chat-type detection and branching logic is channel-agnostic.
 * Group-name resolution uses memory/groups/group_names.json — operators must
 * populate it with channel-appropriate keys (see HOOK.md for format).
 */

const FS = require('fs');
const PATH = require('path');

const DM_ENTRY_NAME = 'APM_SESSION_START.md';
const GROUP_ENTRY_NAME = 'APM_GROUP_SESSION_START.md';
const APM_MAX_TOTAL_CHARS = 12000;   // Cap to stay well under bootstrap total limit
const DAILY_NOTE_MAX_CHARS = 6000;   // Per-day cap for today/yesterday daily notes
const FILE_READ_MAX_CHARS = 30000;   // Per-file read cap for non-daily files

/**
 * Read a text file safely with a char cap. Returns null on any error.
 */
function safeReadText(filePath, maxChars = FILE_READ_MAX_CHARS) {
  try {
    if (!FS.existsSync(filePath)) return null;
    const stat = FS.statSync(filePath);
    if (!stat.isFile()) return null;
    const content = FS.readFileSync(filePath, 'utf8');
    if (content.length > maxChars) {
      return (
        content.slice(0, maxChars) +
        `\n\n[... truncated at ${maxChars} chars; original ${content.length} chars at ${filePath}]`
      );
    }
    return content;
  } catch (e) {
    return null;
  }
}

/**
 * Read a JSON file safely. Returns null on any error.
 */
function safeReadJSON(filePath) {
  try {
    if (!FS.existsSync(filePath)) return null;
    return JSON.parse(FS.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return null;
  }
}

function localDateStr(date) {
  const d = date || new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/**
 * Detect chat type from sessionKey.
 * Returns: 'direct' | 'channel' | 'subagent' | 'cron' | 'unknown'
 *
 * Channel-agnostic: works for any OpenClaw channel whose sessionKey includes
 * one of {direct, channel, group, subagent, cron-*} as a token.
 */
function detectChatTypeFromSessionKey(sessionKey) {
  if (!sessionKey || typeof sessionKey !== 'string') return 'unknown';
  if (sessionKey.startsWith('cron:') || sessionKey.includes(':cron-')) return 'cron';
  if (sessionKey.includes(':subagent:')) return 'subagent';
  if (sessionKey.includes(':direct:')) return 'direct';
  if (sessionKey.includes(':channel:') || sessionKey.includes(':group:')) return 'channel';
  return 'unknown';
}

/**
 * Extract the channel-specific identifier (room id, chat id, channel id) from sessionKey.
 * Returns the full suffix after the last (direct|channel|group) token, preserving
 * any domain separator so the operator can use the full key for lookups.
 *
 *   - Matrix    : '!roomId:domain.example'    (full key for friendly-name lookup)
 *   - Telegram  : '<chat_id>'                 (numeric, may be negative)
 *   - Slack     : '<channel_id>'              (snowflake)
 *   - Discord   : '<channel_id>'              (snowflake)
 */
function extractChannelIdFromSessionKey(sessionKey) {
  if (!sessionKey) return null;
  const m = sessionKey.match(/:(direct|channel|group):(.+)$/);
  if (!m) return null;
  return m[2];
}

/**
 * Resolve friendly group name from a channel id using memory/groups/group_names.json.
 *
 * Lookup strategy (channel-agnostic):
 *   1. Full key match (e.g. '!roomId:domain.example' for Matrix, chat_id for others)
 *   2. Matrix-specific room-only fallback (strip ':domain' suffix)
 *
 * Operators must populate memory/groups/group_names.json with keys matching
 * whatever the channel uses as the room/chat/channel identifier. For Matrix
 * both full and room-only forms should work; for numeric/snowflake ids only
 * the full key matters.
 *
 * Expected JSON shape:
 *   {
 *     "<channel_id_key>": { "name": "<friendly_name>", "channel": "matrix|telegram|slack|discord" }
 *   }
 */
function resolveGroupName(workspaceDir, channelId) {
  if (!channelId) return null;
  const map = safeReadJSON(PATH.join(workspaceDir, 'memory', 'groups', 'group_names.json'));
  if (!map || typeof map !== 'object') return null;
  if (map[channelId] && map[channelId].name) return map[channelId].name;
  // Matrix-specific fallback: '!roomId:domain' -> '!roomId' (other channels lack the
  // ':' separator so this is a no-op for them and the full-key match above is used).
  const roomOnly = channelId.split(':')[0];
  if (roomOnly !== channelId && map[roomOnly] && map[roomOnly].name) return map[roomOnly].name;
  return null;
}

/**
 * Compose the DM APM context string from workspace/memory/* files.
 * Returns null if APM is not initialized (no L0 index.md).
 */
function composeApmContext(workspaceDir) {
  const memoryDir = PATH.join(workspaceDir, 'memory');
  const mainDir = PATH.join(memoryDir, 'main');

  // L0 — entry gate (required)
  const indexContent = safeReadText(PATH.join(mainDir, 'index.md'));
  if (!indexContent) {
    return null; // APM not initialized
  }

  const attention = safeReadText(PATH.join(mainDir, 'attention.md'));
  const longterm = safeReadText(PATH.join(mainDir, 'longterm.md'));
  const dailySynced = safeReadText(PATH.join(mainDir, 'daily-synced.md'));

  const todayStr = localDateStr();
  const yesterdayDate = new Date();
  yesterdayDate.setDate(yesterdayDate.getDate() - 1);
  const yesterdayStr = localDateStr(yesterdayDate);

  const todayNote = safeReadText(
    PATH.join(memoryDir, `${todayStr}.md`),
    DAILY_NOTE_MAX_CHARS
  );
  const yesterdayNote = safeReadText(
    PATH.join(memoryDir, `${yesterdayStr}.md`),
    DAILY_NOTE_MAX_CHARS
  );

  const flushState = safeReadJSON(PATH.join(memoryDir, 'flush-state.json'));

  const out = [];
  out.push(`# APM Session Start Context (DM)`);
  out.push(`> Auto-injected by apm_session_start hook at ${new Date().toISOString()}`);
  out.push(`> Chat type: direct | Loaded per APM 1.6.0 protocol (memory/main/index.md L0 entry gate)`);
  out.push(`> Workspace: ${workspaceDir}`);
  out.push('');

  out.push(`## L0 — Routing Index (memory/main/index.md)`);
  out.push(indexContent.trim());
  out.push('');

  if (attention) {
    out.push(`## P0 — Attention (active tasks / blockers)`);
    out.push(attention.trim());
    out.push('');
  } else {
    out.push(`## P0 — Attention`);
    out.push('_(memory/main/attention.md not present)_');
    out.push('');
  }

  if (longterm) {
    out.push(`## P1 — Longterm (distilled MEMORY.md summary)`);
    out.push(longterm.trim());
    out.push('');
  } else {
    out.push(`## P1 — Longterm`);
    out.push('_(memory/main/longterm.md not present)_');
    out.push('');
  }

  if (dailySynced) {
    out.push(`## P2 — Daily Synced`);
    out.push(dailySynced.trim());
    out.push('');
  } else {
    out.push(`## P2 — Daily Synced`);
    out.push('_(memory/main/daily-synced.md not present)_');
    out.push('');
  }

  if (todayNote) {
    out.push(`## Daily — Today (${todayStr})`);
    out.push(todayNote.trim());
    out.push('');
  }

  if (yesterdayNote) {
    out.push(`## Daily — Yesterday (${yesterdayStr})`);
    out.push(yesterdayNote.trim());
    out.push('');
  }

  if (flushState) {
    out.push(`## Flush State (memory/flush-state.json)`);
    out.push('```json');
    out.push(JSON.stringify(flushState, null, 2));
    out.push('```');
    out.push('');
  }

  let composed = out.join('\n');
  if (composed.length > APM_MAX_TOTAL_CHARS) {
    composed =
      composed.slice(0, APM_MAX_TOTAL_CHARS) +
      `\n\n[... APM context truncated at ${APM_MAX_TOTAL_CHARS} chars; full set lives in memory/main/ and memory/*.md]`;
  }
  return composed;
}

/**
 * Compose the group-chat APM context string.
 *
 * Per AGENTS.md "Group Chats — Progressive Disclosure Protocol":
 *   1. Entry Gate : memory/groups/{name}.md (only legal entry)
 *   2. Index Routing : L0 index contains routing table
 *   3. Intent Match : agent decides which P-file to load on first user message
 *   4. Explicit Load : max 2 P-files (attention/project/experience/people)
 *   5. Budget Cutoff : stop if memory_budget exceeded
 *
 * For bootstrap injection we can only deterministically load the L0 entry;
 * higher-P files load on-demand via the L0 routing table.
 *
 * PRIVACY: Group-chat sessions MUST NOT see DM-only memory (MEMORY.md,
 * memory/main/*, memory/YYYY-MM-DD.md). Those contain private context.
 * This compose function is the only safe gate; if you change it, audit.
 *
 * Returns null if {name}.md is missing (first-join scenario → defer to AGENTS.md).
 */
function composeGroupChatContext(workspaceDir, groupName, channelId) {
  const groupsDir = PATH.join(workspaceDir, 'memory', 'groups');

  // L0 — entry gate (required)
  const indexContent = safeReadText(PATH.join(groupsDir, `${groupName}.md`));
  if (!indexContent) {
    return null; // first-join scenario; AGENTS.md handles it
  }

  // Group-only flush state (note: NOT memory/flush-state.json — that's DM-only)
  const groupFlushState = safeReadJSON(PATH.join(groupsDir, 'flush-state.json'));

  const out = [];
  out.push(`# APM Group Session Start Context`);
  out.push(`> Auto-injected by apm_session_start hook at ${new Date().toISOString()}`);
  out.push(`> Chat type: channel/group | Group: ${groupName} | Channel: ${channelId}`);
  out.push(`> Loaded per AGENTS.md "Group Chats — Progressive Disclosure Protocol"`);
  out.push(`> Workspace: ${workspaceDir}`);
  out.push('');
  out.push(`⛔️  GROUP CHAT PROTOCOL — DO NOT bypass this.`);
  out.push(`- Only legal entry: \`memory/groups/${groupName}.md\` (L0)`);
  out.push(`- DO NOT read \`memory/main/*\` (DM-only private APM context)`);
  out.push(`- DO NOT read \`MEMORY.md\` (DM-only curated long-term)`);
  out.push(`- DO NOT read \`memory/YYYY-MM-DD.md\` (DM-only daily notes / personal diary)`);
  out.push(`- Higher-P files under \`memory/groups/${groupName}/\` load on-demand per L0 routing table (max 2 per session)`);
  out.push('');

  out.push(`## L0 — Group Index (memory/groups/${groupName}.md)`);
  out.push(indexContent.trim());
  out.push('');

  if (groupFlushState) {
    out.push(`## Group Flush State (memory/groups/flush-state.json)`);
    out.push('```json');
    out.push(JSON.stringify(groupFlushState, null, 2));
    out.push('```');
    out.push('');
  }

  out.push('---');
  out.push(`> Higher-P files (attention / project / experience / people) under \`memory/groups/${groupName}/\` should be loaded on-demand per the L0 routing table above (max 2 per session).`);
  out.push(`> Use \`memory_get("memory/groups/${groupName}/{file}.md")\` to load them; do not bypass the index.`);

  let composed = out.join('\n');
  if (composed.length > APM_MAX_TOTAL_CHARS) {
    composed =
      composed.slice(0, APM_MAX_TOTAL_CHARS) +
      `\n\n[... group context truncated at ${APM_MAX_TOTAL_CHARS} chars; full set lives in memory/groups/${groupName}/]`;
  }
  return composed;
}

/**
 * Main handler — invoked by OpenClaw on every agent:bootstrap event.
 */
async function handler(event) {
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  const context = event.context;
  if (!context || !Array.isArray(context.bootstrapFiles)) {
    return;
  }

  if (context.bootstrapFiles.length === 0) {
    return;
  }

  const workspaceDir = context.workspaceDir;
  if (!workspaceDir || typeof workspaceDir !== 'string') {
    return;
  }

  // Detect chat type from sessionKey (agent:bootstrap event has no chatType field)
  const chatType = detectChatTypeFromSessionKey(event.sessionKey);

  // Skip subagent / cron — the renderer filters these anyway
  if (chatType === 'subagent' || chatType === 'cron') {
    return;
  }

  let entryName;
  let entryContent;
  let contentPath;

  if (chatType === 'channel') {
    // === Group chat path ===
    const channelId = extractChannelIdFromSessionKey(event.sessionKey);
    const groupName = resolveGroupName(workspaceDir, channelId);

    if (!groupName) {
      // Channel detected but no friendly-name mapping. Likely a brand-new group
      // or one whose group_names.json mapping was forgotten. Fall back to DM
      // protocol so the agent still gets *some* context, but log loudly so
      // operators notice the gap. The agent should follow AGENTS.md
      // "First-Join Flow" — ask the group about purpose and create the index.
      console.warn(
        `[apm_session_start] group chat detected but no friendly-name mapping for channel "${channelId}". ` +
        `Add it to memory/groups/group_names.json. Falling back to DM protocol (NOT RECOMMENDED — ` +
        `private memory may leak into group chat).`
      );
      entryName = DM_ENTRY_NAME;
      entryContent = composeApmContext(workspaceDir);
      contentPath = PATH.join(workspaceDir, 'memory', entryName);
    } else {
      entryContent = composeGroupChatContext(workspaceDir, groupName, channelId);
      if (!entryContent) {
        // Friendly name mapped but index.md missing — first-join scenario.
        // Per AGENTS.md, the agent should ask the group about its purpose
        // before creating memory/groups/{name}.md. Don't inject anything;
        // let the agent decide.
        console.log(
          `[apm_session_start] group "${groupName}" (${channelId}) has no memory/groups/${groupName}.md; ` +
          `first-join scenario, skipping injection (agent will follow AGENTS.md "First-Join Flow")`
        );
        return;
      }
      entryName = GROUP_ENTRY_NAME;
      contentPath = PATH.join(workspaceDir, 'memory', 'groups', entryName);
    }
  } else {
    // === DM path (also covers 'unknown' chatType — backward compatible) ===
    entryName = DM_ENTRY_NAME;
    entryContent = composeApmContext(workspaceDir);
    if (!entryContent) {
      console.log(
        '[apm_session_start] memory/main/index.md not found; APM not initialized; skipping'
      );
      return;
    }
    contentPath = PATH.join(workspaceDir, 'memory', entryName);

    if (chatType === 'unknown') {
      console.warn(
        `[apm_session_start] unrecognized sessionKey pattern "${event.sessionKey}"; ` +
        `defaulting to DM protocol. If this is a group chat, the sessionKey format may have changed.`
      );
    }
  }

  // Idempotency — already injected this session
  const alreadyInjected = context.bootstrapFiles.some(
    (file) => file && file.name === entryName
  );
  if (alreadyInjected) {
    return;
  }

  context.bootstrapFiles.push({
    name: entryName,
    path: contentPath,
    content: entryContent,
    missing: false,
  });

  console.log(
    `[apm_session_start] injected ${entryName} (${entryContent.length} chars) for ${chatType} session ${event.sessionKey || 'unknown'}`
  );
}

module.exports = { handler };
