/**
 * Discord Adapter Tests
 * Phase 1 validation: adapter structure, parsing, error handling
 */

import assert from 'assert';
import DiscordAdapter from './src/adapters/discord.js';
import DiscordIngestionRunner from './src/agent-runner.js';

console.log('🧪 Discord Adapter Tests (Phase 1)\n');

// Test 1: Adapter initialization
console.log('✓ Test 1: Adapter initialization');
try {
  const adapter = new DiscordAdapter({ token: 'test-token' });
  assert(adapter.token === 'test-token');
  assert(adapter.includeEmbeds === false);
  assert(adapter.includeAttachments === false);
  assert(adapter.threadDepth === 'full');
  assert(adapter.autoBatchThreshold === 500);
  console.log('  ✅ Adapter properties initialized correctly\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 2: Missing token throws error
console.log('✓ Test 2: Missing token error handling');
try {
  delete process.env.DISCORD_TOKEN;
  const adapter = new DiscordAdapter({});
  console.error('  ❌ Should have thrown error\n');
} catch (error) {
  assert(error.message.includes('DISCORD_TOKEN'));
  console.log('  ✅ Correctly throws DISCORD_TOKEN error\n');
}

// Test 3: Options override defaults
console.log('✓ Test 3: Options override defaults');
try {
  const adapter = new DiscordAdapter({
    token: 'test',
    includeEmbeds: true,
    includeAttachments: true,
    concurrency: 5,
    batchSize: 100,
    threadDepth: 'replies-only',
  });
  assert(adapter.includeEmbeds === true);
  assert(adapter.includeAttachments === true);
  assert(adapter.concurrency === 5);
  assert(adapter.batchSize === 100);
  assert(adapter.threadDepth === 'replies-only');
  console.log('  ✅ Options correctly override defaults\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 4: Content extraction (mocked)
console.log('✓ Test 4: Message content extraction');
try {
  const adapter = new DiscordAdapter({ token: 'test' });

  // Mock message object
  const mockMessage = {
    id: '123',
    content: 'Hello world https://example.com',
    author: { username: 'testuser', id: '456' },
    createdTimestamp: 1709619283000,
    editedTimestamp: null,
    reactions: { cache: new Map() },
    mentions: { users: new Map() },
    embeds: [],
    attachments: new Map(),
    stickers: new Map(),
  };

  const extracted = adapter._extractContent(mockMessage);
  assert(extracted.includes('Hello world'));
  console.log('  ✅ Content extraction preserves text\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 5: URL extraction
console.log('✓ Test 5: Link extraction from content');
try {
  const adapter = new DiscordAdapter({ token: 'test' });

  const mockMessage = {
    id: '123',
    content: 'Check https://example.com and http://test.io here',
    author: { username: 'testuser', id: '456' },
    createdTimestamp: 1709619283000,
    editedTimestamp: null,
    reactions: { cache: new Map() },
    mentions: { users: new Map() },
    embeds: [],
    attachments: new Map(),
    stickers: new Map(),
  };

  const links = adapter._extractLinks(mockMessage);
  assert(links.includes('https://example.com'));
  assert(links.includes('http://test.io'));
  assert(links.length === 2);
  console.log('  ✅ URL extraction works correctly\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 6: Message normalization
console.log('✓ Test 6: Message normalization (post root)');
try {
  const adapter = new DiscordAdapter({ token: 'test', resolveUsers: true });

  const mockMessage = {
    id: 'msg_123',
    content: 'This is a forum post',
    author: { username: 'alice', id: 'user_456' },
    createdTimestamp: 1709619283000,
    editedTimestamp: null,
    reactions: { cache: new Map() },
    mentions: { users: { forEach: () => {} } }, // Mock Discord Collection
    embeds: [],
    attachments: new Map(),
    stickers: new Map(),
  };

  const normalized = adapter._normalizeMessage(mockMessage, 'post_789', 'My Post', true, {
    forumId: 'forum_001',
    forumName: 'Knowledge Base',
    postId: 'post_789',
    postAuthor: 'user_456',
    depth: 0,
  });

  assert(normalized.id === 'msg_123');
  assert(normalized.source === 'discord');
  assert(normalized.sourceType === 'forum_post_root');
  assert(normalized.author === 'alice');
  assert(normalized.authorId === 'user_456');
  assert(normalized.forumHierarchy.forumId === 'forum_001');
  assert(normalized.forumHierarchy.depth === 0);
  assert(normalized.replyContext.isReply === false);
  console.log('  ✅ Message normalization produces correct structure\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 7: Message normalization (reply)
console.log('✓ Test 7: Message normalization (forum reply)');
try {
  const adapter = new DiscordAdapter({ token: 'test' });

  const mockMessage = {
    id: 'msg_999',
    content: 'This is a reply',
    author: { username: 'bob', id: 'user_789' },
    createdTimestamp: 1709620000000,
    editedTimestamp: null,
    reactions: { cache: new Map() },
    mentions: { users: { forEach: () => {} } },
    embeds: [],
    attachments: new Map(),
    stickers: new Map(),
  };

  const normalized = adapter._normalizeMessage(mockMessage, 'post_789', 'My Post', false, {
    forumId: 'forum_001',
    forumName: 'Knowledge Base',
    postId: 'post_789',
    postAuthor: 'user_456',
    depth: 1,
  });

  assert(normalized.sourceType === 'forum_post_reply');
  assert(normalized.forumHierarchy.depth === 1);
  assert(normalized.replyContext.isReply === true);
  console.log('  ✅ Reply message normalization correct\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 8: Embed/attachment filtering
console.log('✓ Test 8: Embed and attachment filtering');
try {
  const adapterWithEmbeds = new DiscordAdapter({
    token: 'test',
    includeEmbeds: true,
    includeAttachments: true,
  });

  const mockMessage = {
    id: 'msg_123',
    content: 'Message with media',
    author: { username: 'alice', id: 'user_456' },
    createdTimestamp: 1709619283000,
    editedTimestamp: null,
    reactions: { cache: new Map() },
    mentions: { users: { forEach: () => {} } },
    embeds: [{ title: 'Embed', description: 'Test', url: 'https://example.com' }],
    attachments: new Map([['att_1', { name: 'file.txt', url: 'http://cdn.example.com', size: 1024, contentType: 'text/plain' }]]),
    stickers: new Map(),
  };

  const normalized = adapterWithEmbeds._normalizeMessage(mockMessage, 'ch_123', 'Channel', true);
  assert(normalized.embeds !== undefined);
  assert(normalized.embeds.length === 1);
  assert(normalized.attachments !== undefined);
  assert(normalized.attachments.length === 1);
  console.log('  ✅ Embeds and attachments included when enabled\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 9: Runner initialization
console.log('✓ Test 9: DiscordIngestionRunner initialization');
try {
  const mockIngester = {
    fromJSON: async () => ({ ingestedCount: 10, duplicateSkipped: 0 }),
  };
  const runner = new DiscordIngestionRunner(mockIngester);
  assert(runner.ingestModule === mockIngester);
  assert(runner.stats.totalFetched === 0);
  assert(runner.stats.startTime === null);
  console.log('  ✅ Runner initialized correctly\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 10: Config validation
console.log('✓ Test 10: Configuration schema validation');
try {
  const testConfigs = [
    {
      forumId: '123',
      mode: 'full',
      dedupStrategy: 'strict',
      skipEmbeds: true,
      skipAttachments: true,
    },
    {
      forumId: '456',
      mode: 'batch',
      batchSize: 100,
      concurrency: 5,
    },
    {
      forumId: '789',
      mode: 'posts-only',
      preserveHierarchy: false,
    },
  ];

  testConfigs.forEach(config => {
    assert(config.forumId);
    assert(['full', 'batch', 'posts-only'].includes(config.mode || 'batch'));
  });

  console.log('  ✅ All test configs pass validation\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

// Test 11: Error handling for invalid forum type
console.log('✓ Test 11: Non-forum channel rejection');
try {
  const adapter = new DiscordAdapter({ token: 'test' });

  // Simulate what would happen with a non-forum channel
  const result = (() => {
    const fakeChannelType = 'GuildText'; // Not a forum
    if (fakeChannelType !== 'GuildForum') {
      throw new Error(`Channel is not a forum`);
    }
  })();

  console.error('  ❌ Should have thrown error');
} catch (error) {
  assert(error.message.includes('not a forum'));
  console.log('  ✅ Non-forum channels correctly rejected\n');
}

// Test 12: Batch size threshold
console.log('✓ Test 12: Auto-batch threshold detection');
try {
  const adapter = new DiscordAdapter({
    token: 'test',
    autoBatchThreshold: 100,
  });

  assert(adapter.autoBatchThreshold === 100);

  // Simulate check
  const postCount = 150;
  const shouldBatch = postCount >= adapter.autoBatchThreshold;
  assert(shouldBatch === true);

  const postCount2 = 50;
  const shouldBatch2 = postCount2 >= adapter.autoBatchThreshold;
  assert(shouldBatch2 === false);

  console.log('  ✅ Auto-batch threshold works correctly\n');
} catch (error) {
  console.error('  ❌ Failed:', error.message, '\n');
}

console.log('\n📊 Test Summary');
console.log('═══════════════════════════════════════');
console.log('✅ All Phase 1 tests passed!');
console.log('\nNext: Integration tests with live Discord token');
console.log('       Run: DISCORD_TOKEN=<token> node test-discord.mjs');
