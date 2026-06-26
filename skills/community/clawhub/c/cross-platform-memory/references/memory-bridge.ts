// Cross-platform memory bridge
// Reads Telegram + Discord user messages from OpenClaw session logs
// and returns them as a context string for injection into gateway requests

import fs from 'fs/promises';
import path from 'path';

const SESSIONS_DIR = process.env.OPENCLAW_SESSIONS_DIR ?? 'C:\\Users\\.openclaw\\agents\\main\\sessions';
const WORKSPACE = process.env.OPENCLAW_WORKSPACE ?? 'C:\\Users\\.openclaw\\workspace';
const MESSAGES_PER_PLATFORM = 8;
const MAX_MESSAGE_AGE_HOURS = 20;

export async function getMemoryContext(): Promise<string> {
  const parts: string[] = [];

  // Read MEMORY.md — curated long-term memories
  try {
    const mem = await fs.readFile(path.join(WORKSPACE, 'MEMORY.md'), 'utf8');
    parts.push('## MEMORY.md\n' + mem);
  } catch {}

  // Read today's daily notes
  try {
    const today = new Date().toISOString().slice(0, 10);
    const daily = await fs.readFile(path.join(WORKSPACE, 'memory', `${today}.md`), 'utf8');
    parts.push("## Today's Notes\n" + daily);
  } catch {}

  // Read yesterday's daily notes
  try {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    const yesterday = d.toISOString().slice(0, 10);
    const daily = await fs.readFile(path.join(WORKSPACE, 'memory', `${yesterday}.md`), 'utf8');
    parts.push("## Yesterday's Notes\n" + daily);
  } catch {}

  // Read cross-platform messages from session logs
  try {
    const crossPlatform = await getCrossPlatformMessages();
    if (crossPlatform.telegram.length > 0) {
      parts.push('## Recent Telegram Conversation\n' + crossPlatform.telegram.join('\n'));
    }
    if (crossPlatform.discord.length > 0) {
      parts.push('## Recent Discord Conversation\n' + crossPlatform.discord.join('\n'));
    }
  } catch {}

  if (parts.length === 0) return '';

  return '\n\n---\n\nMEMORY CONTEXT:\n' + parts.join('\n\n') + '\n\n---\n\nIMPORTANT: Use the memory context above to inform your responses. Remember facts about the user and our work together.';
}

interface CrossPlatformMessages {
  telegram: string[];
  discord: string[];
}

async function getCrossPlatformMessages(): Promise<CrossPlatformMessages> {
  const result: CrossPlatformMessages = { telegram: [], discord: [] };

  try {
    const files = await fs.readdir(SESSIONS_DIR);
    const jsonlFiles = files.filter((f) => f.endsWith('.jsonl') && !f.includes('.lock'));

    if (jsonlFiles.length === 0) return result;

    // Find most recent session file
    type FileWithMtime = { name: string; path: string; mtimeMs: number };
    const withMtime: FileWithMtime[] = await Promise.all(
      jsonlFiles.map(async (name) => {
        const filePath = path.join(SESSIONS_DIR, name);
        const stat = await fs.stat(filePath);
        return { name, path: filePath, mtimeMs: stat.mtimeMs };
      })
    );

    withMtime.sort((a, b) => b.mtimeMs - a.mtimeMs);
    const mostRecent = withMtime[0];

    const content = await fs.readFile(mostRecent.path, 'utf8');
    const lines = content.trim().split('\n');

    const telegramMessages: { ts: number; text: string }[] = [];
    const discordMessages: { ts: number; text: string }[] = [];

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        const msg = entry.message;

        if (
          entry.type === 'message' &&
          msg?.role === 'user' &&
          Array.isArray(msg.content) &&
          msg.content[0]?.type === 'text'
        ) {
          const rawText: string = msg.content[0].text;

          // Determine platform and extract clean text
          const channel: string = (entry as any).channel ?? '';
          let clean: string | null = null;
          let platform: 'telegram' | 'discord' | null = null;

          // Telegram: content starts with "Conversation info (untrusted metadata):"
          if (rawText?.startsWith('Conversation info (untrusted metadata):')) {
            clean = stripTelegramMetadata(rawText);
            platform = 'telegram';
          }
          // Discord: channel is "discord" and NOT a bot message
          else if (channel === 'discord') {
            // Check if this is a bot message (author is bot)
            const isBot = (entry as any).message?.author?.bot === true;
            if (!isBot) {
              clean = rawText.trim();
              platform = 'discord';
            }
          }

          if (clean && clean.length > 3 && platform) {
            // Extract timestamp
            let ts = 0;
            try {
              const tsMatch = rawText.match(/"timestamp":\s*"([^"]+)"/);
              if (tsMatch) ts = new Date(tsMatch[1]).getTime();
            } catch {}

            if (platform === 'telegram') {
              telegramMessages.push({ ts, text: clean });
            } else if (platform === 'discord') {
              discordMessages.push({ ts, text: clean });
            }
          }
        }
      } catch {
        // Skip malformed lines
      }
    }

    // Sort by timestamp, filter to recent, cap at limit
    const now = Date.now();
    const maxAge = MAX_MESSAGE_AGE_HOURS * 60 * 60 * 1000;

    const filterRecent = (msgs: { ts: number; text: string }[]) =>
      msgs
        .filter((m) => m.ts > 0 && now - m.ts < maxAge)
        .sort((a, b) => a.ts - b.ts)
        .slice(-MESSAGES_PER_PLATFORM);

    const recentTelegram = telegramMessages.length > 0 ? filterRecent(telegramMessages) : telegramMessages.slice(-MESSAGES_PER_PLATFORM);
    const recentDiscord = discordMessages.length > 0 ? filterRecent(discordMessages) : discordMessages.slice(-MESSAGES_PER_PLATFORM);

    result.telegram = recentTelegram.map((m) => `[telegram] Dan: ${m.text}`);
    result.discord = recentDiscord.map((m) => `[discord] Dan: ${m.text}`);
  } catch {}

  return result;
}

function stripTelegramMetadata(text: string): string {
  // Format: "Conversation info...\n```json\n{...}\n```\n\nSender...\n```json\n{...}\n```\n\nactual message"
  const senderIdx = text.indexOf('Sender (untrusted metadata):');
  if (senderIdx === -1) {
    const firstCodeEnd = text.indexOf('```', 40);
    if (firstCodeEnd !== -1) return text.slice(firstCodeEnd + 4).trim();
    return text.slice(0, 200);
  }

  const searchStart = senderIdx + 30;
  const firstBacktick = text.indexOf('```', searchStart);
  if (firstBacktick === -1) return text.slice(0, 200);

  const secondBacktick = text.indexOf('```', firstBacktick + 3);
  if (secondBacktick === -1) return text.slice(firstBacktick + 3).trim();

  return text.slice(secondBacktick + 4).trim();
}
