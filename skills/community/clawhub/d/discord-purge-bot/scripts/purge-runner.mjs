#!/usr/bin/env node
import { buildConfirmCode, buildJobId } from './job-code.mjs';
import {
  asBoolean,
  chunkList,
  parseArgs,
  printJson,
  resolveToken,
  sleep,
  writeJson,
} from './common.mjs';
import { bulkDeleteMessages, deleteMessage } from './discord-api.mjs';
import { normalizeFilters, scanMessages, splitMessagesByAge } from './scan-filter.mjs';

const helpText = `Usage:
  node scripts/purge-runner.mjs --channel-id <id> --confirm <code> [options]

Options:
  --token <token>            Discord bot token (or use DISCORD_BOT_TOKEN)
  --channel-id <id>          Target guild channel id
  --confirm <code>           Confirmation code from preview
  --author-id <id>           Only include messages from this author
  --contains <text>          Include messages containing text
  --regex <pattern>          Include messages matching regex pattern
  --regexFlags <flags>       Regex flags (default: i)
  --after <iso>              Include messages after datetime
  --before <iso>             Include messages before datetime
  --include-pinned           Include pinned messages
  --max-scan <n>             Max scanned messages (default: 5000)
  --max-matches <n>          Stop after this many matches
  --state-file <path>        Persist run state JSON
  --out <path>               Persist final result JSON
  --reason <text>            Audit log reason
  --dry-run                  Do not delete messages
  --single-only              Disable bulk-delete
  --delete-delay-ms <n>      Delay after each delete request
  --help                     Show this message
`;

function summarizeFilters(args, filters) {
  return {
    authorId: args['author-id'] ?? null,
    contains: args.contains ?? null,
    regex: args.regex ?? null,
    regexFlags: args.regexFlags ?? 'i',
    after: args.after ?? null,
    before: args.before ?? null,
    includePinned: filters.includePinned,
    maxScan: filters.maxScan,
    maxMatches: filters.maxMatches ?? null,
  };
}

async function writeState(stateFile, state) {
  if (!stateFile) return;
  await writeJson(stateFile, state);
}

async function deleteRecentMessages({ token, channelId, messages, reason, singleOnly, deleteDelayMs }) {
  let deleted = 0;
  let failed = 0;

  const ids = Array.from(new Set(messages.map((message) => message.id)));
  const batches = chunkList(ids, 100);

  for (const batch of batches) {
    if (singleOnly || batch.length === 1) {
      for (const messageId of batch) {
        try {
          await deleteMessage({ token, channelId, messageId, reason });
          deleted += 1;
        } catch (error) {
          failed += 1;
          process.stderr.write(`Failed single delete for ${messageId}: ${error.message}\n`);
        }
        await sleep(deleteDelayMs);
      }
      continue;
    }

    try {
      await bulkDeleteMessages({ token, channelId, messageIds: batch, reason });
      deleted += batch.length;
    } catch (error) {
      process.stderr.write(`Bulk delete failed for ${batch.length} messages: ${error.message}\n`);
      for (const messageId of batch) {
        try {
          await deleteMessage({ token, channelId, messageId, reason });
          deleted += 1;
        } catch (singleError) {
          failed += 1;
          process.stderr.write(`Fallback single delete failed for ${messageId}: ${singleError.message}\n`);
        }
        await sleep(deleteDelayMs);
      }
    }
  }

  return { deleted, failed };
}

async function deleteOldMessages({ token, channelId, messages, reason, deleteDelayMs }) {
  let deleted = 0;
  let failed = 0;

  for (const message of messages) {
    try {
      await deleteMessage({ token, channelId, messageId: message.id, reason });
      deleted += 1;
    } catch (error) {
      failed += 1;
      process.stderr.write(`Failed old-message delete for ${message.id}: ${error.message}\n`);
    }
    await sleep(deleteDelayMs);
  }

  return { deleted, failed };
}

async function main() {
  const args = parseArgs();

  if (args.help) {
    process.stdout.write(helpText);
    return;
  }

  const channelId = String(args['channel-id'] ?? '');
  if (!channelId) throw new Error('Missing required argument --channel-id');

  const token = resolveToken(args);
  const filters = normalizeFilters(args);
  const dryRun = asBoolean(args['dry-run'], false);
  const singleOnly = asBoolean(args['single-only'], false);
  const deleteDelayMs = Number.parseInt(String(args['delete-delay-ms'] ?? '0'), 10) || 0;

  const expectedCode = buildConfirmCode({
    channelId,
    authorId: args['author-id'],
    contains: args.contains,
    regex: args.regex,
    after: args.after,
    before: args.before,
    includePinned: filters.includePinned,
  });

  const providedCode = String(args.confirm ?? '');
  if (!providedCode) throw new Error('Missing required argument --confirm');
  if (providedCode !== expectedCode) {
    throw new Error(`Confirmation mismatch. Expected ${expectedCode}`);
  }

  const stateFile = args['state-file'] ? String(args['state-file']) : undefined;
  const result = {
    jobId: buildJobId('run'),
    startedAt: new Date().toISOString(),
    phase: 'scanning',
    channelId,
    filters: summarizeFilters(args, filters),
    dryRun,
    singleOnly,
    scannedCount: 0,
    matchedCount: 0,
    recentCount: 0,
    oldCount: 0,
    deletedCount: 0,
    failedCount: 0,
    expectedConfirmCode: expectedCode,
  };

  await writeState(stateFile, result);

  const scanResult = await scanMessages({
    token,
    channelId,
    filters,
    onPage: async (progress) => {
      result.scannedCount = progress.scannedCount;
      result.matchedCount = progress.matchedCount;
      await writeState(stateFile, result);
    },
  });

  result.scannedCount = scanResult.scannedCount;
  result.matchedCount = scanResult.matchedMessages.length;

  const split = splitMessagesByAge(scanResult.matchedMessages);
  result.recentCount = split.recentMessages.length;
  result.oldCount = split.oldMessages.length;

  if (dryRun) {
    result.phase = 'done';
    result.finishedAt = new Date().toISOString();
    await writeState(stateFile, result);
    if (args.out) await writeJson(String(args.out), result);
    printJson(result);
    return;
  }

  result.phase = 'deleting-recent';
  await writeState(stateFile, result);

  const recentDelete = await deleteRecentMessages({
    token,
    channelId,
    messages: split.recentMessages,
    reason: args.reason ? String(args.reason) : undefined,
    singleOnly,
    deleteDelayMs,
  });

  result.deletedCount += recentDelete.deleted;
  result.failedCount += recentDelete.failed;
  await writeState(stateFile, result);

  result.phase = 'deleting-old';
  await writeState(stateFile, result);

  const oldDelete = await deleteOldMessages({
    token,
    channelId,
    messages: split.oldMessages,
    reason: args.reason ? String(args.reason) : undefined,
    deleteDelayMs,
  });

  result.deletedCount += oldDelete.deleted;
  result.failedCount += oldDelete.failed;
  result.phase = 'done';
  result.finishedAt = new Date().toISOString();

  await writeState(stateFile, result);
  if (args.out) await writeJson(String(args.out), result);
  printJson(result);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
