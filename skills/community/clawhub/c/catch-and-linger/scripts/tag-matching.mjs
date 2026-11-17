#!/usr/bin/env node
/**
 * tag-matching.mjs —— 标签归一与相似度匹配的**纯函数**部分。
 *
 * 零依赖、纯计算、不碰网络不碰文件，方便离线单测。
 * tag-resolver.mjs 负责取数与写库，这里只回答两个问题：
 *
 *     1) 「我打算用的这个标签，命名空间里是不是已经有更合适的？」
 *     2) 「命名空间里哪些标签其实是同一个东西的不同写法？」
 *
 * 关系分四类，**不可混为一谈**：
 *
 *   exact    归一后完全相同 —— 同一个词的不同写法（springboot / spring boot）
 *   alias    命中「等价组」—— 同一个概念，canonical 为首选写法
 *   related  命中「同族组」—— 同一领域但**不等价**，只提示，绝不自动替换
 *            （java / java nio / java并发 属于同族，但不能互相替代）
 *   prefix   包含关系 —— 一个是另一个的上下位概念
 *
 * 归一有两层：
 *   · baseNormalize  —— 与服务端 normalizeTagName 对齐（小写、去 #、折叠空白）
 *   · similarityKey  —— 额外去掉分隔符，用来判定「同一个词的不同写法」
 */

/** 相似度比较时忽略的分隔符与标点（保留 + # & 等有语义的符号）。 */
const SEPARATORS = /[\s\-_./,，、·:：;；!！?？()（）\[\]【】{}「」『』"'“”‘’]/gu;

/** 与服务端 normalizeTagName 对齐的基础归一。 */
export function baseNormalize(raw) {
  if (typeof raw !== 'string') return '';
  return raw.trim().replace(/^#+/, '').replace(/\s+/g, ' ').toLowerCase();
}

/** 相似度用的 key：再抹掉分隔符。 */
export function similarityKey(raw) {
  return baseNormalize(raw).replace(SEPARATORS, '');
}

/** 拉丁词切分（用于「token 有交集」这条弱关系）。CJK 没有空格，不切。 */
export function tokenize(raw) {
  const base = baseNormalize(raw);
  if (!/^[\x20-\x7e]+$/.test(base)) return [];
  return base.split(/[^a-z0-9+#.]+/).filter(Boolean);
}

/**
 * 两个 key 的上下位关系：
 *   exact                   —— 完全相同
 *   proposed-more-specific  —— 提议的更细，候选是它的上位概念
 *   existing-more-specific  —— 候选是提议的下位概念
 */
export function relationBetween(inputKey, candidateKey) {
  if (!inputKey || !candidateKey) return null;
  if (inputKey === candidateKey) return 'exact';
  if (inputKey.includes(candidateKey)) return 'proposed-more-specific';
  if (candidateKey.includes(inputKey)) return 'existing-more-specific';
  return null;
}

/** 关系 → 权重。分数越高越可信。 */
export const RELATION_SCORE = {
  exact: 1,
  alias: 0.95,
  'proposed-more-specific': 0.72,
  'existing-more-specific': 0.66,
  related: 0.6,
  'token-overlap': 0.55,
};

/**
 * 「更通用的既有标签已有多少人用」达到这个数，才建议把细分标签收进它。
 * 阈值 2 的含义：一个标签至少被两条收藏用过，才算「命名空间里已经站稳了」。
 */
export const GENERALIZE_MIN_COUNT = 2;

/**
 * 别名表 → 索引。
 * @param {{equivalent?: Array, related?: Array}} config
 * @returns {{equivalent: Map, related: Map}}
 *   两个 Map 都是 memberKey → { canonical, canonicalKey, memberKeys:Set }
 */
export function buildAliasIndex(config) {
  const build = (groups) => {
    const index = new Map();
    for (const group of groups ?? []) {
      const members = group.members ?? [];
      const memberKeys = new Set(members.map((m) => similarityKey(m)).filter(Boolean));
      if (memberKeys.size === 0) continue;
      const canonicalKey = group.canonical ? similarityKey(group.canonical) : null;
      const entry = {
        canonical: group.canonical ?? null,
        canonicalKey,
        memberKeys,
        prefer: group.prefer ?? 'canonical',
      };
      for (const key of memberKeys) index.set(key, entry);
    }
    return index;
  };

  const cfg = config ?? {};
  // 兼容旧格式：直接传数组时视为全部是等价组
  const equivalent = Array.isArray(cfg) ? cfg : cfg.equivalent;
  const related = Array.isArray(cfg) ? [] : cfg.related;

  return { equivalent: build(equivalent), related: build(related) };
}

/** 把既有标签整理成带 key / token 的结构。 */
export function prepareExisting(tags) {
  return (tags ?? []).map((t) => ({
    name: t.name,
    count: t.count ?? 0,
    key: similarityKey(t.name),
    base: baseNormalize(t.name),
    tokens: tokenize(t.name),
  }));
}

/** 找出候选标签与提议标签的关系。 */
function relationTo(input, candidate, aliasIndex) {
  const direct = relationBetween(input.key, candidate.key);
  if (direct) return direct;

  const eq = aliasIndex.equivalent.get(input.key);
  if (eq && eq.memberKeys.has(candidate.key)) return 'alias';

  const rel = aliasIndex.related.get(input.key);
  if (rel && rel.memberKeys.has(candidate.key)) return 'related';

  if (input.tokens.length >= 1 && candidate.tokens.length >= 1) {
    const shared = input.tokens.filter((t) => candidate.tokens.includes(t));
    if (shared.length > 0) return 'token-overlap';
  }
  return null;
}

/** 关系优先级：数字小的更「权威」。 */
const RELATION_RANK = {
  exact: 0,
  alias: 1,
  'proposed-more-specific': 2,
  'existing-more-specific': 3,
  related: 4,
  'token-overlap': 5,
};

/**
 * 解析一个候选标签。
 *
 * @param {string} raw            打算使用的标签名
 * @param {Array}  existing       prepareExisting() 的结果
 * @param {Object} aliasIndex     buildAliasIndex() 的结果
 * @returns {{input:string, key:string, action:string, resolved:string|null,
 *            reason:string, candidates:Array}}
 */
export function resolveTag(raw, existing, aliasIndex) {
  const key = similarityKey(raw);
  const input = { key, base: baseNormalize(raw), tokens: tokenize(raw) };

  const candidates = [];
  for (const candidate of existing) {
    const relation = relationTo(input, candidate, aliasIndex);
    if (!relation) continue;
    candidates.push({
      name: candidate.name,
      count: candidate.count,
      score: RELATION_SCORE[relation],
      relation,
    });
  }

  candidates.sort(
    (a, b) =>
      RELATION_RANK[a.relation] - RELATION_RANK[b.relation] ||
      b.count - a.count ||
      a.name.length - b.name.length,
  );

  const eqGroup = aliasIndex.equivalent.get(key);
  const relGroup = aliasIndex.related.get(key);

  if (candidates.length === 0) {
    return {
      input: raw,
      key,
      action: 'new',
      resolved: null,
      reason: `既有 ${existing.length} 个标签里没有相近的`,
      candidates: [],
    };
  }

  const best = candidates[0];

  // ① 等价组命中：统一到 canonical（这是防「新造第三种写法」的主闸门）
  if (eqGroup) {
    const canonicalExisting = existing.find((e) => e.key === eqGroup.canonicalKey);
    const inGroup = candidates.filter((c) => c.relation === 'alias' || c.relation === 'exact');
    // prefer=most-used 时统一到用得最多的那个；默认统一到 canonical
    const preferMostUsed = eqGroup.prefer === 'most-used';
    const mostUsed = [...inGroup].sort((a, b) => b.count - a.count)[0];

    const pick =
      preferMostUsed && mostUsed
        ? mostUsed
        : canonicalExisting
          ? { name: canonicalExisting.name, count: canonicalExisting.count }
          : mostUsed;

    if (pick) {
      return {
        input: raw,
        key,
        action: 'reuse',
        resolved: pick.name,
        reason: canonicalExisting
          ? `与既有标签「${canonicalExisting.name}」属于同一概念（等价组：${eqGroup.canonical}）`
          : `等价组「${eqGroup.canonical}」里已有「${pick.name}」（${pick.count} 条收藏在用），复用它`,
        candidates,
      };
    }
  }

  // ② 归一后完全同词：复用既有写法（统一拼写）
  if (best.relation === 'exact') {
    return {
      input: raw,
      key,
      action: 'reuse',
      resolved: best.name,
      reason: `与既有标签「${best.name}」归一化后完全一致（已有 ${best.count} 条收藏在用）`,
      candidates,
    };
  }

  // ③ 同族但不等价：只提示，不自动替换
  if (best.relation === 'related' || relGroup) {
    const family = relGroup?.canonical ?? best.name;
    return {
      input: raw,
      key,
      action: 'candidate',
      resolved: best.name,
      reason: `与「${family}」这一族的既有标签相近，但它们并不等价 —— 确认该用哪一个，或确实需要新增`,
      candidates,
    };
  }

  // ④ 上下位关系：提议更细 → 建议收进用得多的上位标签
  if (best.relation === 'proposed-more-specific') {
    const established = best.count >= GENERALIZE_MIN_COUNT;
    return {
      input: raw,
      key,
      action: 'candidate',
      resolved: best.name,
      reason: established
        ? `既有标签「${best.name}」是它的上位概念且已有 ${best.count} 条收藏在用 —— 优先复用它`
        : `既有标签「${best.name}」是它的上位概念，但只有 ${best.count} 条收藏在用 —— 确认能否通用`,
      candidates,
    };
  }

  // ⑤ 其余情况
  const why = {
    'existing-more-specific': '是它的下位概念（更细）',
    'token-overlap': '与它共享部分词元',
  }[best.relation] ?? '与它相近';

  return {
    input: raw,
    key,
    action: 'candidate',
    resolved: best.name,
    reason: `既有标签「${best.name}」${why}（已有 ${best.count} 条收藏在用）—— 确认它能否表达你要的语义`,
    candidates,
  };
}

/**
 * 一次性解析多个候选标签（批量场景用）。
 * 输入会按归一 key 去重，避免同一个标签反复查。
 */
export function resolveTags(proposed, existing, aliasConfig, { locale } = {}) {
  if (locale && !/^(en|zh)(?:-[a-z0-9]+)*$/i.test(locale)) {
    throw new Error('UNSUPPORTED_LOCALE: use en, en-US, zh, zh-CN or zh-TW');
  }
  const prepared = prepareExisting(existing);
  const aliasIndex = buildAliasIndex(aliasConfig);
  const seen = new Map();
  for (const raw of proposed ?? []) {
    const key = similarityKey(raw);
    if (!seen.has(key)) seen.set(key, raw);
  }
  return [...seen.values()].map((raw) => {
    if (!locale) return resolveTag(raw, prepared, aliasIndex);
    // Locale controls generated vocabulary, not the source page language.
    // Technical names such as java remain Latin in Chinese collections too.
    const hasHan = (name) => /\p{Script=Han}/u.test(name);
    const english = /^en(?:-|$)/i.test(locale);
    if (english && hasHan(raw)) {
      throw new Error('INVALID_TAG_LANGUAGE: generate English candidate tags before resolving');
    }
    const compatible = prepared.filter((tag) => hasHan(tag.name) === hasHan(raw));
    return resolveTag(raw, compatible, aliasIndex);
  });
}

/**
 * 审计既有标签里的近重复分组。
 *
 * kind:
 *   same-key —— 归一后同一个词的不同写法（springboot / spring boot）
 *   alias    —— 命中等价组（限流 / 流量控制）
 *   related  —— 命中同族组，或存在上下位包含关系（gis / gis数据）
 */
export function findNearDuplicates(existing, aliasConfig) {
  const prepared = prepareExisting(existing);
  const aliasIndex = buildAliasIndex(aliasConfig);
  const groupsOut = [];
  const used = new Set();

  // same-key
  const byKey = new Map();
  for (const e of prepared) {
    if (!e.key) continue;
    if (!byKey.has(e.key)) byKey.set(e.key, []);
    byKey.get(e.key).push(e);
  }
  for (const [key, members] of byKey) {
    if (members.length > 1) {
      groupsOut.push({
        kind: 'same-key',
        key,
        members: members.map((m) => ({ name: m.name, count: m.count })),
      });
      members.forEach((m) => used.add(m.name));
    }
  }

  // 等价组
  const emitGroup = (kind, canonicalName, members) => {
    if (members.length < 2) return;
    groupsOut.push({
      kind,
      canonical: canonicalName,
      members: members.map((m) => ({ name: m.name, count: m.count })),
    });
    members.forEach((m) => used.add(m.name));
  };

  const collect = (index, kind) => {
    const byGroup = new Map();
    for (const e of prepared) {
      const g = index.get(e.key);
      if (!g) continue;
      const gk = g.canonicalKey ?? [...g.memberKeys][0];
      if (!byGroup.has(gk)) byGroup.set(gk, { canonical: g.canonical, members: [] });
      byGroup.get(gk).members.push(e);
    }
    for (const [, g] of byGroup) emitGroup(kind, g.canonical, g.members);
  };
  collect(aliasIndex.equivalent, 'alias');
  collect(aliasIndex.related, 'related');

  // 包含关系（上下位），排除已在上面出现过的
  const rest = prepared.filter((e) => !used.has(e.name) && e.key);
  for (let i = 0; i < rest.length; i += 1) {
    for (let j = i + 1; j < rest.length; j += 1) {
      const a = rest[i];
      const b = rest[j];
      const rel = relationBetween(a.key, b.key);
      if (!rel || rel === 'exact') continue;
      // 一方完全包含另一方，且长度差 ≥2 才算「细分 vs 通用」，避免 jvm/jvmgc 这类误报
      const shorter = a.key.length <= b.key.length ? a : b;
      const longer = shorter === a ? b : a;
      if (longer.key.length - shorter.key.length < 2) continue;
      groupsOut.push({
        kind: 'related',
        canonical: shorter.name,
        members: [
          { name: a.name, count: a.count },
          { name: b.name, count: b.count },
        ],
      });
    }
  }

  return groupsOut;
}
