'use strict';
/**
 * tender-compliance-audit.js —— 招投标全案合规审计（本包）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 本包只做两项检查，别无其他：
 *   1. 逐家报价算术校验 —— 每行核对「合价 = 数量 × 单价」，按投标人归集；
 *   2. 模板占位符扫描   —— 搜出残留的【…】、XXX、＿＿、（此处填写）这类没替换干净的地方。
 *
 * **订阅版（买断版）：上面两项 + 下面四项，共 6 项全部执行**
 *   招标文件要素体检、合同草案必备条款与陷阱条款扫描、跨家串通线索、统一整改清单与阻断判定。
 *   因此订阅版会读本包明确不读的 `tenderText`（招标文件正文）与 `contractText`（合同草案正文）。
 * 材料没给到的检查**不会假装跑过**：记进 `checks_not_run`，阻断判定给 `null`——
 * 绝不把"没查"说成"通过"。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const TOLERANCE = 0.01;

const CHECKS_GIVEN = [
  '逐家报价算术校验', '模板占位符扫描',
  '招标文件要素体检', '合同草案必备条款与陷阱条款扫描', '跨家串通线索', '统一整改清单与阻断判定',
];

// 订阅版没有"未执行"的检查项（材料没给到的会进 checks_not_run，不会被说成"跑过了"）
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

/* ------------------------------------------------------------ 占位符扫描
 * 记忆里沉淀的真实失效模式：「关键词命中式校验会被未填模板骗过」
 * —— 空白模板里的【填写：xxx】本身就含关键词。所以完备性校验必须与占位符扫描解耦。
 */

const PLACEHOLDER_PATTERNS = [
  { name: '中文方括号占位', re: /【[^】\n]{0,40}】/g },
  { name: '英文占位词', re: /[Xx]{3,}|TODO|TBD|FIXME|Lorem ipsum/g },
  { name: '下划线占位', re: /_{3,}|＿{2,}/g },
  { name: '括号内填写提示', re: /[（(][^）)\n]{0,20}?(?:此处|请|自行|需要)?(?:填写|填入|补充|待定|待填|填)[^）)\n]{0,20}?[）)]/g },
  { name: '空括号', re: /[（(]\s*[)）]/g },
  { name: '未替换变量', re: /\{\{[^}\n]{1,30}\}\}|\$\{[^}\n]{1,30}\}/g },
  { name: '全角空括号', re: /［\s*］|\[\s*\]/g },
];

function scanPlaceholders(text) {
  const t = String(text == null ? '' : text);
  const hits = [];
  for (const p of PLACEHOLDER_PATTERNS) {
    const m = t.match(p.re);
    if (m && m.length) hits.push({ type: p.name, count: m.length, samples: [...new Set(m)].slice(0, 3) });
  }
  return { total: hits.reduce((a, b) => a + b.count, 0), hits };
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
  const text = bidder.text;
  if (text.trim().length >= 2) return { rows: parseText(text), source: 'text', raw_count: 0 };
  return { rows: [], source: 'none', raw_count: 0 };
}

/* ================================================================== 订阅版追加检查
 * 本包声明了 4 项"未执行"的检查，订阅版**逐项真的执行**（不多做、不少做）：
 *   招标文件要素体检 / 合同草案必备条款与陷阱条款扫描 / 跨家串通线索 / 统一整改清单与阻断判定
 * 因此订阅版会读本包**明确不读**的 `tenderText`（招标文件正文）与 `contractText`（合同草案正文）。
 * 材料没给到的检查**不会假装跑过**：会记进 `checks_not_run` 并说明缺什么，阻断判定给 `null`。
 * ================================================================ */

const TENDER_ELEMENTS = [
  ['项目名称', /项目名称|工程名称|采购项目/],
  ['招标编号', /招标编号|项目编号|采购编号|标段编号/],
  ['招标人', /招标人|采购人|招标单位/],
  ['投标截止时间', /投标截止|递交投标文件截止|开标时间|响应截止/],
  ['投标保证金', /投标保证金|保证金金额|保证金/],
  ['评标办法', /评标办法|评审办法|评标标准|综合评估法|经评审的最低/],
  ['资格要求', /资格要求|投标人资格|资质要求|合格投标人/],
  ['合同主要条款', /合同主要条款|合同条款|付款方式|合同价款/],
  ['投标文件组成', /投标文件组成|投标文件的组成|投标文件格式|应提交的/],
];

const CONTRACT_REQUIRED = [
  ['标的/工程内容', /标的|工程内容|服务内容|货物名称|承包范围/],
  ['合同价款', /合同价款|合同价格|合同金额|价款|总价/],
  ['工期/交货期', /工期|交货期|服务期限|履行期限|完成时间/],
  ['质量标准与验收', /质量标准|验收标准|验收方式|合格标准/],
  ['付款方式', /付款方式|支付方式|付款节点|结算方式/],
  ['违约责任', /违约责任|违约金|赔偿/],
  ['争议解决', /争议解决|仲裁|诉讼|管辖/],
];

const CONTRACT_TRAPS = [
  [/无限连带责任|连带责任.*无限/, '无限连带责任'],
  [/甲方有权(随时|单方)?(解除|终止)|发包人有权随时解除/, '单方解除权'],
  [/不予调整|不作调整|概不调整|包死|固定总价.*不因/, '价款包死不予调整'],
  [/放弃(索赔|追偿|抗辩|诉讼|仲裁)/, '放弃索赔/抗辩权'],
  [/自动续期|自动续约|期满自动顺延/, '自动续期'],
  [/全部风险由(乙方|承包方|供应方|卖方)承担|风险.*全部由.*承担/, '风险单方承担'],
  [/视为(已)?认可|逾期(未|不)回复视为|默认验收/, '沉默视为认可'],
  [/罚款(不设上限|无上限)|违约金.*不设上限/, '罚款无上限'],
  [/概不负责|不负任何责任|不承担任何责任/, '免责条款'],
  [/最终解释权/, '最终解释权归一方'],
];

const TENDER_ELEMENT_CHECK = { level: 'P1', label: '招标文件要素体检' };
const CONTRACT_CLAUSE_CHECK = { level: 'P0', label: '合同草案必备条款与陷阱条款扫描' };
const CROSS_LEAD_CHECK = { level: 'P0', label: '跨家串通线索' };
const UNIFIED_CHECK = { level: 'P1', label: '统一整改清单与阻断判定' };

const TENDER_BASIS = {
  '招标文件要素体检': '《招标投标法》第十六条、第十九条（招标文件应载明实质性要求与评标办法）',
  '合同草案必备条款与陷阱条款扫描': '《民法典》第四百七十条（合同一般条款）与《招标投标法》第四十六条',
  '跨家串通线索': '《招标投标法实施条例》第四十条',
  '统一整改清单与阻断判定': '内部整改用：P0 未清零不建议提交',
};

function tRaw(text) {
  return String(text == null ? '' : text).replace(/\r\n?/g, '\n');
}

function tSegments(text) {
  return new Set(tRaw(text).split(/\n+|(?<=[。；;])/)
    .map((x) => x.replace(/\s+/g, ' ').trim())
    .filter((x) => x.length >= 20 && /[\u4e00-\u9fa5]/.test(x)));
}

/* --- 1) 招标文件要素体检 --- */
function checkTenderElements(tenderText, findings, notRun) {
  const text = tRaw(tenderText);
  if (text.trim().length < 20) {
    notRun.push({ check: '招标文件要素体检', reason: '没有给 tenderText（招标文件正文），无法体检其要素' });
    return;
  }
  const missing = TENDER_ELEMENTS.filter(([, re]) => !re.test(text)).map(([n]) => n);
  if (!missing.length) return;
  findings.push({
    type: 'TENDER_ELEMENT_MISSING',
    level: TENDER_ELEMENT_CHECK.level,
    label: TENDER_ELEMENT_CHECK.label,
    basis: TENDER_BASIS['招标文件要素体检'],
    detail: `招标文件里没找到 ${missing.length} 项要素：${missing.join('、')}`,
    evidence: { missing, checked: TENDER_ELEMENTS.map(([n]) => n) },
    advice: '缺"评标办法/投标截止时间/保证金"这类要素会直接导致招标文件被质疑或澄清：'
      + '发布前补齐，或确认这些内容写在了别处（附件/公告）并注明。',
  });
}

/* --- 2) 合同草案必备条款与陷阱条款扫描 --- */
function checkContract(contractText, findings, notRun) {
  const text = tRaw(contractText);
  if (text.trim().length < 20) {
    notRun.push({ check: '合同草案必备条款与陷阱条款扫描', reason: '没有给 contractText（合同草案正文），无法扫描条款' });
    return;
  }
  const missing = CONTRACT_REQUIRED.filter(([, re]) => !re.test(text)).map(([n]) => n);
  if (missing.length) {
    findings.push({
      type: 'CONTRACT_CLAUSE_MISSING',
      level: 'P1',
      label: CONTRACT_CLAUSE_CHECK.label,
      basis: TENDER_BASIS['合同草案必备条款与陷阱条款扫描'],
      detail: `合同草案里没找到 ${missing.length} 项必备条款：${missing.join('、')}`,
      evidence: { missing },
      advice: '必备条款缺失会在签约阶段变成扯皮：签约前补齐标的、价款、工期、验收、付款、违约、争议解决。',
    });
  }
  for (const [re, label] of CONTRACT_TRAPS) {
    const m = text.match(re);
    if (!m) continue;
    const idx = text.indexOf(m[0]);
    findings.push({
      type: 'CONTRACT_TRAP_CLAUSE',
      level: CONTRACT_CLAUSE_CHECK.level,
      label: CONTRACT_CLAUSE_CHECK.label,
      basis: TENDER_BASIS['合同草案必备条款与陷阱条款扫描'],
      detail: `合同草案里出现陷阱条款：${label}（原文「${m[0]}」）`,
      evidence: { trap: label, phrase: m[0], context: text.slice(Math.max(0, idx - 30), idx + m[0].length + 30).replace(/\s+/g, ' ') },
      advice: '这类条款把风险单向压给一方：签约前要求删除或改为对等表述，并留存谈判记录。',
    });
  }
}

/* --- 3) 跨家串通线索 --- */
function tContacts(text) {
  const s = String(text == null ? '' : text).replace(/\u3000/g, ' ').replace(/[\s\u00a0]+/g, ' ');
  const person = (s.match(/(?:项目经理|项目负责人|联系人|委托代理人)\s*[:：]?\s*([\u4e00-\u9fa5]{2,4})/) || [])[1] || null;
  return {
    phones: s.match(/1[3-9]\d{9}/g) || [],
    emails: s.match(/[\w.+-]+@[\w-]+\.[\w.]+/g) || [],
    uscc: s.match(/\b[0-9A-HJ-NPQRTUWXY]{18}\b/g) || [],
    person: person ? [person] : [],
  };
}

function checkCrossLeads(bidders, findings) {
  const kinds = [['phones', '电话'], ['emails', '邮箱'], ['uscc', '统一社会信用代码'], ['person', '关键人员']];
  for (const [field, label] of kinds) {
    const map = new Map();
    for (const b of bidders) {
      for (const v of new Set(tContacts(b.text)[field])) {
        if (!map.has(v)) map.set(v, new Set());
        map.get(v).add(b.name);
      }
    }
    for (const [value, who] of map) {
      if (who.size < 2) continue;
      findings.push({
        type: 'CROSS_BIDDER_LEAD',
        level: CROSS_LEAD_CHECK.level,
        label: CROSS_LEAD_CHECK.label,
        basis: TENDER_BASIS['跨家串通线索'],
        detail: `${[...who].join(' 与 ')} 的${label}相同`,
        evidence: { kind: label, bidders: [...who], value: field === 'person' ? `${String(value)[0]}*` : String(value).replace(/^(\d{3})\d+(\d{2})$/, '$1****$2') },
        advice: '同一联系方式/同一关键人员出现在多家投标文件里，属于法定视为串通的情形之一：留存证据并报告。',
      });
    }
  }
  const segMap = new Map();
  for (const b of bidders) {
    for (const seg of tSegments(b.text)) {
      if (!segMap.has(seg)) segMap.set(seg, new Set());
      segMap.get(seg).add(b.name);
    }
  }
  let shown = 0;
  for (const [seg, who] of segMap) {
    if (who.size < 2 || shown >= 10) continue;
    shown += 1;
    findings.push({
      type: 'CROSS_BIDDER_LEAD',
      level: CROSS_LEAD_CHECK.level,
      label: CROSS_LEAD_CHECK.label,
      basis: TENDER_BASIS['跨家串通线索'],
      detail: `${[...who].join(' 与 ')} 的材料里有 ${seg.length} 个字完全相同的一整段`,
      evidence: { segment: seg.length > 70 ? seg.slice(0, 70) + '…' : seg, bidders: [...who] },
      advice: '整段一致通常来自同一份底稿：核对各家的文件来源与制作记录。',
    });
  }
}

/* --- 4) 统一整改清单与阻断判定 --- */
function buildUnified(perBidder, extraFindings, result) {
  const rank = { P0: 0, P1: 1, P2: 2 };
  const items = [];
  for (const b of perBidder) {
    for (const f of (b.findings || [])) {
      items.push({ level: f.level || 'P1', label: '报价算术校验', scope: b.bidder, detail: f.message });
    }
  }
  for (const f of extraFindings) {
    items.push({ level: f.level, label: f.label, scope: (f.evidence && f.evidence.bidder) || ((f.evidence && f.evidence.bidders) || []).join('、') || '全局', detail: f.detail });
  }
  items.sort((a, b) => (rank[a.level] - rank[b.level]) || String(a.label).localeCompare(String(b.label)));
  result.actions = items.map((x, i) => ({ order: i + 1, ...x }));
  const p0 = items.filter((x) => x.level === 'P0').length;
  const p1 = items.filter((x) => x.level === 'P1').length;
  result.action_summary = { total: items.length, p0, p1, p2: items.filter((x) => x.level === 'P2').length };

  // 阻断判定：有 P0 ⇒ blocked=true；材料不足以做完整判定 ⇒ null（**不许把"没查"说成"通过"**）
  const notRun = result.checks_not_run || [];
  if (p0 > 0) {
    result.blocked = true;
    result.blocking_reasons = items.filter((x) => x.level === 'P0').map((x) => `${x.label}：${x.detail}`);
  } else if (notRun.length) {
    result.blocked = null;
    result.blocking_reasons = ['材料不全，无法给出"不阻断"的结论：' + notRun.map((x) => x.check).join('、')];
  } else {
    result.blocked = false;
    result.blocking_reasons = [];
  }
}

/* ------------------------------------------------------------------ 主入口 */

/** 单家投标人：报价算术 + 模板占位符 */
function checkOneBidder(bidder) {
  const findings = [];

  /* --- 1) 逐家报价算术校验 --- */
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
        : (bidder.text.trim()
          ? `text 有 ${bidder.text.trim().length} 个字符，但没有识别出可校验的报价明细行`
          : '既没有 items（结构化明细），也没有 text（可解析的报价表文本）'));
    findings.push({
      level: 'P2',
      category: '报价算术',
      message: `本家报价算术未执行：${why}`,
      advice: '补齐 items [{"name","qty","price","amount"}]，或提供「名称 数量 单价 合价」格式的报价文本。',
    });
  } else {
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
  }

  /* --- 2) 模板占位符扫描 --- */
  const placeholders = scanPlaceholders(bidder.text);
  if (placeholders.total > 0) {
    const detail = placeholders.hits
      .map((h) => `${h.type}×${h.count}${h.samples.length ? `（如「${h.samples.join('」「')}」）` : ''}`)
      .join('、');
    findings.push({
      level: placeholders.total >= 5 ? 'P0' : 'P1',
      category: '模板未填',
      message: `发现 ${placeholders.total} 处未替换的模板占位符：${detail}`,
      advice: '递交前必须替换全部占位符，空白模板会被判未实质响应。',
      evidence: placeholders.hits,
    });
  }

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  // 「可体检」= 有可核对的报价行，或有可扫占位符的正文；
  // 有行但一个数字都没有时不算可体检（那句话已经写成 P2 的"未执行"提示）
  const checkable = rowsUsable.length > 0 || bidder.text.trim().length >= 2;

  return {
    bidder: bidder.name,
    verdict: !checkable ? 'NOT_CHECKED'
      : (p0 > 0 ? 'HIGH_RISK' : (p1 > 0 ? 'MEDIUM_RISK' : 'LOW_RISK')),
    summary: { p0, p1, p2, total: findings.length },
    rows: rows.length,
    rows_usable: rowsUsable.length,
    rows_arithmetic_checked: checked,
    rows_unverifiable: unverifiable,
    placeholders_total: placeholders.total,
    findings,
  };
}

/**
 * 执行本包的两项AI体检。
 * @param {Object|Array} payload { bidders: [{ name, items?, text? }] } 或直接给 bidders 数组
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return {
      status: 'insufficient_input',
      missing: [`入参不是对象或数组（收到的是 ${typeof payload}）`],
      advice: '传 {"bidders":[{"name":"…","items":[{"name","qty","price","amount"}],"text":"投标文件正文…"}]}；或直接传 bidders 数组。',
    };
  }
  if (payload && !Array.isArray(payload) && payload.bidders !== undefined && !Array.isArray(payload.bidders)) {
    return {
      status: 'insufficient_input',
      missing: [`bidders 不是数组（收到的是 ${typeof payload.bidders}）`],
      advice: 'bidders 需要是数组：[{"name":"投标人甲","items":[…],"text":"…"}, …]，至少 1 家。',
    };
  }

  const rawList = Array.isArray(payload) ? payload : (payload && Array.isArray(payload.bidders) ? payload.bidders : []);
  if (!rawList.length) {
    return {
      status: 'insufficient_input',
      missing: ['bidders 是空的：没有收到任何投标人的材料'],
      advice: '请传 bidders 数组，至少 1 家；每家可带报价明细 items 与投标材料正文 text。',
    };
  }

  const bidders = rawList.map((b, i) => {
    const o = (b && typeof b === 'object') ? b : {};
    const name = String(o.name != null ? o.name : (o.bidder != null ? o.bidder : `投标人${i + 1}`));
    return { name, items: o.items, text: typeof o.text === 'string' ? o.text : '' };
  });

  const perBidder = bidders.map((b) => checkOneBidder(b));
  const checkable = perBidder.filter((b) => b.verdict !== 'NOT_CHECKED');
  if (!checkable.length) {
    const lacking = perBidder.map((b) => {
      const detail = b.findings[0] ? b.findings[0].message.replace(/^本家报价算术未执行：/, '') : '无材料';
      return `${b.bidder}（${detail}）`;
    });
    return {
      status: 'insufficient_input',
      missing: [
        '没有任何一家的材料可以体检：既没有可校验的报价明细行，也没有可用于扫描占位符的正文',
        `逐家情况：${lacking.join('；')}`,
      ],
      advice: '每家至少给一样：报价明细 items [{"name","qty","price","amount"}]，或投标材料正文 text（至少 2 个字符）。',
    };
  }

  let totalP0 = 0;
  let totalP1 = 0;
  let totalP2 = 0;
  let placeholderTotal = 0;
  for (const b of perBidder) {
    totalP0 += b.summary.p0;
    totalP1 += b.summary.p1;
    totalP2 += b.summary.p2;
    placeholderTotal += b.placeholders_total;
  }
  const highRisk = perBidder.filter((b) => b.verdict === 'HIGH_RISK').map((b) => b.bidder);
  const unchecked = perBidder.filter((b) => b.verdict === 'NOT_CHECKED').map((b) => b.bidder);

  /* --- 订阅版追加的四项检查 --- */
  const extraFindings = [];
  const checksNotRun = [];
  checkTenderElements(payload && payload.tenderText, extraFindings, checksNotRun);
  checkContract(payload && payload.contractText, extraFindings, checksNotRun);
  checkCrossLeads(bidders, extraFindings);
  for (const f of extraFindings) {
    if (f.level === 'P0') totalP0 += 1;
    else if (f.level === 'P1') totalP1 += 1;
    else totalP2 += 1;
  }

  const overall = totalP0 > 0 ? 'HIGH_RISK'
    : (totalP1 > 0 ? 'MEDIUM_RISK' : (unchecked.length ? 'NEEDS_INPUT' : 'LOW_RISK'));

  const result = {
    status: 'success',
    service_type: 'TENDER_COMPLIANCE_AUDIT_FULL',
    scope: {
      checks: CHECKS_GIVEN,
      full_tier: paid,
      bidders: bidders.length,
      bidders_checkable: checkable.length,
      bidders_unchecked: unchecked.length,
      rows_total: perBidder.reduce((n, b) => n + b.rows, 0),
      rows_usable_total: perBidder.reduce((n, b) => n + b.rows_usable, 0),
      rows_arithmetic_checked: perBidder.reduce((n, b) => n + b.rows_arithmetic_checked, 0),
      placeholders_total: placeholderTotal,
      scanned_inputs: '完整档会扫：各家投标材料正文 bidders[].text + 招标文件 tenderText + 合同草案 contractText',
      tolerance: TOLERANCE,
      executed_locally: true,
      network_used: false,
      full_tier: '完整档执行全部 6 项；材料没给到的检查记在 checks_not_run 里',

    },
    findings: extraFindings,
    checks_not_run: checksNotRun,
    bid_checkup: {
      per_bidder: perBidder,
      summary: {
        bidders: bidders.length,
        checked_bidders: checkable.length,
        unchecked_bidders: unchecked.length,
        unchecked_bidder_names: unchecked,
        high_risk_bidders: highRisk,
        total_p0: totalP0,
        total_p1: totalP1,
        total_p2: totalP2,
        placeholders_total: placeholderTotal,
      },
    },
    summary: {
      bidders: bidders.length,
      total_p0: totalP0,
      total_p1: totalP1,
      total_p2: totalP2,
      placeholders_total: placeholderTotal,
      high_risk_bidders: highRisk,
      overall_verdict: overall,
      omitted: 0,
    },
    note: '本结果只覆盖「逐家报价算术校验」与「模板占位符扫描」；其余检查项见 checks_withheld，本次未执行。'
      + 'verdict 为 NOT_CHECKED 的家表示材料里没有可体检的内容 —— 那是"没查"，不是"查过且干净"。',
    disclaimer: '只做AI核对，不做技术标评审、不做资格判定、不构成评标意见；'
      + '结论可由第三方用同一份输入复算。',
  };

  buildUnified(perBidder, extraFindings, result);
  if (result.blocked === true) {
    result.findings.push({
      type: 'UNIFIED_ACTIONS',
      level: UNIFIED_CHECK.level,
      label: UNIFIED_CHECK.label,
      basis: TENDER_BASIS['统一整改清单与阻断判定'],
      detail: `共 ${result.action_summary.total} 条整改项，其中 ${result.action_summary.p0} 条为 P0 ⇒ 判定为**阻断**`,
      evidence: { blocking_reasons: result.blocking_reasons.slice(0, 3) },
      advice: '按清单从 P0 开始整改；P0 未清零前不建议提交。',
    });
  }

  return { status: 'success', result };
}

module.exports = {
  run,
  parseText,
  scanPlaceholders,
  pickNumber,
  fmt,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
