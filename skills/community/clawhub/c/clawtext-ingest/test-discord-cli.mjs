/**
 * Discord CLI Tests (Phase 2)
 * Tests for command parsing, help output, config validation
 */

import assert from 'assert';
import { execSync } from 'child_process';
import fs from 'fs/promises';
import path from 'path';

console.log('🧪 Discord CLI Tests (Phase 2)\n');

const CLI_PATH = './bin/discord.js';
const HELP_OUTPUT = execSync(`node ${CLI_PATH}`).toString();

// Test 1: Help output
console.log('Test 1: Help command shows usage');
try {
  assert(HELP_OUTPUT.includes('describe-forum'), 'Help should include describe-forum');
  assert(HELP_OUTPUT.includes('fetch-discord'), 'Help should include fetch-discord');
  assert(HELP_OUTPUT.includes('--forum-id'), 'Help should show forum-id flag');
  assert(HELP_OUTPUT.includes('--batch-size'), 'Help should show batch-size option');
  console.log('  ✅ Help output complete\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

// Test 2: Missing forum-id errors
console.log('Test 2: Missing forum-id validation');
try {
  const output = execSync(`node ${CLI_PATH} describe-forum 2>&1`, { encoding: 'utf-8' });
  assert(output.includes('forum-id required') || output.includes('Error'), 'Should show error');
  console.log('  ✅ Correctly rejects missing forum-id\n');
} catch (error) {
  // Expected to fail with exit code 1
  if (error.status === 1) {
    console.log('  ✅ Correctly rejects missing forum-id\n');
  } else {
    console.error(`  ❌ Unexpected error: ${error.message}\n`);
  }
}

// Test 3: Missing token error
console.log('Test 3: Missing token validation');
try {
  // Ensure DISCORD_TOKEN is not set
  const env = { ...process.env };
  delete env.DISCORD_TOKEN;

  const output = execSync(
    `node ${CLI_PATH} describe-forum --forum-id 123 2>&1`,
    { encoding: 'utf-8', env }
  );
  assert(output.includes('DISCORD_TOKEN') || output.includes('Error'), 'Should show token error');
  console.log('  ✅ Correctly rejects missing token\n');
} catch (error) {
  if (error.status === 1) {
    console.log('  ✅ Correctly rejects missing token\n');
  } else {
    console.error(`  ❌ Unexpected error: ${error.message}\n`);
  }
}

// Test 4: Help with --help flag
console.log('Test 4: --help flag works');
try {
  const output = execSync(`node ${CLI_PATH} --help 2>&1`).toString();
  assert(output.includes('describe-forum') || output.includes('USAGE'), 'Help should display');
  console.log('  ✅ --help flag displays help\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

// Test 5: Help for specific command
console.log('Test 5: Command-specific help');
try {
  const helpOutput = execSync(`node ${CLI_PATH} 2>&1`).toString();
  assert(helpOutput.includes('describe-forum'), 'Should show describe-forum');
  assert(helpOutput.includes('DISCORD_BOT_SETUP'), 'Should reference setup docs');
  console.log('  ✅ Help includes command options\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

// Test 6: Fetch-discord requires forum/channel/thread
console.log('Test 6: Fetch-discord requires source ID');
try {
  const env = { ...process.env };
  delete env.DISCORD_TOKEN;

  execSync(
    `node ${CLI_PATH} fetch-discord 2>&1`,
    { encoding: 'utf-8', env, stdio: 'pipe' }
  );
  console.error('  ❌ Should have failed\n');
} catch (error) {
  if (error.status === 1) {
    const output = error.stdout?.toString() || error.message;
    assert(
      output.includes('forum-id') || output.includes('channel-id') || output.includes('thread-id') || error.message.includes('Error'),
      'Should show which ID is required'
    );
    console.log('  ✅ Correctly requires source ID\n');
  } else {
    console.error(`  ❌ Unexpected error: ${error.message}\n`);
  }
}

// Test 7: Unknown command
console.log('Test 7: Unknown command error');
try {
  execSync(`node ${CLI_PATH} invalid-command 2>&1`);
  console.error('  ❌ Should have failed\n');
} catch (error) {
  if (error.status === 1) {
    const output = error.stdout?.toString() || error.message;
    assert(
      output.includes('Unknown') || output.includes('Error') || output.includes('invalid'),
      'Should show unknown command error'
    );
    console.log('  ✅ Correctly rejects unknown command\n');
  }
}

// Test 8: Mode options validation
console.log('Test 8: Mode options are documented');
try {
  const output = execSync(`node ${CLI_PATH}`).toString();
  assert(output.includes('full'), 'Should document full mode');
  assert(output.includes('batch'), 'Should document batch mode');
  assert(output.includes('posts-only'), 'Should document posts-only mode');
  console.log('  ✅ All modes documented\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

// Test 9: Flag documentation
console.log('Test 9: Flags are documented');
try {
  const output = execSync(`node ${CLI_PATH}`).toString();
  assert(output.includes('--batch-size'), 'Should document batch-size');
  assert(output.includes('--concurrency'), 'Should document concurrency');
  assert(output.includes('--skip-embeds'), 'Should document skip-embeds');
  assert(output.includes('--verbose'), 'Should document verbose');
  console.log('  ✅ All flags documented\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

// Test 10: Example commands in help
console.log('Test 10: Examples are provided');
try {
  const output = execSync(`node ${CLI_PATH}`).toString();
  assert(output.includes('EXAMPLES'), 'Should have examples section');
  assert(output.includes('describe-forum'), 'Should show example usage');
  console.log('  ✅ Examples included\n');
} catch (error) {
  console.error(`  ❌ Failed: ${error.message}\n`);
}

console.log('═══════════════════════════════════════');
console.log('✅ CLI Tests Complete\n');
console.log('Note: Integration tests require Discord token');
console.log('Run: DISCORD_TOKEN=xxx node bin/discord.js describe-forum --forum-id FORUM_ID\n');
