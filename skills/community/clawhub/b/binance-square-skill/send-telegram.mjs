/**
 * Standalone Telegram sender for binance-square skill.
 *
 * Reads from env vars:
 *   TG_BOT_TOKEN   — bot token from @BotFather (required)
 *   TG_CHAT_ID     — chat ID to send to (required, your numeric user ID for DM)
 *
 * Usage:
 *   node send-telegram.mjs "message text"           # send markdown
 *   echo "..." | node send-telegram.mjs --stdin     # read from stdin
 *   node send-telegram.mjs --file path/to/msg.txt   # read from file
 *   node send-telegram.mjs --test                   # send a ping
 *
 * For Markdown safety with $ signs, prefer --stdin or --file modes.
 */

import { readFileSync } from 'fs';

const TOKEN = process.env.TG_BOT_TOKEN;
const CHAT_ID = process.env.TG_CHAT_ID;

if (!TOKEN || !CHAT_ID) {
  console.error('ERROR: TG_BOT_TOKEN and TG_CHAT_ID env vars are required.');
  console.error('  Set them in your shell, .env file, or pass via cron environment.');
  console.error('  Get a bot token from @BotFather, get your chat ID from @userinfobot.');
  process.exit(1);
}

const API = `https://api.telegram.org/bot${TOKEN}`;

async function sendMessage(text, parseMode = 'Markdown') {
  const truncated = text.length > 4096 ? text.slice(0, 4050) + '\n...(truncated)' : text;
  const res = await fetch(`${API}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text: truncated,
      parse_mode: parseMode,
      disable_web_page_preview: true,
    }),
  });
  const json = await res.json();
  if (!json.ok) {
    // Retry without parse mode if Markdown fails
    const retry = await fetch(`${API}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: CHAT_ID,
        text: truncated,
        disable_web_page_preview: true,
      }),
    });
    const retryJson = await retry.json();
    if (!retryJson.ok) throw new Error(`Telegram API: ${retryJson.description || 'unknown'}`);
    return retryJson.result;
  }
  return json.result;
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (c) => (data += c));
    process.stdin.on('end', () => resolve(data.trim()));
    process.stdin.on('error', reject);
    setTimeout(() => { if (!data) reject(new Error('stdin timeout (5s)')); }, 5000);
  });
}

async function main() {
  const args = process.argv.slice(2);
  let text;

  if (args[0] === '--test') {
    text = '✅ binance-square skill TG sender test — *bold* `code` $100';
  } else if (args[0] === '--stdin') {
    text = await readStdin();
  } else if (args[0] === '--file') {
    if (!args[1]) throw new Error('--file requires a path');
    text = readFileSync(args[1], 'utf8').trim();
  } else if (args.length > 0 && !args[0].startsWith('--')) {
    text = args.join(' ');
  } else {
    console.error('Usage: send-telegram.mjs ["text" | --stdin | --file PATH | --test]');
    process.exit(1);
  }

  if (!text) throw new Error('No message content');

  const result = await sendMessage(text);
  console.log(JSON.stringify({ ok: true, message_id: result.message_id, chars: text.length }));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
