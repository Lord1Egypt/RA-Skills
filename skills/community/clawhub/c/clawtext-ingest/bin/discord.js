#!/usr/bin/env node

/**
 * Discord Integration Commands for ClawText-Ingest
 * Phase 2: CLI commands with progress bars and agent integration
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import DiscordAdapter from '../src/adapters/discord.js';
import DiscordIngestionRunner from '../src/agent-runner.js';
import { ClawTextIngest } from '../src/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Progress bar renderer
 */
class ProgressBar {
  constructor(total, width = 40) {
    this.total = total;
    this.current = 0;
    this.width = width;
    this.startTime = Date.now();
  }

  update(current, label = '') {
    this.current = current;
    const percent = this.current / this.total;
    const filled = Math.floor(this.width * percent);
    const empty = this.width - filled;

    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    const percentage = Math.floor(percent * 100);
    const elapsed = ((Date.now() - this.startTime) / 1000).toFixed(1);

    process.stdout.write(
      `\r[${bar}] ${percentage}% | ${this.current}/${this.total} | ${elapsed}s | ${label}`.padEnd(120)
    );
  }

  finish(label = '') {
    const elapsed = ((Date.now() - this.startTime) / 1000).toFixed(1);
    console.log(`\n✅ Complete in ${elapsed}s | ${label}\n`);
  }
}

/**
 * Parse command-line arguments
 */
function parseArgs(args) {
  const parsed = { _: [] };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      parsed[key] = value === undefined ? true : value;
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1);
      parsed[key] = args[++i] || true;
    } else {
      parsed._.push(arg);
    }
  }

  return parsed;
}

/**
 * Show help for Discord commands
 */
function showDiscordHelp() {
  console.log(`
ClawText-Ingest Discord Commands (Phase 2)
Ingest Discord forums, channels, and threads into memory

COMMANDS:
  describe-forum    Show forum structure without fetching messages
  fetch-discord     Fetch Discord forum/channel/thread and ingest

USAGE:
  clawtext-ingest describe-forum --forum-id FORUM_ID [options]
  clawtext-ingest fetch-discord --forum-id|--channel-id|--thread-id ID [options]

DESCRIBE-FORUM OPTIONS:
  --forum-id ID                 Forum ID (required)
  --verbose                     Show details (post names, message counts)
  --token TOKEN                 Discord bot token (or DISCORD_TOKEN env var)

FETCH-DISCORD OPTIONS:
  Forum/Channel/Thread (pick one):
    --forum-id ID               Fetch entire forum
    --channel-id ID             Fetch text channel
    --thread-id ID              Fetch single thread

  Fetch options:
    --mode full|batch|posts-only  Default: auto-detect (full<500, batch>=500)
    --batch-size N              Messages per batch (default: 50)
    --concurrency N             Parallel post fetches (default: 3)
    --skip-embeds               Exclude embeds from messages
    --skip-attachments          Exclude attachment links
    --no-hierarchy              Don't preserve post↔reply structure
    --dedup strict|lenient|skip Deduplication strategy (default: strict)

  Output options:
    --output FILE               Save results to JSON file
    --verbose                   Show detailed progress
    --quiet                     Minimal output
    --token TOKEN               Discord bot token (or DISCORD_TOKEN env var)

EXAMPLES:
  # Inspect forum structure
  clawtext-ingest describe-forum --forum-id 123456789 --verbose

  # Fetch and ingest small forum
  clawtext-ingest fetch-discord --forum-id 123456789 --mode full

  # Ingest large forum in batches with progress
  clawtext-ingest fetch-discord \\
    --forum-id 987654321 \\
    --mode batch \\
    --batch-size 100 \\
    --concurrency 5 \\
    --output ingestion.json \\
    --verbose

  # Fetch just post roots (fast survey)
  clawtext-ingest fetch-discord --forum-id 555555555 --mode posts-only

  # Ingest channel
  clawtext-ingest fetch-discord --channel-id 111111111

ENVIRONMENT:
  DISCORD_TOKEN    Discord bot token (alternative to --token flag)

See documentation:
  - DISCORD_BOT_SETUP.md - How to create a Discord bot
  - API_REFERENCE.md - Full API documentation
  - QUICKSTART.md - Quick start guide
`);
}

/**
 * Command: describe-forum
 * Show forum structure without fetching all messages
 */
async function cmdDescribeForum(args) {
  const forumId = args['forum-id'];
  const verbose = args.verbose || false;
  const token = args.token || process.env.DISCORD_TOKEN;

  if (!forumId) {
    console.error('❌ Error: --forum-id required');
    process.exit(1);
  }

  if (!token) {
    console.error('❌ Error: DISCORD_TOKEN env var or --token flag required');
    process.exit(1);
  }

  try {
    const adapter = new DiscordAdapter({ token });
    await adapter.authenticate();

    console.log('📊 Fetching forum structure...\n');

    const info = await adapter.describeForumStructure(forumId);

    console.log(`📁 Forum: ${info.name}`);
    console.log(`   ID: ${info.id}`);
    console.log(`   Topic: ${info.topic || '(none)'}`);
    console.log(`   Posts: ${info.postCount}`);
    console.log(`   Est. Messages: ${info.estimatedMessageCount}`);
    console.log(`   Tags: ${info.tags.join(', ') || '(none)'}`);
    console.log(`   Fetched at: ${info.fetchedAt}\n`);

    if (verbose) {
      const hierarchy = await adapter.fetchForumHierarchy(forumId);
      console.log(`📝 Posts (${hierarchy.length} total):`);
      hierarchy.slice(0, 10).forEach((post, i) => {
        console.log(`   ${i + 1}. "${post.postName}" (${post.messageCount} messages)`);
      });
      if (hierarchy.length > 10) {
        console.log(`   ... and ${hierarchy.length - 10} more`);
      }
      console.log();
    }

    await adapter.disconnect();
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Command: fetch-discord
 * Fetch Discord forum/channel/thread and ingest
 */
async function cmdFetchDiscord(args) {
  // Validate input
  const forumId = args['forum-id'];
  const channelId = args['channel-id'];
  const threadId = args['thread-id'];
  const token = args.token || process.env.DISCORD_TOKEN;

  if (!forumId && !channelId && !threadId) {
    console.error('❌ Error: Must specify --forum-id, --channel-id, or --thread-id');
    process.exit(1);
  }

  if (!token) {
    console.error('❌ Error: DISCORD_TOKEN env var or --token flag required');
    process.exit(1);
  }

  const sourceId = forumId || channelId || threadId;
  const sourceType = forumId ? 'forum' : channelId ? 'channel' : 'thread';

  // Parse options
  const mode = args.mode || 'auto';
  const batchSize = parseInt(args['batch-size']) || 50;
  const concurrency = parseInt(args.concurrency) || 3;
  const skipEmbeds = args['skip-embeds'] ? true : false;
  const skipAttachments = args['skip-attachments'] ? true : false;
  const preserveHierarchy = args['no-hierarchy'] ? false : true;
  const dedupStrategy = args.dedup || 'strict';
  const outputPath = args.output;
  const verbose = args.verbose ? true : !args.quiet;

  let progressBar;
  const startTime = Date.now();

  try {
    // Initialize
    const adapter = new DiscordAdapter({
      token,
      includeEmbeds: !skipEmbeds,
      includeAttachments: !skipAttachments,
      concurrency,
      batchSize,
      progressCallback: verbose ? (progress) => {
        if (!progressBar) {
          progressBar = new ProgressBar(progress.total, 40);
        }
        progressBar.update(progress.processed, progress.currentPost || sourceId);
      } : null,
    });

    await adapter.authenticate();

    if (verbose) {
      console.log(`🔗 Connected to Discord\n`);
    }

    let records, relationshipMap, metadata;

    if (forumId) {
      // Forum: auto-detect mode based on size
      if (mode === 'auto') {
        const info = await adapter.describeForumStructure(forumId);
        const autoMode = info.postCount >= 500 ? 'batch' : 'full';
        if (verbose) {
          console.log(`📊 Forum: ${info.name} (${info.postCount} posts)`);
          console.log(`   Auto-selected mode: ${autoMode}\n`);
        }

        if (autoMode === 'batch') {
          // Batch mode
          records = [];
          relationshipMap = {};
          let batchCount = 0;

          progressBar = new ProgressBar(info.estimatedMessageCount, 40);

          for await (const batch of adapter.fetchForumInBatches(forumId, { batchSize, concurrency })) {
            records.push(...batch.records);
            Object.assign(relationshipMap, batch.relationshipMap);
            batchCount++;
            progressBar.update(records.length, `Batch ${batchCount}`);
          }

          metadata = {
            source: 'discord',
            sourceType: 'forum',
            forumId,
            forumName: info.name,
            preserveHierarchy,
            mode: 'batch',
            batchCount,
          };
        } else {
          // Full mode
          progressBar = new ProgressBar(info.postCount, 40);
          const result = await adapter.fetchForumCompletely(forumId);
          records = result.records;
          relationshipMap = result.relationshipMap;
          metadata = {
            source: 'discord',
            sourceType: 'forum',
            forumId,
            forumName: result.forumMetadata.forumName,
            preserveHierarchy,
            mode: 'full',
          };
        }
      } else if (mode === 'batch') {
        // Explicit batch mode
        records = [];
        relationshipMap = {};
        let batchCount = 0;
        let totalEstimate = 0;

        const info = await adapter.describeForumStructure(forumId);
        progressBar = new ProgressBar(info.estimatedMessageCount, 40);

        for await (const batch of adapter.fetchForumInBatches(forumId, { batchSize, concurrency })) {
          records.push(...batch.records);
          Object.assign(relationshipMap, batch.relationshipMap);
          batchCount++;
          progressBar.update(records.length, `Batch ${batchCount}`);
        }

        metadata = {
          source: 'discord',
          sourceType: 'forum',
          forumId,
          forumName: info.name,
          preserveHierarchy,
          mode: 'batch',
          batchCount,
        };
      } else if (mode === 'posts-only') {
        // Posts-only mode
        const hierarchy = await adapter.fetchForumHierarchy(forumId);
        records = hierarchy.map(post => ({
          id: `post_root_${post.postId}`,
          source: 'discord',
          sourceType: 'forum_post_root',
          content: post.postName,
          author: post.authorId,
          timestamp: post.createdAt,
          forumHierarchy: { postId: post.postId, depth: 0 },
          metadata: { messageCount: post.messageCount },
        }));
        relationshipMap = {};
        metadata = { source: 'discord', sourceType: 'forum', forumId, mode: 'posts-only' };
      } else {
        // Full mode (explicit)
        const info = await adapter.describeForumStructure(forumId);
        progressBar = new ProgressBar(info.postCount, 40);
        const result = await adapter.fetchForumCompletely(forumId);
        records = result.records;
        relationshipMap = result.relationshipMap;
        metadata = {
          source: 'discord',
          sourceType: 'forum',
          forumId,
          forumName: result.forumMetadata.forumName,
          preserveHierarchy,
          mode: 'full',
        };
      }
    } else if (channelId) {
      // Channel
      const result = await adapter.fetchChannel(channelId);
      records = result.records;
      relationshipMap = result.relationshipMap;
      metadata = {
        source: 'discord',
        sourceType: 'channel',
        channelId,
        channelName: result.channelMetadata.channelName,
      };
    } else if (threadId) {
      // Thread
      const result = await adapter.fetchThread(threadId);
      records = result.records;
      relationshipMap = result.relationshipMap;
      metadata = {
        source: 'discord',
        sourceType: 'thread',
        threadId,
        threadName: result.threadMetadata.threadName,
      };
    }

    if (progressBar) {
      progressBar.finish(`${records.length} messages fetched`);
    } else if (verbose) {
      console.log(`✅ Fetched ${records.length} messages\n`);
    }

    // Ingest to ClawText
    if (verbose) {
      console.log(`📥 Ingesting to ClawText...`);
    }

    const ingester = new ClawTextIngest();
    const ingestResult = await ingester.fromJSON(
      records,
      {
        ...metadata,
        relationshipMap: preserveHierarchy ? relationshipMap : null,
      },
      { checkDedupe: dedupStrategy !== 'skip' }
    );

    if (progressBar) {
      // Progress bar doesn't include ingest time in its counter
      const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
      console.log(`✅ Ingestion complete in ${totalTime}s\n`);
    } else if (verbose) {
      console.log(`✅ Ingestion complete\n`);
    }

    // Summary
    if (verbose) {
      console.log('📊 Summary:');
      console.log(`   Fetched: ${records.length} messages`);
      console.log(`   Ingested: ${ingestResult.ingestedCount}`);
      console.log(`   Deduplicated: ${ingestResult.duplicateSkipped}`);
      if (sourceType === 'forum') {
        console.log(`   Posts: ${Object.keys(relationshipMap).length}`);
        console.log(`   Hierarchy Preserved: ${preserveHierarchy}`);
      }
      console.log();
    }

    // Save output if requested
    if (outputPath) {
      if (verbose) {
        console.log(`💾 Saving results to ${outputPath}...`);
      }
      await fs.mkdir(path.dirname(outputPath || '.'), { recursive: true });
      await fs.writeFile(
        outputPath,
        JSON.stringify({
          metadata,
          recordsCount: records.length,
          ingestResult,
          relationshipMap: preserveHierarchy ? relationshipMap : null,
          timestamp: new Date().toISOString(),
        }, null, 2)
      );
      if (verbose) {
        console.log(`✅ Results saved\n`);
      }
    }

    await adapter.disconnect();
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    if (args.verbose) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

/**
 * Main
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === 'help' || args[0] === '--help') {
    showDiscordHelp();
    process.exit(0);
  }

  const command = args[0];
  const options = parseArgs(args.slice(1));

  switch (command) {
    case 'describe-forum':
      await cmdDescribeForum(options);
      break;
    case 'fetch-discord':
      await cmdFetchDiscord(options);
      break;
    default:
      console.error(`❌ Unknown command: ${command}`);
      showDiscordHelp();
      process.exit(1);
  }
}

main().catch(error => {
  console.error(`❌ Fatal error: ${error.message}`);
  process.exit(1);
});
