#!/usr/bin/env node
/**
 * Telegram Draft Handler - Integration Example
 * Shows how to reply to forwarded messages with routing buttons
 */

const router = require('./draft-router.js');

// Simulate receiving a forwarded message
function handleIncomingDraft(content, chatId = 'default') {
  // Get button configuration from router
  const result = router.handleDraft(content, `telegram:${chatId}`);
  
  // Output the configuration for OpenClaw's message tool
  console.log('DRAFT_ROUTER_OUTPUT:');
  console.log(JSON.stringify({
    message: result.text,
    buttons: result.buttons
  }, null, 2));
  
  return result;
}

// If run directly with content
if (require.main === module) {
  const content = process.argv.slice(2).join(' ');
  if (!content) {
    console.log('Usage: node telegram-handler.js "<draft content>"');
    process.exit(1);
  }
  handleIncomingDraft(content);
}

module.exports = { handleIncomingDraft };
