'use strict';
/**
 * batch-quote-checkup.js —— 多标书批量合规体检（本包）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 本包只做一项检查，别无其他：
 *   逐家报价算术校验 —— 按投标人分组，每家的每一行都核对「合价 = 数量 × 单价」，
 *   不符的行给出差额，并给每家一个 verdict 与问题清单。
 *
 * **订阅版（买断版）：上面这一项 + 下面六项，共 7 项全部执行**
 *   否决条款响应核对、模板占位符扫描、基本要件扫描、跨家串通线索、
 *   报价离散度分析、按风险排序的整改清单。
 *   本包**不用**入参里的投标总价（price），订阅版把它用于离散度分析。
 * 判据全部可复算：占位符/要件用固定词表，离散度用变异系数与极差占比，整改清单按等级排序。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const TOLERANCE = 0.01;

const CHECKS_GIVEN = [
  '逐家报价算术校验',
  '否决条款响应核对', '模板占位符扫描', '基本要件扫描',
  '跨家串通线索', '报价离散度分析', '按风险排序的整改清单',
];

// 订阅版没有"未执行"的检查项（空数组本身就是对买家的承诺，由 buyout_tier_check.py 兜底）
const CHECKS_WITHHELD = [];

/* ------------------------------------------------------------ 通用小工具 */

/** 数字解析：接受数字、带千分位/全角逗号的数字串、带「万元/元」后缀的金额串
 *（货币符号不单独处理：下面的数字正则本来就会跳过它，例如「符号100」也能取到 100） */
function pickNumber(v) {
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  s = s.split(',').join('').split('，').join('');
  s = s.split(/\s+/).join('');
  let mult = 1;
  if (s.endsWith('万元')) { mult = 1e4; s = s.slice(0, -2); }
  else if (s.endsWith('万')) { mult = 1e4; s = s.slice(0, -1); }
  else if (s.endsWith('元')) { s = s.slice(0, -1); }
  const m = /-?\d+(?:\.\d+)?/.exec(s);
  if (!m) return null;
  const n = parseFloat(m[0]) * mult;
  return Number.isFinite(n) ? Math.round(n * 100) / 100 : null;
}

function fmt(v) {
  if (v === null || v === undefined) return '—';
  const n = Number(v);
  if (!Number.isFinite(n)) return '—';
  return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

/* ------------------------------------------------- 报价文本 → 明细行解析
 * 与「宁可失败也不猜错数字」同一原则：只接受列结构明确的表格行，
 * 有歧义就跳过，一行都没解析出来就返回空数组（由调用方给出明确的材料不足提示）。
 */

const HEADER_ALIASES = {
  name: ['名称', '项目名称', '分项名称', '材料名称', '设备名称', '项目', '分项', '品名', '货物名称'],
  unit: ['单位', '计量单位'],
  qty: ['数量', '工程量', '数 量'],
  price: ['单价', '综合单价', '单价（元）', '综合单价（元）', '单价(元)'],
  amount: ['合价', '金额', '合计', '总价', '合价（元）', '金额（元）', '合价(元)'],
  seq: ['序号', '编号', '项次', '序 号'],
};

const UNIT_TOKENS = new Set([
  't', 'T', 'kg', 'KG', 'g', '吨', '公斤', '千克', 'm', 'M', 'm2', 'm3', '㎡', 'm³',
  '米', '延米', '平方米', '立方米', 'km', '公里', '项', '个', '台', '套', '组', '批',
  '樘', '处', '座', '孔', '根', '块', '片', '张', '条', '只', '付', '对', '户', '人',
  '工日', '台班', '月', '年', '次', '站', '系统', 'km·对',
]);

const NUM_TOKEN = /^-?\d{1,3}(?:,\d{3})+(?:\.\d+)?$|^-?\d+(?:\.\d+)?$/;

function numOf(token) {
  if (typeof token !== 'string') return null;
  const t = token.trim();
  if (!NUM_TOKEN.test(t)) return null;
  const n = Number(t.replace(/,/g, ''));
  return Number.isFinite(n) ? n : null;
}

/** 只去掉首尾空列，**保留中间空列**（删掉中间空列会让数量/单价/合价整体前移） */
function splitDelimited(line, sep) {
  const parts = line.split(sep).map((x) => x.trim());
  while (parts.length && parts[0] === '') parts.shift();
  while (parts.length && parts[parts.length - 1] === '') parts.pop();
  return parts;
}

function splitRow(line) {
  if (line.includes('|')) return splitDelimited(line, '|');
  if (line.includes('\t')) return splitDelimited(line, '\t');
  if (line.includes('，') || line.includes(',')) {
    const parts = line.split(/[，]|,(?!\d{3}\b)/).map((x) => x.trim()).filter((x) => x !== '');
    if (parts.length >= 3) return parts;
  }
  const wide = line.split(/\s{2,}/).map((x) => x.trim()).filter((x) => x !== '');
  if (wide.length >= 3) return wide;
  return line.split(/\s+/).map((x) => x.trim()).filter((x) => x !== '');
}

function parseHeader(tokens) {
  const map = {};
  tokens.forEach((tok, i) => {
    const clean = tok.replace(/[\s（）()]/g, '');
    for (const field of Object.keys(HEADER_ALIASES)) {
      if (map[field] !== undefined) continue;
      if (HEADER_ALIASES[field].some((a) => clean === a.replace(/[\s（）()]/g, ''))) { map[field] = i; break; }
    }
  });
  const hasQtyPrice = map.qty !== undefined && map.price !== undefined;
  const hasPriceAmount = map.price !== undefined && map.amount !== undefined;
  return (hasQtyPrice || hasPriceAmount) ? map : null;
}

function isNoiseLine(line) {
  const t = line.trim();
  if (!t) return true;
  if (/^(序号|合计|小计|总计|备注|说明|注[:：]|以下空白)/.test(t)) return true;
  if (/^[-=—_·\s|]+$/.test(t)) return true;
  return false;
}

function rowByHeader(tokens, map, lineNo) {
  const pick = (i) => (i === undefined || i < 0 || i >= tokens.length ? null : tokens[i]);
  const name = (pick(map.name) || '').trim();
  const unit = (pick(map.unit) || '').trim();
  const qty = numOf(pick(map.qty) || '');
  const price = numOf(pick(map.price) || '');
  const amount = numOf(pick(map.amount) || '');
  if (!name) return null;
  if (qty === null && price === null && amount === null) return null;
  return { name, unit: UNIT_TOKENS.has(unit) ? unit : (unit || undefined), qty, price, amount, line: lineNo };
}

function rowByTailNumbers(tokens, lineNo) {
  if (tokens.length < 3) return null;
  const nums = [];
  let cut = tokens.length;
  for (let i = tokens.length - 1; i >= 0; i--) {
    const n = numOf(tokens[i]);
    if (n === null) break;
    nums.unshift(n);
    cut = i;
  }
  if (nums.length < 2 || nums.length > 3) return null;
  let nameTokens = tokens.slice(0, cut);
  if (nameTokens.length > 1 && /^\d{1,3}$/.test(nameTokens[0])) nameTokens = nameTokens.slice(1);
  let unit;
  if (nameTokens.length > 1) {
    const last = nameTokens[nameTokens.length - 1];
    if (UNIT_TOKENS.has(last)) { unit = last; nameTokens = nameTokens.slice(0, -1); }
  }
  const name = nameTokens.join(' ').trim();
  if (!name) return null;
  const [qty, price, amount] = nums.length === 3 ? nums : [nums[0], nums[1], null];
  return { name, unit, qty, price, amount, line: lineNo };
}

function parseText(text) {
  const raw = String(text == null ? '' : text);
  if (!raw.trim()) return [];
  const items = [];
  let headerMap = null;
  const lines = raw.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const tokens = splitRow(line);
    if (tokens.length < 2) continue;
    const asHeader = parseHeader(tokens);
    if (asHeader) { headerMap = asHeader; continue; }
    if (isNoiseLine(line)) continue;
    const row = headerMap ? rowByHeader(tokens, headerMap, i + 1) : rowByTailNumbers(tokens, i + 1);
    if (row) items.push(row);
  }
  return items;
}

/* -------------------------------------------------------------- 入参归一 */

/** 结构化 items 的一行 */
function itemRow(raw, idx) {
  if (!raw || typeof raw !== 'object') return null;
  const rawName = raw.name != null ? raw.name
    : (raw['项目名称'] != null ? raw['项目名称']
      : (raw['名称'] != null ? raw['名称'] : (raw.item != null ? raw.item : '')));
  const name = String(rawName == null ? '' : rawName).trim() || `第${idx + 1}项`;
  const qty = pickNumber(raw.qty !== undefined ? raw.qty : (raw.quantity !== undefined ? raw.quantity : raw['数量']));
  const price = pickNumber(raw.price !== undefined ? raw.price : (raw.unitPrice !== undefined ? raw.unitPrice : raw['单价']));
  const amount = pickNumber(raw.amount !== undefined ? raw.amount : (raw.total !== undefined ? raw.total : raw['合价']));
  // 只有"既没有名称、三个数也都没有"的纯垃圾条目才丢弃。有名称但数字为空的行必须留下 ——
  // 它正是「缺漏/无法核对」要报的对象，静默丢掉会变成"查过且没问题"的假结论。
  if (qty === null && price === null && amount === null && !String(rawName == null ? '' : rawName).trim()) return null;
  return { name, qty, price, amount, line: idx + 1, where: `第${idx + 1}项` };
}

function hasAnyNumber(row) {
  return row.qty !== null || row.price !== null || row.amount !== null;
}

/** 一家的报价明细行：优先 items，其次 text（可解析的报价表文本） */
function rowsOf(bidder) {
  const items = Array.isArray(bidder.items) ? bidder.items : null;
  if (items && items.length) {
    const rows = [];
    for (let i = 0; i < items.length; i++) {
      const r = itemRow(items[i], i);
      if (r) rows.push(r);
    }
    return { rows, source: 'items', raw_count: items.length };
  }
  const text = typeof bidder.text === 'string' ? bidder.text : '';
  if (text.trim().length >= 2) {
    return { rows: parseText(text), source: 'text', raw_count: 0 };
  }
  return { rows: [], source: 'none', raw_count: 0 };
}

/* ================================================================== 订阅版追加检查
 * 本包声明了 6 项"未执行"的检查，订阅版**逐项真的执行**（不多做、不少做）：
 *   否决条款响应核对 / 模板占位符扫描 / 基本要件扫描 /
 *   跨家串通线索 / 报价离散度分析 / 按风险排序的整改清单
 * 判据全部可复算；本包**不用**的 `price`（投标总价）在订阅版里用于离散度分析。
 * ================================================================ */

const PLACEHOLDER_PATTERNS = [
  [/\bX{3,}\b|××+|ｘ{3,}/i, '连续占位符（XXX/×××）'],
  [/[【〔\[]\s*[】〕\]]/, '空的中文方括号'],
  [/待填|待定|待补充|请填写|自行填写|TODO|\$\{|\{\{/, '待填标记（待填/TODO/${}）'],
  [/某[某公司单位集团]|某某|甲公司|乙公司|A公司|B公司|XX公司/i, '泛指主体（某某公司/甲公司）'],
  [/[△▲]{2,}|_{3,}|＿{3,}|…{3,}/, '空白占位行'],
  [/（\s*）|\(\s*\)/, '空括号'],
];

const BASIC_ELEMENTS = [
  ['投标函', /投标函|投标书|投标申请书/],
  ['法定代表人身份证明', /法定代表人身份证明|法人身份证明|法定代表人证明/],
  ['授权委托书', /授权委托书|法人授权|委托书/],
  ['报价表', /报价表|开标一览表|报价明细|投标报价/],
  ['营业执照', /营业执照|统一社会信用代码/],
  ['资质证书', /资质证书|资质等级|施工资质|企业资质/],
  ['投标保证金凭证', /保证金|投标保证金/],
];

const NON_RESPONSE_PHRASES = ['不响应', '不予响应', '不满足', '不能满足', '无法满足', '无法响应', '不接受', '不承诺', '偏离招标文件'];

const DENIAL_BLOCKING = { level: 'P0', label: '否决条款响应核对' };
const PLACEHOLDER = { level: 'P1', label: '模板占位符扫描' };
const BASIC_ELEMENT = { level: 'P1', label: '基本要件扫描' };
const CROSS_LEAD = { level: 'P0', label: '跨家串通线索' };
const DISPERSION = { level: 'P1', label: '报价离散度分析' };
const RISK_ACTIONS = { level: 'P2', label: '按风险排序的整改清单' };

const BASIS_MAP = {
  '否决条款响应核对': '《招标投标法实施条例》第五十一条（投标文件未对招标文件实质性要求作出响应）',
  '模板占位符扫描': '投标文件实质性内容不完整（形式评审常见否决项）',
  '基本要件扫描': '投标文件组成不完整（形式评审/资格评审常见否决项）',
  '跨家串通线索': '《招标投标法实施条例》第四十条',
  '报价离散度分析': '《招标投标法实施条例》第四十条（五）',
  '按风险排序的整改清单': '内部整改用：按风险等级排序，先处理 P0',
};

function rawLines(text) {
  return String(text == null ? '' : text).replace(/\r\n?/g, '\n').split('\n');
}

function allBidderText(b) {
  const parts = [];
  if (typeof b.text === 'string') parts.push(b.text);
  if (Array.isArray(b.items)) parts.push(JSON.stringify(b.items));
  return parts.join('\n');
}

/* --- 1) 否决条款响应核对 --- */
function checkDenials(bidder, findings) {
  const text = allBidderText(bidder);
  const hits = NON_RESPONSE_PHRASES.filter((p) => text.includes(p));
  // 结构化入参优先：{ denials:[{clause, responded}] } 或 { responses:{...} }
  const structured = [];
  const list = Array.isArray(bidder.denials) ? bidder.denials : [];
  for (const d of list) {
    if (d && typeof d === 'object' && d.responded === false) structured.push(String(d.clause || d.name || '未命名否决条款'));
    if (typeof d === 'string') structured.push(d);
  }
  for (const c of structured) {
    findings.push({
      type: 'DENIAL_NOT_RESPONDED',
      level: DENIAL_BLOCKING.level,
      label: DENIAL_BLOCKING.label,
      basis: BASIS_MAP['否决条款响应核对'],
      detail: `${bidder.name} 对否决条款「${c}」未作出响应`,
      evidence: { bidder: bidder.name, clause: c, source: '结构化入参 denials' },
      advice: '否决条款未响应在形式评审阶段即被否决：补齐响应或澄清后再投。',
    });
  }
  for (const h of hits) {
    findings.push({
      type: 'DENIAL_NOT_RESPONDED',
      level: DENIAL_BLOCKING.level,
      label: DENIAL_BLOCKING.label,
      basis: BASIS_MAP['否决条款响应核对'],
      detail: `${bidder.name} 的材料里出现「${h}」表述（可能未响应实质性要求）`,
      evidence: { bidder: bidder.name, phrase: h, source: '正文' },
      advice: '核对被"不响应/偏离"的那一条是否属于否决项；属于就必须改到响应为止。',
    });
  }
}

/* --- 2) 模板占位符扫描 --- */
function checkPlaceholders(bidder, findings) {
  const text = allBidderText(bidder);
  for (const [re, label] of PLACEHOLDER_PATTERNS) {
    const m = text.match(re);
    if (!m) continue;
    const idx = text.indexOf(m[0]);
    const around = text.slice(Math.max(0, idx - 18), idx + m[0].length + 18).replace(/\s+/g, ' ');
    findings.push({
      type: 'TEMPLATE_PLACEHOLDER',
      level: PLACEHOLDER.level,
      label: PLACEHOLDER.label,
      basis: BASIS_MAP['模板占位符扫描'],
      detail: `${bidder.name} 的材料里还有模板占位符：${label}`,
      evidence: { bidder: bidder.name, kind: label, sample: around },
      advice: '占位符没删掉等于该项内容不存在，形式评审会按"内容不完整"处理。',
    });
  }
}

/* --- 3) 基本要件扫描 --- */
function checkBasicElements(bidder, findings) {
  const text = allBidderText(bidder);
  if (text.trim().length < 10) return;                      // 材料为空由"材料不足"处理，不在这里下结论
  const missing = BASIC_ELEMENTS.filter(([, re]) => !re.test(text)).map(([n]) => n);
  if (!missing.length) return;
  findings.push({
    type: 'BASIC_ELEMENT_MISSING',
    level: BASIC_ELEMENT.level,
    label: BASIC_ELEMENT.label,
    basis: BASIS_MAP['基本要件扫描'],
    detail: `${bidder.name} 的材料里没找到 ${missing.length} 项基本要件`,
    evidence: { bidder: bidder.name, missing },
    advice: '逐项补齐；其中投标函、报价表、授权委托书缺一项就会被否决。',
  });
}

/* --- 4) 跨家串通线索 --- */
function extractContacts(text) {
  const s = String(text == null ? '' : text).replace(/\u3000/g, ' ').replace(/[\s\u00a0]+/g, ' ');
  const pick = (re) => { const m = s.match(re); return m ? m[1] : null; };
  const phones = s.match(/1[3-9]\d{9}/g) || [];
  const emails = s.match(/[\w.+-]+@[\w-]+\.[\w.]+/g) || [];
  const uscc = s.match(/\b[0-9A-HJ-NPQRTUWXY]{18}\b/g) || [];
  const accounts = s.match(/(?:账号|账户)\s*[:：]?\s*([0-9]{8,25})/g) || [];
  const person = pick(/(?:项目经理|项目负责人|联系人|委托代理人)\s*[:：]?\s*([\u4e00-\u9fa5]{2,4})/);
  return { phones, emails, uscc, accounts: accounts.map((x) => x.replace(/[^\d]/g, '')), person };
}

/** 去掉"标准要件名 + 通用词"之后还剩多少实义中文 —— 太短就不算雷同证据。
 *  招投标文件里"投标函 授权委托书 报价表…"这种要件清单家家都一模一样，
 *  把它报成 P0 串通线索会让整份报告失去可信度（第一版就报错了）。 */
const GENERIC_WORDS = ['投标', '文件', '材料', '提供', '加盖', '公章', '复印件', '原件', '我方', '本项目', '招标', '要求', '承诺', '证明', '身份', '法定', '代表', '授权', '委托', '报价', '营业', '执照', '资质', '证书', '保证金', '凭证', '统一', '社会', '信用', '代码', '副本', '正本', '扫描件'];

function substanceLength(seg) {
  let rest = seg;
  for (const [, re] of BASIC_ELEMENTS) rest = rest.replace(new RegExp(re.source, 'g'), '');
  for (const w of GENERIC_WORDS) rest = rest.split(w).join('');
  return rest.replace(/[\s\d\p{P}\p{S}]/gu, '').length;
}

function checkCrossBidderCrossLead(pool, findings) {
  const kinds = [['phones', '电话'], ['emails', '邮箱'], ['uscc', '统一社会信用代码'], ['accounts', '银行账号'], ['person', '关键人员']];
  for (const [field, label] of kinds) {
    const map = new Map();
    for (const b of pool) {
      const c = extractContacts(allBidderText(b));
      const values = field === 'person' ? (c.person ? [c.person] : []) : c[field];
      for (const v of new Set(values)) {
        if (!map.has(v)) map.set(v, new Set());
        map.get(v).add(b.name);
      }
    }
    for (const [value, who] of map) {
      if (who.size < 2) continue;
      findings.push({
        type: 'CROSS_BIDDER_LEAD',
        level: CROSS_LEAD.level,
        label: CROSS_LEAD.label,
        basis: BASIS_MAP['跨家串通线索'],
        detail: `${[...who].join(' 与 ')} 的${label}相同`,
        evidence: { kind: label, value: field === 'person' ? `${String(value)[0]}*` : String(value).replace(/^(\d{3})\d+(\d{2})$/, '$1****$2'), bidders: [...who] },
        advice: '同一联系方式/同一关键人员出现在多家投标文件里，属于法定视为串通的情形之一：留存证据并报告。',
      });
    }
  }
  // 正文长句完全相同（同一份底稿的强线索）
  const segMap = new Map();
  for (const b of pool) {
    const segs = new Set(rawLines(b.text).map((l) => l.replace(/\s+/g, ' ').trim())
      .filter((l) => l.length >= 20 && /[\u4e00-\u9fa5]/.test(l) && substanceLength(l) >= 12));
    for (const s of segs) {
      if (!segMap.has(s)) segMap.set(s, new Set());
      segMap.get(s).add(b.name);
    }
  }
  let shown = 0;
  for (const [seg, who] of segMap) {
    if (who.size < 2 || shown >= 10) continue;
    shown += 1;
    findings.push({
      type: 'CROSS_BIDDER_LEAD',
      level: CROSS_LEAD.level,
      label: CROSS_LEAD.label,
      basis: BASIS_MAP['跨家串通线索'],
      detail: `${[...who].join(' 与 ')} 的材料里有 ${seg.length} 个字完全相同的一整行`,
      evidence: { segment: seg.length > 70 ? seg.slice(0, 70) + '…' : seg, bidders: [...who] },
      advice: '整行一致通常来自同一份底稿：核对各家的文件来源与制作记录。',
    });
  }
}

/* --- 5) 报价离散度分析 --- */
function priceOf(b) {
  const v = pickNumber(b.price !== undefined ? b.price : (b['投标总价'] !== undefined ? b['投标总价'] : b.totalPrice));
  return v;
}

function checkPriceDispersion(pool, findings) {
  const rows = pool.map((b) => ({ name: b.name, price: priceOf(b) })).filter((r) => r.price !== null && r.price > 0);
  // ⛔ 统计量放**结果**里，不要为了"报告一下"就产出一条 finding：
  //    finding 必须表示"有问题"，否则干净样例永远不干净（第一版就栽在这）。
  if (rows.length < 3) return null;
  const values = rows.map((r) => r.price);
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length;
  const sd = Math.sqrt(variance);
  const cv = mean ? sd / mean : 0;
  const spread = (Math.max(...values) - Math.min(...values)) / mean;
  const stats = {
    count: rows.length,
    mean: Number(mean.toFixed(2)),
    sd: Number(sd.toFixed(2)),
    cv: Number(cv.toFixed(6)),
    spread: Number(spread.toFixed(6)),
    quotes: rows.map((r) => ({ bidder: r.name, price: r.price })),
  };
  // 判据（可复算）：变异系数 < 0.5% 或 极差/均值 < 1% ⇒ 报价异常集中
  if (cv < 0.005 || spread < 0.01) {
    findings.push({
      type: 'PRICE_DISPERSION',
      level: DISPERSION.level,
      label: DISPERSION.label,
      basis: BASIS_MAP['报价离散度分析'],
      detail: `${rows.length} 家报价异常集中（变异系数 ${(cv * 100).toFixed(3)}%、极差占比 ${(spread * 100).toFixed(3)}%）`,
      evidence: stats,
      advice: '正常竞争报价的离散度不会这么小：核对各家报价的编制来源与电子文件。',
    });
  }
  return stats;
}

/* --- 6) 按风险排序的整改清单 --- */
function buildRiskRankedActions(findings, result) {
  const rank = { P0: 0, P1: 1, P2: 2 };
  const actions = findings
    .slice()
    .sort((a, b) => (rank[a.level] - rank[b.level]) || a.label.localeCompare(b.label))
    .map((f, i) => ({ order: i + 1, level: f.level, label: f.label, bidder_or_scope: f.evidence.bidder || (f.evidence.bidders || []).join('、') || '全局', action: f.advice, detail: f.detail }));
  result.actions = actions;
  result.action_summary = {
    total: actions.length,
    p0: actions.filter((x) => x.level === 'P0').length,
    p1: actions.filter((x) => x.level === 'P1').length,
    p2: actions.filter((x) => x.level === 'P2').length,
  };
  if (result.action_summary.p0 > 0) {
    findings.push({
      type: 'RISK_RANKED_ACTIONS',
      level: RISK_ACTIONS.level,
      label: RISK_ACTIONS.label,
      basis: BASIS_MAP['按风险排序的整改清单'],
      detail: `共 ${actions.length} 条整改项，其中 ${result.action_summary.p0} 条为 P0（不改完不建议提交）`,
      evidence: { first_three: actions.slice(0, 3).map((x) => `#${x.order} [${x.level}] ${x.label} · ${x.bidder_or_scope}`) },
      advice: '按清单顺序从 P0 开始整改；P0 未清零时提交会被形式评审否决。',
    });
  }
}

/* ------------------------------------------------------------------ 主入口 */

/** 单家投标人的报价算术核对 */
function checkOneBidder(bidder) {
  const findings = [];
  const picked = rowsOf(bidder);
  const rows = picked.rows;
  const rowsUsable = rows.filter(hasAnyNumber);
  let checked = 0;
  let unverifiable = 0;

  if (!rowsUsable.length) {
    const why = rows.length
      ? `items 有 ${rows.length} 行，但每一行的 数量/单价/合价 都是空的，没有任何一行可以核对`
      : (picked.raw_count
        ? `items 有 ${picked.raw_count} 行，但没有一行能解析出数量/单价/合价中的任何一个数字`
        : (typeof bidder.text === 'string' && bidder.text.trim()
          ? `text 有 ${bidder.text.trim().length} 个字符，但没有识别出可校验的报价明细行`
          : '既没有 items（结构化明细），也没有 text（可解析的报价表文本）'));
    findings.push({
      level: 'P2',
      category: '报价算术',
      message: `本家报价算术未执行：${why}`,
      advice: '补齐 items [{"name","qty","price","amount"}]，或提供「名称 数量 单价 合价」格式的报价文本。',
    });
    return {
      bidder: bidder.name,
      verdict: 'NOT_CHECKED',
      summary: { p0: 0, p1: 0, p2: findings.length, total: findings.length },
      rows: rows.length,
      rows_usable: 0,
      rows_arithmetic_checked: 0,
      rows_unverifiable: 0,
      findings,
    };
  }

  for (const row of rows) {
    const lacks = [];
    if (row.qty === null) lacks.push('数量');
    if (row.price === null) lacks.push('单价');
    if (row.amount === null) lacks.push('合价');

    if (lacks.length) {
      // 缺字段的行算不出「数量 × 单价」—— 只报"无法核对"，绝不伪造算术结论
      unverifiable++;
      findings.push({
        level: 'P1',
        category: '报价算术',
        message: `${row.where || `第${row.line}行`}「${row.name}」缺少：${lacks.join('、')}，该行算术无法核对`,
        advice: '补齐该行报价。报价缺漏项在多数招标文件中按无效投标或不利修正处理。',
      });
      continue;
    }

    checked++;
    const expected = round2(row.qty * row.price);
    const diff = round2(row.amount - expected);
    if (Math.abs(diff) > TOLERANCE) {
      findings.push({
        level: 'P0',
        category: '报价算术',
        message: `${row.where || `第${row.line}行`}「${row.name}」合价 ${fmt(row.amount)} 与 数量 × 单价 = ${fmt(expected)} 不符（差 ${fmt(diff)}）`,
        advice: '核对该项合价，按招标文件规定的修正规则处理；报价修正可能改变中标结果。',
      });
    }
  }

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  return {
    bidder: bidder.name,
    verdict: p0 > 0 ? 'HIGH_RISK' : (p1 > 0 ? 'MEDIUM_RISK' : 'LOW_RISK'),
    summary: { p0, p1, p2, total: findings.length },
    rows: rows.length,
    rows_usable: rowsUsable.length,
    rows_arithmetic_checked: checked,
    rows_unverifiable: unverifiable,
    findings,
  };
}

/**
 * 执行本包的逐家报价算术校验。
 * @param {Object|Array} payload { bidders: [{ name, items?, text? }] } 或直接给 bidders 数组
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return {
      status: 'insufficient_input',
      missing: [`入参不是对象或数组（收到的是 ${typeof payload}）`],
      advice: '传 {"bidders":[{"name":"…","items":[{"name","qty","price","amount"}]}, …]}；或直接传 bidders 数组。',
    };
  }
  if (payload && !Array.isArray(payload) && payload.bidders !== undefined && !Array.isArray(payload.bidders)) {
    return {
      status: 'insufficient_input',
      missing: [`bidders 不是数组（收到的是 ${typeof payload.bidders}）`],
      advice: 'bidders 需要是数组：[{"name":"投标人甲","items":[{"name":"钢筋制安","qty":10,"price":100,"amount":1000}]}, …]。',
    };
  }

  const rawList = Array.isArray(payload) ? payload : (payload && Array.isArray(payload.bidders) ? payload.bidders : []);
  if (!rawList.length) {
    return {
      status: 'insufficient_input',
      missing: ['bidders 是空的：没有收到任何投标人的材料'],
      advice: '请传 bidders 数组，至少 1 家，每家带报价明细 items（或可解析成表格的 text）。',
    };
  }

  const bidders = rawList.map((b, i) => {
    const o = (b && typeof b === 'object') ? b : {};
    const name = String(o.name != null ? o.name : (o.bidder != null ? o.bidder : `投标人${i + 1}`));
    // ⛔ 必须把订阅版要用的字段带过来：本包只用到 name/items/text，
    //    第一版忘了带 price/denials，结果「报价离散度分析」永远算不出（= 假装跑过了）。
    return {
      name, items: o.items, text: typeof o.text === 'string' ? o.text : '',
      price: o.price !== undefined ? o.price : (o['投标总价'] !== undefined ? o['投标总价'] : o.totalPrice),
      denials: o.denials, contacts: o.contacts,
    };
  });

  const perBidder = bidders.map((b) => checkOneBidder(b));
  const withRows = perBidder.filter((b) => b.rows_usable > 0);
  if (!withRows.length) {
    const lacking = perBidder.map((b) => `${b.bidder}（${b.findings[0] ? b.findings[0].message.replace(/^本家报价算术未执行：/, '') : '无报价明细'}）`);
    return {
      status: 'insufficient_input',
      missing: [
        '没有任何一家提供了可校验的报价明细行（数量 / 单价 / 合价 至少要有一个能解析成数字）',
        `逐家情况：${lacking.join('；')}`,
      ],
      advice: '每家的报价写成 items [{"name":"钢筋制安","qty":10,"price":100,"amount":1000}]，'
        + '或给「名称 数量 单价 合价」格式的报价文本；数字不要夹带说明文字。',
    };
  }

  let totalP0 = 0;
  let totalP1 = 0;
  let totalP2 = 0;
  for (const b of perBidder) {
    totalP0 += b.summary.p0;
    totalP1 += b.summary.p1;
    totalP2 += b.summary.p2;
  }
  const highRisk = perBidder.filter((b) => b.verdict === 'HIGH_RISK').map((b) => b.bidder);
  const unchecked = perBidder.filter((b) => b.verdict === 'NOT_CHECKED').map((b) => b.bidder);

  /* --- 订阅版追加的六项检查 --- */
  const extraFindings = [];
  for (const b of bidders) {
    checkDenials(b, extraFindings);
    checkPlaceholders(b, extraFindings);
    checkBasicElements(b, extraFindings);
  }
  checkCrossBidderCrossLead(bidders, extraFindings);
  const dispersion = checkPriceDispersion(bidders, extraFindings);
  // informational 的项只作说明（例如"离散度正常"），不计入风险计数
  for (const f of extraFindings) {
    if (f.informational) continue;
    if (f.level === 'P0') totalP0 += 1;
    else if (f.level === 'P1') totalP1 += 1;
    else totalP2 += 1;
  }

  const overall = totalP0 > 0 ? 'HIGH_RISK'
    : (totalP1 > 0 ? 'MEDIUM_RISK' : (unchecked.length ? 'NEEDS_INPUT' : 'LOW_RISK'));

  const result = {
    status: 'success',
    service_type: 'BATCH_BID_CHECKUP_FULL',
    scope: {
      checks: CHECKS_GIVEN,
      full_tier: paid,
      bidders: bidders.length,
      bidders_with_rows: withRows.length,
      bidders_unchecked: unchecked.length,
      rows_total: perBidder.reduce((n, b) => n + b.rows, 0),
      rows_usable_total: perBidder.reduce((n, b) => n + b.rows_usable, 0),
      rows_arithmetic_checked: perBidder.reduce((n, b) => n + b.rows_arithmetic_checked, 0),
      tolerance: TOLERANCE,
      executed_locally: true,
      network_used: false,
    },
    per_bidder: perBidder,
    findings: extraFindings,
    price_dispersion: dispersion,
    summary: {
      bidders: bidders.length,
      checked_bidders: withRows.length,
      unchecked_bidders: unchecked.length,
      unchecked_bidder_names: unchecked,
      high_risk_bidders: highRisk,
      total_p0: totalP0,
      total_p1: totalP1,
      total_p2: totalP2,
      overall_verdict: overall,
      omitted: 0,
    },
    note: '本结果覆盖全部 7 项检查（完整档无未执行项）。'
      + 'verdict 为 NOT_CHECKED 的家表示材料里没有可校验的报价行 —— 那是"没查"，不是"查过且一致"。',
    disclaimer: '只做算术核对，不做技术标评审、不做资格判定、不构成评标意见；'
      + '结论可由第三方用同一份输入复算。',
  };

  buildRiskRankedActions(extraFindings, result);

  return { status: 'success', result };
}

module.exports = {
  run,
  parseText,
  pickNumber,
  fmt,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
