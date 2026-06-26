import { asBoolean, asInteger, isOlderThanTwoWeeks, parseDateToTs } from './common.mjs';
import { fetchMessagesPage } from './discord-api.mjs';

export function normalizeFilters(args) {
  const contains = args.contains ? String(args.contains) : undefined;
  const regexPattern = args.regex ? String(args.regex) : undefined;
  const regexFlags = args.regexFlags ? String(args.regexFlags) : 'i';
  const afterTs = parseDateToTs(args.after, undefined);
  const beforeTs = parseDateToTs(args.before, undefined);

  let regex;
  if (regexPattern) {
    regex = new RegExp(regexPattern, regexFlags);
  }

  return {
    authorId: args['author-id'] ? String(args['author-id']) : undefined,
    contains,
    regex,
    afterTs,
    beforeTs,
    includePinned: asBoolean(args['include-pinned'], false),
    maxScan: asInteger(args['max-scan'], 5000),
    maxMatches: asInteger(args['max-matches'], undefined),
  };
}

export function matchesFilter(message, filters) {
  if (!filters.includePinned && message.pinned) return false;

  if (filters.authorId && message.author?.id !== filters.authorId) return false;

  const content = message.content ?? '';
  if (filters.contains && !content.toLowerCase().includes(filters.contains.toLowerCase())) {
    return false;
  }

  if (filters.regex && !filters.regex.test(content)) {
    return false;
  }

  const messageTs = Date.parse(message.timestamp);
  if (filters.afterTs !== undefined && messageTs < filters.afterTs) return false;
  if (filters.beforeTs !== undefined && messageTs > filters.beforeTs) return false;

  return true;
}

export async function scanMessages({ token, channelId, filters, beforeCursor, onPage }) {
  const matchedMessages = [];
  let scannedCount = 0;
  let pageCount = 0;
  let cursor = beforeCursor;

  while (true) {
    const remaining = filters.maxScan === undefined ? 100 : filters.maxScan - scannedCount;
    if (remaining !== undefined && remaining <= 0) break;

    const pageLimit = Math.min(100, Math.max(1, remaining ?? 100));
    const page = await fetchMessagesPage({
      token,
      channelId,
      before: cursor,
      limit: pageLimit,
    });

    if (!Array.isArray(page) || page.length === 0) break;

    scannedCount += page.length;
    pageCount += 1;

    for (const message of page) {
      if (matchesFilter(message, filters)) {
        matchedMessages.push(message);
      }
    }

    cursor = page[page.length - 1].id;

    if (typeof onPage === 'function') {
      await onPage({
        pageCount,
        scannedCount,
        matchedCount: matchedMessages.length,
        cursor,
      });
    }

    if (filters.maxMatches !== undefined && matchedMessages.length >= filters.maxMatches) {
      break;
    }
  }

  return {
    scannedCount,
    pageCount,
    matchedMessages,
    cursor,
  };
}

export function splitMessagesByAge(messages, nowTs = Date.now()) {
  const recentMessages = [];
  const oldMessages = [];

  for (const message of messages) {
    if (isOlderThanTwoWeeks(message.timestamp, nowTs)) {
      oldMessages.push(message);
    } else {
      recentMessages.push(message);
    }
  }

  return { recentMessages, oldMessages };
}
