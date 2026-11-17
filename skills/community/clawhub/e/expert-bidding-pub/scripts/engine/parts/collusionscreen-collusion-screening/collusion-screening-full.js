'use strict';
/**
 * collusion-screening.js —— 串通投标线索筛查（本包）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 本包只做两项跨家交叉比对，别无其他：
 *   1. 联系方式一致 —— 电话 / 邮箱 / 统一社会信用代码 / 银行账号 在不同投标人之间重复；
 *   2. 项目成员交叉 —— 项目经理、技术负责人等关键人名在不同投标人之间重复。
 *
 * **输出一律脱敏**：电话/邮箱/统一社会信用代码/银行账号 与 自然人姓名 都先脱敏再进结果
 * （例如 13800138000 → 138****00，张三 → 张*）。投标人（机构）名称保留原样 ——
 * 线索必须能落到具体是哪两家，否则这份报告没法用；机构名称本身不是个人信息。
 *
 * **订阅版（买断版）：上面两项 + 下面六项，共 8 项全部执行**
 *   3) 文本异常一致   4) 报价规律性差异   5) 文件相互混装
 *   6) 同一处错漏     7) 保证金同源       8) 格式指纹一致
 * 判据全部可复算；其中「文本异常一致」「同一处错漏」会**先剔除模板套话**，
 * 避免把招投标文件里家家都有的"投标人须知/承诺书"当成雷同证据。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const CHECKS_GIVEN = [
  '联系方式一致', '项目成员交叉',
  '文本异常一致', '报价规律性差异', '文件相互混装',
  '同一处错漏', '保证金同源', '格式指纹一致',
];

// 订阅版没有"未执行"的检查项 —— 这个空数组本身就是对买家的承诺，
// 由 tools/buyout_tier_check.py 兜底核对。
const CHECKS_WITHHELD = [];

const FINDING_TYPES = {
  CONTACT_SHARED: { level: 'P0', label: '联系方式一致', basis: '《招标投标法实施条例》第四十条（二）' },
  PERSONNEL_SHARED: { level: 'P0', label: '项目成员交叉', basis: '《招标投标法实施条例》第四十条（三）' },
  MIXED_DOCS: { level: 'P0', label: '文件相互混装', basis: '《招标投标法实施条例》第四十条（六）' },
  DEPOSIT_SAME_SOURCE: { level: 'P0', label: '保证金同源', basis: '《招标投标法实施条例》第四十条（六）' },
  TEXT_IDENTICAL: { level: 'P1', label: '文本异常一致', basis: '《招标投标法实施条例》第四十条（一）' },
  PRICE_PATTERN: { level: 'P1', label: '报价规律性差异', basis: '《招标投标法实施条例》第四十条（五）' },
  SAME_TYPO: { level: 'P1', label: '同一处错漏', basis: '《招标投标法实施条例》第四十条（一）' },
  FORMAT_FINGERPRINT: { level: 'P2', label: '格式指纹一致', basis: '《招标投标法实施条例》第四十条（一）' },
};

/* ---------------------------------------------------------------- 工具 */

function normalize(text) {
  return String(text == null ? '' : text)
    .replace(/\u3000/g, ' ')
    .replace(/[\s\u00a0]+/g, ' ');
}

/** 至少 2 个字符才算"有正文可比对"（1 个字符比不出任何东西，不能被当成"已检查且干净"） */
function usableText(bidder) {
  return normalize(bidder.text).trim().length >= 2;
}

/* ---------------------------------------------------------------- 脱敏 */

function maskContact(v) {
  const s = String(v);
  if (s.includes('@')) {
    const parts = s.split('@');
    return `${parts[0].slice(0, 2)}***@${parts.slice(1).join('@')}`;
  }
  if (s.length <= 6) return s.slice(0, 1) + '***';
  return `${s.slice(0, 3)}****${s.slice(-2)}`;
}

function maskName(n) {
  const s = String(n == null ? '' : n);
  return s.length <= 1 ? s : s[0] + '*'.repeat(s.length - 1);
}

/* ------------------------------------------------------------ 联系方式提取 */

/** 统一社会信用代码的字符集（不含 I O S V Z） */
const USCC_CHARS = '0-9A-HJ-NPQRTUWXY';

function extractContacts(text) {
  const t = String(text == null ? '' : text);
  const out = { phones: new Set(), emails: new Set(), uscc: new Set(), accounts: new Set() };

  for (const m of t.matchAll(/(?<!\d)(1[3-9]\d{9})(?!\d)/g)) out.phones.add(m[1]);
  for (const m of t.matchAll(/(?<!\d)(0\d{2,3}-?\d{7,8})(?!\d)/g)) out.phones.add(m[1].replace(/-/g, ''));
  for (const m of t.matchAll(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g)) out.emails.add(m[0].toLowerCase());

  // 统一社会信用代码：① 带标签的直接取；② 裸串必须是 18 位且至少含一个字母
  //（纯 18 位数字更可能是银行账号，把它当成信用代码会凭空造出一条假线索）
  for (const m of t.matchAll(/(?:统一社会信用代码|信用代码|纳税人识别号)[:：]?\s*([0-9A-Z]{15,20})/g)) out.uscc.add(m[1]);
  const bareUscc = new RegExp(`(?<![0-9A-Z])[${USCC_CHARS}]{18}(?![0-9A-Z])`, 'g');
  for (const m of t.matchAll(bareUscc)) {
    if (/[A-Z]/.test(m[0])) out.uscc.add(m[0]);
  }

  for (const m of t.matchAll(/(?:账号|帐号|账户|卡号)[:：]?\s*([0-9]{8,25})/g)) out.accounts.add(m[1]);

  return out;
}

/* ------------------------------------------------------------ 人名提取 */

const LEADING_NOISE_CHARS = new Set('由派拟经系为该本我其并及与和的将把对向从据依'.split(''));

const NON_NAME_TOKENS = new Set([
  '签字', '盖章', '负责', '常驻', '现场', '全面', '管理', '姓名', '身份', '职务',
  '电话', '手机', '邮箱', '地址', '联系', '方式', '简历', '证书', '资质', '业绩',
  '经验', '能力', '水平', '情况', '说明', '备注', '附件', '表格', '填写', '办理',
  '进行', '工作', '内容', '要求', '标准', '规范', '规定', '项目', '工程', '公司',
  '单位', '部门', '人员', '法定', '代表', '委托', '代理', '承诺', '保证', '同意',
  '接受', '遵守', '执行', '完成', '提供', '以上', '如下', '下述', '有关', '相关',
]);

/**
 * 从文本中提取关键岗位的人名。
 * 必须保守：把「签字盖章」当成一个人名，会让用户看到一条假的人员交叉线索 ——
 * 一条明显的假警报会让人怀疑整份报告，比漏报更伤可信度。
 */
function extractPersonnel(text) {
  const t = String(text == null ? '' : text);
  const names = new Set();

  const clean = (raw) => {
    let cand = raw;
    // 剥掉可能被吃进来的前导虚词，但剥完仍需至少 2 字（避免把复姓削掉）
    if (cand.length > 2 && LEADING_NOISE_CHARS.has(cand[0])) cand = cand.slice(1);
    if (NON_NAME_TOKENS.has(cand)) return null;
    if (cand.length < 2) return null;
    return cand;
  };

  const follower = '负责|签字|盖章|电话|手机|联系|常驻|全面|管理|同志|先生|女士|经理|工程师|驻场|到场';
  const boundary = `[，。；、,.;:：\\s）)】」”"'/]|$|${follower}`;
  // 「法定代表人」必须排在「法人」前面，否则「法定代表人：王五」只会匹配到「法人」，
  // 后面紧跟的「代表」又不是合法姓名 —— 这一步顺序错了会整条漏掉。
  const roles = '项目经理|项目负责人|技术负责人|项目总监|总监理工程师|建造师|总监|负责人|联系人|法定代表人|法人';
  const forward = new RegExp(`(?:${roles})[:：\\s]*([\\u4e00-\\u9fa5]{2,3})(?=${boundary})`, 'g');
  for (const m of t.matchAll(forward)) {
    const cand = clean(m[1]);
    if (cand) names.add(cand);
  }

  // 人名在前、职务在后（「张伟明担任项目经理」）—— 只认前一种写法会漏掉一半真实标书
  const reverse = new RegExp(
    `([\\u4e00-\\u9fa5]{2,3})(?:担任|作为|任|系|为|出任)(?:本项目的?|该项目?的?|项目的?)?(?:${roles})`,
    'g',
  );
  for (const m of t.matchAll(reverse)) {
    const cand = clean(m[1]);
    if (cand) names.add(cand);
  }

  return names;
}

/* -------------------------------------------------------------- 入参归一 */

function pickText(b) {
  if (typeof b.text === 'string') return b.text;
  if (typeof b.content === 'string') return b.content;
  if (typeof b.body === 'string') return b.body;
  return '';
}

function toBidders(input) {
  const raw = Array.isArray(input) ? input : (input && Array.isArray(input.bidders) ? input.bidders : []);
  const list = [];
  for (let i = 0; i < raw.length; i++) {
    const b = (raw[i] && typeof raw[i] === 'object') ? raw[i] : {};
    const name = String(b.name != null ? b.name : (b.bidder != null ? b.bidder : (b.company != null ? b.company : `投标人${i + 1}`)));
    const personnel = [];
    const src = Array.isArray(b.personnel) ? b.personnel : (Array.isArray(b.members) ? b.members : (Array.isArray(b.staff) ? b.staff : []));
    for (const p of src) {
      const n = typeof p === 'string' ? p : (p && (p.name || p.姓名));
      if (n) personnel.push(String(n).trim());
    }
    const contacts = (b.contacts && typeof b.contacts === 'object') ? b.contacts : {};
    list.push({
      name, text: pickText(b), personnel, contacts, index: i,
      // 订阅版追加检查要用到（报价规律、保证金同源）：本包不需要，所以这里才带上
      quote: b.quote != null ? b.quote : (b.amount != null ? b.amount : b.报价),
      deposit: b.deposit || b.保证金 || null,
    });
  }
  return list;
}

/* ================================================================== 订阅版追加检查
 * 本包声明了 6 项"未执行"的检查，订阅版**逐项真的执行**：
 *   3) 文本异常一致   4) 报价规律性差异   5) 文件相互混装
 *   6) 同一处错漏     7) 保证金同源       8) 格式指纹一致
 * 全部判据都写成"能从材料里复算出来"的形式，不含任何主观打分。
 * 输出与本包一致：电话/邮箱/统一社会信用代码/银行账号/自然人姓名先脱敏再进结果。
 * ================================================================ */

/* 常见非规范写法（错别字/异体字）。只用于「同一处错漏」：
 * 光有错字不算线索，**两家以上在同一个句子里犯同一个错**才算。 */
const NONSTANDARD_VARIANTS = ['峻工', '签定', '帐', '按装', '既使', '必须品'];

/* 通用词：与 BOILERPLATE 一起用于剔除套话（见 segments 里 substance 判定） */
const GENERIC_WORDS = ['投标', '文件', '材料', '提供', '加盖', '公章', '复印件', '原件', '我方', '本项目', '招标', '要求', '承诺', '证明', '身份', '法定', '代表', '授权', '委托', '报价', '营业', '执照', '资质', '证书', '保证金', '凭证', '统一', '社会', '信用', '代码', '正本', '副本', '扫描件'];

/* 模板化套话（招投标文件里家家都有，不能当"异常一致"的证据） */
const BOILERPLATE = [
  '投标人名称', '法定代表人', '投标人须知', '招标文件', '投标文件', '投标有效期',
  '承诺书', '授权委托书', '我方承诺', '特此声明', '投标报价表', '开标一览表',
];

/** 把正文切成可比的"段"：按换行与中文句末标点切，去空白、去纯数字/纯标点。 */
function rawText(text) {
  // ⛔ 不能用 normalize()：它把 \n 也压成空格（那是给"跨行比对"用的），
  //    分段与格式指纹都必须保留原始换行，否则整篇会变成一段。
  return String(text == null ? '' : text).replace(/\r\n?/g, '\n')
    .replace(/[\t\u3000\u00a0]+/g, ' ');
}

function segments(text) {
  const norm = rawText(text);
  const parts = norm.split(/\n+|(?<=[。；;])/);
  const out = [];
  for (const raw of parts) {
    const seg = raw.replace(/[ \t\u3000]+/g, ' ').trim();
    if (seg.length < 10) continue;
    if (!/[\u4e00-\u9fa5]/.test(seg)) continue;                  // 必须含中文，纯数字/符号段不要
    // 套话剔除：把"标准要件名 + 通用词"去掉后剩下的实义中文太少 ⇒ 不算可比对的雷同证据。
    // （第一版只挡短段，于是"投标函 法定代表人身份证明 授权委托书…"这种清单被当成异常一致。）
    let rest = seg;
    for (const b of BOILERPLATE) rest = rest.split(b).join('');
    for (const w of GENERIC_WORDS) rest = rest.split(w).join('');
    if (rest.replace(/[\s\d\p{P}\p{S}]/gu, '').length < 12) continue;
    out.push(seg);
  }
  return out;
}

/** 脱敏：把段里的电话/邮箱/统一社会信用代码/银行账号/自然人姓名都打码。 */
function maskSegment(seg, personnelNames) {
  let s = seg;
  s = s.replace(/1[3-9]\d{9}/g, (m) => maskContact(m));
  s = s.replace(/[\w.+-]+@[\w-]+\.[\w.]+/g, (m) => maskContact(m));
  s = s.replace(/\b[A-Z0-9]{18}\b/g, (m) => maskContact(m));
  s = s.replace(/\b\d{12,25}\b/g, (m) => maskContact(m));
  for (const n of personnelNames) {
    if (n && n.length >= 2) s = s.split(n).join(maskName(n));
  }
  // 身份证号（18 位，最后一位可能是 X）
  s = s.replace(/\b\d{17}[\dXx]\b/g, (m) => m.slice(0, 6) + '********' + m.slice(-2));
  return s;
}

/** 报价：优先用结构化字段，其次从正文里找"投标报价/报价/总价"后的数字。 */
function quoteOf(b) {
  const direct = [b.quote, b.amount, b.price, b.total, b['报价'], b['投标报价']];
  for (const v of direct) {
    if (v === undefined || v === null || v === '') continue;
    const n = Number(String(v).replace(/[,，\s元]/g, ''));
    if (Number.isFinite(n) && n > 0) return n;
  }
  const m = normalize(b.text).match(/(?:投标报价|报价|总价|投标总价)[^\d]{0,8}([0-9][0-9,]*(?:\.[0-9]+)?)/);
  if (m) {
    const n = Number(m[1].replace(/,/g, ''));
    if (Number.isFinite(n) && n > 0) return n;
  }
  return null;
}

/** 保证金：结构化 deposit，或正文里的"保证金 … 账户/付款人/单位"。 */
function depositOf(b) {
  const d = (b.deposit && typeof b.deposit === 'object') ? b.deposit : {};
  const out = {
    payer: String(d.payer || d['付款人'] || d['缴纳人'] || d['单位'] || '').trim(),
    account: String(d.account || d['账号'] || d['账户'] || '').trim(),
    bank: String(d.bank || d['开户行'] || '').trim(),
  };
  const text = normalize(b.text);
  const mp = text.match(/保证金[^\n。；]{0,40}?(?:付款人|缴纳人|缴纳单位|投标人)[^\u4e00-\u9fa5]{0,4}([\u4e00-\u9fa5（）()]{4,30})/);
  if (!out.payer && mp) out.payer = mp[1].replace(/[（）()]/g, '').trim();
  const ma = text.match(/(?:保证金|投标保证金)[^\n。；]{0,60}?(?:账号|账户)\s*[:：]?\s*([0-9]{8,25})/);
  if (!out.account && ma) out.account = ma[1];
  return out;
}

/** 格式指纹：行数 + 小标题序列（"一、/第X章/…："这类）。 */
function fingerprintOf(b) {
  const lines = rawText(b.text).split(/\n+/).map((x) => x.trim()).filter(Boolean);
  const heads = lines.filter((l) => /^([一二三四五六七八九十百]+[、.．)）]|第[一二三四五六七八九十百]+[章节条部分]|[\u4e00-\u9fa5]{2,12}[:：]$)/.test(l))
    .map((l) => l.replace(/\s+/g, ''));
  return { lineCount: lines.length, heads, headKey: heads.join('|') };
}

/** 段落 -> 出现的投标人下标集合。 */
function segmentIndex(pool) {
  const map = new Map();
  for (const b of pool) {
    for (const seg of segments(b.text)) {
      if (!map.has(seg)) map.set(seg, new Set());
      map.get(seg).add(b.index);
    }
  }
  return map;
}

/** --- 3) 文本异常一致：两家以上出现**同一段**较长的文字（>20 字）。 */
function checkTextIdentical(pool, segmentsMap, findings) {
  const hits = [];
  for (const [seg, who] of segmentsMap) {
    if (who.size < 2) continue;
    if (seg.length < 20) continue;
    hits.push({ seg, who: [...who] });
  }
  hits.sort((x, y) => y.seg.length - x.seg.length || x.who[0] - y.who[0]);
  for (const h of hits.slice(0, 20)) {
    const names = h.who.map((i) => pool.find((b) => b.index === i).name);
    const seg = maskSegment(h.seg, allPersonnel(pool));
    findings.push({
      type: 'TEXT_IDENTICAL',
      level: FINDING_TYPES.TEXT_IDENTICAL.level,
      label: FINDING_TYPES.TEXT_IDENTICAL.label,
      basis: FINDING_TYPES.TEXT_IDENTICAL.basis,
      detail: `${names.join(' 与 ')} 的正文里有 ${h.seg.length} 个字完全相同`,
      evidence: { segment: seg.length > 80 ? seg.slice(0, 80) + '…' : seg, length: h.seg.length, bidders: names },
      advice: '核对这几家的投标文件是不是同一台机器、同一份底稿改出来的：'
        + '比对文档属性（作者/创建时间）与文件命名习惯。',
    });
  }
}

/** --- 4) 报价规律性差异：3 家以上时，报价呈等差/等比或固定比例。 */
function checkPricePattern(pool, findings) {
  const rows = pool.map((b) => ({ name: b.name, q: quoteOf(b) })).filter((r) => r.q !== null);
  if (rows.length < 3) return;
  const sorted = [...rows].sort((x, y) => x.q - y.q);
  const diffs = [];
  for (let i = 1; i < sorted.length; i++) diffs.push(sorted[i].q - sorted[i - 1].q);
  const ratios = [];
  for (let i = 1; i < sorted.length; i++) ratios.push(sorted[i].q / sorted[i - 1].q);

  const diffEqual = diffs.length >= 2 && (Math.max(...diffs) - Math.min(...diffs)) <= Math.max(1, sorted[0].q * 0.0005);
  const ratioEqual = ratios.length >= 2 && (Math.max(...ratios) - Math.min(...ratios)) <= 0.0005;

  if (!diffEqual && !ratioEqual) return;
  const how = diffEqual && ratioEqual ? '既等差又等比' : (diffEqual ? '等差' : '等比');
  findings.push({
    type: 'PRICE_PATTERN',
    level: FINDING_TYPES.PRICE_PATTERN.level,
    label: FINDING_TYPES.PRICE_PATTERN.label,
    basis: FINDING_TYPES.PRICE_PATTERN.basis,
    detail: `${sorted.length} 家报价从低到高呈「${how}」规律（差 ${diffs.map((d) => d.toFixed(2)).join('、')}）`,
    evidence: {
      quotes: sorted.map((r) => ({ bidder: r.name, quote: r.q })),
      diffs: diffs.map((d) => Number(d.toFixed(2))),
      ratios: ratios.map((r) => Number(r.toFixed(6))),
    },
    advice: '报价呈机械规律通常意味着同源报价：调取各家的报价编制过程与电子文件。',
  });
}

/** --- 5) 文件相互混装：甲家的正文里出现乙家的公司名。 */
function checkMixedDocs(pool, findings) {
  const nameOf = new Map(pool.map((b) => [b.index, b.name]));
  for (const b of pool) {
    const text = normalize(b.text);
    for (const other of pool) {
      if (other.index === b.index) continue;
      const nm = String(other.name).replace(/\s+/g, '');
      if (nm.length < 4) continue;                                 // 太短的名字容易误命中
      if (text.replace(/\s+/g, '').includes(nm)) {
        findings.push({
          type: 'MIXED_DOCS',
          level: FINDING_TYPES.MIXED_DOCS.level,
          label: FINDING_TYPES.MIXED_DOCS.label,
          basis: FINDING_TYPES.MIXED_DOCS.basis,
          detail: `${b.name} 的正文里出现了「${other.name}」的名称`,
          evidence: { inBidder: b.name, foundName: other.name },
          advice: '这通常说明两家共用同一份底稿：核对文件来源、制作机器与递交记录。',
        });
      }
    }
  }
}

/** --- 6) 同一处错漏：两家以上在同一句话里出现同一个非规范写法。 */
function checkSameTypo(pool, segmentsMap, findings) {
  const names = allPersonnel(pool);
  for (const [seg, who] of segmentsMap) {
    if (who.size < 2) continue;
    const bad = NONSTANDARD_VARIANTS.filter((v) => seg.includes(v));
    if (!bad.length) continue;
    const bidders = [...who].map((i) => pool.find((b) => b.index === i).name);
    findings.push({
      type: 'SAME_TYPO',
      level: FINDING_TYPES.SAME_TYPO.level,
      label: FINDING_TYPES.SAME_TYPO.label,
      basis: FINDING_TYPES.SAME_TYPO.basis,
      detail: `${bidders.join(' 与 ')} 在同一句话里都写成「${bad.join('、')}」`,
      evidence: {
        segment: maskSegment(seg.length > 80 ? seg.slice(0, 80) + '…' : seg, names),
        variants: bad, bidders,
      },
      advice: '同一个非规范写法出现在多家的同一句话里，是"同一份底稿"的强线索：'
        + '比对这几处文字的上下文与排版。',
    });
  }
}

/** --- 7) 保证金同源：付款人/账号/开户行在多家中重复。 */
function checkDepositSameSource(pool, findings) {
  const kinds = [['payer', '付款人'], ['account', '账号'], ['bank', '开户行']];
  for (const [field, label] of kinds) {
    const map = new Map();
    for (const b of pool) {
      const v = depositOf(b)[field];
      if (!v) continue;
      if (field === 'bank' && v.length < 4) continue;               // 开户行太短不判
      if (!map.has(v)) map.set(v, new Set());
      map.get(v).add(b.index);
    }
    for (const [value, who] of map) {
      if (who.size < 2) continue;
      const bidders = [...who].map((i) => pool.find((b) => b.index === i).name);
      findings.push({
        type: 'DEPOSIT_SAME_SOURCE',
        level: FINDING_TYPES.DEPOSIT_SAME_SOURCE.level,
        label: FINDING_TYPES.DEPOSIT_SAME_SOURCE.label,
        basis: FINDING_TYPES.DEPOSIT_SAME_SOURCE.basis,
        detail: `${bidders.join(' 与 ')} 的投标保证金${label}相同`,
        evidence: {
          kind: label,
          value: field === 'bank' ? value : maskContact(value),
          bidders,
        },
        advice: '保证金由同一主体缴纳是《招标投标法实施条例》第四十条列明的情形之一：'
          + '调取银行进账凭证与缴款回单。',
      });
    }
  }
}

/** --- 8) 格式指纹一致：小标题序列（≥4 个）与行数完全一致。 */
function checkFormatFingerprint(pool, findings) {
  const fps = pool.map((b) => ({ name: b.name, fp: fingerprintOf(b) }));
  for (let i = 0; i < fps.length; i++) {
    for (let j = i + 1; j < fps.length; j++) {
      const a = fps[i].fp; const b = fps[j].fp;
      if (a.heads.length < 4) continue;
      if (a.headKey !== b.headKey) continue;
      if (Math.abs(a.lineCount - b.lineCount) > 1) continue;
      findings.push({
        type: 'FORMAT_FINGERPRINT',
        level: FINDING_TYPES.FORMAT_FINGERPRINT.level,
        label: FINDING_TYPES.FORMAT_FINGERPRINT.label,
        basis: FINDING_TYPES.FORMAT_FINGERPRINT.basis,
        detail: `${fps[i].name} 与 ${fps[j].name} 的小标题序列（${a.heads.length} 个）与行数（${a.lineCount}/${b.lineCount}）完全一致`,
        evidence: { bidders: [fps[i].name, fps[j].name], headings: a.heads.slice(0, 8), lineCounts: [a.lineCount, b.lineCount] },
        advice: '结构逐项对齐通常来自同一模板：核对文件属性（作者、创建时间、模板路径）。',
      });
    }
  }
}

/** 汇总池里所有出现过的自然人姓名（用于脱敏）。 */
function allPersonnel(pool) {
  const set = new Set();
  for (const b of pool) {
    for (const n of extractPersonnel(b.text)) set.add(n);
    for (const n of b.personnel) set.add(String(n).trim());
  }
  return [...set];
}

/* ------------------------------------------------------------------ 主入口 */

/**
 * 执行本包的两项跨家交叉比对。
 * @param {Object|Array} payload { bidders: [{ name, text, contacts?, personnel? }] } 或直接给数组
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  // 入参类型不对时如实报"材料不足"，绝不把空材料当成"已检查且干净"
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return {
      status: 'insufficient_input',
      missing: [`入参不是对象或数组（收到的是 ${typeof payload}）`],
      advice: '传 {"bidders":[{"name":"…","text":"…"}, …]}，至少 2 家；或直接传 bidders 数组。',
    };
  }
  if (payload && !Array.isArray(payload) && payload.bidders !== undefined && !Array.isArray(payload.bidders)) {
    return {
      status: 'insufficient_input',
      missing: [`bidders 不是数组（收到的是 ${typeof payload.bidders}）`],
      advice: 'bidders 需要是数组：[{"name":"投标人甲","text":"投标文件正文…"}, …]，至少 2 家。',
    };
  }

  const bidders = toBidders(payload);
  if (bidders.length < 2) {
    return {
      status: 'insufficient_input',
      missing: [`跨家交叉比对至少需要 2 家投标人，当前只有 ${bidders.length} 家`],
      advice: '串通线索只能从多家材料的交叉比对里看出来，单家材料比不出任何东西：'
        + '请把同一标段各家投标文件的正文（text）一并传进来。',
    };
  }

  const withText = bidders.filter(usableText);
  if (withText.length < 2) {
    const lacking = bidders
      .filter((b) => !usableText(b))
      .map((b) => `${b.name}（text ${normalize(b.text).trim() ? `只有 ${normalize(b.text).trim().length} 个字符` : '为空'}）`);
    return {
      status: 'insufficient_input',
      missing: [
        `需要有 2 家以上提供可比的 text 正文，当前只有 ${withText.length} 家够用`,
        `正文不可用的投标人：${lacking.join('、')}`,
      ],
      advice: '联系方式与项目管理成员都只能从正文里提取：请补齐每一家的 text（投标文件的正文部分）。',
    };
  }

  const findings = [];

  /* --- 1) 联系方式一致 --- */
  const kinds = [
    ['phones', '电话'],
    ['emails', '邮箱'],
    ['uscc', '统一社会信用代码'],
    ['accounts', '银行账号'],
  ];
  for (const [field, kindLabel] of kinds) {
    const map = new Map();   // 值 -> Set(投标人下标)
    for (const b of withText) {
      const c = extractContacts(b.text);
      const extra = b.contacts[field];
      const values = new Set([...c[field], ...[].concat(extra === undefined || extra === null ? [] : extra).filter(Boolean).map(String)]);
      for (const v of values) {
        if (!map.has(v)) map.set(v, new Set());
        map.get(v).add(b.index);
      }
    }
    for (const [value, who] of map) {
      if (who.size < 2) continue;
      const names = [...who].map((i) => bidders[i].name);
      findings.push({
        type: 'CONTACT_SHARED',
        level: FINDING_TYPES.CONTACT_SHARED.level,
        label: FINDING_TYPES.CONTACT_SHARED.label,
        basis: FINDING_TYPES.CONTACT_SHARED.basis,
        detail: `${names.join(' 与 ')} 的${kindLabel}相同`,
        evidence: { kind: kindLabel, value: maskContact(value), bidders: names },
        advice: '核对投标文件的编制人、委托代理人及联系方式来源；调取相应文件的制作记录。',
      });
    }
  }

  /* --- 2) 项目成员交叉 --- */
  const personMap = new Map();
  for (const b of withText) {
    const names = new Set([...extractPersonnel(b.text), ...b.personnel]);
    for (const n of names) {
      const name = String(n).trim();
      if (name.length < 2) continue;
      if (!personMap.has(name)) personMap.set(name, new Set());
      personMap.get(name).add(b.index);
    }
  }
  for (const [name, who] of personMap) {
    if (who.size < 2) continue;
    const names = [...who].map((i) => bidders[i].name);
    findings.push({
      type: 'PERSONNEL_SHARED',
      level: FINDING_TYPES.PERSONNEL_SHARED.level,
      label: FINDING_TYPES.PERSONNEL_SHARED.label,
      basis: FINDING_TYPES.PERSONNEL_SHARED.basis,
      detail: `人员「${maskName(name)}」同时出现在 ${who.size} 家投标人的文件中`,
      evidence: { personnel: maskName(name), bidders: names },
      advice: '核对该人员的社保缴纳单位与劳动合同归属；确认是否存在挂靠或代编。',
    });
  }

  /* --- 3~8) 订阅版追加的六项检查 --- */
  const pool = withText;
  const segMap = segmentIndex(pool);
  checkTextIdentical(pool, segMap, findings);
  checkPricePattern(pool, findings);
  checkMixedDocs(pool, findings);
  checkSameTypo(pool, segMap, findings);
  checkDepositSameSource(pool, findings);
  checkFormatFingerprint(pool, findings);

  const levelRank = { P0: 0, P1: 1, P2: 2 };
  findings.sort((a, b) => (levelRank[a.level] - levelRank[b.level]) || a.type.localeCompare(b.type));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const extractStats = withText.reduce((acc, b) => {
    const c = extractContacts(b.text);
    acc.contacts += c.phones.size + c.emails.size + c.uscc.size + c.accounts.size;
    acc.personnel += extractPersonnel(b.text).size + b.personnel.length;
    return acc;
  }, { contacts: 0, personnel: 0 });

  const result = {
    status: 'success',
    service_type: 'COLLUSION_SCREEN_FULL',
    scope: {
      checks: CHECKS_GIVEN,
      full_tier: paid,
      bidders: bidders.length,
      bidders_compared: withText.length,
      bidders_without_usable_text: bidders.length - withText.length,
      contacts_extracted: extractStats.contacts,
      personnel_extracted: extractStats.personnel,
      desensitized: true,
      masking: '电话/邮箱/统一社会信用代码/银行账号/自然人姓名均已脱敏（如 138****00、张*）；投标人机构名称保留',
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      p0,
      p1,
      p2,
      total: findings.length,
      verdict: findings.length ? 'SHARED_LEAD_FOUND' : 'NO_SHARED_LEAD',
      omitted: 0,
    },
    note: '本结果覆盖全部 8 项跨家交叉比对（完整档无未执行项）；'
      + '命中只是**客观线索**，不是串通的认定。',
    disclaimer: '只输出客观、可复算的雷同线索，不做串通投标的法律定性；'
      + '认定权在评标委员会与行政监督部门。线索可由第三方用同一份输入复算。',
  };

  return { status: 'success', result };
}

module.exports = {
  run,
  extractContacts,
  extractPersonnel,
  maskContact,
  maskName,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
