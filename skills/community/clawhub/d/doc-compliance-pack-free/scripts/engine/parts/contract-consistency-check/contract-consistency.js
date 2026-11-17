'use strict';
/**
 * contract-consistency.js —— 合同一致性AI核对（免费档）本地引擎
 *
 * 设计原则（与仓库里"宁可失败也不猜错"的教训一致）：
 *   · 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件
 *     （技能包是从注册表单独下载安装的，跨包引用一定会断）；
 *   · **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）；
 *   · 每条结论都必须能由第三方用同一份输入复算：消息里直接引用出问题的原文、数字、行号；
 *   · 材料不足时绝不输出"未发现问题"，而是返回 insufficient_input 并说明缺什么。
 *
 * 免费档只做六项检查，别无其他：
 *   1. 当事方名称不一致       2. 日期矛盾             3. 金额矛盾
 *   4. 占位符残留             5. 条款交叉引用失效     6. 定义词卫生
 *
 * 中英文合同都支持。刻意不实现本版本范围之外的检查项（见 CHECKS_WITHHELD），
 * 它们只会以"未执行"的名义出现，绝不会被伪造出来。
 */

/* ------------------------------------------------------------------ 常量 */

const CHECKS_GIVEN = [
  '当事方名称不一致',
  '日期矛盾',
  '金额矛盾',
  '占位符残留',
  '条款交叉引用失效',
  '定义词卫生',
];

const CHECKS_WITHHELD = [
  '违约责任与赔偿上限一致性核对',
  '付款节点与比例一致性核对',
  '知识产权归属与授权范围核对',
  '保密期限与例外情形核对',
  '争议解决与管辖条款一致性核对',
  '解除与终止条件核对',
  '签署权限与主体资格核对',
  '附件清单与正文引用完整性核对',
];

/** 一段材料至少要有这么长，才谈得上"核对" */
const MIN_MATERIAL_CHARS = 12;

const TOLERANCE = 0.01;

/* ------------------------------------------------------------ 通用小工具 */

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice: advice };
}

/** 每行的起始偏移，用于"字符位置 → 行号" */
function lineStarts(text) {
  const starts = [0];
  for (let i = 0; i < text.length; i++) {
    if (text.charCodeAt(i) === 10) starts.push(i + 1);
  }
  return starts;
}

function lineOf(starts, idx) {
  let lo = 0;
  let hi = starts.length - 1;
  while (lo < hi) {
    const mid = (lo + hi + 1) >> 1;
    if (starts[mid] <= idx) lo = mid; else hi = mid - 1;
  }
  return lo + 1;
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

function fmtMoney(n) {
  if (n === null || n === undefined || !Number.isFinite(Number(n))) return '—';
  return Number(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function uniq(arr) {
  return Array.from(new Set(arr));
}

/** 名称归一：只去掉空白与常见标点，**不动词干**（"有限公司"与"有限责任公司"必须判为不同） */
function normName(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]/g, '')
    .replace(/[“”"'‘’《》〈〉（）()【】\[\]、,，.。;；:：]/g, '');
}

function clip(s, n) {
  const t = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  return t.length > n ? t.slice(0, n) + '…' : t;
}

/** 只在"连接词"范围内才算相邻证据（大写/单词金额 与 阿拉伯数字 之间必须是这种文本） */
function onlyConnectors(s) {
  const t = String(s == null ? '' : s).replace(
    /(大写|小写|人民币|金额|合计|总计|整|正|圆|元|US\s+Dollars?|United\s+States\s+Dollars?|Dollars?|RMB|CNY|USD)/gi,
    ' '
  );
  return /^[\s\u00A0()（）\[\]【】:：,，、;；\-—–\/|]*$/.test(t);
}

/* ------------------------------------------------------------- 中文数字 */

const CN_DIGITS = {
  '〇': 0, '零': 0, '○': 0,
  '一': 1, '壹': 1, '二': 2, '贰': 2, '两': 2, '三': 3, '叁': 3,
  '四': 4, '肆': 4, '五': 5, '伍': 5, '六': 6, '陆': 6, '七': 7, '柒': 7,
  '八': 8, '捌': 8, '九': 9, '玖': 9,
};

const CN_UNITS = {
  '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000,
};

/** 纯中文数字串 → 数值（支持 万 / 亿 分段）；出现非数字字符返回 null */
function cnToNumber(s) {
  const str = String(s == null ? '' : s);
  if (!str) return null;
  let total = 0;
  let section = 0;
  let current = 0;
  let seen = false;
  for (const ch of str) {
    if (CN_DIGITS[ch] !== undefined) {
      current = CN_DIGITS[ch];
      seen = true;
    } else if (CN_UNITS[ch] !== undefined) {
      const u = CN_UNITS[ch];
      section += (current || 1) * u;
      current = 0;
      seen = true;
    } else if (ch === '万' || ch === '亿' || ch === '兆') {
      const mult = ch === '万' ? 1e4 : (ch === '亿' ? 1e8 : 1e12);
      section = (section + current) * mult;
      total += section;
      section = 0;
      current = 0;
      seen = true;
    } else {
      return null;
    }
  }
  if (!seen) return null;
  return total + section + current;
}

/** 中文大写金额（壹佰万元整 / 叁仟贰佰元伍角）→ 数值 */
function parseCnCapital(token) {
  let t = String(token == null ? '' : token);
  if (!t) return null;
  t = t.replace(/^人民币/, '').replace(/[整正]$/, '');
  let intPart = t;
  let fracPart = '';
  const m = /^(.*?)[元圆](.*)$/.exec(t);
  if (m) {
    intPart = m[1];
    fracPart = m[2];
  } else if (!/[拾佰仟万亿兆]/.test(t)) {
    return null;
  }
  intPart = intPart.replace(/[整正]/g, '') || '零';
  const base = cnToNumber(intPart);
  if (base === null) return null;
  let val = base;
  const jiao = /([零〇壹贰叁肆伍陆柒捌玖])角/.exec(fracPart);
  const fen = /([零〇壹贰叁肆伍陆柒捌玖])分/.exec(fracPart);
  if (jiao) val += CN_DIGITS[jiao[1]] / 10;
  if (fen) val += CN_DIGITS[fen[1]] / 100;
  return Number.isFinite(val) ? round2(val) : null;
}

/* ------------------------------------------------------------ 英文数字词 */

const EN_ONES = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9,
  ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15,
  sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
};
const EN_TENS = {
  twenty: 20, thirty: 30, forty: 40, fifty: 50, sixty: 60, seventy: 70, eighty: 80, ninety: 90,
};
const EN_SCALES = { hundred: 100, thousand: 1e3, million: 1e6, billion: 1e9, trillion: 1e12 };

const EN_WORD_ALT = Object.keys(EN_ONES).concat(Object.keys(EN_TENS)).concat(Object.keys(EN_SCALES)).join('|');

/** 英文数字词短语 → 数值；含非数字词返回 null */
function parseEnWords(phrase) {
  const words = String(phrase == null ? '' : phrase)
    .toLowerCase()
    .replace(/[-,]/g, ' ')
    .split(/\s+/)
    .filter((w) => w && w !== 'and');
  if (!words.length) return null;
  let total = 0;
  let current = 0;
  let seen = false;
  for (const w of words) {
    if (EN_ONES[w] !== undefined) { current += EN_ONES[w]; seen = true; }
    else if (EN_TENS[w] !== undefined) { current += EN_TENS[w]; seen = true; }
    else if (EN_SCALES[w] !== undefined) {
      const sc = EN_SCALES[w];
      if (sc === 100) current = (current || 1) * 100;
      else { total += (current || 1) * sc; current = 0; }
      seen = true;
    } else {
      return null;
    }
  }
  return seen ? total + current : null;
}

/* -------------------------------------------------------------- 行/段落 */

/** 段落起点：从第 i 行往上找到空行之后的第一行 */
function paragraphStart(lines, i) {
  let j = i;
  while (j > 0 && lines[j - 1].trim() !== '') j--;
  return j;
}

/* ------------------------------------------------------------ 材料收集 */

/**
 * 从入参里取出"可核对的材料"。
 * 空 / 只有空白 / 只有一个字符 / 类型不对 / null / 裸数组 —— 一律 insufficient，绝不出结论。
 */
function collectMaterial(payload) {
  let text = null;

  if (payload === null || payload === undefined) {
    return { missing: ['没有收到任何材料：入参是 null（或 undefined）。'], };
  }
  if (Array.isArray(payload)) {
    return {
      missing: [`入参是数组（${payload.length} 个元素），不是一份合同文本。`],
      advice: '请给 {"text": "合同全文"}，或直接把合同正文当作纯文本传入。',
    };
  }
  if (typeof payload === 'string') {
    text = payload;
  } else if (typeof payload === 'number' || typeof payload === 'boolean') {
    return {
      missing: [`入参是 ${typeof payload}（${JSON.stringify(payload)}），不是合同文本。`],
      advice: '请给 {"text": "合同全文"}，或直接把合同正文当作纯文本传入。',
    };
  } else if (typeof payload === 'object') {
    if (typeof payload.text === 'string') text = payload.text;
    else if (typeof payload.content === 'string') text = payload.content;
    else if (payload.text !== undefined && payload.text !== null) {
      return {
        missing: [`text 不是字符串（收到的是 ${Array.isArray(payload.text) ? 'array' : typeof payload.text}：${clip(JSON.stringify(payload.text), 40)}）。`],
        advice: '把合同正文放进 text 字符串字段，例如 {"text": "第一条 ..."}。',
      };
    } else {
      return {
        missing: ['入参对象里没有可用的 text（或 content）字符串字段。'],
        advice: '把合同正文放进 text 字符串字段，例如 {"text": "第一条 ..."}。',
      };
    }
  } else {
    return { missing: [`入参类型是 ${typeof payload}，无法当作合同文本。`] };
  }

  const raw = String(text);
  const trimmed = raw.trim();
  if (!trimmed) {
    return {
      missing: ['材料是空的（只有空白字符），没有任何可以核对的内容。'],
      advice: '把合同全文粘贴进 text 字段，至少包含当事方、日期、金额、条款编号、定义或签署栏之一。',
    };
  }
  if (trimmed.length < MIN_MATERIAL_CHARS) {
    return {
      missing: [`材料只有 ${trimmed.length} 个字符（「${clip(trimmed, 20)}」），不构成一份可以核对的合同文本。`],
      advice: '请提供完整合同正文（或至少包含一个可核对要素的片段）。',
    };
  }
  return { text: raw };
}

/** 内容信号：合同该有的要素出现了几种 */
function contentSignals(analysis) {
  const s = [];
  if (analysis.dates.length) s.push('日期');
  if (analysis.amounts.length || analysis.capitals.length || analysis.words.length) s.push('金额');
  if (analysis.parties.length) s.push('当事方');
  if (analysis.clauses.length) s.push('条款编号');
  if (analysis.placeholders.length) s.push('占位符');
  if (analysis.definitions.length) s.push('定义句式');
  if (analysis.signatureIndex >= 0) s.push('签署栏');
  return s;
}

/* ------------------------------------------------------ 各要素的抽取器 */

/** 阿拉伯数字金额（带币种/单位/千分位；已排除条款编号、日期、百分号） */
function collectAmounts(text, starts) {
  const out = [];
  const re = /(?:\u00A5|\uFFE5|USD|RMB|CNY|\$|\u20AC|\u00A3|人民币|美元)?\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?:\s*(亿元|亿|万元|万|元|美元))?/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const rawNum = m[1];
    const unit = m[2] || '';
    const at = m.index + m[0].indexOf(rawNum);
    const after = text[at + rawNum.length] || '';
    const before = at > 0 ? text[at - 1] : '';
    if (after === '%' || after === '\uFF05') continue;
    if (after === '-') continue;
    if (after === '/' || before === '/') continue;
    if (after === '\u5E74' || after === '\u6708' || after === '\u65E5') continue;
    if (before === '\u5E74' || before === '\u6708' || before === '\u65E5') continue;
    if (/\d/.test(after)) continue;
    if (after === '.' && /\d/.test(text[at + rawNum.length + 1] || '')) continue;
    if (/[\d.]/.test(before)) continue;
    const digits = rawNum.replace(/,/g, '');
    const intLen = digits.split('.')[0].length;
    const fracLen = (digits.split('.')[1] || '').length;
    const hasSep = rawNum.indexOf(',') >= 0;
    if (!hasSep && !unit && intLen < 3 && fracLen !== 2) continue;
    const line = lineOf(starts, at);
    const ls = starts[line - 1];
    const head = text.slice(ls, at);
    if (/^\s*$/.test(head) && /^[.、)）]/.test(after)) continue;   // 行首的 1.2 / 3、 是条款编号
    const mult = (unit === '亿' || unit === '亿元') ? 1e8 : ((unit === '万' || unit === '万元') ? 1e4 : 1);
    const value = round2(parseFloat(digits) * mult);
    if (!Number.isFinite(value)) continue;
    out.push({
      raw: text.slice(at, at + rawNum.length + unit.length),
      numText: rawNum,
      unit: unit,
      value: value,
      index: at,
      end: at + rawNum.length + unit.length,
      line: line,
    });
  }
  return out;
}

/** 中文大写金额 token */
function collectCnCapitals(text, starts) {
  const out = [];
  const re = /[零〇壹贰叁肆伍陆柒捌玖拾佰仟万亿兆圆元角分整正]{2,}/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const tok = m[0];
    if (!/[零〇壹贰叁肆伍陆柒捌玖]/.test(tok)) continue;
    if (!/[元圆]/.test(tok) && !/[拾佰仟万亿兆]/.test(tok)) continue;
    const value = parseCnCapital(tok);
    if (value === null || !(value > 0)) continue;
    out.push({ raw: tok, value: value, index: m.index, end: m.index + tok.length, line: lineOf(starts, m.index) });
  }
  return out;
}

/** 英文数字词短语 + 其数值 */
function collectEnWordAmounts(text, starts) {
  const out = [];
  const re = new RegExp('\\b(?:' + EN_WORD_ALT + ')(?:[\\s-]+(?:and[\\s-]+)?(?:' + EN_WORD_ALT + '))*\\b', 'gi');
  let m;
  while ((m = re.exec(text)) !== null) {
    const value = parseEnWords(m[0]);
    if (value === null || !(value > 0)) continue;
    out.push({ raw: m[0], value: value, index: m.index, end: m.index + m[0].length, line: lineOf(starts, m.index) });
  }
  return out;
}

const MONTHS = {
  january: 1, february: 2, march: 3, april: 4, may: 5, june: 6, july: 7, august: 8,
  september: 9, october: 10, november: 11, december: 12,
  jan: 1, feb: 2, mar: 3, apr: 4, jun: 6, jul: 7, aug: 8, sep: 9, sept: 9, oct: 10, nov: 11, dec: 12,
};
const MONTH_ALT = Object.keys(MONTHS).join('|');

function daysInMonth(y, m) {
  if (!(y >= 1 && y <= 9999)) return 0;
  if (m === 2) {
    const leap = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
    return leap ? 29 : 28;
  }
  return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1] || 0;
}

function cnDigitsToInt(s) {
  const t = String(s);
  let out = '';
  for (const ch of t) {
    if (CN_DIGITS[ch] === undefined || CN_DIGITS[ch] > 9) return null;
    if (ch === '十' || ch === '拾') return null;
    out += String(CN_DIGITS[ch]);
  }
  const n = parseInt(out, 10);
  return Number.isFinite(n) ? n : null;
}

/** 日期抽取：支持 2026-03-01 / 2026/3/1 / 2026.3.1 / 2026年3月1日 / 03/01/2026 / March 1, 2026 / 二〇二六年三月一日 */
function collectDates(text, starts) {
  const out = [];
  const push = (raw, y, mo, d, index, kind) => {
    const valid = Number.isFinite(y) && Number.isFinite(mo) && Number.isFinite(d)
      && y >= 1000 && y <= 2999 && mo >= 1 && mo <= 12 && d >= 1 && d <= daysInMonth(y, mo);
    out.push({
      raw: raw, y: y, m: mo, d: d, index: index, line: lineOf(starts, index),
      kind: kind, valid: valid,
      iso: Number.isFinite(y) && Number.isFinite(mo) && Number.isFinite(d)
        ? `${String(y).padStart(4, '0')}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}` : null,
    });
  };

  const patterns = [
    [/\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b/g, 'iso', (m) => [Number(m[1]), Number(m[2]), Number(m[3])]],
    [/(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日/g, 'cn', (m) => [Number(m[1]), Number(m[2]), Number(m[3])]],
    [/\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b/g, 'slash', (m) => [Number(m[3]), Number(m[1]), Number(m[2])]],
    [new RegExp('\\b(' + MONTH_ALT + ')\\s+(\\d{1,2})(?:st|nd|rd|th)?,?\\s+(\\d{4})\\b', 'gi'), 'en-mdy',
      (m) => [Number(m[3]), MONTHS[String(m[1]).toLowerCase()], Number(m[2])]],
    [new RegExp('\\b(\\d{1,2})(?:st|nd|rd|th)?\\s+(' + MONTH_ALT + ')\\s+(\\d{4})\\b', 'gi'), 'en-dmy',
      (m) => [Number(m[3]), MONTHS[String(m[2]).toLowerCase()], Number(m[1])]],
    [/([〇零一二三四五六七八九]{4})\s*年\s*([〇零一二三四五六七八九]{1,3})\s*月\s*([〇零一二三四五六七八九]{1,3})\s*日/g, 'cn-num',
      (m) => [cnDigitsToInt(m[1]), cnDigitsToInt(m[2]), cnDigitsToInt(m[3])]],
  ];

  for (const [re, kind, pick] of patterns) {
    let m;
    while ((m = re.exec(text)) !== null) {
      const [y, mo, d] = pick(m);
      push(m[0], y, mo, d, m.index, kind);
    }
  }

  // 同一个位置被多种模式命中时只留最早登记的那条
  const seen = new Set();
  const result = [];
  for (const d of out) {
    const key = d.index + ':' + d.raw;
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(d);
  }
  result.sort((a, b) => a.index - b.index);
  return result;
}

/* --------------------------------------------------------------- 当事方 */

const PARTY_LABELS = [
  ['甲方', /甲\s*方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['乙方', /乙\s*方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['丙方', /丙\s*方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['出租方', /出租方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['承租方', /承租方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['买方', /买\s*方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
  ['卖方', /卖\s*方(?:\s*(?:名称|全称))?\s*[:：]\s*([^\n，,；;。：:、]{2,60})/g],
];

/** 英文角色别名：NAME (the "Licensor") 这种写法，别名必须在白名单里 */
const EN_ROLE_WORDS = [
  'Licensor', 'Licensee', 'Client', 'Contractor', 'Customer', 'Supplier', 'Vendor',
  'Consultant', 'Purchaser', 'Provider', 'Service Provider', 'Disclosing Party',
  'Receiving Party', 'Lessor', 'Lessee', 'Borrower', 'Lender', 'Employer', 'Employee',
  'Contractor', 'Company',
];
const EN_ROLE_ALT = EN_ROLE_WORDS.map((w) => w.replace(/\s+/g, '\\s+')).join('|');
const EN_LABELED = new RegExp('\\b(' + EN_ROLE_ALT + '|Party\\s*[A-Z])\\s*[:：]\\s*([^\\n,;:]{2,80})', 'gi');
const EN_ALIAS = new RegExp('([A-Z][^\\n,;:()]{1,70}?)\\s*\\(\\s*(?:the\\s+|this\\s+)?["“]([^"”]{2,40})["”]\\s*\\)', 'g');

function cleanPartyName(s) {
  let name = String(s == null ? '' : s);
  name = name.replace(/[（(]\s*(?:以下|下称|简称)[^）)]*[）)]/g, '');
  name = name.replace(/\(\s*(?:the|this)\s+["“][^"”]*["”]\s*\)/gi, '');
  // 名称后面紧跟下一个角色标记或条款编号时，在那里截断（一行里写了整份合同的情况）
  name = name.split(/\s*(?:甲\s*方|乙\s*方|丙\s*方|丁\s*方|Party\s*[A-Z]|第\s*[〇零一二三四五六七八九十百千\d]{1,6}\s*[条章款])\s*/)[0];
  name = name.split(/\s+(?:and|与|和|及)\s+/)[0];
  name = name.replace(/^(?:the|The)\s+/, '');
  name = name.replace(/[，,、；;。\s]+$/, '');
  return name.trim();
}

function collectParties(text, starts) {
  const out = [];
  const seen = new Set();
  const add = (role, name, index, source) => {
    const nm = cleanPartyName(name);
    if (!nm || nm.length < 2) return;
    if (/^(?:甲方|乙方|丙方|Party\s*[A-Z])$/i.test(nm)) return;
    if (/\b(Agreement|Contract)\b/i.test(nm)) return;
    if (/[协议合同]$/.test(nm) && nm.length > 6) return;
    const key = role + '|' + normName(nm) + '|' + index;
    if (seen.has(key)) return;
    seen.add(key);
    out.push({ role: role, name: nm, index: index, line: lineOf(starts, index), source: source });
  };

  for (const [role, re] of PARTY_LABELS) {
    let m;
    while ((m = re.exec(text)) !== null) add(role, m[1], m.index, 'labeled');
  }
  let m;
  while ((m = EN_LABELED.exec(text)) !== null) {
    add(m[1].replace(/\s+/g, ' '), m[2], m.index, 'labeled');
  }
  while ((m = EN_ALIAS.exec(text)) !== null) {
    const role = EN_ROLE_WORDS.find((w) => w.toLowerCase() === String(m[2]).trim().toLowerCase());
    if (!role) continue;
    add(role, m[1], m.index, 'alias');
  }
  out.sort((a, b) => a.index - b.index);
  return out;
}

const SIGNATURE_RE = /(签字|签章|盖章|签署|签名|Signature|Signed|SIGNED|Signing\s+Date)/;

function findSignatureStart(lines) {
  let last = -1;
  for (let i = 0; i < lines.length; i++) {
    if (SIGNATURE_RE.test(lines[i])) last = i;
  }
  if (last < 0) return -1;
  return paragraphStart(lines, last);
}

/* -------------------------------------------------------------- 条款编号 */

const CN_NUM_CHARS = '〇零一二三四五六七八九十百千';

function cnClauseNumber(s) {
  const t = String(s == null ? '' : s).trim();
  if (!t) return null;
  if (/^\d+$/.test(t)) return parseInt(t, 10);
  if (!new RegExp('^[' + CN_NUM_CHARS + ']+$').test(t)) return null;
  return cnToNumber(t);
}

const CLAUSE_HEAD_PATTERNS = [
  { re: /^\s*第\s*([〇零一二三四五六七八九十百千\d]{1,6})\s*条/, ns: 'cn-article', kind: 'cn' },
  { re: /^\s*(?:Article|ARTICLE|Section|SECTION|Clause|CLAUSE)\s+(\d{1,3}(?:\.\d{1,3})*)/, ns: 'en-section', kind: 'en' },
  { re: /^\s*(\d{1,2}(?:\.\d{1,2}){0,2})[.、)）]?\s+\S/, ns: 'numeric', kind: 'num' },
  { re: /^\s*([一二三四五六七八九十]{1,3})\s*[、.]\s*\S/, ns: 'cn-heading', kind: 'cn' },
];

function collectClauses(lines) {
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    for (const p of CLAUSE_HEAD_PATTERNS) {
      const m = p.re.exec(line);
      if (!m) continue;
      let label = m[1];
      if (p.kind === 'cn') {
        const n = cnClauseNumber(label);
        if (n === null) continue;
        label = String(n);
      }
      out.push({ ns: p.ns, label: label, line: i + 1, text: clip(line, 60), index: i });
      break;
    }
  }
  return out;
}

function collectClauseRefs(text, starts, lines) {
  const refs = [];
  const cnRe = /第\s*([〇零一二三四五六七八九十百千\d]{1,6})\s*条/g;
  let m;
  while ((m = cnRe.exec(text)) !== null) {
    const line = lineOf(starts, m.index);
    const ls = starts[line - 1];
    const head = text.slice(ls, m.index);
    if (/^\s*$/.test(head) && CLAUSE_HEAD_PATTERNS[0].re.test(lines[line - 1])) continue;  // 这是标题本身
    const n = cnClauseNumber(m[1]);
    if (n === null) continue;
    refs.push({ ns: 'cn-article', label: String(n), raw: m[0], line: line, index: m.index });
  }
  const enRe = /\b(?:Section|Article|Clause|SECTION|ARTICLE|CLAUSE)\s+(\d{1,3}(?:\.\d{1,3})*)/g;
  while ((m = enRe.exec(text)) !== null) {
    const line = lineOf(starts, m.index);
    const ls = starts[line - 1];
    const head = text.slice(ls, m.index);
    if (/^\s*$/.test(head) && /^\s*(?:Article|ARTICLE|Section|SECTION|Clause|CLAUSE)\s/.test(lines[line - 1])) continue;
    refs.push({ ns: 'en-section', label: m[1], raw: m[0], line: line, index: m.index });
  }
  refs.sort((a, b) => a.index - b.index);
  return refs;
}

/* ------------------------------------------------------------ 占位符规则 */

const PLACEHOLDER_RULES = [
  { re: /\bX{2,}\b/g, label: 'XXX 占位', level: 'P1' },
  { re: /\bTBD\b/gi, label: 'TBD 占位', level: 'P1' },
  { re: /\bTBC\b/gi, label: 'TBC 占位', level: 'P1' },
  { re: /【[^】\n]{0,40}】/g, label: '【…】方括号占位', level: 'P1' },
  { re: /＿{2,}/g, label: '＿＿ 下划线占位', level: 'P1' },
  { re: /_{3,}/g, label: '____ 下划线占位', level: 'P1' },
  { re: /\{\{[^}\n]{1,40}\}\}/g, label: '{{var}} 模板变量占位', level: 'P1' },
  { re: /待填|此处填写|请填写|待补充|待定/g, label: '中文待填占位', level: 'P1' },
  { re: /\[\s*\]/g, label: '[ ] 空方括号占位', level: 'P2' },
  { re: /\bN\/A\b/g, label: 'N/A 占位', level: 'P2' },
];

function collectPlaceholders(text, starts) {
  const out = [];
  const taken = [];
  for (const rule of PLACEHOLDER_RULES) {
    rule.re.lastIndex = 0;
    let m;
    while ((m = rule.re.exec(text)) !== null) {
      if (taken.some((t) => m.index >= t[0] && m.index < t[1])) continue;
      taken.push([m.index, m.index + m[0].length]);
      out.push({ raw: m[0], label: rule.label, level: rule.level, index: m.index, line: lineOf(starts, m.index) });
    }
  }
  out.sort((a, b) => a.index - b.index);
  return out;
}

/* -------------------------------------------------------------- 定义词 */

const DEF_PATTERNS = [
  { re: /["“]([^"”\n]{2,40})["”]\s*(?:means|shall mean|refers to|has the meaning)/gi, kind: 'en-quoted', term: 1 },
  { re: /\b([A-Z][A-Za-z]{2,25}(?:\s+[A-Z][A-Za-z]{2,25}){0,3})\s+(?:means|shall mean)\b/g, kind: 'en-bare', term: 1 },
  { re: /["“]([^"”\n]{2,40})["”]\s*(?:是指|系指|指)/g, kind: 'cn-quoted', term: 1 },
  { re: /\(\s*(?:the|this)\s+["“]([^"”\n]{2,40})["”]\s*\)/gi, kind: 'en-alias', term: 1 },
  { re: /(?:以下简称|以下称|下称)\s*["“]?([^"”\n，,。；;\s]{2,25})["”]?/g, kind: 'cn-alias', term: 1 },
];

function collectDefinitions(text, starts) {
  const out = [];
  for (const p of DEF_PATTERNS) {
    p.re.lastIndex = 0;
    let m;
    while ((m = p.re.exec(text)) !== null) {
      const term = String(m[p.term] || '').trim();
      if (!term || term.length < 2) continue;
      out.push({ term: term, kind: p.kind, index: m.index, line: lineOf(starts, m.index), raw: clip(m[0], 70) });
    }
  }
  out.sort((a, b) => a.index - b.index);
  return out;
}

/** 引号里的词（中文合同里"给术语加引号"就是定义的信号） */
function collectQuotedTerms(text, starts) {
  const out = [];
  const re = /["“]([^"”\n]{2,30})["”]/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const term = String(m[1]).trim();
    if (!term) continue;
    out.push({ term: term, index: m.index, line: lineOf(starts, m.index) });
  }
  return out;
}

const CN_TERM_STOPWORDS = [
  '甲方', '乙方', '丙方', '丁方', '双方', '各方', '本合同', '本协议', '签字', '盖章',
  '附件', '前述', '以上', '以下', '上述', '约定', '条款', '日期', '金额', '服务', '产品',
];
const EN_TERM_STOPWORDS = [
  'Agreement', 'Contract', 'Party', 'Parties', 'Section', 'Sections', 'Article', 'Clause',
  'Exhibit', 'Schedule', 'Annex', 'Appendix', 'Signature', 'Notice', 'Notices', 'Day', 'Days',
  'Month', 'Months', 'Year', 'Years', 'Effective Date', 'Term', 'Termination', 'Total',
  'Amount', 'Fee', 'Fees', 'Payment', 'Service', 'Services', 'Provider', 'Customer', 'Vendor',
  'Purchaser', 'Supplier', 'Consultant', 'Company', 'Client', 'Contractor', 'Licensor',
  'Licensee', 'Buyer', 'Seller', 'Employer', 'Employee', 'Lessor', 'Lessee', 'Borrower',
  'Lender', 'Software', 'License', 'USD', 'RMB', 'CNY', 'Date', 'Time', 'This', 'That',
  'These', 'Those', 'Such', 'Each', 'Every', 'Any', 'All', 'Where', 'When', 'With', 'Without',
  'However', 'Notwithstanding', 'Neither', 'Either', 'Hereof', 'Herein', 'Hereto', 'Whereof',
  'Shall', 'Will', 'Must', 'May', 'Written', 'Business',
];

function countOccurrences(text, term) {
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  let re;
  if (/^[A-Za-z][A-Za-z\s-]*$/.test(term)) {
    re = new RegExp('\\b' + escaped.replace(/\s+/g, '\\s+') + '\\b', 'gi');
  } else {
    re = new RegExp(escaped, 'g');
  }
  const hits = [];
  let m;
  while ((m = re.exec(text)) !== null) {
    hits.push(m.index);
    if (hits.length > 200) break;
  }
  return hits;
}

/* ---------------------------------------------------------------- 分析 */

function analyze(text) {
  const starts = lineStarts(text);
  const lines = text.split(/\r\n|\r|\n/);
  const a = {
    text: text,
    starts: starts,
    lines: lines,
    dates: collectDates(text, starts),
    amounts: collectAmounts(text, starts),
    capitals: collectCnCapitals(text, starts),
    words: collectEnWordAmounts(text, starts),
    parties: collectParties(text, starts),
    clauses: collectClauses(lines),
    placeholders: collectPlaceholders(text, starts),
    definitions: collectDefinitions(text, starts),
    quoted: collectQuotedTerms(text, starts),
    signatureIndex: findSignatureStart(lines),
  };
  a.refs = collectClauseRefs(text, starts, lines);
  return a;
}

/* ------------------------------------------------------------ 六项检查 */

function finding(level, category, line, message, advice, evidence) {
  return { level: level, category: category, line: line, message: message, advice: advice, evidence: evidence };
}

/* 1. 当事方名称不一致 */
function checkParties(a) {
  const out = [];
  const byRole = new Map();
  for (const p of a.parties) {
    if (!byRole.has(p.role)) byRole.set(p.role, []);
    byRole.get(p.role).push(p);
  }
  for (const [role, list] of byRole) {
    const groups = new Map();
    for (const p of list) {
      const k = normName(p.name);
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k).push(p);
    }
    if (groups.size > 1) {
      const variants = Array.from(groups.values()).map((g) => `第${g[0].line}行「${g[0].name}」`);
      out.push(finding(
        'P0',
        '当事方名称不一致',
        list[0].line,
        `同一角色「${role}」在全文出现 ${groups.size} 个不同名称：${variants.join('、')}。`,
        '统一当事方名称（含全称/简称）并核对与营业执照一致；名称不一致的合同主体认定存在争议。',
        variants.join(' / ')
      ));
    }
  }

  if (a.signatureIndex >= 0) {
    // 只在签署栏确实是文档末尾一小块时才做"正文 vs 签署栏"比对：
    // 否则（没有空行、签署的字样出现在开头）整篇都会落进签署栏，比对没有意义。
    const sigSpan = a.lines.length - a.signatureIndex;
    if (a.signatureIndex > 0 && sigSpan < a.lines.length * 0.6) {
      const sigText = a.lines.slice(a.signatureIndex).join('\n');
      const bodyParties = a.parties.filter((p) => p.line - 1 < a.signatureIndex);
      const sigParties = a.parties.filter((p) => p.line - 1 >= a.signatureIndex);

      for (const p of sigParties) {
        const k = normName(p.name);
        const inBody = a.parties.some((q) => q.line - 1 < a.signatureIndex && normName(q.name) === k);
        if (!inBody) {
          out.push(finding(
            'P1',
            '当事方名称不一致',
            p.line,
            `签署栏第${p.line}行出现当事方名称「${p.name}」，正文中从未出现过该名称。`,
            '核对签署栏主体是否为正文当事方；签署栏与正文主体不一致会导致签署主体存疑。',
            clip(a.lines[p.line - 1], 80)
          ));
        }
      }
      for (const p of bodyParties) {
        const k = normName(p.name);
        if (!normName(sigText).includes(k)) {
          out.push(finding(
            'P1',
            '当事方名称不一致',
            p.line,
            `正文第${p.line}行的当事方「${p.name}」在签署栏里找不到同名主体。`,
            '补齐签署栏（或核对正文与签署栏的主体名称）。',
            clip(a.lines[p.line - 1], 80)
          ));
        }
      }
    }
  }
  return out;
}

const DATE_LABEL_RULES = [
  { key: 'signing', re: /(签订日期|签署日期|签字日期|签订时间|签署时间|订立日期|签约日期|签订于|签署于|签订日|签署日|Date\s+of\s+Signing|Signing\s+Date|Signed\s+on|Execution\s+Date|Date\s+of\s+Execution|entered\s+into\s+on|dated)/i },
  { key: 'effective', re: /(生效日期|生效时间|生效日|生效|Effective\s+Date|Effective\s+as\s+of|takes\s+effect|Commencement\s+Date|comes\s+into\s+effect)/i },
  { key: 'expiry', re: /(到期日|有效期至|届满|终止日期|失效日期|终止于|期满|Expiration\s+Date|Expiry\s+Date|Expires\s+on|Termination\s+Date|End\s+Date|终止日)/i },
];

const DATE_LABEL_CN = { signing: '签订日期', effective: '生效日期', expiry: '到期/终止日期' };

/* 2. 日期矛盾 */
function checkDates(a) {
  const out = [];
  const dates = a.dates;
  if (!dates.length) return out;

  for (const d of dates) {
    if (!d.valid) {
      const why = [];
      if (!(d.m >= 1 && d.m <= 12)) why.push(`月份 ${d.m} 不在 1–12 之间`);
      else if (!(d.d >= 1 && d.d <= daysInMonth(d.y, d.m))) why.push(`${d.y} 年 ${d.m} 月没有 ${d.d} 日`);
      if (!(d.y >= 1000 && d.y <= 2999)) why.push(`年份 ${d.y} 超出合理范围`);
      out.push(finding(
        'P0',
        '日期矛盾',
        d.line,
        `第${d.line}行「${d.raw}」不是合法日期：${why.join('；') || '年月日无法成立'}。`,
        '改写成合法日期，并统一使用同一种书写格式（推荐 YYYY-MM-DD 或 YYYY年M月D日）。',
        clip(a.lines[d.line - 1], 80)
      ));
    }
  }

  // 关键词标注：先认「自A起生效，至B止」这类固定句式，再退回就近关键词
  const labels = new Map();
  const setLabel = (d, key) => {
    if (!labels.has(d)) labels.set(d, key);
  };
  const D = '(?:\\d{4}[年\\-/.]\\d{1,2}[月\\-/.]\\d{1,2}日?|\\d{1,2}[/-]\\d{1,2}[/-]\\d{4})';
  const idioms = [
    { re: new RegExp('自\\s*(' + D + ')\\s*(?:起|开始)?[^。；\\n]{0,12}?(?:生效|有效)[^。；\\n]{0,20}?至\\s*(' + D + ')\\s*(?:止|结束|届满)', 'g'), a: 'effective', b: 'expiry' },
    { re: new RegExp('有效期[^。；\\n]{0,10}?(' + D + ')\\s*(?:至|到|—|-)\\s*(' + D + ')', 'g'), a: 'effective', b: 'expiry' },
    { re: new RegExp('\\bfrom\\s+(' + D + ')\\s+(?:to|through|until)\\s+(' + D + ')', 'gi'), a: 'effective', b: 'expiry' },
  ];
  for (const idiom of idioms) {
    let m;
    while ((m = idiom.re.exec(a.text)) !== null) {
      const rawA = m[1];
      const rawB = m[2];
      const dA = dates.find((d) => d.index >= m.index && d.index < m.index + m[0].length && d.raw === rawA);
      const dB = dates.find((d) => d.index > (dA ? dA.index : m.index) && d.index < m.index + m[0].length && d.raw === rawB);
      if (dA) setLabel(dA, idiom.a);
      if (dB) setLabel(dB, idiom.b);
    }
  }
  for (const d of dates) {
    if (labels.has(d) || !d.valid) continue;
    const ls = a.starts[d.line - 1];
    const before = a.text.slice(Math.max(ls, d.index - 16), d.index);
    const after = a.text.slice(d.index + d.raw.length, d.index + d.raw.length + 16);
    for (const rule of DATE_LABEL_RULES) {
      if (rule.re.test(before)) { setLabel(d, rule.key); break; }
    }
    if (!labels.has(d)) {
      for (const rule of DATE_LABEL_RULES) {
        if (rule.re.test(after)) { setLabel(d, rule.key); break; }
      }
    }
  }

  const groups = new Map();
  for (const [d, key] of labels) {
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(d);
  }

  for (const [key, list] of groups) {
    const firstOfIso = new Map();
    for (const d of list) if (!firstOfIso.has(d.iso)) firstOfIso.set(d.iso, d);
    const distinct = Array.from(firstOfIso.keys());
    if (distinct.length > 1) {
      const ev = Array.from(firstOfIso.values()).map((d) => `第${d.line}行「${d.raw}」`).join('、');
      out.push(finding(
        'P0',
        '日期矛盾',
        list[0].line,
        `${DATE_LABEL_CN[key]}在同一文档中出现 ${distinct.length} 个互不相同的值：${ev}。`,
        `同一语义的日期只能有一个值，请删掉或更正多余的一处。`,
        ev
      ));
    }
  }

  const pick = (key) => {
    const list = groups.get(key) || [];
    return list.length ? list[list.length - 1] : null;
  };
  const signing = pick('signing');
  const effective = pick('effective');
  const expiry = pick('expiry');

  if (signing && effective && signing.iso > effective.iso) {
    out.push(finding(
      'P0',
      '日期矛盾',
      signing.line,
      `签订日期 ${signing.iso}（第${signing.line}行「${signing.raw}」）晚于生效日期 ${effective.iso}（第${effective.line}行「${effective.raw}」）。`,
      '先签订后生效才成立；请核对两个日期或调整措辞（例如"自双方签署之日起生效"）。',
      `签订 ${signing.raw} / 生效 ${effective.raw}`
    ));
  }
  if (expiry && effective && expiry.iso < effective.iso) {
    out.push(finding(
      'P0',
      '日期矛盾',
      expiry.line,
      `到期/终止日期 ${expiry.iso}（第${expiry.line}行「${expiry.raw}」）早于生效日期 ${effective.iso}（第${effective.line}行「${effective.raw}」）。`,
      '有效期必须晚于生效日；请核对期限条款。',
      `到期 ${expiry.raw} / 生效 ${effective.raw}`
    ));
  }
  if (expiry && signing && expiry.iso < signing.iso) {
    out.push(finding(
      'P0',
      '日期矛盾',
      expiry.line,
      `到期/终止日期 ${expiry.iso}（第${expiry.line}行「${expiry.raw}」）早于签订日期 ${signing.iso}（第${signing.line}行「${signing.raw}」）。`,
      '期限在签署之前就已届满，请核对日期。',
      `到期 ${expiry.raw} / 签订 ${signing.raw}`
    ));
  }

  // 同一组年月日在两处用了互不一致的书写格式
  const isoDates = dates.filter((d) => d.valid && d.kind === 'iso');
  const slashDates = dates.filter((d) => d.valid && d.kind === 'slash');
  for (const s of slashDates) {
    const parts = [s.y, s.m, s.d].join(',');
    const twin = isoDates.find((i) => [i.y, i.m, i.d].join(',') === parts);
    if (twin) {
      out.push(finding(
        'P2',
        '日期矛盾',
        s.line,
        `同一组年月日出现两种互不一致的书写格式：第${twin.line}行「${twin.raw}」（年-月-日）与第${s.line}行「${s.raw}」（未标明是 月/日/年 还是 日/月/年）。`,
        '统一日期格式，避免 03/04/2026 这类无法确定月日的写法。',
        `${twin.raw} ↔ ${s.raw}`
      ));
      break;
    }
  }
  return out;
}

const AMOUNT_LABELS = [
  '合同总金额', '合同总价', '合同金额', '总金额', '总额', '总计金额', '价款总额', '总费用',
  'Total Amount', 'Contract Price', 'Total Fee', 'Aggregate Amount', 'Total Contract Value',
];

/* 3. 金额矛盾 */
function checkAmounts(a) {
  const out = [];
  const { text, lines, amounts, capitals, words } = a;

  // 3.1 大写 / 单词金额 与旁边的阿拉伯数字互校
  const nearDigits = (x) => amounts.filter((n) => Math.abs(n.line - x.line) <= 1);
  const compared = new Set();

  const crossCheck = (token, kindLabel) => {
    for (const n of nearDigits(token)) {
      let between;
      if (token.end <= n.index) between = text.slice(token.end, n.index);
      else if (n.end <= token.index) between = text.slice(n.end, token.index);
      else continue;
      if (between.length > 80) continue;
      if (!onlyConnectors(between)) continue;
      const key = kindLabel + '|' + token.index + '|' + n.index;
      if (compared.has(key)) continue;
      compared.add(key);
      if (Math.abs(round2(token.value - n.value)) > TOLERANCE) {
        out.push(finding(
          'P0',
          '金额矛盾',
          Math.min(token.line, n.line),
          `${kindLabel}「${token.raw}」= ${fmtMoney(token.value)}，与第${n.line}行阿拉伯数字「${n.raw}」= ${fmtMoney(n.value)} 不一致（差 ${fmtMoney(round2(token.value - n.value))}）。`,
          '以大写（或文字）金额为准更正数字金额，或反过来统一；两者不一致时争议金额认定会按合同约定规则处理。',
          `${token.raw} ↔ ${n.raw}`
        ));
      }
    }
  };
  for (const c of capitals) crossCheck(c, '中文大写金额');
  for (const w of words) crossCheck(w, '英文文字金额');

  // 3.2 分项加总 ≠ 声明的合计
  const TOTAL_RE = /(?:^|[\s（(])(合计|小计|总计|总额|总计金额|总价|Total|Subtotal|Grand Total|Sum)\s*[:：]?/i;
  const ITEM_RE = /^\s*(?:\d{1,3}\s*[.、)）]|[（(]\s*\d{1,3}\s*[)）]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫]|[一二三四五六七八九十]{1,3}\s*[、.])\s*(.*)$/;

  const itemOf = (line, lineNo) => {
    const m = ITEM_RE.exec(line);
    if (!m) return null;
    const rest = m[1].trim();
    const localAmounts = amounts.filter((n) => n.line === lineNo);
    if (localAmounts.length !== 1) return null;
    const n = localAmounts[0];
    if (!new RegExp(escapeRe(n.raw) + '\\s*[。.；;，,]?$').test(rest)) return null;
    let label = rest.slice(0, rest.lastIndexOf(n.raw)).trim();
    label = label.replace(/[:：]\s*$/, '').trim();
    if (!label || label.length > 40) return null;
    return { label: label, amount: n };
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!TOTAL_RE.test(line)) continue;
    const totalAmounts = amounts.filter((n) => n.line === i + 1);
    if (totalAmounts.length !== 1) continue;
    const total = totalAmounts[0];
    if (!new RegExp(escapeRe(total.raw) + '\\s*[。.；;，,]?\\s*$').test(line.trim())) continue;
    const comps = [];
    for (let j = i - 1; j >= 0; j--) {
      if (!lines[j].trim()) continue;   // 空行不打断连续分项块
      const it = itemOf(lines[j], j + 1);
      if (!it) break;
      comps.unshift(it);
    }
    if (comps.length < 2) continue;
    const sum = round2(comps.reduce((s, c) => s + c.amount.value, 0));
    if (Math.abs(round2(sum - total.value)) > TOLERANCE) {
      const detail = comps.map((c) => `${c.label} ${fmtMoney(c.amount.value)}`).join(' + ');
      out.push(finding(
        'P0',
        '金额矛盾',
        i + 1,
        `第${i + 1}行合计「${total.raw}」= ${fmtMoney(total.value)}，但上方 ${comps.length} 个分项相加 = ${fmtMoney(sum)}（${detail}），差 ${fmtMoney(round2(sum - total.value))}。`,
        '核对分项与合计，按合同约定的修正规则处理。',
        `${detail} = ${fmtMoney(sum)} ≠ ${fmtMoney(total.value)}`
      ));
    }
  }

  // 3.3 同一个金额标签在同一文档里给了两个值
  const byLabel = new Map();
  for (const label of AMOUNT_LABELS) {
    const re = new RegExp(escapeRe(label) + '[^\\n]{0,40}', 'gi');
    let m;
    while ((m = re.exec(text)) !== null) {
      const end = m.index + m[0].length;
      const inside = amounts.filter((n) => n.index >= m.index && n.index < end);
      for (const n of inside) {
        const k = label.toLowerCase();
        if (!byLabel.has(k)) byLabel.set(k, { label: label, items: [] });
        byLabel.get(k).items.push(n);
      }
    }
  }
  for (const { label, items } of byLabel.values()) {
    const distinct = uniq(items.map((n) => String(n.value)));
    if (distinct.length > 1) {
      const ev = items.map((n) => `第${n.line}行「${n.raw}」`).join('、');
      out.push(finding(
        'P0',
        '金额矛盾',
        items[0].line,
        `同一金额表述「${label}」在全文中出现 ${distinct.length} 个不同数值：${ev}。`,
        '同一项金额只能有一个数值，请删掉或更正多余的一处。',
        `${label}：${ev}`
      ));
    }
  }
  return out;
}

function escapeRe(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/* 4. 占位符残留 */
function checkPlaceholders(a) {
  const out = [];
  const seen = new Map();
  for (const p of a.placeholders) {
    const key = p.label + '|' + p.raw;
    if (seen.has(key)) {
      seen.get(key).count++;
      seen.get(key).lines.push(p.line);
      continue;
    }
    seen.set(key, { p: p, count: 1, lines: [p.line] });
  }
  for (const { p, count, lines } of seen.values()) {
    const where = lines.slice(0, 5).map((l) => `第${l}行`).join('、') + (lines.length > 5 ? '等' : '');
    out.push(finding(
      p.level,
      '占位符残留',
      p.line,
      `发现${p.label}「${p.raw}」${count > 1 ? `${count} 处（${where}）` : `（第${p.line}行）`}：${clip(a.lines[p.line - 1], 80)}`,
      '把占位符替换成确定内容后再签署；带占位符的条款在履行时无法确定权利义务。',
      p.raw
    ));
  }
  return out;
}

/* 5. 条款交叉引用失效 */
function checkClauses(a) {
  const out = [];

  // 5.1 重复编号
  const byNs = new Map();
  for (const c of a.clauses) {
    const k = c.ns + '|' + c.label;
    if (!byNs.has(k)) byNs.set(k, []);
    byNs.get(k).push(c);
  }
  for (const [k, list] of byNs) {
    if (list.length < 2) continue;
    if (list[0].ns === 'cn-heading') continue;
    const ev = list.map((c) => `第${c.line}行「${clip(c.text, 30)}」`).join('、');
    out.push(finding(
      'P1',
      '条款交叉引用失效',
      list[0].line,
      `条款编号「${list[0].ns === 'cn-article' ? '第' + list[0].label + '条' : list[0].label}」重复出现 ${list.length} 次：${ev}。`,
      '条款编号必须唯一，重复编号会让交叉引用指向不明。',
      ev
    ));
  }

  // 5.2 编号跳跃
  for (const ns of ['cn-article', 'numeric']) {
    const nums = uniq(a.clauses.filter((c) => c.ns === ns && /^\d+$/.test(c.label)).map((c) => parseInt(c.label, 10)))
      .filter((n) => Number.isFinite(n)).sort((x, y) => x - y);
    if (nums.length < 3) continue;
    const top = nums[nums.length - 1];
    if (top > 200) continue;
    const missing = [];
    for (let n = 1; n <= top; n++) if (nums.indexOf(n) < 0) missing.push(n);
    if (!missing.length) continue;
    const label = ns === 'cn-article' ? (n) => `第${n}条` : (n) => `${n}`;
    out.push(finding(
      'P2',
      '条款交叉引用失效',
      a.clauses.find((c) => c.ns === ns).line,
      `条款编号不连续：定义了 ${nums.join('、')}，缺少 ${missing.map(label).join('、')}。`,
      '核对是否有条款在编辑时被删除，或编号需要重排。',
      `已定义 ${nums.join('、')}；缺 ${missing.join('、')}`
    ));
  }

  // 5.3 引用指向不存在的编号
  const defined = new Map();
  for (const c of a.clauses) {
    if (!defined.has(c.ns)) defined.set(c.ns, new Set());
    defined.get(c.ns).add(c.label);
  }
  const reported = new Set();
  /** 引用命名空间 → 可接受的编号命名空间（英文合同常写成 "5. Termination"，引用写成 "Section 5"） */
  const NS_FALLBACK = { 'cn-article': ['cn-article', 'cn-heading'], 'en-section': ['en-section', 'numeric'] };
  for (const r of a.refs) {
    const namespaces = NS_FALLBACK[r.ns] || [r.ns];
    const sets = namespaces.map((ns) => defined.get(ns)).filter((s) => s && s.size);
    const set = sets[0] || null;
    const key = r.ns + '|' + r.label;
    if (reported.has(key)) continue;
    if (!set) {
      reported.add(key);
      out.push(finding(
        'P1',
        '条款交叉引用失效',
        r.line,
        `第${r.line}行引用了「${r.raw}」，但全文没有任何条款编号标题可供对照（未识别到"第N条"或"Section N"形式的编号）。`,
        '补上条款编号，或确认引用目标是否存在。',
        clip(a.lines[r.line - 1], 80)
      ));
      continue;
    }
    if (!set.has(r.label)) {
      reported.add(key);
      const known = Array.from(set).filter((x) => /^\d+$/.test(x)).map(Number).sort((x, y) => x - y);
      const knownText = known.length ? `${known[0]}–${known[known.length - 1]}` : Array.from(set).join('、');
      out.push(finding(
        'P0',
        '条款交叉引用失效',
        r.line,
        `第${r.line}行引用了「${r.raw}」，但文档中不存在编号 ${r.label}（现有编号：${knownText}）。`,
        '修正引用编号或补上被引用的条款；指向空编号的引用在争议时会失效。',
        clip(a.lines[r.line - 1], 80)
      ));
    }
  }
  return out;
}

/* 6. 定义词卫生 */
function checkDefinitions(a) {
  const out = [];
  const defs = new Map();
  for (const d of a.definitions) {
    const k = normName(d.term).toLowerCase();
    if (!defs.has(k)) defs.set(k, d);
  }

  // 6.1 定义了却没再用
  for (const [k, d] of defs) {
    const hits = countOccurrences(a.text, d.term);
    const outside = hits.filter((idx) => idx < d.index || idx >= d.index + d.raw.length);
    if (!outside.length) {
      out.push(finding(
        'P2',
        '定义词卫生',
        d.line,
        `第${d.line}行定义了「${d.term}」，但全文再没有出现第二次（定义句式：${clip(d.raw, 50)}）。`,
        '删除未被使用的定义，或补齐使用它的条款；空定义容易让人以为漏了条款。',
        clip(d.raw, 70)
      ));
    }
  }

  // 6.2 用了却没定义（加引号的术语 / 反复出现的大写词）
  const usedReported = new Set();
  const quotedGroups = new Map();
  for (const q of a.quoted) {
    const k = normName(q.term).toLowerCase();
    if (!quotedGroups.has(k)) quotedGroups.set(k, { term: q.term, items: [] });
    quotedGroups.get(k).items.push(q);
  }
  for (const [k, g] of quotedGroups) {
    if (g.items.length < 2) continue;
    if (defs.has(k)) continue;
    if (CN_TERM_STOPWORDS.indexOf(g.term) >= 0) continue;
    if (usedReported.has('cn|' + k)) continue;
    usedReported.add('cn|' + k);
    const lines = uniq(g.items.map((x) => x.line));
    out.push(finding(
      'P1',
      '定义词卫生',
      lines[0],
      `「${g.term}」在全文被引号标注了 ${g.items.length} 次（第${lines.slice(0, 5).join('、')}行），但没有任何一处给出定义（缺少"…是指…"或"…means…"）。`,
      '给该术语加上定义条款，或去掉引号改为普通表述。',
      `${g.term} ×${g.items.length}（第${lines.slice(0, 5).join('、')}行）`
    ));
  }

  const capRe = /\b([A-Z][A-Za-z]{3,}(?:\s+[A-Z][A-Za-z]{3,}){0,2})\b/g;
  const capGroups = new Map();
  let m;
  while ((m = capRe.exec(a.text)) !== null) {
    const term = m[1];
    const k = normName(term).toLowerCase();
    if (!capGroups.has(k)) capGroups.set(k, { term: term, hits: [] });
    capGroups.get(k).hits.push(m.index);
  }
  for (const [k, g] of capGroups) {
    if (defs.has(k)) continue;
    if (EN_TERM_STOPWORDS.some((w) => w.toLowerCase() === k)) continue;
    if (MONTHS[k] !== undefined) continue;                       // 月份名不算术语
    if (a.parties.some((p) => normName(p.name).toLowerCase().includes(k.replace(/\s/g, '')))) continue;
    if (g.hits.length < 3) continue;
    if (usedReported.has('en|' + k)) continue;
    const ls = uniq(g.hits.map((idx) => lineOf(a.starts, idx)));
    usedReported.add('en|' + k);
    out.push(finding(
      'P2',
      '定义词卫生',
      ls[0],
      `大写术语「${g.term}」在全文出现 ${g.hits.length} 次（第${ls.slice(0, 5).join('、')}行），但没有任何一处给出定义（缺少 "… means …"）。`,
      '给该术语加上定义，或改成小写普通表述。',
      `${g.term} ×${g.hits.length}`
    ));
  }

  return out;
}

/* ---------------------------------------------------------------- 样例 */

const SAMPLE_TEXT = [
  '技术服务合同',
  '',
  '甲方：北京星河科技有限公司',
  '乙方：上海云帆信息技术有限公司',
  '',
  '第一条 服务内容',
  '乙方为甲方提供系统运维服务，服务标准见第八条。',
  '',
  '第二条 合同金额',
  '合同总金额：人民币壹拾万元整（小写 80,000.00）。',
  '分项如下：',
  '一、基础运维费：60,000.00',
  '二、应急响应费：15,000.00',
  '三、培训费：5,000.00',
  '合计：85,000.00',
  '',
  '第三条 服务期限',
  '本协议自 2026年3月1日 起生效，至 2027年2月28日 止。',
  '签订日期：2026-04-15。',
  '失效日期：2026-02-30。',
  '',
  '第四条 保密',
  '“保密信息”是指乙方在履约过程中知悉的甲方商业秘密。',
  '乙方应对保密信息承担保密义务。',
  '“服务标准”以乙方公布口径为准，“服务标准”的变更需书面确认。',
  '“服务水平”是指双方约定的响应时限与可用率目标。',
  '',
  '第五条 签署',
  '甲方：北京星河科技有限责任公司',
  '乙方：上海云帆信息技术有限公司',
  '签署日期：2026-03-01（Signing Date 03/01/2026）',
  '',
  '备注：具体口径 TBD，详见附件。',
].join('\n');

/* -------------------------------------------------------------- 主入口 */

/**
 * 执行免费档的六项AI核对。
 * @param {Object|String} payload {text} | {content} | 纯文本
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const mat = collectMaterial(payload);
  if (!mat.text) return insufficient(mat.missing, mat.advice || '请提供合同全文后再核对。');

  const a = analyze(mat.text);
  const signals = contentSignals(a);
  if (!signals.length && !(a.lines.filter((l) => l.trim()).length >= 3 && a.text.trim().length >= 60)) {
    return insufficient(
      [`这段材料（${a.text.trim().length} 个字符）里没有识别出任何可核对的合同要素：当事方标记、日期、金额、条款编号、占位符、定义句式、签署栏，一个都没有。`],
      '请提供合同正文（中英文均可）。要触发检查，材料里至少要有其中一类要素。'
    );
  }

  const findings = [].concat(
    checkParties(a),
    checkDates(a),
    checkAmounts(a),
    checkPlaceholders(a),
    checkClauses(a),
    checkDefinitions(a)
  ).sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'CONTRACT_CONSISTENCY_FREE',
    scope: {
      checks: CHECKS_GIVEN,
      chars: a.text.trim().length,
      lines: a.lines.length,
      counts: {
        dates: a.dates.length,
        amounts: a.amounts.length,
        cn_capitals: a.capitals.length,
        en_word_amounts: a.words.length,
        parties: a.parties.length,
        clauses: a.clauses.length,
        clause_refs: a.refs.length,
        placeholders: a.placeholders.length,
        definitions: a.definitions.length,
      },
      signals: signals,
      tolerance: TOLERANCE,
      executed_locally: true,
      network_used: false,
    },
    findings: findings,
    summary: {
      p0: p0,
      p1: p1,
      p2: p2,
      total: findings.length,
      verdict: p0 ? 'CONTRADICTION_FOUND' : (findings.length ? 'ISSUES_FOUND' : 'CLEAN'),
      omitted: 0,
    },
    note: '本结果只覆盖上面六项AI核对，每一条都引用了出问题的原文、数字或行号，可由第三方用同一份输入复算；'
      + '其余检查项见 checks_withheld，本次未执行，也不会用默认值编造结论。',
    disclaimer: '只做AI一致性核对，不构成法律意见、不做合法性认定、不评估商业条款是否公平；'
      + '本工具不联网、不外发材料，也不调用任何模型。',
  };

  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectMaterial,
  collectDates,
  collectAmounts,
  collectCnCapitals,
  collectEnWordAmounts,
  collectParties,
  collectClauses,
  collectPlaceholders,
  collectDefinitions,
  parseCnCapital,
  parseEnWords,
  cnToNumber,
  normName,
  SAMPLE_TEXT,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
