#!/usr/bin/env node
import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createDouyinSession, disconnect } from '../src/index.js';
import { acquireBrowserTaskLock } from './browser-task-lock.js';

const DATA_URLS = {
  account: 'https://creator.douyin.com/creator-micro/data-center/operation',
  content: 'https://creator.douyin.com/creator-micro/data-center/content',
};

function usage() {
  console.error(`Usage:
  node scripts/douyin-data-analysis.js [--output /abs/report.json] [--days 90]
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
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

function parseMetric(text, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = text.match(new RegExp(`${escaped}\\s+([^\\s]+)`));
  return match?.[1] || null;
}

function parsePercentMetric(text, label) {
  const value = parseMetric(text, label);
  if (!value) return null;
  const num = Number(String(value).replace('%', ''));
  return Number.isFinite(num) ? num : null;
}

function toNumber(value) {
  if (value === null || value === undefined || value === '') return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
}

function toPercent(value) {
  const num = toNumber(value);
  return num === null ? null : num * 100;
}

function parseJsonPreservingLongIds(text) {
  const patched = String(text)
    .replace(/("(?:id|item_id|user_id|uid|sec_item_id)"\s*:\s*)(\d{16,})/g, '$1"$2"');
  return JSON.parse(patched);
}

function formatDateTimeFromUnixSeconds(seconds) {
  const num = Number(seconds);
  if (!Number.isFinite(num)) return null;
  const date = new Date(num * 1000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function normalizeWorkItem(item) {
  const metrics = item.metrics || {};
  const durationMs = toNumber(item.video_info?.duration);
  return {
    id: String(item.id || ''),
    title: item.description || '',
    publishTime: formatDateTimeFromUnixSeconds(item.create_time),
    createTimeRaw: item.create_time || null,
    type: item.type ?? null,
    reviewStatus: item.review?.status ?? null,
    downloadable: Boolean(item.downloadable),
    visibility: item.visibility || {},
    video: {
      durationMs,
      durationSeconds: durationMs === null ? null : durationMs / 1000,
      isVr: Boolean(item.video_info?.is_vr),
    },
    cover: {
      uri: item.cover?.uri || null,
      urls: item.cover?.url_list || [],
    },
    metrics: {
      viewCount: toNumber(metrics.view_count),
      likeCount: toNumber(metrics.like_count),
      commentCount: toNumber(metrics.comment_count),
      shareCount: toNumber(metrics.share_count),
      favoriteCount: toNumber(metrics.favorite_count),
      danmakuCount: toNumber(metrics.danmaku_count),
      downloadCount: toNumber(metrics.download_count),
      dislikeCount: toNumber(metrics.dislike_count),
      homepageVisitCount: toNumber(metrics.homepage_visit_count),
      subscribeCount: toNumber(metrics.subscribe_count),
      unsubscribeCount: toNumber(metrics.unsubscribe_count),
      coverShow: toNumber(metrics.cover_show),
      avgViewSecond: toNumber(metrics.avg_view_second),
      avgViewProportion: toPercent(metrics.avg_view_proportion),
      completionRate: toPercent(metrics.completion_rate),
      completionRate5s: toPercent(metrics.completion_rate_5s),
      bounceRate2s: toPercent(metrics.bounce_rate_2s),
      fanViewProportion: toPercent(metrics.fan_view_proportion),
      likeRate: toPercent(metrics.like_rate),
      commentRate: toPercent(metrics.comment_rate),
      shareRate: toPercent(metrics.share_rate),
      favoriteRate: toPercent(metrics.favorite_rate),
      subscribeRate: toPercent(metrics.subscribe_rate),
      unsubscribeRate: toPercent(metrics.unsubscribe_rate),
      dislikeRate: toPercent(metrics.dislike_rate),
    },
  };
}

function buildItemInsights(details) {
  if (!details.length) return [];
  const byViews = [...details].sort((a, b) => (b.metrics.viewCount || 0) - (a.metrics.viewCount || 0));
  const by5s = [...details].sort((a, b) => (b.metrics.completionRate5s || 0) - (a.metrics.completionRate5s || 0));
  const byBounce = [...details].sort((a, b) => (a.metrics.bounceRate2s ?? Infinity) - (b.metrics.bounceRate2s ?? Infinity));
  const bestView = byViews[0];
  const worstView = byViews.at(-1);
  const best5s = by5s[0];
  const bestBounce = byBounce[0];
  const insights = [];
  if (bestView) insights.push(`播放最高作品：${bestView.title}，播放 ${bestView.metrics.viewCount ?? '-'}。`);
  if (worstView && worstView.id !== bestView?.id) insights.push(`播放最低作品：${worstView.title}，播放 ${worstView.metrics.viewCount ?? '-'}。`);
  if (best5s) insights.push(`5 秒完播最好作品：${best5s.title}，5 秒完播率 ${best5s.metrics.completionRate5s?.toFixed?.(2) ?? '-'}%。`);
  if (bestBounce) insights.push(`2 秒跳出最低作品：${bestBounce.title}，2 秒跳出率 ${bestBounce.metrics.bounceRate2s?.toFixed?.(2) ?? '-'}%。`);
  return insights;
}

function buildAnalysis(accountText, contentText, itemData = null) {
  const account = {
    period: accountText.match(/统计周期：([^（]+)（/)?.[1]?.trim() || null,
    yesterday: {
      plays: parseMetric(accountText, '播放量'),
      profileVisits: parseMetric(accountText, '主页访问'),
      likes: parseMetric(accountText, '作品点赞'),
      shares: parseMetric(accountText, '作品分享'),
      comments: parseMetric(accountText, '作品评论'),
      netFans: parseMetric(accountText, '净增粉丝'),
      totalFans: parseMetric(accountText, '总粉丝量'),
    },
    diagnosis: [...accountText.matchAll(/(投稿活跃度|视频播放量|视频完播率|互动指数|粉丝净增量):\s*([^提升]+?)(?:提升建议|短视频|直播|数据表现|$)/g)]
      .map((m) => ({ item: m[1], text: m[2].trim() })),
    hotTopics: [...accountText.matchAll(/#([^\s#]+)\s+([\d,.]+万|[\d,.]+亿)/g)]
      .slice(0, 10)
      .map((m) => ({ topic: `#${m[1]}`, heat: m[2] })),
  };

  const content = {
    posts: parseMetric(contentText, '周期内投稿量'),
    avgClickRate: parseMetric(contentText, '条均点击率'),
    avg5sCompletionRate: parseMetric(contentText, '条均5s完播率'),
    avg2sBounceRate: parseMetric(contentText, '条均2s跳出率'),
    avgWatchTime: contentText.match(/条均播放时长\s+([^\s]+秒)/)?.[1] || null,
    medianPlays: parseMetric(contentText, '播放量中位数'),
    avgLikes: parseMetric(contentText, '条均点赞数'),
    avgComments: parseMetric(contentText, '条均评论量'),
    avgShares: parseMetric(contentText, '条均分享量'),
  };

  const suggestions = [];
  if ((Number(account.yesterday.plays) || 0) <= 10) suggestions.push('播放量偏低，优先提高发布频率和标题/封面吸引力。');
  if ((parsePercentMetric(contentText, '条均5s完播率') || 0) < 45) suggestions.push('5 秒完播率偏低，视频前 2 秒需要更直接给出冲突、结果或利益点。');
  if ((parsePercentMetric(contentText, '条均点击率') || 0) < 1) suggestions.push('点击率偏低，封面文字和标题需要更明确的单一卖点。');
  if ((Number(content.avgComments) || 0) < 3) suggestions.push('评论量偏低，可在文案结尾增加一个容易回答的问题。');
  if (account.hotTopics.length) suggestions.push(`可优先参考热点：${account.hotTopics.slice(0, 5).map((x) => x.topic).join('、')}。`);

  const itemDetails = (itemData?.items || []).map(normalizeWorkItem);

  return {
    account,
    content,
    items: {
      count: itemDetails.length,
      hasMore: Boolean(itemData?.has_more),
      total: itemData?.total ?? itemDetails.length,
      dateRange: itemData?.dateRange || null,
      details: itemDetails,
      topSummary: itemData?.summary || null,
      insights: buildItemInsights(itemDetails),
    },
    summary: suggestions.length ? suggestions : ['数据已获取，样本较少，建议继续积累发布数据后复盘。'],
  };
}

async function pageText(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
  await new Promise((resolve) => setTimeout(resolve, 6000));
  return page.evaluate(() => ({
    url: location.href,
    title: document.title,
    text: (document.body?.innerText || '').replace(/\s+/g, ' ').trim(),
  }));
}

async function fetchItemDetails(page, opts = {}) {
  const days = Math.max(1, Math.min(365, Number(opts.days || 90)));
  const payload = await page.evaluate(async (days) => {
    const dayMs = 24 * 60 * 60 * 1000;
    const now = new Date();
    const end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);
    const start = new Date(end.getTime() - days * dayMs);
    const params = new URLSearchParams({
      count: '50',
      order_by: '1',
      fields: 'metrics,review,visibility',
      need_cooperation: 'true',
      start_time: String(start.getTime()),
      end_time: String(end.getTime()),
      need_long_article: 'true',
    });
    const itemRes = await fetch(`/web/api/creator/item/list?${params.toString()}`, {
      credentials: 'include',
      headers: { accept: 'application/json' },
    });
    const itemText = await itemRes.text();
    let summaryText = '';
    try {
      const summaryRes = await fetch('/dp/douyin/v1/creator/item/item_summary', {
        method: 'POST',
        credentials: 'include',
        headers: { 'content-type': 'application/json', accept: 'application/json' },
        body: '{}',
      });
      summaryText = await summaryRes.text();
    } catch (err) {
      summaryText = JSON.stringify({ error: err.message });
    }
    const parsedForStatus = JSON.parse(itemText);
    return {
      itemText,
      summaryText,
      status: itemRes.status,
      ok: itemRes.ok && (parsedForStatus.status_code === 0 || parsedForStatus.BaseResp?.StatusCode === 0),
      dateRange: {
        startTime: start.getTime(),
        endTime: end.getTime(),
        startDate: start.toISOString().slice(0, 10),
        endDate: end.toISOString().slice(0, 10),
        days,
      },
    };
  }, days);
  const itemJson = parseJsonPreservingLongIds(payload.itemText);
  let summary = null;
  try {
    summary = parseJsonPreservingLongIds(payload.summaryText);
  } catch {
    summary = { raw: payload.summaryText };
  }
  return {
    ok: payload.ok,
    status: payload.status,
    statusCode: itemJson.status_code ?? itemJson.BaseResp?.StatusCode ?? null,
    statusMessage: itemJson.status_msg || itemJson.BaseResp?.StatusMessage || '',
    has_more: Boolean(itemJson.has_more),
    total: itemJson.total ?? null,
    max_cursor: itemJson.max_cursor || null,
    min_cursor: itemJson.min_cursor || null,
    items: itemJson.items || [],
    summary,
    dateRange: payload.dateRange,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }
  const releaseLock = await acquireBrowserTaskLock('data-analysis');
  const { page, ops } = await createDouyinSession();
  try {
    const login = await ops.checkLogin();
    if (!login.loggedIn) {
      console.log(JSON.stringify({ ok: false, error: 'login_required', login }, null, 2));
      process.exitCode = 3;
      return;
    }
    const days = Math.max(1, Math.min(365, Number(args.days || 90)));
    await page.evaluateOnNewDocument((value) => {
      window.__DOUYIN_DATA_DAYS__ = value;
    }, days);
    const accountPage = await pageText(page, DATA_URLS.account);
    const contentPage = await pageText(page, DATA_URLS.content);
    const itemData = await fetchItemDetails(page, { days });
    const analysis = buildAnalysis(accountPage.text, contentPage.text, itemData);
    const result = {
      ok: true,
      collectedAt: new Date().toISOString(),
      days,
      pages: {
        account: { url: accountPage.url, textSample: accountPage.text.slice(0, 1200) },
        content: { url: contentPage.url, textSample: contentPage.text.slice(0, 1200) },
      },
      analysis,
    };
    if (args.output) {
      mkdirSync(join(args.output, '..'), { recursive: true });
      writeFileSync(args.output, `${JSON.stringify(result, null, 2)}\n`);
      result.output = args.output;
    }
    console.log(JSON.stringify(result, null, 2));
  } finally {
    disconnect();
    releaseLock();
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
