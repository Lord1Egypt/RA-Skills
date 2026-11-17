'use strict';
/**
 * bid-doc.js —— 投标文件生成引擎（确定性、离线、零依赖）
 *
 * 输入：项目基本信息 + 招标文件关键条款 + 投标人资质业绩。
 * 输出：投标文件全册目录（分册/章节/要点/字数建议）、逐条响应表、
 *       否决条款自查表、材料清单、废标雷区清单、材料完整度评分。
 *
 * 设计原则：
 *   - **确定性**：同一份输入任何时候跑，输出逐字节一致，可被第三方按同一口径复核。
 *   - **不编造**：条款没给就不生成响应行；材料不足直接报缺什么，绝不产出"看起来完整"的空壳。
 *   - **不越界**：引擎只做结构化生成与机械匹配，不替用户判断报价策略与竞争格局。
 *
 * 术语说明：本引擎输出的是**可交付的投标文件骨架与应答口径**，
 * 不是"帮你写完整标书正文"——正文的技术方案、施工组织设计等仍需投标人自行撰写。
 */

const L = require('./bid-lexicon.js');

// ------------------------------------------------------------------ 工具

function s(v) {
  return String(v == null ? '' : v).trim();
}

function list(v) {
  return Array.isArray(v) ? v.filter((x) => x != null && s(x) !== '') : [];
}

function normKey(v) {
  return s(v).toLowerCase().replace(/[\s_\-]+/g, '');
}

/** 稳定排序：同输入必得同序。 */
function stableSort(arr, keyFn) {
  return arr
    .map((x, i) => ({ x, i, k: keyFn(x) }))
    .sort((a, b) => (a.k < b.k ? -1 : a.k > b.k ? 1 : a.i - b.i))
    .map((o) => o.x);
}

/** 金额格式化：只在输入是可解析数字时才格式化，否则原样返回（不猜测）。 */
function formatMoney(v) {
  const raw = s(v).replace(/[¥￥,\s]/g, '');
  if (!/^\d+(\.\d+)?$/.test(raw)) return s(v) || '';
  const n = Number(raw);
  if (!Number.isFinite(n)) return s(v);
  const [int, dec] = n.toFixed(2).split('.');
  const withComma = int.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return `¥${withComma}.${dec}`;
}

// ------------------------------------------------------------------ 条款归一

const CLAUSE_TYPES = ['reject', 'qualification', 'commercial', 'technical', 'other'];

/**
 * 判定条款类型。优先用显式 type；否则按关键词打分（可复核）。
 * 返回 { type, evidence }：evidence 说明为什么判成这个类型。
 */
function classifyClause(text) {
  const t = s(text);
  const hits = [];
  for (const [type, kws] of Object.entries(L.CLAUSE_TYPE_KEYWORDS)) {
    let n = 0;
    const matched = [];
    for (const kw of kws) {
      if (t.includes(kw)) { n++; matched.push(kw); }
    }
    if (n > 0) hits.push({ type, n, matched });
  }
  if (!hits.length) return { type: 'other', evidence: '未命中任何类型关键词' };
  hits.sort((a, b) => (b.n - a.n) || (a.type < b.type ? -1 : 1));
  const top = hits[0];
  return { type: top.type, evidence: `命中 ${top.matched.slice(0, 3).join('、')}` };
}

function normalizeClauses(payload) {
  const out = [];
  const raw = list(payload.clauses);
  raw.forEach((c, i) => {
    const text = s(typeof c === 'string' ? c : c && (c.text || c.clause || c.content));
    if (!text) return;
    const explicit = s(typeof c === 'object' && c ? c.type : '').toLowerCase();
    const cls = CLAUSE_TYPES.includes(explicit)
      ? { type: explicit, evidence: '由输入显式指定' }
      : classifyClause(text);
    out.push({
      index: i,
      no: s(typeof c === 'object' && c ? (c.no || c.id || c.index) : '') || `条款${i + 1}`,
      text,
      type: cls.type,
      typeEvidence: cls.evidence,
      mandatory: !!(typeof c === 'object' && c && (c.mandatory === true || c.required === true)),
    });
  });
  // 独立的否决条款清单（有些招标文件单独成表）
  list(payload.rejectClauses).forEach((rc, i) => {
    const text = s(typeof rc === 'string' ? rc : rc && (rc.text || rc.content));
    if (!text) return;
    out.push({
      index: raw.length + i,
      no: s(typeof rc === 'object' && rc ? (rc.no || rc.id) : '') || `否决条款${i + 1}`,
      text,
      type: 'reject',
      typeEvidence: '来自 rejectClauses 清单',
      mandatory: true,
    });
  });
  return stableSort(out, (c) => c.no);
}

// ------------------------------------------------------------------ 响应判定

/**
 * 最长公共子串（LCS-substring）—— 确定性、可解释。
 *
 * 为什么不用 includes()：
 *   投标人写的是"计算机信息系统集成资质二级"，招标文件写的是"须具备计算机信息系统集成资质"。
 *   用 `text.includes(token)` 做整串包含**必然全部落空**，会把每一行都判成"需补充"，
 *   等于给用户一份毫无信息量的表 —— 这是本项目第一版实测踩到的真缺陷。
 *   LCS 能定位到两者共有的最短可信片段（"计算机信息系统集成资质"），
 *   并把**命中的那一段原样报出来**，用户可逐条复核，正好是本引擎的卖点。
 *
 * @returns {string} 命中的公共子串；无命中返回 ''
 */
function lcsSubstring(a, b, minLen = 4) {
  if (!a || !b) return '';
  const A = s(a), B = s(b);
  if (A.length < minLen || B.length < minLen) return '';
  let best = '', bestLen = 0;
  // dp[j] = 以 B[j] 结尾的公共子串长度
  let prev = new Array(B.length + 1).fill(0);
  for (let i = 1; i <= A.length; i++) {
    const cur = new Array(B.length + 1).fill(0);
    for (let j = 1; j <= B.length; j++) {
      if (A[i - 1] === B[j - 1]) {
        cur[j] = prev[j - 1] + 1;
        if (cur[j] > bestLen) {
          bestLen = cur[j];
          best = A.slice(i - bestLen, i);
        }
      }
    }
    prev = cur;
  }
  return bestLen >= minLen ? best : '';
}

/** 从金额字符串里取出数值；取不到返回 null（不猜测）。 */
function toNumber(v) {
  const raw = s(v).replace(/[¥￥,，\s]/g, '');
  if (!/^\d+(\.\d+)?$/.test(raw)) return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : null;
}

/**
 * 报价类条款的超预算判定（确定性）。
 * 招标文件写了"不得超过预算 X 万元"且用户给了 price/budget 时，直接算出来 ——
 * 超预算是**直接废标**项，值得单独判，不能混在"需补充"里。
 */
function checkBudget(clause, ctx) {
  const text = clause.text;
  if (!/(不得|不能|禁止)?\s*(超过|高于|超出)/.test(text)) return null;
  const price = toNumber(ctx.price);
  if (price == null) return null;
  // 从条款里抓金额：支持 "130 万元" / "1300000元" / "130万元"
  const m = text.match(/(\d+(?:\.\d+)?)\s*(万元|万|元)/);
  if (!m) return null;
  let limit = Number(m[1]);
  if (m[2] === '万元' || m[2] === '万') limit *= 10000;
  if (!Number.isFinite(limit) || limit <= 0) return null;
  const over = price > limit;
  return {
    limit,
    price,
    over,
    note: `招标文件限额 ${formatMoney(limit)}，你的报价 ${formatMoney(price)}`,
  };
}

/**
 * 对单条条款给出响应结论。
 * 只做**机械匹配**：把条款文本与投标人已提供的资质/业绩/材料做 LCS 对照。
 * 命中 → 可响应；未命中且条款含"必须/应提供"或属否决条款 → 需补充；否则 → 待确认。
 */
function respond(clause, ctx) {
  const text = clause.text;
  const owned = ctx.evidenceTokens; // [{token, source}]

  const matched = [];
  for (const e of owned) {
    const hit = lcsSubstring(e.token, text);
    if (hit) matched.push({ source: e.source, hit });
  }

  const needsMaterial = L.MATERIAL_HINTS.some((h) => text.includes(h));
  const budget = clause.type === 'commercial' || clause.type === 'reject' ? checkBudget(clause, ctx) : null;

  let verdict, basis;
  if (budget && budget.over) {
    verdict = '需补充';
    basis = `报价超过招标文件限额：${budget.note} —— 超预算通常直接导致投标无效，必须调整报价或确认限额口径`;
  } else if (matched.length > 0) {
    verdict = '响应';
    basis = `条款中命中你已提供的「${matched.map((m) => m.hit).join('、')}」`
      + `（对应：${matched.map((m) => m.source).join('、')}）`
      + (budget ? `；同时报价未超限额（${budget.note}）` : '');
  } else if (budget) {
    verdict = '响应';
    basis = `报价未超招标文件限额：${budget.note}`;
  } else if (needsMaterial || clause.mandatory || clause.type === 'reject') {
    verdict = '需补充';
    basis = '条款要求提供证明材料，但条款文本未命中你已提供的任何资质/业绩';
  } else {
    verdict = '待确认';
    basis = '条款未命中你已提供的任何资质或业绩，需人工确认是否适用本项目';
  }

  const attached = [];
  for (const m of matched) {
    for (const mat of L.MATERIAL_BY_SOURCE[m.source] || []) {
      if (!attached.includes(mat)) attached.push(mat);
    }
  }

  return {
    no: clause.no,
    type: clause.type,
    verdict,
    basis,
    evidence: clause.typeEvidence,
    matchedPhrases: matched.map((m) => m.hit),
    budget,
    materials: attached,
    talkTrack: L.TALK_TRACK[verdict] || '',
  };
}

// ------------------------------------------------------------------ 全册结构

function buildVolumes(bidType) {
  const spec = L.BID_TYPES[bidType] || L.BID_TYPES.goods;
  return spec.volumes.map((v) => ({
    key: v.key,
    name: v.name,
    purpose: v.purpose,
    chapters: v.chapters.map((c) => ({
      name: c.name,
      points: c.points,
      words: c.words,
    })),
    chapterCount: v.chapters.length,
    wordTotal: v.chapters.reduce((a, c) => a + c.words, 0),
  }));
}

// ------------------------------------------------------------------ 主流程

const MIN = { projectName: 2, bidder: 2 };

function generate(payload) {
  if (payload == null || typeof payload !== 'object' || Array.isArray(payload)) {
    return { ok: false, code: 3, reason: '入参不是对象', message: '需要一个 JSON 对象，字段见 --help。' };
  }

  const projectName = s(payload.projectName || payload.project || payload.name);
  const bidder = s(payload.bidder || payload.bidderName || payload.company);

  // 边界层：材料不足就明确说缺什么，绝不产出"看起来正常"的空壳
  const missing = [];
  if (projectName.length < MIN.projectName) missing.push('projectName（项目名称）');
  if (bidder.length < MIN.bidder) missing.push('bidder（投标人名称）');
  if (missing.length) {
    return {
      ok: false,
      code: 3,
      reason: '缺少必要字段',
      message: '生成投标文件骨架至少需要知道"投哪个项目"和"谁来投"。',
      detail: { missing, need: 'projectName + bidder' },
    };
  }

  const bidType = L.BID_TYPES[normKey(payload.bidType)] ? normKey(payload.bidType) : 'goods';
  const bidTypeInferred = !L.BID_TYPES[normKey(payload.bidType)];

  const qualification = list(payload.qualification || payload.qualifications);
  const performance = list(payload.performance || payload.cases);
  const deliverables = list(payload.deliverables || payload.materials);
  const clauses = normalizeClauses(payload);

  const evidenceTokens = [];
  qualification.forEach((q) => evidenceTokens.push({ token: s(q), source: s(q) }));
  performance.forEach((p) => {
    const n = s(typeof p === 'string' ? p : p && (p.name || p.project));
    if (n) evidenceTokens.push({ token: n, source: n });
  });
  deliverables.forEach((d) => evidenceTokens.push({ token: s(d), source: s(d) }));

  const volumes = buildVolumes(bidType);
  const rawPrice = payload.price || payload.bidPrice;
  const responses = clauses.map((c) => respond(c, { evidenceTokens, price: rawPrice }));

  const byVerdict = { 响应: 0, 需补充: 0, 待确认: 0 };
  for (const r of responses) byVerdict[r.verdict] = (byVerdict[r.verdict] || 0) + 1;
  const overBudget = responses.filter((r) => r.budget && r.budget.over);

  const rejectRows = responses.filter((r) => r.type === 'reject');
  const missingMaterials = [];
  for (const r of responses) {
    for (const m of r.materials) if (!missingMaterials.includes(m)) missingMaterials.push(m);
  }
  const requiredMaterials = L.BASE_MATERIALS.map((m) => ({
    name: m.name,
    stamp: m.stamp,
    note: m.note,
  }));

  // 材料完整度评分（可复算：各分项加权后求和，无随机、无主观系数）
  // 否决条款全部可响应单独占 10 分 —— 这些条款不响应就是废标，不能与普通条款等价看待。
  const rejectReady = rejectRows.length > 0 && rejectRows.every((r) => r.verdict === '响应');
  const items = [
    { key: '项目信息', ok: true, weight: 10 },
    { key: '投标人名称', ok: true, weight: 10 },
    { key: '资质清单', ok: qualification.length > 0, weight: 20 },
    { key: '业绩清单', ok: performance.length > 0, weight: 15 },
    { key: '招标条款', ok: clauses.length > 0, weight: 20 },
    { key: '报价', ok: !!s(rawPrice), weight: 15 },
    { key: '否决条款全部可响应', ok: rejectReady, weight: 10 },
  ];
  const score = items.reduce((a, it) => a + (it.ok ? it.weight : 0), 0);
  const gaps = items.filter((it) => !it.ok).map((it) => it.key);

  return {
    ok: true,
    meta: {
      projectName,
      projectNo: s(payload.projectNo || payload.projectCode),
      tenderer: s(payload.tenderer || payload.tendererName),
      bidder,
      bidType,
      bidTypeInferred,
      price: formatMoney(payload.price || payload.bidPrice),
      generatedBy: 'bidwriter-doc-generator',
      engine: 'deterministic-v1',
    },
    summary: {
      volumes: volumes.length,
      chapters: volumes.reduce((a, v) => a + v.chapterCount, 0),
      wordTotal: volumes.reduce((a, v) => a + v.wordTotal, 0),
      clauses: clauses.length,
      responded: byVerdict['响应'] || 0,
      toSupplement: byVerdict['需补充'] || 0,
      toConfirm: byVerdict['待确认'] || 0,
      rejectClauses: rejectRows.length,
      overBudget: overBudget.length,
      score,
      gaps,
    },
    volumes,
    responses,
    rejectRows,
    materials: {
      required: requiredMaterials,
      fromClauses: missingMaterials,
      fromDeliverables: deliverables.map((d) => s(d)),
    },
    landmines: L.LANDMINES[bidType] || L.LANDMINES.goods,
  };
}

module.exports = { generate, classifyClause, formatMoney, lcsSubstring, checkBudget };
