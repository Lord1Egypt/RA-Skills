#!/usr/bin/env node
/**
 * Register user with the FirstKnow backend.
 * Reads from ~/.firstknow/config.json and ~/.firstknow/portfolio.json
 */
import { loadConfig, loadPortfolio, getChatId, getBotToken, apiCall, log } from './lib.js';

async function main() {
  const config = loadConfig();
  const portfolio = loadPortfolio();

  if (!config || !portfolio) {
    console.error('Error: Run setup first. Missing config.json or portfolio.json');
    process.exit(1);
  }

  const chatId = getChatId();
  const botToken = getBotToken();

  if (!chatId || !botToken) {
    console.error('Error: Missing Telegram chatId or botToken in config.json');
    process.exit(1);
  }

  log('register', `Registering user ${chatId} with ${portfolio.holdings.length} holdings`);

  const result = await apiCall('POST', '/api/users/register', {
    chat_id: chatId,
    bot_token: botToken,
    holdings: portfolio.holdings,
    language: config.language || 'en',
    timezone: config.timezone || null,
    alert_level: config.alert_level || 'all',
    quiet_hours: config.quiet_hours || null,
  });

  console.log(JSON.stringify(result, null, 2));
  log('register', 'Registration successful! Backend will start pushing alerts.');
}

main().catch((err) => {
  console.error('Registration failed:', err.message);
  process.exit(1);
});
