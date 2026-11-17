'use strict';
/**
 * quote-audit.js —— 投标报价AI审查（免费档）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 免费档只做两项检查，别无其他：
 *   1. 分项算术校验 —— 逐行核对「合价 = 数量 × 单价」，不符时给出差额；
 *   2. 缺漏项提示   —— 数量 / 单价 / 合价 任一为空的行单独指出。
 *
 * 刻意不实现（那些属于本版本范围之外的检查项，见 CHECKS_WITHHELD）：
 *   分项加总校验、最高投标限价校验、大小写金额互校、投标保证金比例校验、不平衡报价预警。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const TOLERANCE = 0.01;   // 金额容差（与投标报价的两位小数口径一致）

const CHECKS_GIVEN = ['分项算术校验', '缺漏项提示'];

const CHECKS_WITHHELD = [
  '分项加总校验',
  '最高投标限价校验',
  '大小写金额互校',
  '投标保证金比例校验',
  '不平衡报价预警',
];

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

/** 金额展示：统一两位小数、带千分位；空值给「—」而不是 0（不能把"没填"显示成"0"） */
function fmt(v) {
  if (v === null || v === undefined) return '—';
  const n = Number(v);
  if (!Number.isFinite(n)) return '—';
  return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice: advice };
}

/* ------------------------------------------------- 报价文本 → 明细行解析
 * 与「宁可失败也不猜错数字」同一原则：只接受列结构明确的表格行，
 * 有歧义就跳过，一行都没解析出来就返回空数组（由调用方给出明确的材料不足提示）。
 */

/** 表头关键词 → 标准字段 */
const HEADER_ALIASES = {
  name: ['名称', '项目名称', '分项名称', '材料名称', '设备名称', '项目', '分项', '品名', '货物名称'],
  unit: ['单位', '计量单位'],
  qty: ['数量', '工程量', '数 量'],
  price: ['单价', '综合单价', '单价（元）', '综合单价（元）', '单价(元)'],
  amount: ['合价', '金额', '合计', '总价', '合价（元）', '金额（元）', '合价(元)'],
  seq: ['序号', '编号', '项次', '序 号'],
};

/** 常见计量单位：用于把「名称」和「数量」之间的单位词切出来 */
const UNIT_TOKENS = new Set([
  't', 'T', 'kg', 'KG', 'g', '吨', '公斤', '千克', 'm', 'M', 'm2', 'm3', '㎡', 'm³',
  '米', '延米', '平方米', '立方米', 'km', '公里', '项', '个', '台', '套', '组', '批',
  '樘', '处', '座', '孔', '根', '块', '片', '张', '条', '只', '付', '对', '户', '人',
  '工日', '台班', '月', '年', '次', '站', '系统', 'km·对',
]);

/** 纯数字（允许千分位与负号） */
const NUM_TOKEN = /^-?\d{1,3}(?:,\d{3})+(?:\.\d+)?$|^-?\d+(?:\.\d+)?$/;

function numOf(token) {
  if (typeof token !== 'string') return null;
  const t = token.trim();
  if (!NUM_TOKEN.test(t)) return null;
  const n = Number(t.replace(/,/g, ''));
  return Number.isFinite(n) ? n : null;
}

/** 按分隔符切列：只去掉首尾空列，**保留中间空列**（Excel 里空格子会产生连续两个 Tab，
 *  删掉中间空列会让数量/单价/合价整体前移 —— 把数字安到错误的列上比直接报错危险得多） */
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

/** 该行是否是表头；是则返回列位置映射 */
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

/** 无表头时的兜底：行尾必须是连续的「数量 单价 合价」或「数量 单价」 */
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
  if (nums.length < 2 || nums.length > 3) return null;   // 4 个以上数字无法判断列义，放弃
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

/**
 * 解析报价文本。
 * @param {String} text
 * @returns {Array<{name:string,qty:number|null,price:number|null,amount:number|null,line:number}>}
 */
function parseText(text) {
  const raw = String(text == null ? '' : text);
  if (!raw.trim()) return [];

  const items = [];
  let headerMap = null;
  const lines = raw.split(/\r?\n/);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNo = i + 1;
    const tokens = splitRow(line);
    if (tokens.length < 2) continue;

    // 先判表头再判噪音：表头行常以「序号」开头，会被噪音规则误杀
    const asHeader = parseHeader(tokens);
    if (asHeader) { headerMap = asHeader; continue; }

    if (isNoiseLine(line)) continue;

    const row = headerMap ? rowByHeader(tokens, headerMap, lineNo) : rowByTailNumbers(tokens, lineNo);
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
  // 只有"既没有名称、三个数也都没有"的纯垃圾条目才丢弃。
  // 有名称但数字为空的行**必须留下** —— 它正是「缺漏项」要报的对象；
  // 静默丢掉它就等于把"没填"变成"查过且没问题"，那是最危险的一类假结论。
  if (qty === null && price === null && amount === null && !String(rawName == null ? '' : rawName).trim()) return null;
  return { name, qty, price, amount, line: idx + 1, where: `第${idx + 1}项` };
}

function hasAnyNumber(row) {
  return row.qty !== null || row.price !== null || row.amount !== null;
}

/**
 * 收集待校验的明细行。
 * 依次尝试 items（结构化）→ text（报价文本）；两者都拿不到可校验的行时，
 * 返回 { rows: [], missing, advice }，由 run() 转成"材料不足"。
 */
function collectRows(payload) {
  // 顶层直接给数组时按 items 处理（等价于 { items: [...] }），省得调用方多包一层
  if (Array.isArray(payload)) payload = { items: payload };
  const objectInput = payload && typeof payload === 'object' && !Array.isArray(payload);

  if (objectInput && Array.isArray(payload.items) && payload.items.length) {
    const raw = payload.items;
    const rows = [];
    for (let i = 0; i < raw.length; i++) {
      const r = itemRow(raw[i], i);
      if (r) rows.push(r);
    }
    if (!rows.length || !rows.some(hasAnyNumber)) {
      // 「有行但一个数字都没有」与「一行都没有」都算材料不足：
      // 这两种情况下算术校验根本无法执行，必须明说，而不是给一个空结论
      const why = rows.length
        ? `items 有 ${rows.length} 行，但每一行的 数量 / 单价 / 合价 都是空的，没有任何一行可以核对`
        : `items 有 ${raw.length} 行，但没有任何一行能解析出数字：数量 / 单价 / 合价必须至少有一个是数字`;
      return {
        rows: [],
        missing: [why],
        advice: 'items 的每一行写成 {"name":"钢筋制安","qty":10,"price":100,"amount":1000}；数字不要夹带说明文字。',
      };
    }
    return { rows, source: 'items' };
  }

  let text = '';
  if (typeof payload === 'string') text = payload;
  else if (objectInput && typeof payload.text === 'string') text = payload.text;
  else if (objectInput && typeof payload.content === 'string') text = payload.content;
  else if (objectInput && payload.text !== undefined && payload.text !== null) {
    return {
      rows: [],
      missing: [`text 不是字符串（收到的是 ${Array.isArray(payload.text) ? 'array' : typeof payload.text}）`],
      advice: '把报价表粘贴成字符串传给 text，或改用 items 结构化明细。',
    };
  }

  const trimmed = String(text).trim();
  if (!trimmed) {
    return {
      rows: [],
      missing: ['没有收到任何报价材料：text（或 content）为空，items 也不是非空数组'],
      advice: '两种入参二选一：① text 粘贴报价表（需为「名称 数量 单价 合价」这样的表格行）；'
        + '② items 结构化明细 [{"name","qty","price","amount"}]。',
    };
  }
  if (trimmed.length < 2) {
    return {
      rows: [],
      missing: [`text 只有 1 个字符（「${trimmed}」），不构成一份可校验的报价材料`],
      advice: '请粘贴完整的报价表文本，或改用 items 结构化明细。',
    };
  }

  const rows = parseText(trimmed);
  if (!rows.length) {
    return {
      rows: [],
      missing: [`这段 text（${trimmed.length} 个字符）里没有识别出可校验的报价明细行`],
      advice: 'text 需为「名称 数量 单价 合价」这样的表格行（支持从 Excel 直接粘贴，带表头最佳，'
        + 'Tab / 竖线 / 逗号 / 多空格分隔均可）；格式特殊时请改用 items 结构化入参。',
    };
  }
  return { rows, source: 'text' };
}

/* ------------------------------------------------------------------ 主入口 */

/**
 * 执行免费档的两项AI核对。
 * @param {Object|String} payload {text} | {items} | 纯文本
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const picked = collectRows(payload);
  if (!picked.rows.length) return insufficient(picked.missing, picked.advice);

  const rows = picked.rows;
  const findings = [];
  let checkedRows = 0;
  let missingFieldRows = 0;

  for (const row of rows) {
    const lacks = [];
    if (row.qty === null) lacks.push('数量');
    if (row.price === null) lacks.push('单价');
    if (row.amount === null) lacks.push('合价');

    if (lacks.length) {
      // 缺字段的行算不出「数量 × 单价」，所以只报缺漏，不伪造算术结论
      missingFieldRows++;
      findings.push({
        level: 'P1',
        category: '缺漏项',
        row: row.line,
        name: row.name,
        message: `${row.where || `第${row.line}行`}「${row.name}」缺少：${lacks.join('、')}`,
        advice: '补齐该行的分项报价。报价缺漏项在多数招标文件中按无效投标或不利修正处理。',
      });
      continue;
    }

    checkedRows++;
    const expected = round2(row.qty * row.price);
    const diff = round2(row.amount - expected);
    if (Math.abs(diff) > TOLERANCE) {
      findings.push({
        level: 'P0',
        category: '分项算术',
        row: row.line,
        name: row.name,
        message: `${row.where || `第${row.line}行`}「${row.name}」合价 ${fmt(row.amount)} 与 数量 × 单价 = ${fmt(expected)} 不符（差 ${fmt(diff)}）`,
        advice: '核对该项合价，按招标文件规定的修正规则处理；报价修正可能改变中标结果。',
      });
    }
  }

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'QUOTE_AUDIT_FREE',
    scope: {
      checks: CHECKS_GIVEN,
      source: picked.source,
      rows: rows.length,
      rows_arithmetic_checked: checkedRows,
      rows_with_missing_fields: missingFieldRows,
      tolerance: TOLERANCE,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      p0,
      p1,
      p2,
      total: findings.length,
      rows: rows.length,
      verdict: p0 ? 'ARITHMETIC_MISMATCH' : (p1 ? 'INCOMPLETE_QUOTE' : 'ARITHMETIC_CONSISTENT'),
      omitted: 0,
    },
    note: '本结果只覆盖「分项算术校验」与「缺漏项提示」两项AI核对；'
      + '其余检查项见 checks_withheld，本次未执行，也不会用默认值编造结论。',
    disclaimer: '只做算术核对，不做技术标评审、不做资格判定、不构成评标意见；'
      + '结论可由第三方用同一份输入复算。',
  };

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
