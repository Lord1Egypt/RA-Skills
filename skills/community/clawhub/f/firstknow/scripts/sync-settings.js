#!/usr/bin/env node
/**
 * Sync local config settings to the backend.
 * Reads ~/.firstknow/config.json and pushes language, alert_level, quiet_hours to backend.
 */
import { loadConfig, getChatId, apiCall, log } from './lib.js';

async function main() {
  const config = loadConfig();
  const chatId = getChatId();

  if (!config || !chatId) {
    console.error('Missing config or chatId. Run setup first.');
    process.exit(1);
  }

  const update = {
    language: config.language,
    alert_level: config.alert_level,
    quiet_hours: config.quiet_hours,
    timezone: config.timezone,
  };

  log('sync', `Syncing settings for user ${chatId}`);
  const result = await apiCall('PUT', `/api/users/${chatId}`, update);
  console.log(JSON.stringify(result, null, 2));
  log('sync', 'Settings synced to backend');
}

main().catch((err) => {
  console.error('Sync failed:', err.message);
  process.exit(1);
});
