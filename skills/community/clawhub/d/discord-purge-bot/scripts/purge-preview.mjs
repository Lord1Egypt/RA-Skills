#!/usr/bin/env node
import { buildConfirmCode, buildJobId } from './job-code.mjs';
import { normalizeFilters, scanMessages, splitMessagesByAge } from './scan-filter.mjs';
import { parseArgs, printJson, resolveToken, writeJson } from './common.mjs';

const helpText = `Usage:
  node scripts/purge-preview.mjs --channel-id <id> [options]

Options:
  --token <token>            Discord bot token (or use DISCORD_BOT_TOKEN)
  --channel-id <id>          Target guild channel id
  --author-id <id>           Only include messages from this author
  --contains <text>          Include messages containing text
  --regex <pattern>          Include messages matching regex pattern
  --regexFlags <flags>       Regex flags (default: i)
  --after <iso>              Include messages after datetime
  --before <iso>             Include messages before datetime
  --include-pinned           Include pinned messages
  --max-scan <n>             Max scanned messages (default: 5000)
  --max-matches <n>          Stop after this many matches
  --out <path>               Write JSON to file
  --help                     Show this message
`;

async function main() {
  const args = parseArgs();

  if (args.help) {
    process.stdout.write(helpText);
    return;
  }

  if (!args['channel-id']) {
    throw new Error('Missing required argument --channel-id');
  }

  const token = resolveToken(args);
  const channelId = String(args['channel-id']);
  const filters = normalizeFilters(args);

  const { scannedCount, pageCount, matchedMessages } = await scanMessages({
    token,
    channelId,
    filters,
  });

  const { recentMessages, oldMessages } = splitMessagesByAge(matchedMessages);

  const confirmCode = buildConfirmCode({
    channelId,
    authorId: args['author-id'],
    contains: args.contains,
    regex: args.regex,
    after: args.after,
    before: args.before,
    includePinned: filters.includePinned,
  });

  const result = {
    jobId: buildJobId('preview'),
    generatedAt: new Date().toISOString(),
    channelId,
    filters: {
      authorId: args['author-id'] ?? null,
      contains: args.contains ?? null,
      regex: args.regex ?? null,
      regexFlags: args.regexFlags ?? 'i',
      after: args.after ?? null,
      before: args.before ?? null,
      includePinned: filters.includePinned,
      maxScan: filters.maxScan,
      maxMatches: filters.maxMatches ?? null,
    },
    scannedCount,
    pageCount,
    matchedCount: matchedMessages.length,
    deletableRecentCount: recentMessages.length,
    needsSingleDeleteCount: oldMessages.length,
    estimatedBulkRequests: Math.ceil(Math.max(0, recentMessages.length - 1) / 100),
    estimatedSingleRequests: oldMessages.length,
    confirmCode,
    runCommand: `node scripts/purge-runner.mjs --channel-id ${channelId} --confirm ${confirmCode}`,
  };

  if (args.out) {
    await writeJson(String(args.out), result);
  }

  printJson(result);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
