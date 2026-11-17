#!/usr/bin/env node
/**
 * tag-resolver.mjs —— 标签命名空间的读写工具。
 *
 * 用法：
 *   node tag-resolver.mjs list                      紧凑列出既有标签（name×count）
 *   node tag-resolver.mjs resolve <标签> [...] [--locale en-US|zh-CN|zh-TW]
 *                                                  按输出语言解析候选标签
 *   node tag-resolver.mjs audit                     找出既有标签里的近重复分组
 *   node tag-resolver.mjs merge <from> <to> [--dry-run]   把 from 合并进 to
 *
 * 配置沿用 catchlinger-api.mjs：环境变量 CATCHLINGER_API_BASE / CATCHLINGER_API_KEY，
 * 或写在 ~/.config/catchlinger/env。
 *
 * 零依赖，只用 Node 内置 fetch。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolveTags, findNearDuplicates, baseNormalize, similarityKey } from './tag-matching.mjs';
import { loadCatchLingerEnv } from './catchlinger-env.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ALIAS_FILE = path.join(HERE, '..', 'data', 'tag-aliases.json');

function loadEnv() {
  const env = loadCatchLingerEnv();
  if (!env) {
    console.error(
      JSON.stringify(
        { error: '缺少配置：请设置 CATCHLINGER_API_BASE 与 CATCHLINGER_API_KEY（可在 CatchLinger 的「设置 → API Key」生成）' },
        null,
        2,
      ),
    );
    process.exit(1);
  }
  return env;
}

function loadAliases() {
  if (!fs.existsSync(ALIAS_FILE)) return { equivalent: [], related: [], avoid: [] };
  try {
    const raw = JSON.parse(fs.readFileSync(ALIAS_FILE, 'utf8'));
    return {
      equivalent: raw.equivalent ?? [],
      related: raw.related ?? [],
      avoid: raw.avoid ?? [],
    };
  } catch (e) {
    console.error(JSON.stringify({ error: `别名表解析失败：${ALIAS_FILE} —— ${e.message}` }, null, 2));
    process.exit(1);
  }
}

async function api(env, pathname, { method = 'GET', body } = {}) {
  const res = await fetch(`${env.base}${pathname}`, {
    method,
    headers: {
      authorization: `Bearer ${env.key}`,
      accept: 'application/json',
      ...(body ? { 'content-type': 'application/json' } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const text = await res.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    payload = { raw: text };
  }
  if (!res.ok) {
    const error = payload?.error ?? { code: `HTTP_${res.status}`, message: text };
    throw new Error(`${error.code}: ${error.message}`);
  }
  return payload?.data ?? payload;
}

async function fetchTags(env) {
  const data = await api(env, '/tags');
  const tags = data?.tags ?? [];
  // id 必须带上：merge 要用标签 id 调 DELETE
  return tags.map((t) => ({ id: t.id, name: t.name, count: t.count ?? 0 }));
}

/**
 * 按名字找既有标签：**先精确匹配**，再退回归一匹配。
 *
 * 归一匹配是兜底 —— 因为 `springboot` 与 `spring boot` 归一后同 key，
 * 若不先精确匹配，from 会挑到另一条标签上。
 */
function pickTag(tags, name) {
  const exact = tags.find((t) => t.name === name);
  if (exact) return exact;
  const key = similarityKey(name);
  return tags.find((t) => similarityKey(t.name) === key);
}

function argv() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const positional = [];
  let locale;
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--locale') {
      locale = args[++i];
      if (!locale || !/^(en|zh)(?:-[a-z0-9]+)*$/i.test(locale)) {
        throw new Error('UNSUPPORTED_LOCALE: use --locale en-US, zh-CN or zh-TW');
      }
    } else if (!arg.startsWith('--')) {
      positional.push(arg);
    }
  }
  return { positional, dryRun, locale };
}

const { positional, dryRun, locale } = argv();
const command = positional[0];
const env = loadEnv();
const aliases = loadAliases();

switch (command) {
  // ── list：紧凑列表，给人和 Agent 快速扫一眼 ──────────────────────────
  case 'list': {
    const tags = await fetchTags(env);
    tags.sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
    console.log(tags.map((t) => `${t.name}×${t.count}`).join('  '));
    console.log(`\n共 ${tags.length} 个标签`);
    break;
  }

  // ── resolve：把候选标签映射到既有标签 ────────────────────────────────
  case 'resolve': {
    const proposed = positional.slice(1);
    if (proposed.length === 0) {
      console.error(JSON.stringify({ error: '用法：resolve <标签> [...]' }, null, 2));
      process.exit(1);
    }
    const tags = await fetchTags(env);
    const results = resolveTags(proposed, tags, aliases, { locale });

    const avoidKeys = new Set(aliases.avoid.map((n) => similarityKey(n)));
    for (const r of results) {
      if (avoidKeys.has(r.key)) {
        r.warning = `「${r.input}」是来源站点名，通常不作为主题标签使用（items.source 记录的是采集通道，不是发布平台）——确认这是有意的`;
      }
    }

    console.log(
      JSON.stringify(
        {
          existingTags: tags.length,
          ...(locale ? { locale } : {}),
          results,
          hint: 'action=reuse 直接用 resolved；action=candidate 确认语义后用 resolved；action=new 才可新建。',
        },
        null,
        2,
      ),
    );
    break;
  }

  // ── audit：既有标签里的近重复 ────────────────────────────────────────
  case 'audit': {
    const tags = await fetchTags(env);
    const groups = findNearDuplicates(tags, aliases);
    const avoidKeys = new Set(aliases.avoid.map((n) => similarityKey(n)));
    const avoidHits = tags.filter((t) => avoidKeys.has(similarityKey(t.name)));

    console.log(
      JSON.stringify(
        {
          existingTags: tags.length,
          nearDuplicateGroups: groups,
          sourceSiteTags: avoidHits.map((t) => ({ name: t.name, count: t.count })),
          mergeHint: 'node tag-resolver.mjs merge <from> <to>  —— 先 --dry-run 看影响面',
        },
        null,
        2,
      ),
    );
    break;
  }

  // ── merge：把 from 标签的收藏全部改挂到 to，再删掉 from ──────────────
  case 'merge': {
    const from = positional[1];
    const to = positional[2];
    if (!from || !to) {
      console.error(JSON.stringify({ error: '用法：merge <from> <to> [--dry-run]' }, null, 2));
      process.exit(1);
    }
    if (baseNormalize(from) === baseNormalize(to)) {
      console.error(JSON.stringify({ error: 'from 与 to 归一化后相同，无需合并' }, null, 2));
      process.exit(1);
    }

    const tags = await fetchTags(env);
    const fromTag = pickTag(tags, from);
    const toTag = pickTag(tags, to);

    if (!fromTag) {
      console.error(JSON.stringify({ error: `找不到标签「${from}」` }, null, 2));
      process.exit(1);
    }
    if (fromTag.id === toTag?.id) {
      console.error(
        JSON.stringify(
          {
            error: `from「${from}」与 to「${to}」指向同一个标签（${fromTag.name}），无需合并`,
            hint: '两个名字归一后相同。要合并的是具体某一条既有标签，请写它的原名。',
          },
          null,
          2,
        ),
      );
      process.exit(1);
    }

    const list = await api(env, `/items?status=all&limit=200&tag=${encodeURIComponent(fromTag.name)}`);
    const items = list?.items ?? [];

    const plan = [];
    const toName = toTag?.name ?? to;
    for (const item of items) {
      const names = (item.tags ?? []).map((t) => t.name);
      // 按**原名**剔除，不能按归一 key —— 否则 `springboot` 会把 `spring boot` 一起误删
      const next = names.filter((n) => n !== fromTag.name);
      if (!next.includes(toName)) next.push(toName);
      plan.push({
        id: item.id,
        url: item.url,
        from: names.length,
        to: next.length,
        tags: next,
        tooMany: next.length > 3,
      });
    }

    console.log(
      JSON.stringify(
        {
          action: dryRun ? 'dry-run' : 'merge',
          from: fromTag.name,
          to: toTag?.name ?? to,
          affectedItems: plan.length,
          note: 'Agent 通道每个收藏至多 3 个标签；合并不会增加标签数（除非目标标签不在该收藏上）。',
          plan: plan.map((p) => ({ id: p.id, url: p.url, tags: p.tags, tooMany: p.tooMany })),
        },
        null,
        2,
      ),
    );

    if (dryRun) break;

    let moved = 0;
    const failed = [];
    for (const p of plan) {
      if (p.tooMany) {
        failed.push({ id: p.id, reason: `目标标签集有 ${p.to} 个，超过 Agent 通道 3 个上限，需在 Web 端手工调整` });
        continue;
      }
      try {
        await api(env, `/items/${p.id}`, { method: 'PATCH', body: { tags: p.tags } });
        moved += 1;
      } catch (e) {
        failed.push({ id: p.id, reason: e.message });
      }
    }

    if (moved === plan.length) {
      await api(env, `/tags/${fromTag.id}`, { method: 'DELETE' });
    }

    console.log(
      JSON.stringify(
        {
          done: true,
          moved,
          failed,
          fromDeleted: moved === plan.length,
          note: moved === plan.length ? `标签「${fromTag.name}」已删除，收藏改挂到「${toTag?.name ?? to}」` : '有失败项，from 标签未删除',
        },
        null,
        2,
      ),
    );
    break;
  }

  default: {
    console.error(
      JSON.stringify(
        {
          error: '未知命令。可用：list / resolve / audit / merge',
          commands: ['list', 'resolve', 'audit', 'merge'],
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }
}
