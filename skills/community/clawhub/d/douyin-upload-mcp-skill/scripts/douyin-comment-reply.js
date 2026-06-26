#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { createDouyinSession, disconnect } from '../src/index.js';
import { acquireBrowserTaskLock, shouldDeferToPublish } from './browser-task-lock.js';
import { generateReply, keyFor, loadState, rulesFallbackAllowed, saveState, withCommentReplyMeta } from './douyin-auto-reply.js';

const COMMENT_URL = 'https://creator.douyin.com/creator-micro/interactive/comment';
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const AUTO_REPLY_STATE_PATH = process.env.DOUYIN_AUTO_REPLY_STATE || join(STATE_DIR, 'auto-reply-state.json');

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sleepUntilNoPublish(ms, owner = 'comment:auto-reply') {
  const deadline = Date.now() + Math.max(0, Number(ms || 0));
  while (Date.now() < deadline) {
    if (shouldDeferToPublish(owner)) return false;
    await sleep(Math.min(1000, deadline - Date.now()));
  }
  return true;
}

function usage() {
  console.error(`Usage:
  node scripts/douyin-comment-reply.js list [--latest] [--all-works] [--unreplied]
  node scripts/douyin-comment-reply.js reply --text "感谢支持" [--index 0] [--latest] [--work-index 1] [--work-title "标题"] [--unreplied] [--execute]
  node scripts/douyin-comment-reply.js reply-unreplied-by-filter [--execute] [--max-works 20] [--limit 50]

Default reply mode is dry-run; add --execute to send one reply to the first visible comment.
Use --author-reply-check to expand visible reply threads and mark comments already replied by the author.
Use --pages 3 to scroll and collect more newest-first visible comments.
Use --all-works --max-works 20 to scan comments across visible works; this is read-only for list.
reply-unreplied-by-filter uses Douyin's "未回复" dropdown per work: reply first visible pending comment, refresh, repeat, then move to next work.
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function trustLocalReplyState(args = {}) {
  return Boolean(args.trustLocalState)
    || process.env.DOUYIN_COMMENT_TRUST_LOCAL_STATE === 'true';
}

function normalize(text = '') {
  return String(text || '').replace(/\s+/g, ' ').trim();
}

function stripMeta(text) {
  return normalize(text)
    .replace(/陌生人消息|白日梦想家|作者|粉丝|昨天|今天|刚刚|删除|举报|回复|查看\d+条回复|收起|发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/g, ' ')
    .replace(/\d+\s*(分钟前|小时前|天前)|\d{1,2}:\d{2}|\d{2}月\d{2}日|C:/g, ' ')
    .replace(/\b\d+\b/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function fingerprintText(text) {
  return stripMeta(text).replace(/[，。！？!?、:：,.()[\]（）【】\s]+/g, ' ').trim().slice(0, 200);
}

function commentFingerprint(row, text) {
  const author = fingerprintText(row?.authorName || '');
  const body = fingerprintText(text || row?.commentText || row?.sample || '');
  return [author, body].filter(Boolean).join('|') || body;
}

function commentApproxAtMs(row = {}) {
  if (row.commentApproxAt) {
    const fixed = Date.parse(row.commentApproxAt);
    if (Number.isFinite(fixed)) return fixed;
  }
  const raw = normalize(row.commentTime || '');
  const now = Date.now();
  if (!raw) return null;
  if (/刚刚/.test(raw)) return now;
  let match = raw.match(/(\d+)\s*分钟前/);
  if (match) return now - Number(match[1]) * 60 * 1000;
  match = raw.match(/(\d+)\s*小时前/);
  if (match) return now - Number(match[1]) * 60 * 60 * 1000;
  match = raw.match(/(\d+)\s*天前/);
  if (match) return now - Number(match[1]) * 24 * 60 * 60 * 1000;
  match = raw.match(/^(\d{1,2}):(\d{2})$/);
  if (match) {
    const date = new Date();
    date.setHours(Number(match[1]), Number(match[2]), 0, 0);
    if (date.getTime() > now + 10 * 60 * 1000) date.setDate(date.getDate() - 1);
    return date.getTime();
  }
  match = raw.match(/(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2})?/);
  if (match) {
    const date = new Date();
    date.setMonth(Number(match[1]) - 1, Number(match[2]));
    date.setHours(Number(match[3] || 0), Number(match[4] || 0), 0, 0);
    if (date.getTime() > now + 24 * 60 * 60 * 1000) date.setFullYear(date.getFullYear() - 1);
    return date.getTime();
  }
  return null;
}

function replyIsRecent(value, fallbackHours = 168) {
  const at = Date.parse(value?.at || '');
  if (!Number.isFinite(at)) return false;
  const hours = Math.max(1, Number(process.env.DOUYIN_COMMENT_LOCAL_REPLY_TTL_HOURS || fallbackHours));
  return Date.now() - at <= hours * 60 * 60 * 1000;
}

function loadAutoReplyState() {
  try {
    if (!existsSync(AUTO_REPLY_STATE_PATH)) return { replied: {} };
    return { replied: {}, ...JSON.parse(readFileSync(AUTO_REPLY_STATE_PATH, 'utf8')) };
  } catch {
    return { replied: {} };
  }
}

function recordCommentReply(state, row, reply, verification = null) {
  const sourceText = row?.commentText || row?.sample || '';
  const key = keyFor('comment', 0, sourceText, row);
  state.replied ||= {};
  state.replied[key] = {
    at: new Date().toISOString(),
    reply,
    sourceText,
    row: withCommentReplyMeta(row),
    verified: Boolean(verification?.ok || verification?.found),
    targetVerification: verification || null,
  };
}

function selectVisibleUnrepliedCandidates(comments, args = {}, state = loadAutoReplyState()) {
  const skipReplyThread = process.env.DOUYIN_COMMENT_SKIP_REPLY_THREAD_IN_FILTER !== 'false';
  const trustLocalState = trustLocalReplyState(args);
  const rows = [];
  const stats = {
    visibleCount: comments.length,
    skippedOwn: 0,
    skippedAuthorReply: 0,
    skippedReplyThread: 0,
    skippedLocalReply: 0,
  };
  for (let visibleIndex = 0; visibleIndex < comments.length; visibleIndex += 1) {
    const comment = comments[visibleIndex];
    const localReply = trustLocalState ? localReplyForComment(comment, state) : null;
    if (!args.force && comment.isOwn) {
      stats.skippedOwn += 1;
      continue;
    }
    if (!args.force && comment.hasAuthorReply) {
      stats.skippedAuthorReply += 1;
      continue;
    }
    if (!args.force && trustLocalState && localReply) {
      stats.skippedLocalReply += 1;
      continue;
    }
    if (!args.force && skipReplyThread && comment.hasReplyThread) {
      stats.skippedReplyThread += 1;
      continue;
    }
    rows.push({
      ...comment,
      visibleIndex,
      localReply: localReply ? {
        at: localReply.at,
        reply: localReply.reply,
        sourceText: localReply.sourceText,
      } : null,
    });
  }
  return { comments: rows, stats };
}

function relatedBody(a, b) {
  const left = fingerprintText(a);
  const right = fingerprintText(b);
  if (!left || !right) return false;
  return left === right
    || (left.length >= 4 && right.includes(left))
    || (right.length >= 4 && left.includes(right));
}

function localReplyForComment(comment, state) {
  const normalized = commentFingerprint(comment, comment.commentText || comment.sample || '');
  const currentAuthor = fingerprintText(comment.authorName || '');
  const currentBody = fingerprintText(comment.commentText || comment.sample || '');
  const currentApprox = commentApproxAtMs(comment);
  for (const [key, value] of Object.entries(state?.replied || {})) {
    if (!key.startsWith('comment:')) continue;
    const row = value?.row || {};
    const sourceText = value?.sourceText || row.commentText || '';
    const previousNormalized = commentFingerprint(row, sourceText);
    const previousAuthor = fingerprintText(row.authorName || '');
    const previousBody = fingerprintText(sourceText || row.commentText || '');
    const authorMatches = !currentAuthor || !previousAuthor || currentAuthor === previousAuthor;
    const bodyMatches = previousNormalized === normalized
      || key.includes(`:${normalized}`)
      || (authorMatches && relatedBody(currentBody, previousBody));
    if (!bodyMatches) continue;
    const previousApprox = commentApproxAtMs(row);
    const previousReplyAt = Date.parse(value?.at || '');
    if (Number.isFinite(currentApprox) && Number.isFinite(previousApprox)) {
      if (Math.abs(currentApprox - previousApprox) <= 2 * 60 * 60 * 1000) return value;
      continue;
    }
    if (Number.isFinite(currentApprox) && Number.isFinite(previousReplyAt)) {
      if (currentApprox <= previousReplyAt + 10 * 60 * 1000) return value;
      continue;
    }
    if (replyIsRecent(value)) return value;
  }
  return null;
}

function annotateAndFilterComments(comments, args = {}, state = loadAutoReplyState()) {
  let filteredByLocalReply = 0;
  let filteredByAuthorReply = 0;
  let filteredOwn = 0;
  const trustLocalState = trustLocalReplyState(args);
  const annotated = (comments || []).map((comment) => {
    const localReply = trustLocalState ? localReplyForComment(comment, state) : null;
    return {
      ...comment,
      locallyReplied: Boolean(localReply),
      localReply: localReply ? {
        at: localReply.at,
        reply: localReply.reply,
        sourceText: localReply.sourceText,
      } : null,
    };
  });
  if (!args.unreplied || args.force) {
    return { comments: annotated, filteredByLocalReply, filteredByAuthorReply, filteredOwn, unfilteredCount: annotated.length };
  }
  const commentsOut = annotated.filter((comment) => {
    if (comment.isOwn) {
      filteredOwn += 1;
      return false;
    }
    if (comment.hasAuthorReply) {
      filteredByAuthorReply += 1;
      return false;
    }
    if (trustLocalState && comment.locallyReplied) {
      filteredByLocalReply += 1;
      return false;
    }
    return true;
  });
  return { comments: commentsOut, filteredByLocalReply, filteredByAuthorReply, filteredOwn, unfilteredCount: annotated.length };
}

async function gotoComments(page) {
  await page.goto(COMMENT_URL, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
  await waitForUsefulBody(page, 10_000);
}

async function ensureCommentsPageReady(page) {
  for (let i = 0; i < 2; i += 1) {
    const ready = await page.evaluate(() => {
      const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
      return { ok: /评论管理/.test(text) && /选择作品/.test(text), sample: text.slice(0, 1000) };
    }).catch((err) => ({ ok: false, error: err.message }));
    if (ready.ok) return { ok: true, ready };
    await gotoComments(page);
    await closeKnownOverlays(page);
    await sleep(1500);
  }
  const last = await page.evaluate(() => {
    const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
    return { ok: /评论管理/.test(text) && /选择作品/.test(text), sample: text.slice(0, 1000), url: location.href };
  }).catch((err) => ({ ok: false, error: err.message }));
  return { ok: Boolean(last.ok), ready: last };
}

async function waitForUsefulBody(page, timeout = 10_000) {
  const deadline = Date.now() + timeout;
  let last = null;
  while (Date.now() < deadline) {
    last = await page.evaluate(() => {
      const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
      return { length: text.length, hasCommentUi: /评论管理|选择作品|全部评论|未回复/.test(text), sample: text.slice(0, 500) };
    }).catch((err) => ({ error: err.message }));
    if (last?.hasCommentUi && last.length > 20) return { ok: true, last };
    await sleep(500);
  }
  return { ok: false, last };
}

function installCommentCardHelpersSource() {
  return `
    const compact = (text = '') => text.replace(/\\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const blockedCardText = /高清发布|首页|活动管理|内容管理|作品管理|评论管理 选择作品|没有更多评论/;
    const looksCommentCard = (itemText, rect) => {
      const replyCount = (itemText.match(/回复/g) || []).length;
      const deleteCount = (itemText.match(/删除/g) || []).length;
      return replyCount >= 1
        && deleteCount >= 1
        && /举报/.test(itemText)
        && !blockedCardText.test(itemText)
        && rect.width > 300
        && rect.height >= 40;
    };
    window.__douyinCommentHelpers = {
      compact,
      visible,
      getCommentCards: () => {
      const roughCards = [...document.querySelectorAll('[class*="container-"], div, li, section, article')]
        .filter(visible)
        .map((el) => {
          const rect = el.getBoundingClientRect();
          const itemText = compact(el.innerText || el.textContent || '');
          return { el, itemText, text: itemText, rect, area: rect.width * rect.height, className: String(el.className || '') };
        })
        .filter(({ itemText, rect }) => looksCommentCard(itemText, rect));
      const leafCards = roughCards
        .filter((candidate) => !roughCards.some((other) => (
          other.el !== candidate.el
          && candidate.el.contains(other.el)
          && looksCommentCard(other.itemText, other.rect)
          && other.area < candidate.area
        )));
      const sourceCards = leafCards.length ? leafCards : roughCards;
      const minX = sourceCards.length ? Math.min(...sourceCards.map((item) => item.rect.x)) : 0;
      const rawCards = sourceCards
        .filter((item) => item.rect.x <= minX + 16)
        .sort((a, b) => (a.rect.top - b.rect.top) || (a.area - b.area));
      const cards = [];
      for (const item of rawCards) {
        if (cards.some((seen) => Math.abs(seen.rect.top - item.rect.top) < 12 || item.text.includes(seen.text) || seen.text.includes(item.text))) continue;
        cards.push(item);
      }
      return cards;
      },
    };
  `;
}

async function waitForCommentListSettled(page, timeout = 12_000) {
  const deadline = Date.now() + timeout;
  let last = null;
  while (Date.now() < deadline) {
    last = await page.evaluate(() => {
      const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
      const visible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const body = compact(document.body?.innerText || '');
      const cards = [...document.querySelectorAll('[class*="container-"], li, section, article, div')]
        .filter(visible)
        .map((el) => {
          const text = compact(el.innerText || el.textContent || '');
          const rect = el.getBoundingClientRect();
          return { text, rect };
        })
        .filter(({ text, rect }) => (
          (text.match(/回复/g) || []).length >= 1
          && (text.match(/删除/g) || []).length >= 1
          && /举报/.test(text)
          && !/高清发布|首页|活动管理|内容管理|作品管理|评论管理 选择作品|没有更多评论/.test(text)
          && rect.width > 300
          && rect.height >= 40
        ));
      return {
        ready: cards.length > 0 || /暂无评论|没有更多评论|还没有评论/.test(body),
        cardCount: cards.length,
        sample: body.slice(-600),
      };
    }).catch((err) => ({ ready: false, error: err.message }));
    if (last?.ready) return { ok: true, last };
    await sleep(500);
  }
  return { ok: false, last };
}

async function clickSmallestExactText(page, text) {
  const target = await page.evaluate((wanted) => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const candidates = [...document.querySelectorAll('button, [role="button"], [role="option"], div, span')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          el,
          text: compact(el.innerText || el.textContent || ''),
          rect,
          area: rect.width * rect.height,
        };
      })
      .filter((item) => item.text === wanted)
      .sort((a, b) => (a.area - b.area) || (a.rect.y - b.rect.y) || (a.rect.x - b.rect.x));
    const item = candidates[0];
    if (!item) return { ok: false, error: 'text_target_not_found', text: wanted, count: 0 };
    item.el.click();
    return {
      ok: true,
      text: wanted,
      count: candidates.length,
      rect: {
        x: Math.round(item.rect.x),
        y: Math.round(item.rect.y),
        width: Math.round(item.rect.width),
        height: Math.round(item.rect.height),
      },
    };
  }, text);
  await sleep(1000);
  return target;
}

async function openWorkSelector(page) {
  await ensureCommentsPageReady(page);
  await page.evaluate(() => {
    const scroller = document.scrollingElement || document.documentElement || document.body;
    scroller.scrollTo({ top: 0, behavior: 'instant' });
  }).catch(() => {});
  await sleep(300);
  const opened = await clickSmallestExactText(page, '选择作品');
  if (!opened.ok) return opened;
  const deadline = Date.now() + 8000;
  let last = null;
  while (Date.now() < deadline) {
    last = await page.evaluate(() => {
      const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
      const visible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const works = [...document.querySelectorAll('.douyin-creator-interactive-sidesheet [class*="container-"], [role="dialog"] [class*="container-"]')]
        .filter(visible)
        .map((el) => compact(el.innerText || el.textContent || ''))
        .filter((text) => /发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/.test(text));
      return { ok: works.length > 0, visibleWorks: works.length, sample: works.slice(0, 3) };
    }).catch((err) => ({ ok: false, error: err.message }));
    if (last.ok) return { ...opened, selectorReady: last };
    await sleep(500);
  }
  return { ...opened, ok: false, error: 'work_selector_not_ready', selectorReady: last };
}

async function listSelectableWorks(page, maxWorks = 20) {
  const opened = await openWorkSelector(page);
  if (!opened.ok) return { ok: false, opened, works: [] };
  const works = await page.evaluate((max) => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const nodes = [...document.querySelectorAll('.douyin-creator-interactive-sidesheet [class*="container-"], [role="dialog"] [class*="container-"]')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = compact(el.innerText || el.textContent || '');
        const commentCountMatch = text.match(/(\d+)\s*$/);
        return {
          text,
          rect,
          el,
          commentCount: commentCountMatch ? Number(commentCountMatch[1]) : null,
        };
      })
      .filter((item) => /发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/.test(item.text))
      .sort((a, b) => (a.rect.y - b.rect.y) || (a.rect.x - b.rect.x))
      .slice(0, Number(max) || 20)
      .map((item, index) => ({
        index,
        title: item.text.replace(/\s*发布于.*$/, '').trim(),
        workText: item.text.slice(0, 300),
        commentCount: item.commentCount,
        rect: {
          x: Math.round(item.rect.x),
          y: Math.round(item.rect.y),
          width: Math.round(item.rect.width),
          height: Math.round(item.rect.height),
        },
      }));
    return nodes;
  }, maxWorks);
  return { ok: true, opened, works };
}

async function selectWorkByIndex(page, index = 0) {
  const selected = await page.evaluate((wantedIndex) => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const works = [...document.querySelectorAll('.douyin-creator-interactive-sidesheet [class*="container-"], [role="dialog"] [class*="container-"]')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = compact(el.innerText || el.textContent || '');
        const countMatch = text.match(/(\d+)\s*$/);
        return { el, text, rect, commentCount: countMatch ? Number(countMatch[1]) : null };
      })
      .filter((item) => /发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/.test(item.text))
      .sort((a, b) => (a.rect.y - b.rect.y) || (a.rect.x - b.rect.x));
    const item = works[Number(wantedIndex) || 0];
    if (!item) return { ok: false, error: 'work_not_found', index: wantedIndex, visibleWorks: works.length };
    item.el.click();
    return {
      ok: true,
      workIndex: Number(wantedIndex) || 0,
      workTitle: item.text.replace(/\s*发布于.*$/, '').trim(),
      workText: item.text.slice(0, 300),
      workCommentCount: item.commentCount,
      visibleWorks: works.length,
    };
  }, index);
  await sleep(2500);
  await waitForUsefulBody(page, 8000);
  return selected;
}

async function selectWorkByText(page, workText = '') {
  const selected = await page.evaluate((targetText) => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const needle = compact(targetText).slice(0, 40);
    const works = [...document.querySelectorAll('.douyin-creator-interactive-sidesheet [class*="container-"], [role="dialog"] [class*="container-"]')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = compact(el.innerText || el.textContent || '');
        const countMatch = text.match(/(\d+)\s*$/);
        return { el, text, rect, commentCount: countMatch ? Number(countMatch[1]) : null };
      })
      .filter((item) => /发布于\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}/.test(item.text))
      .sort((a, b) => (a.rect.y - b.rect.y) || (a.rect.x - b.rect.x));
    const item = works.find((candidate) => candidate.text.includes(needle)) || works[0];
    if (!item) return { ok: false, error: 'work_not_found_by_text', targetText, visibleWorks: works.length };
    item.el.click();
    return {
      ok: true,
      workTitle: item.text.replace(/\s*发布于.*$/, '').trim(),
      workText: item.text.slice(0, 300),
      workCommentCount: item.commentCount,
      visibleWorks: works.length,
    };
  }, workText);
  await sleep(1800);
  await waitForUsefulBody(page, 6000);
  return selected;
}

async function selectLatestWork(page) {
  const opened = await openWorkSelector(page);
  if (!opened.ok) return opened;
  const selected = await selectWorkByIndex(page, 0);
  return { ...selected, opened };
}

async function selectCommentFilter(page, filterText = '未回复') {
  const opened = await page.evaluate(() => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const candidates = [...document.querySelectorAll('[role="combobox"], button, div, span')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return { el, text: compact(el.innerText || el.textContent || ''), rect, area: rect.width * rect.height };
      })
      .filter((item) => /^(全部评论|未回复|包含问题|可能打扰)$/.test(item.text) && item.rect.x > 220 && item.rect.y > 450)
      .sort((a, b) => (a.rect.x - b.rect.x) || (a.area - b.area));
    const firstFilter = candidates[0];
    if (!firstFilter) return { ok: false, error: 'comment_filter_dropdown_not_found' };
    firstFilter.el.click();
    return {
      ok: true,
      currentText: firstFilter.text,
      rect: {
        x: Math.round(firstFilter.rect.x),
        y: Math.round(firstFilter.rect.y),
        width: Math.round(firstFilter.rect.width),
        height: Math.round(firstFilter.rect.height),
      },
    };
  });
  if (!opened.ok) return opened;
  await sleep(700);
  const selected = await clickSmallestExactText(page, filterText);
  await sleep(1500);
  await waitForUsefulBody(page, 8000);
  return { ...selected, opened, filterText };
}

async function refreshCurrentCommentPage(page) {
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
  await waitForUsefulBody(page, 10_000);
  await closeKnownOverlays(page);
}

async function refreshUnrepliedFilterByDropdown(page) {
  const all = await selectCommentFilter(page, '全部评论');
  if (!all.ok) return { ok: false, step: 'select_all_comments', all };
  await waitForUsefulBody(page, 5000);
  const unreplied = await selectCommentFilter(page, '未回复');
  if (!unreplied.ok) return { ok: false, step: 'select_unreplied', all, unreplied };
  const settled = await waitForCommentListSettled(page, 8000);
  const empty = await currentCommentEmptyState(page);
  return { ok: true, all, unreplied, settled, empty };
}

async function currentCommentEmptyState(page) {
  return page.evaluate(() => {
    const compact = (value = '') => String(value).replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
    const hasCommentCard = [...document.querySelectorAll('[class*="container-"], div, li, section, article')]
      .filter(visible)
      .some((el) => {
        const rect = el.getBoundingClientRect();
        const itemText = compact(el.innerText || el.textContent || '');
        return (itemText.match(/回复/g) || []).length >= 1
          && (itemText.match(/删除/g) || []).length >= 1
          && /举报/.test(itemText)
          && !/高清发布|首页|活动管理|内容管理|作品管理|评论管理 选择作品/.test(itemText)
          && rect.width > 300
          && rect.height >= 40;
      });
    return {
      empty: !hasCommentCard && /暂无符合条件的评论|换个条件试试吧|暂无评论|还没有评论/.test(text),
      hasCommentCard,
      sample: text.slice(-1000),
    };
  }).catch((err) => ({ empty: false, error: err.message }));
}

async function selectWorkAndUnrepliedFilter(page, workIndex) {
  const workSelector = await openWorkSelector(page);
  if (!workSelector.ok) return { ok: false, error: 'work_selector_failed', workSelector };
  const work = await selectWorkByIndex(page, workIndex);
  if (!work.ok) return { ok: false, error: 'work_select_failed', workSelector, work };
  const filter = await selectCommentFilter(page, '未回复');
  if (!filter.ok) {
    const empty = await currentCommentEmptyState(page);
    return { ok: false, error: 'unreplied_filter_not_available', workSelector, work, filter, empty };
  }
  const settled = await waitForCommentListSettled(page, 8000);
  const empty = await currentCommentEmptyState(page);
  return { ok: true, workSelector, work, filter, settled, empty };
}

async function replyFirstVisibleFilteredComment(page, replyText, execute = false, visibleIndex = 0) {
  const listed = await listCommentsAcrossPages(page, { pages: 1 });
  const first = listed.comments?.[visibleIndex] || null;
  if (!first) {
    const empty = await currentCommentEmptyState(page);
    return { ok: true, action: 'no_visible_unreplied_comment', sent: false, listed, empty };
  }
  const opened = await openCommentReply(page, visibleIndex);
  const fill = opened.ok ? await fillOpenedReply(page, replyText, opened) : opened;
  if (!fill.ok) {
    const clear = fill.ok ? await clearReplyDraft(page) : null;
    return { ok: false, action: 'reply_prepare_failed', target: first, opened, fill, clear };
  }
  if (!execute) {
    const clear = await clearReplyDraft(page);
    return { ok: true, mode: 'dry-run', action: 'would_reply_first_unreplied', sent: false, target: first, reply: replyText, opened, fill, clear };
  }
  if (fill.sendDisabled) {
    return { ok: false, action: 'send_button_disabled', target: first, opened, fill };
  }
  if (shouldDeferToPublish('comment:reply-unreplied-by-filter')) {
    const clear = await clearReplyDraft(page).catch(() => null);
    return { ok: true, action: 'deferred_to_publish', sent: false, skipped: true, target: first, opened, fill, clear };
  }
  await page.mouse.click(fill.x, fill.y);
  await sleep(3000);
  const verification = await verifyReplyVisible(page, replyText, opened);
  return {
    ok: verification.ok,
    mode: 'execute',
    action: verification.ok ? 'comment_reply_sent_verified' : 'comment_reply_clicked_unverified',
    sent: verification.ok,
    target: first,
    reply: replyText,
    opened,
    fill,
    verification,
  };
}

async function replyUnrepliedByFilter(page, args) {
  const maxWorks = Math.max(1, Math.min(50, Number(args.maxWorks || args.works || 20)));
  const limit = Math.max(1, Math.min(200, Number(args.limit || 50)));
  const execute = Boolean(args.execute);
  const afterReplyWaitMs = Math.max(0, Math.min(180_000, Number(args.afterReplyWaitMs || process.env.DOUYIN_COMMENT_AFTER_REPLY_WAIT_MS || 60_000)));
  const afterFailedReplyWaitMs = Math.max(0, Math.min(60_000, Number(args.afterFailedReplyWaitMs || process.env.DOUYIN_COMMENT_AFTER_FAILED_REPLY_WAIT_MS || 5000)));
  const maxFailedAttemptsPerWork = Math.max(1, Math.min(10, Number(args.maxFailedAttemptsPerWork || process.env.DOUYIN_COMMENT_MAX_FAILED_ATTEMPTS_PER_WORK || 3)));
  const listedWorks = await listSelectableWorks(page, maxWorks);
  if (!listedWorks.ok) return { ok: false, error: 'work_list_failed', listedWorks };
  const works = listedWorks.works.slice(0, maxWorks);
  const results = [];
  let sentCount = 0;
  for (const work of works) {
    if (shouldDeferToPublish('comment:reply-unreplied-by-filter')) {
      results.push({
        index: work.index,
        title: work.title,
        pageCommentCount: work.commentCount,
        skipped: true,
        stopBoundary: true,
        reason: 'deferred_to_publish',
      });
      break;
    }
    const workResult = {
      index: work.index,
      title: work.title,
      pageCommentCount: work.commentCount,
      skipped: false,
      sentCount: 0,
      failedCount: 0,
      attempts: [],
    };
    if (Number(work.commentCount || 0) <= 0) {
      workResult.skipped = true;
      workResult.reason = 'no_comments_on_work_card';
      results.push(workResult);
      continue;
    }
    for (let round = 0; round < limit && sentCount < limit; round += 1) {
      if (shouldDeferToPublish('comment:reply-unreplied-by-filter')) {
        workResult.skipped = true;
        workResult.stopBoundary = true;
        workResult.reason = 'deferred_to_publish';
        break;
      }
      const prepared = await selectWorkAndUnrepliedFilter(page, work.index);
      workResult.lastPrepare = prepared;
      if (!prepared.ok) {
        workResult.skipped = true;
        workResult.reason = prepared.error;
        if (prepared.error === 'unreplied_filter_not_available') {
          workResult.stopBoundary = true;
          results.push(workResult);
          break;
        }
        break;
      }
      if (prepared.empty?.empty) {
        workResult.reason = 'no_unreplied_comments';
        break;
      }
      const listed = await listCommentsAcrossPages(page, { pages: 1 });
      const selectable = selectVisibleUnrepliedCandidates(listed.comments || [], args);
      workResult.lastSelectableStats = selectable.stats;
      const visibleTargets = selectable.comments || [];
      const target = visibleTargets[0] || null;
      if (!target) {
        const empty = await currentCommentEmptyState(page);
        workResult.reason = empty.empty || selectable.stats.visibleCount > 0
          ? 'no_unreplied_comments'
          : 'no_visible_comment_after_filter';
        workResult.empty = empty;
        break;
      }
      if (!execute) {
        for (let targetIndex = 0; targetIndex < visibleTargets.length && workResult.attempts.length < limit; targetIndex += 1) {
          const dryTarget = visibleTargets[targetIndex];
          const dryReplyResult = args.text
            ? { text: args.text, source: 'manual' }
            : await generateReply('comment', dryTarget.commentText || dryTarget.sample || '', {
              row: dryTarget,
              workTitle: prepared.work?.workTitle || work.title || '',
            }, args);
          workResult.attempts.push({
            round: targetIndex + 1,
            ok: dryReplyResult.source === 'llm' || Boolean(args.text) || rulesFallbackAllowed(args),
            sent: false,
            action: dryReplyResult.source === 'llm' || Boolean(args.text) || rulesFallbackAllowed(args)
              ? 'would_reply_visible_unreplied'
              : 'skip_without_llm_reply',
            target: {
              authorName: dryTarget.authorName,
              commentTime: dryTarget.commentTime,
              commentText: dryTarget.commentText,
            },
            reply: dryReplyResult.source === 'llm' || Boolean(args.text) || rulesFallbackAllowed(args)
              ? dryReplyResult.text
              : undefined,
            replySource: dryReplyResult.source,
            replyModel: dryReplyResult.model,
            llmFallback: dryReplyResult.llmFallback,
            llmAttempts: dryReplyResult.llmAttempts,
            error: dryReplyResult.source !== 'llm' && !args.text && !rulesFallbackAllowed(args)
              ? 'llm_reply_generation_failed'
              : undefined,
          });
        }
        workResult.reason = 'dry_run_visible_unreplied_preview';
        workResult.previewedVisibleCount = visibleTargets.length;
        break;
      }
      const replyResult = args.text
        ? { text: args.text, source: 'manual' }
        : await generateReply('comment', target.commentText || target.sample || '', {
          row: target,
          workTitle: prepared.work?.workTitle || work.title || '',
        }, args);
      if (!args.text && replyResult.source !== 'llm' && !rulesFallbackAllowed(args)) {
        workResult.attempts.push({
          round: round + 1,
          ok: false,
          sent: false,
          action: 'skip_without_llm_reply',
          target: {
            authorName: target.authorName,
            commentTime: target.commentTime,
            commentText: target.commentText,
          },
          replySource: replyResult.source,
          llmFallback: replyResult.llmFallback,
          llmAttempts: replyResult.llmAttempts,
          error: 'llm_reply_generation_failed',
        });
        workResult.reason = 'llm_reply_generation_failed';
        break;
      }
      const replyText = replyResult.text;
      const reply = await replyFirstVisibleFilteredComment(page, replyText, execute, target.visibleIndex || 0);
      if (execute && reply.sent) {
        const state = loadState();
        recordCommentReply(state, reply.target || target, replyText, reply.verification);
        saveState(state);
      }
      workResult.attempts.push({
        round: round + 1,
        ok: reply.ok,
        sent: reply.sent,
        action: reply.action,
        target: reply.target ? {
          authorName: reply.target.authorName,
          commentTime: reply.target.commentTime,
          commentText: reply.target.commentText,
        } : null,
        reply: reply.reply,
        replySource: replyResult.source,
        replyModel: replyResult.model,
        llmFallback: replyResult.llmFallback,
        llmAttempts: replyResult.llmAttempts,
        error: reply.error || reply.opened?.error || reply.fill?.error,
      });
      if (!reply.ok) {
        workResult.failedCount += 1;
        if (workResult.failedCount >= maxFailedAttemptsPerWork) {
          workResult.reason = 'reply_failed';
          break;
        }
        if (afterFailedReplyWaitMs > 0) {
          const waited = await sleepUntilNoPublish(afterFailedReplyWaitMs, 'comment:reply-unreplied-by-filter');
          if (!waited) {
            workResult.stopBoundary = true;
            workResult.reason = 'deferred_to_publish_after_reply_failure';
            break;
          }
        }
        const retryRefresh = await refreshUnrepliedFilterByDropdown(page);
        workResult.lastFilterRefresh = retryRefresh;
        if (!retryRefresh.ok) {
          workResult.reason = 'filter_refresh_failed_after_reply';
          break;
        }
        continue;
      }
      if (!execute) {
        workResult.reason = 'dry_run_one_attempt_only';
        break;
      }
      if (reply.sent) {
        sentCount += 1;
        workResult.sentCount += 1;
      }
      if (reply.sent && afterReplyWaitMs > 0) {
        const waitStartedAt = new Date().toISOString();
        const waited = await sleepUntilNoPublish(afterReplyWaitMs, 'comment:reply-unreplied-by-filter');
        workResult.lastAfterReplyWait = {
          ok: waited,
          waitStartedAt,
          waitMs: afterReplyWaitMs,
          reason: waited ? 'wait_for_douyin_unreplied_filter_to_update' : 'interrupted_by_publish_priority',
        };
        if (!waited) {
          workResult.stopBoundary = true;
          workResult.reason = 'deferred_to_publish_after_reply';
          break;
        }
      }
      if (shouldDeferToPublish('comment:reply-unreplied-by-filter')) {
        workResult.stopBoundary = true;
        workResult.reason = 'deferred_to_publish_after_reply';
        break;
      }
      const refreshed = await refreshUnrepliedFilterByDropdown(page);
      workResult.lastFilterRefresh = refreshed;
      if (!refreshed.ok) {
        workResult.reason = 'filter_refresh_failed_after_reply';
        break;
      }
    }
    if (!results.includes(workResult)) results.push(workResult);
    if (workResult.stopBoundary) break;
    if (sentCount >= limit) break;
  }
  return {
    ok: results.every((item) => ![
      'reply_failed',
      'llm_reply_generation_failed',
      'filter_refresh_failed_after_reply',
    ].includes(item.reason)),
    mode: execute ? 'execute' : 'dry-run',
    worksAvailable: listedWorks.works.length,
    worksScanned: results.length,
    sentCount,
    results,
  };
}

async function prepareCommentView(page, args) {
  const steps = {};
  if (args.workTitle) {
    steps.workSelector = await openWorkSelector(page);
    steps.work = steps.workSelector.ok
      ? await selectWorkByText(page, args.workTitle)
      : steps.workSelector;
  } else if (args.workIndex !== undefined) {
    steps.workSelector = await openWorkSelector(page);
    steps.work = steps.workSelector.ok
      ? await selectWorkByIndex(page, Number(args.workIndex || 0))
      : steps.workSelector;
  } else if (args.latest) {
    steps.latest = await selectLatestWork(page);
  }
  if (args.unreplied) steps.filter = await selectCommentFilter(page, '未回复');
  if ((args.authorReplyCheck || args.stopAtReplied) || (args.unreplied && !steps.filter?.ok)) {
    steps.beforeAuthorReplyFallback = await waitForCommentListSettled(page, 8000);
    steps.authorReplyFallback = await expandVisibleReplyThreads(page, 10);
  }
  return steps;
}

async function closeKnownOverlays(page) {
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    let clicked = 0;
    for (const el of [...document.querySelectorAll('button, div, span')]) {
      const text = compact(el.innerText || el.textContent || '');
      if (visible(el) && /^(我知道了|知道了|关闭)$/.test(text)) {
        el.click();
        clicked += 1;
      }
    }
    return { ok: true, clicked };
  }).catch((err) => ({ ok: false, error: err.message }));
}

async function listComments(page, args = {}) {
  return page.evaluate((debugEnabled) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const text = compact(document.body?.innerText || '');
    const candidateNodes = [...document.querySelectorAll('[class*="container-"], li, section, article, div')];
    const blockedCardText = /高清发布|首页|活动管理|内容管理|作品管理|评论管理 选择作品|没有更多评论/;
    const looksCommentCard = (itemText, rect) => {
      const replyCount = (itemText.match(/回复/g) || []).length;
      const deleteCount = (itemText.match(/删除/g) || []).length;
      return replyCount >= 1
        && deleteCount >= 1
        && /举报/.test(itemText)
        && !blockedCardText.test(itemText)
        && rect.width > 300
        && rect.height >= 40;
    };
    const roughCards = candidateNodes
      .filter(visible)
      .map((el) => {
        const itemText = compact(el.innerText || '');
        const rect = el.getBoundingClientRect();
        return { el, itemText, rect, area: rect.width * rect.height, className: String(el.className || '') };
      })
      .filter(({ itemText, rect }) => looksCommentCard(itemText, rect));
    const leafCards = roughCards
      .filter((candidate) => !roughCards.some((other) => (
        other.el !== candidate.el
        && candidate.el.contains(other.el)
        && looksCommentCard(other.itemText, other.rect)
        && other.area < candidate.area
      )));
    const sourceCards = leafCards.length ? leafCards : roughCards;
    const minX = sourceCards.length ? Math.min(...sourceCards.map((item) => item.rect.x)) : 0;
    const rawCards = sourceCards
      .filter((item) => item.rect.x <= minX + 16)
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.area - b.area));

    const parseCard = ({ el, itemText, rect }) => {
      const descendants = [...el.querySelectorAll('div, span, button, a')]
        .filter(visible)
        .map((node) => ({
          text: compact(node.innerText || node.textContent || ''),
          className: String(node.className || ''),
          rect: node.getBoundingClientRect(),
        }));
      const findByClass = (pattern) => descendants.find((item) => pattern.test(item.className) && item.text);
      const usernameNode = findByClass(/username|user-name|name/i);
      const timeNode = findByClass(/time/i);
      const commentNode = findByClass(/comment-content|comment.*text|content-text/i);
      const operationNode = findByClass(/operation/i);
      const operationTop = operationNode?.rect?.top || (rect.top + rect.height * 0.62);
      const commentTop = commentNode?.rect?.top || operationTop;
      const exactAuthorBadges = descendants.filter((item) => (
        item.text === '作者'
        && !/comment-content|comment.*text|content-text/i.test(item.className)
      ));
      const hasMainAuthorBadge = exactAuthorBadges.some((item) => item.rect.top < commentTop + 4);
      const hasReplyAuthorBadge = exactAuthorBadges.some((item) => item.rect.top > operationTop + 2);
      const replyIndex = itemText.indexOf('回复');
      const beforeReply = replyIndex >= 0 ? itemText.slice(0, replyIndex).trim() : itemText;
      const cleaned = beforeReply.replace(/^(最新发布\s*)?/, '').trim();
      const timeMatch = cleaned.match(/(?:刚刚|\d+\s*分钟前|\d+\s*小时前|\d+\s*天前|\d{1,2}:\d{2}|\d{2}月\d{2}日\s+\d{1,2}:\d{2})/);
      const authorName = usernameNode?.text || (timeMatch ? cleaned.slice(0, timeMatch.index).trim() : '');
      const afterTime = timeMatch ? cleaned.slice(timeMatch.index + timeMatch[0].length).trim() : cleaned;
      const commentText = commentNode?.text || afterTime.replace(/\s+\d+$/, '').trim() || cleaned;
      const firstReport = itemText.indexOf('举报');
      const replySection = firstReport >= 0 ? itemText.slice(firstReport + 2) : '';
      return {
        authorName: authorName.slice(0, 80),
        commentTime: timeNode?.text || timeMatch?.[0] || '',
        commentText: commentText.slice(0, 220),
        isOwn: hasMainAuthorBadge,
        hasReplyThread: /查看\s*\d+\s*条回复|收起/.test(itemText),
        hasAuthorReply: hasReplyAuthorBadge || /\s作者\s/.test(replySection),
      };
    };

    const comments = [];
    for (const { el, itemText, rect } of rawCards) {
      if (comments.some((item) => Math.abs(item.top - Math.round(rect.top + scrollY)) < 12 || item.sample.includes(itemText) || itemText.includes(item.sample))) continue;
      const parsed = parseCard({ el, itemText, rect });
      comments.push({
        top: Math.round(rect.top + scrollY),
        sample: itemText.slice(0, 500),
        ...parsed,
      });
      if (comments.length >= 20) break;
    }
    return {
      ok: true,
      url: location.href,
      pageText: text.slice(0, 1200),
      count: comments.length,
      filter: /未回复/.test(text) && !/全部评论/.test(text.slice(text.indexOf('评论管理'), text.indexOf('全部人群'))) ? '未回复' : undefined,
      comments,
      order: 'visible_top_to_bottom_latest_first',
      debug: debugEnabled ? {
        candidateCount: candidateNodes.length,
        roughCount: roughCards.length,
        leafCount: leafCards.length,
        rawCount: rawCards.length,
        roughSamples: roughCards.slice(0, 5).map((item) => ({
          text: item.itemText.slice(0, 200),
          className: item.className,
          x: Math.round(item.rect.x),
          y: Math.round(item.rect.y),
          width: Math.round(item.rect.width),
          height: Math.round(item.rect.height),
        })),
      } : undefined,
    };
  }, Boolean(args.debug));
}

function commentKey(comment) {
  return [
    String(comment.authorName || '').trim(),
    String(comment.commentText || '').trim(),
    String(comment.sample || '').slice(0, 120),
  ].join('|');
}

async function scrollCommentPage(page) {
  return page.evaluate(() => {
    const beforeY = window.scrollY;
    const beforeHeight = document.scrollingElement?.scrollHeight || document.body?.scrollHeight || 0;
    const scroller = document.scrollingElement || document.documentElement || document.body;
    scroller.scrollBy({ top: Math.max(520, Math.floor(window.innerHeight * 0.78)), behavior: 'instant' });
    return { ok: true, beforeY, afterY: window.scrollY, beforeHeight };
  }).catch((err) => ({ ok: false, error: err.message }));
}

async function listCommentsAcrossPages(page, args) {
  const pages = Math.max(1, Math.min(8, Number(args.pages || args.maxPages || 1)));
  const comments = [];
  const seen = new Set();
  const pageResults = [];
  for (let pageIndex = 0; pageIndex < pages; pageIndex += 1) {
    const settled = await waitForCommentListSettled(page, pageIndex === 0 ? 12_000 : 5_000);
    if (pageIndex > 0 && (args.authorReplyCheck || args.stopAtReplied || args.unreplied)) {
      await expandVisibleReplyThreads(page, 10);
    }
    const listed = await listComments(page, args);
    pageResults.push({
      pageIndex,
      ok: listed.ok,
      count: listed.count,
      url: listed.url,
      settled,
      debug: args.debug ? listed.debug : undefined,
    });
    for (const comment of listed.comments || []) {
      const key = commentKey(comment);
      if (seen.has(key)) continue;
      seen.add(key);
      comments.push(comment);
    }
    if (pageIndex >= pages - 1) break;
    const scroll = await scrollCommentPage(page);
    await sleep(1300);
    await waitForUsefulBody(page, 4000);
    const after = await page.evaluate(() => ({
      scrollY: window.scrollY,
      scrollHeight: document.scrollingElement?.scrollHeight || document.body?.scrollHeight || 0,
      text: (document.body?.innerText || '').replace(/\s+/g, ' ').slice(-200),
    })).catch((err) => ({ error: err.message }));
    pageResults[pageResults.length - 1].scroll = scroll;
    pageResults[pageResults.length - 1].after = after;
    if (scroll.ok && Math.abs((after.scrollY || 0) - (scroll.beforeY || 0)) < 8 && /没有更多评论/.test(after.text || '')) {
      break;
    }
  }
  const first = pageResults[0] || {};
  return {
    ok: true,
    url: first.url || page.url(),
    count: comments.length,
    comments,
    order: 'newest_first_visible_scroll_pages',
    pagesRequested: pages,
    pagesScanned: pageResults.length,
    pageResults,
  };
}

async function scanAllWorks(page, args, state) {
  const maxWorks = Math.max(1, Math.min(50, Number(args.maxWorks || args.works || 20)));
  const listedWorks = await listSelectableWorks(page, maxWorks);
  if (!listedWorks.ok) return { ok: false, error: 'work_list_failed', workList: listedWorks };
  const works = [];
  const allComments = [];
  const candidates = listedWorks.works
    .filter((work) => Number(work.commentCount || 0) > 0)
    .slice(0, maxWorks);
  for (let i = 0; i < candidates.length; i += 1) {
    const candidate = candidates[i];
    await openWorkSelector(page);
    const selected = await selectWorkByText(page, candidate.workText || candidate.title);
    if (!selected.ok) {
      works.push({ index: candidate.index, ok: false, selected, candidate });
      continue;
    }
    if ((args.authorReplyCheck || args.unreplied)) {
      await waitForCommentListSettled(page, 8000);
      await expandVisibleReplyThreads(page, 10);
    }
    const listed = await listCommentsAcrossPages(page, args);
    const annotated = annotateAndFilterComments(listed.comments, args, state);
    const work = {
      ok: true,
      index: candidate.index,
      title: selected.workTitle,
      workCommentCount: selected.workCommentCount,
      listedCount: listed.count,
      unfilteredCount: annotated.unfilteredCount,
      count: annotated.comments.length,
      filteredByLocalReply: annotated.filteredByLocalReply,
      filteredByAuthorReply: annotated.filteredByAuthorReply,
      filteredOwn: annotated.filteredOwn,
      comments: annotated.comments.map((comment, commentIndex) => ({
        ...comment,
        workIndex: candidate.index,
        workScanIndex: i,
        workCommentIndex: commentIndex,
        workTitle: selected.workTitle,
      })),
    };
    works.push(work);
    allComments.push(...work.comments);
  }
  return {
    ok: true,
    url: page.url(),
    mode: 'all_works',
    worksAvailable: listedWorks.works.length,
    worksWithComments: candidates.length,
    worksScanned: works.length,
    count: allComments.length,
    comments: allComments,
    works,
  };
}

function defaultReplyFor(commentText) {
  if (/多少钱|价格|怎么买|链接|购买|保险/.test(commentText)) {
    return '感谢关注，具体方案可以私信我了解。';
  }
  if (/真的假的|真假|真的吗/.test(commentText)) return '是真的，后面我继续把细节讲清楚。';
  if (/666|nb|牛|厉害|强|棒|好|不错|支持|喜欢|赞/i.test(commentText)) return '谢谢支持，后面继续更新。';
  if (/哈哈|hhh|笑死|有意思|好玩/.test(commentText)) return '哈哈，谢谢互动。';
  return '感谢你的评论。';
}

async function fillReply(page, replyText) {
  return page.evaluate((reply) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const input = [...document.querySelectorAll('[contenteditable="true"], textarea, div[class*="input"]')]
      .filter(visible)
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return br.width * br.height - ar.width * ar.height;
      })[0];
    if (!input) return { ok: false, error: 'reply_input_not_found' };
    input.focus();
    if ('value' in input) {
      input.value = reply;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      input.textContent = reply;
      input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: reply }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    const send = [...document.querySelectorAll('button, div, span')]
      .filter(visible)
      .filter((el) => compact(el.innerText || el.textContent || '') === '发送')
      .sort((a, b) => {
        const ad = /disabled/.test(a.className?.toString?.() || '') ? 1 : 0;
        const bd = /disabled/.test(b.className?.toString?.() || '') ? 1 : 0;
        if (ad !== bd) return ad - bd;
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return (ar.width * ar.height) - (br.width * br.height);
      })[0];
    if (!send) return { ok: false, error: 'send_button_not_found' };
    const rect = send.getBoundingClientRect();
    return {
      ok: true,
      reply,
      inputSelector: input.tagName,
      sendDisabled: /disabled/.test(send.className?.toString?.() || ''),
      x: rect.x + rect.width / 2,
      y: rect.y + rect.height / 2,
      sendText: compact(send.innerText || send.textContent || ''),
    };
  }, replyText);
}

async function openCommentReply(page, index = 0) {
  const target = await page.evaluate((wantedIndex) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const blockedCardText = /高清发布|首页|活动管理|内容管理|作品管理|评论管理 选择作品|没有更多评论/;
    const looksCommentCard = (text, rect) => {
      const replyCount = (text.match(/回复/g) || []).length;
      const deleteCount = (text.match(/删除/g) || []).length;
      return replyCount >= 1
        && deleteCount >= 1
        && /举报/.test(text)
        && !blockedCardText.test(text)
        && rect.width > 300
        && rect.height >= 40;
    };
    const roughCards = [...document.querySelectorAll('[class*="container-"], div, li, section, article')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return { el, text: compact(el.innerText || ''), rect, area: rect.width * rect.height, className: String(el.className || '') };
      })
      .filter(({ text, rect }) => looksCommentCard(text, rect));
    const leafCards = roughCards
      .filter((candidate) => !roughCards.some((other) => (
        other.el !== candidate.el
        && candidate.el.contains(other.el)
        && looksCommentCard(other.text, other.rect)
        && other.area < candidate.area
      )));
    const sourceCards = leafCards.length ? leafCards : roughCards;
    const minX = sourceCards.length ? Math.min(...sourceCards.map((item) => item.rect.x)) : 0;
    const rawCards = sourceCards
      .filter((item) => item.rect.x <= minX + 16)
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.area - b.area));
    const cards = [];
    for (const item of rawCards) {
      if (cards.some((seen) => Math.abs(seen.rect.top - item.rect.top) < 12 || item.text.includes(seen.text))) continue;
      cards.push(item);
    }
    const card = cards[Number(wantedIndex) || 0];
    if (!card) return { ok: false, error: 'comment_card_not_found' };
    card.el.scrollIntoView({ block: 'center', inline: 'nearest' });
    const buttons = [...card.el.querySelectorAll('button, div, span')]
      .filter(visible)
      .map((el) => ({ el, text: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect() }))
      .filter(({ text }) => text === '回复')
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.rect.left - b.rect.left));
    const replyButton = buttons[0];
    if (!replyButton) return { ok: false, error: 'reply_button_not_found', sample: card.text.slice(0, 500) };
    return {
      ok: true,
      sample: card.text.slice(0, 500),
      commentText: card.text.slice(0, card.text.indexOf('回复')).trim(),
      cardTop: Math.round(card.rect.top + window.scrollY),
      x: replyButton.rect.x + replyButton.rect.width / 2,
      y: replyButton.rect.y + replyButton.rect.height / 2,
    };
  }, index);
  if (!target.ok) return target;
  await page.mouse.click(target.x, target.y);
  await sleep(1200);
  return target;
}

async function fillOpenedReply(page, replyText, target = {}) {
  const inputTarget = await page.evaluate((targetTop) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const allInputs = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .map((el) => ({ el, rect: el.getBoundingClientRect(), text: compact(el.innerText || el.textContent || el.value || '') }))
      .map((item) => ({ ...item, absTop: item.rect.top + window.scrollY }))
      .filter(({ rect }) => rect.width >= 120 && rect.height >= 18);
    const scopedInputs = Number.isFinite(targetTop)
      ? allInputs.filter(({ absTop }) => absTop >= targetTop - 24 && absTop <= targetTop + 380)
      : [];
    const inputs = (scopedInputs.length ? scopedInputs : allInputs)
      .sort((a, b) => {
        if (Number.isFinite(targetTop)) return Math.abs(a.absTop - targetTop) - Math.abs(b.absTop - targetTop);
        return b.rect.y - a.rect.y;
      });
    const input = inputs[0]?.el;
    if (!input) return { ok: false, error: 'reply_input_not_found_after_click' };
    const inputRect = input.getBoundingClientRect();
    return {
      ok: true,
      inputSelector: input.tagName,
      inputY: Math.round(inputRect.y),
      inputAbsTop: Math.round(inputRect.top + window.scrollY),
      targetScoped: scopedInputs.length > 0,
      x: inputRect.x + Math.min(24, Math.max(8, inputRect.width / 2)),
      y: inputRect.y + inputRect.height / 2,
    };
  }, Number(target.cardTop));
  if (!inputTarget.ok) return inputTarget;
  if (!inputTarget.targetScoped) {
    return { ...inputTarget, ok: false, error: 'reply_input_not_scoped_to_target_comment' };
  }
  await page.mouse.click(inputTarget.x, inputTarget.y);
  await page.keyboard.down(process.platform === 'darwin' ? 'Meta' : 'Control');
  await page.keyboard.press('A');
  await page.keyboard.up(process.platform === 'darwin' ? 'Meta' : 'Control');
  await page.keyboard.type(replyText, { delay: 20 });
  await sleep(700);
  return page.evaluate(({ reply, inputY, inputAbsTop, targetScoped }) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const send = [...document.querySelectorAll('button, div, span')]
      .filter(visible)
      .map((el) => ({ el, text: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect() }))
      .filter(({ text, rect }) => text === '发送' && rect.y >= inputY - 80)
      .sort((a, b) => Math.abs(a.rect.y - inputY) - Math.abs(b.rect.y - inputY))[0];
    if (!send) return { ok: false, error: 'reply_send_button_not_found' };
    return {
      ok: true,
      reply,
      inputY,
      inputAbsTop,
      targetScoped,
      sendDisabled: /disabled/.test(send.el.className?.toString?.() || '') || send.el.getAttribute('aria-disabled') === 'true',
      x: send.rect.x + send.rect.width / 2,
      y: send.rect.y + send.rect.height / 2,
      sendText: send.text,
    };
  }, {
    reply: replyText,
    inputY: inputTarget.inputY,
    inputAbsTop: inputTarget.inputAbsTop,
    targetScoped: inputTarget.targetScoped,
  });
}

async function revealReplies(page) {
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    let clicked = 0;
    for (const el of [...document.querySelectorAll('button, div, span')]) {
      const text = compact(el.innerText || el.textContent || '');
      if (visible(el) && /查看\s*\d+\s*条回复/.test(text)) {
        el.click();
        clicked += 1;
        if (clicked >= 3) break;
      }
    }
    return { ok: true, clicked };
  }).catch((err) => ({ ok: false, error: err.message }));
}

async function expandVisibleReplyThreads(page, max = 10) {
  let clicked = 0;
  const attempts = [];
  for (let i = 0; i < max; i += 1) {
    const target = await page.evaluate(() => {
      const helpers = window.__douyinCommentHelpers || {};
      const compact = helpers.compact || ((text = '') => text.replace(/\s+/g, ' ').trim());
      const visible = helpers.visible || ((el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      });
      const getCommentCards = helpers.getCommentCards || (() => []);
      let item = [...document.querySelectorAll('.load-more-pDyh1o, [class*="load-more"], button, div, span')]
        .filter(visible)
        .map((el) => ({ el, text: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect() }))
        .filter(({ text }) => /查看\s*\d+\s*条回复/.test(text))
        .sort((a, b) => {
          const aScore = /load-more/.test(String(a.el.className || '')) ? 0 : 1;
          const bScore = /load-more/.test(String(b.el.className || '')) ? 0 : 1;
          return (aScore - bScore)
            || ((a.rect.width * a.rect.height) - (b.rect.width * b.rect.height))
            || (a.rect.y - b.rect.y)
            || (a.rect.x - b.rect.x);
        })[0];
      if (!item) {
        const card = getCommentCards().find((candidate) => /查看\s*\d+\s*条回复/.test(candidate.text));
        if (card) {
          const nodes = [...card.el.querySelectorAll('button, div, span')]
            .filter(visible)
            .map((el) => ({ el, text: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect(), area: el.getBoundingClientRect().width * el.getBoundingClientRect().height }))
            .filter(({ text, rect }) => /查看\s*\d+\s*条回复/.test(text) && rect.top >= card.rect.top && rect.top <= card.rect.bottom)
            .sort((a, b) => (a.area - b.area) || (b.rect.y - a.rect.y));
          item = nodes[0] || {
            el: card.el,
            text: card.text.match(/查看\s*\d+\s*条回复/)?.[0] || '查看回复',
            rect: {
              x: card.rect.x + card.rect.width - 120,
              y: card.rect.bottom - 24,
              width: 100,
              height: 20,
            },
          };
        }
      }
      if (!item) return { ok: false, error: 'no_more_reply_threads' };
      return {
        ok: true,
        text: item.text,
        x: item.rect.x + Math.min(48, Math.max(8, item.rect.width / 2)),
        y: item.rect.y + item.rect.height / 2,
        rect: {
          x: Math.round(item.rect.x),
          y: Math.round(item.rect.y),
          width: Math.round(item.rect.width),
          height: Math.round(item.rect.height),
        },
      };
    });
    attempts.push(target);
    if (!target.ok) break;
    await page.mouse.move(target.x, target.y);
    await page.mouse.click(target.x, target.y);
    clicked += 1;
    await sleep(1400);
  }
  await waitForUsefulBody(page, 3000);
  return { ok: true, clicked, attempts };
}

async function verifyReplyVisible(page, replyText, target = {}) {
  for (let i = 0; i < 6; i += 1) {
    const visible = await page.evaluate(({ reply, targetTop, targetSample }) => {
      const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
      const visibleEl = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const draftStillOpen = [...document.querySelectorAll('[contenteditable="true"], textarea')]
        .filter(visibleEl)
        .some((el) => compact(el.innerText || el.textContent || el.value || '').includes(reply));
      const targetNeedle = compact(targetSample || '').slice(0, 48);
      const cards = [...document.querySelectorAll('[class*="container-"], div, li, section, article')]
        .filter(visibleEl)
        .map((el) => {
          const rect = el.getBoundingClientRect();
          const text = compact(el.innerText || el.textContent || '');
          const hasEditableReply = [...el.querySelectorAll('[contenteditable="true"], textarea')]
            .filter(visibleEl)
            .some((input) => compact(input.innerText || input.textContent || input.value || '').includes(reply));
          return { text, top: Math.round(rect.top + window.scrollY), area: rect.width * rect.height, hasEditableReply };
        })
        .filter((item) => item.text.includes(reply) && !item.hasEditableReply && (!targetNeedle || item.text.includes(targetNeedle)));
      if (cards.length) {
        const nearest = cards
          .sort((a, b) => Math.abs(a.top - targetTop) - Math.abs(b.top - targetTop))[0];
        if (!Number.isFinite(targetTop) || Math.abs(nearest.top - targetTop) < 320) {
          return { found: true, scoped: true, draftStillOpen, top: nearest.top, sample: nearest.text.slice(0, 700) };
        }
      }
      const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
      return { found: false, scoped: false, draftStillOpen, pageHasReplyText: text.includes(reply), sample: text.slice(0, 1400) };
    }, {
      reply: replyText,
      targetTop: Number(target.cardTop),
      targetSample: target.sample || target.commentText || '',
    });
    if (visible.found) return { ok: true, found: true, attempts: i + 1 };
    await revealReplies(page);
    await sleep(1000);
  }
  const final = await page.evaluate(({ reply, targetTop, targetSample }) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visibleEl = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const targetNeedle = compact(targetSample || '').slice(0, 48);
    const draftStillOpen = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visibleEl)
      .some((el) => compact(el.innerText || el.textContent || el.value || '').includes(reply));
    const cards = [...document.querySelectorAll('[class*="container-"], div, li, section, article')]
      .filter(visibleEl)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = compact(el.innerText || el.textContent || '');
        const hasEditableReply = [...el.querySelectorAll('[contenteditable="true"], textarea')]
          .filter(visibleEl)
          .some((input) => compact(input.innerText || input.textContent || input.value || '').includes(reply));
        return { text, top: Math.round(rect.top + window.scrollY), area: rect.width * rect.height, hasEditableReply };
      })
      .filter((item) => item.text.includes(reply) && !item.hasEditableReply && (!targetNeedle || item.text.includes(targetNeedle)))
      .sort((a, b) => Math.abs(a.top - targetTop) - Math.abs(b.top - targetTop));
    const scoped = cards[0] && (!Number.isFinite(targetTop) || Math.abs(cards[0].top - targetTop) < 320);
    const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
    return { found: Boolean(scoped), scoped: Boolean(scoped), draftStillOpen, pageHasReplyText: text.includes(reply), sample: cards[0]?.text?.slice(0, 700) || text.slice(0, 1400) };
  }, {
    reply: replyText,
    targetTop: Number(target.cardTop),
    targetSample: target.sample || target.commentText || '',
  });
  return { ok: final.found, found: final.found, attempts: 6, pageText: final.sample, pageHasReplyText: final.pageHasReplyText };
}

async function clearReplyDraft(page) {
  return page.evaluate(() => {
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const inputs = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return br.width * br.height - ar.width * ar.height;
      });
    let cleared = 0;
    for (const input of inputs) {
      input.focus();
      if ('value' in input) {
        if (!input.value) continue;
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      } else {
        if (!input.textContent) continue;
        input.textContent = '';
        input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'deleteContentBackward', data: null }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
      cleared += 1;
      break;
    }
    return { ok: true, cleared };
  });
}

async function main() {
  const [command] = process.argv.slice(2);
  const args = parseArgs(process.argv.slice(3));
  if (!command || args.help) {
    usage();
    process.exit(command ? 0 : 2);
  }
  const releaseLock = await acquireBrowserTaskLock(`comment:${command}`, undefined, { deferToPublish: true, skipIfPublishActive: true });
  if (!releaseLock) {
    console.log(JSON.stringify({
      ok: true,
      action: 'deferred_to_publish',
      skipped: true,
      message: '发布任务优先，评论自动回复已让路。',
    }, null, 2));
    return;
  }
  const { page, ops } = await createDouyinSession();
  try {
    const helpersSource = installCommentCardHelpersSource();
    await page.evaluateOnNewDocument((source) => {
      // eslint-disable-next-line no-eval
      eval(source);
    }, helpersSource).catch(() => {});
    await page.evaluate((source) => {
      // eslint-disable-next-line no-eval
      eval(source);
    }, helpersSource).catch(() => {});
    const login = await ops.checkLogin();
    if (!login.loggedIn) {
      console.log(JSON.stringify({ ok: false, error: 'login_required', login }, null, 2));
      process.exitCode = 3;
      return;
    }
    await gotoComments(page);
    await closeKnownOverlays(page);
    if (command === 'reply-unreplied-by-filter') {
      const result = await replyUnrepliedByFilter(page, args);
      console.log(JSON.stringify(result, null, 2));
      if (!result.ok) process.exitCode = 1;
      return;
    }
    const prepare = await prepareCommentView(page, args);
    if ((args.workTitle || args.workIndex !== undefined) && !prepare.work?.ok) {
      console.log(JSON.stringify({
        ok: false,
        error: 'target_work_prepare_failed',
        prepare,
      }, null, 2));
      process.exitCode = 1;
      return;
    }
    const localState = loadAutoReplyState();
    if (command === 'list' && args.allWorks) {
      const allWorks = await scanAllWorks(page, args, localState);
      console.log(JSON.stringify({ ...allWorks, prepare, statePath: AUTO_REPLY_STATE_PATH }, null, 2));
      return;
    }
    let listed;
    if (command === 'reply' && args.allWorks) {
      const allWorks = await scanAllWorks(page, args, localState);
      listed = { ...allWorks, statePath: AUTO_REPLY_STATE_PATH };
    } else {
      const listedRaw = await listCommentsAcrossPages(page, args);
      const annotated = annotateAndFilterComments(listedRaw.comments, args, localState);
      listed = {
        ...listedRaw,
        unfilteredCount: annotated.unfilteredCount,
        filteredByLocalReply: annotated.filteredByLocalReply,
        filteredByAuthorReply: annotated.filteredByAuthorReply,
        filteredOwn: annotated.filteredOwn,
        count: annotated.comments.length,
        comments: annotated.comments,
        statePath: AUTO_REPLY_STATE_PATH,
      };
    }
    if (command === 'list') {
      console.log(JSON.stringify({ ...listed, prepare }, null, 2));
      return;
    }
    if (command !== 'reply') {
      usage();
      process.exitCode = 2;
      return;
    }
    const index = Math.max(0, Number(args.index || 0));
    const first = listed.comments[index] || null;
    let targetIndex = index;
    let targetPrepare = null;
    if (first?.workTitle && Number.isFinite(Number(first.workIndex))) {
      await openWorkSelector(page);
      const selected = await selectWorkByText(page, first.workTitle);
      if (!selected.ok) {
        console.log(JSON.stringify({ ok: false, error: 'target_work_select_failed', target: first, selected }, null, 2));
        process.exitCode = 1;
        return;
      }
      if (args.unreplied || args.authorReplyCheck) {
        await waitForCommentListSettled(page, 8000);
        await expandVisibleReplyThreads(page, 10);
      }
      const relistedRaw = await listCommentsAcrossPages(page, args);
      const relisted = annotateAndFilterComments(relistedRaw.comments, args, localState).comments;
      const matchedIndex = relisted.findIndex((comment) => (
        fingerprintText(comment.authorName) === fingerprintText(first.authorName)
        && relatedBody(comment.commentText || comment.sample, first.commentText || first.sample)
      ));
      if (matchedIndex < 0) {
        console.log(JSON.stringify({ ok: false, error: 'target_comment_not_found_after_work_select', target: first, selected }, null, 2));
        process.exitCode = 1;
        return;
      }
      targetIndex = matchedIndex;
      targetPrepare = { selectedWork: selected, relistedCount: relisted.length };
    }
    const replyResult = args.text
      ? { text: args.text, source: 'manual' }
      : await generateReply('comment', first?.commentText || first?.sample || '', {
        row: first,
        workTitle: first?.workTitle || prepare?.latest?.workTitle || prepare?.work?.workTitle || '',
      }, args);
    if (!args.text && replyResult.source !== 'llm' && !rulesFallbackAllowed(args)) {
      console.log(JSON.stringify({
        ok: false,
        mode: args.execute ? 'execute' : 'dry-run',
        error: 'llm_reply_generation_failed',
        target: first,
        prepare,
        targetPrepare,
        replySource: replyResult.source,
        llmFallback: replyResult.llmFallback,
        llmAttempts: replyResult.llmAttempts,
      }, null, 2));
      process.exitCode = 1;
      return;
    }
    const replyText = replyResult.text;
    const opened = await openCommentReply(page, targetIndex);
    const fill = opened.ok ? await fillOpenedReply(page, replyText, opened) : opened;
    if (!args.execute || !fill.ok) {
      const clear = fill.ok ? await clearReplyDraft(page) : null;
      console.log(JSON.stringify({
        ok: fill.ok,
        mode: args.execute ? 'execute' : 'dry-run',
        target: first,
        prepare,
        targetPrepare,
        proposedReply: replyText,
        replySource: replyResult.source,
        replyModel: replyResult.model,
        llmFallback: replyResult.llmFallback,
        llmAttempts: replyResult.llmAttempts,
        opened,
        fill,
        clear,
        executeCommand: `node scripts/douyin-comment-reply.js reply --text ${JSON.stringify(replyText)} --index ${index} --execute`,
      }, null, 2));
      if (!fill.ok) process.exitCode = 1;
      return;
    }
    if (fill.sendDisabled) {
      console.log(JSON.stringify({ ok: false, error: 'send_button_disabled', target: first, prepare, targetPrepare, opened, fill }, null, 2));
      process.exitCode = 1;
      return;
    }
    await page.mouse.click(fill.x, fill.y);
    await sleep(3000);
    const verification = await verifyReplyVisible(page, replyText, opened);
    if (verification.ok) {
      const state = loadState();
      recordCommentReply(state, first, replyText, verification);
      saveState(state);
    }
    console.log(JSON.stringify({
      ok: verification.ok,
      action: verification.ok ? 'comment_reply_sent_verified' : 'comment_reply_clicked_unverified',
      target: first,
      prepare,
      targetPrepare,
      opened,
      reply: replyText,
      replySource: replyResult.source,
      replyModel: replyResult.model,
      llmFallback: replyResult.llmFallback,
      llmAttempts: replyResult.llmAttempts,
      verification,
    }, null, 2));
    if (!verification.ok) process.exitCode = 1;
  } finally {
    disconnect();
    releaseLock();
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
