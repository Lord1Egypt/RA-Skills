#!/usr/bin/env node
/**
 * Deliver a message via Telegram.
 * Usage: node deliver.js --message "text here"
 *    or: echo "text" | node deliver.js
 */
import { loadConfig, log } from './lib.js';

const TG_API = 'https://api.telegram.org';

async function sendTelegram(chatId, text, botToken) {
  // Split long messages (Telegram limit: 4096 chars)
  const chunks = [];
  if (text.length <= 4096) {
    chunks.push(text);
  } else {
    let remaining = text;
    while (remaining.length > 0) {
      if (remaining.length <= 4096) {
        chunks.push(remaining);
        break;
      }
      let cut = remaining.lastIndexOf('\n\n', 4096);
      if (cut < 2000) cut = remaining.lastIndexOf('\n', 4096);
      if (cut < 2000) cut = 4096;
      chunks.push(remaining.slice(0, cut));
      remaining = remaining.slice(cut).trimStart();
    }
  }

  for (const chunk of chunks) {
    const resp = await fetch(`${TG_API}/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: chunk,
        disable_web_page_preview: true,
      }),
    });

    if (!resp.ok) {
      const body = await resp.text();
      throw new Error(`Telegram error ${resp.status}: ${body}`);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  let message = '';

  const msgIdx = args.indexOf('--message');
  if (msgIdx >= 0) {
    message = args.slice(msgIdx + 1).join(' ');
  } else {
    // Read from stdin
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    message = Buffer.concat(chunks).toString().trim();
  }

  if (!message) {
    console.error('No message provided. Use --message "text" or pipe via stdin.');
    process.exit(1);
  }

  const config = loadConfig();
  const chatId = config?.delivery?.chatId;
  const botToken = config?.delivery?.botToken;

  if (!chatId || !botToken) {
    console.error('Missing Telegram chatId or botToken in config. Run setup first.');
    process.exit(1);
  }

  log('deliver', `Sending ${message.length} chars to chat ${chatId}`);
  await sendTelegram(chatId, message, botToken);
  log('deliver', 'Delivered successfully');
}

main().catch((err) => {
  console.error('Delivery failed:', err.message);
  process.exit(1);
});
