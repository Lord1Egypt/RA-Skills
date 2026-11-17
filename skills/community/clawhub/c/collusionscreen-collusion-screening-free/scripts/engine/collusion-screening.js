'use strict';
/**
 * collusion-screening.js —— 串通投标线索筛查（免费档）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 免费档只做两项跨家交叉比对，别无其他：
 *   1. 联系方式一致 —— 电话 / 邮箱 / 统一社会信用代码 / 银行账号 在不同投标人之间重复；
 *   2. 项目成员交叉 —— 项目经理、技术负责人等关键人名在不同投标人之间重复。
 *
 * **输出一律脱敏**：电话/邮箱/统一社会信用代码/银行账号 与 自然人姓名 都先脱敏再进结果
 * （例如 13800138000 → 138****00，张三 → 张*）。投标人（机构）名称保留原样 ——
 * 线索必须能落到具体是哪两家，否则这份报告没法用；机构名称本身不是个人信息。
 *
 * 刻意不实现（那些属于本版本范围之外的检查项，见 CHECKS_WITHHELD）：
 *   文本异常一致、报价规律性差异、文件相互混装、同一处错漏、保证金同源、格式指纹一致。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const CHECKS_GIVEN = ['联系方式一致', '项目成员交叉'];

const CHECKS_WITHHELD = [
  '文本异常一致',
  '报价规律性差异',
  '文件相互混装',
  '同一处错漏',
  '保证金同源',
  '格式指纹一致',
];

const FINDING_TYPES = {
  CONTACT_SHARED: { level: 'P0', label: '联系方式一致', basis: '《招标投标法实施条例》第四十条（二）' },
  PERSONNEL_SHARED: { level: 'P0', label: '项目成员交叉', basis: '《招标投标法实施条例》第四十条（三）' },
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
    list.push({ name, text: pickText(b), personnel, contacts, index: i });
  }
  return list;
}

/* ------------------------------------------------------------------ 主入口 */

/**
 * 执行免费档的两项跨家交叉比对。
 * @param {Object|Array} payload { bidders: [{ name, text, contacts?, personnel? }] } 或直接给数组
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
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

  findings.sort((a, b) => (a.type === b.type ? 0 : (a.type === 'CONTACT_SHARED' ? -1 : 1)));
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
    service_type: 'COLLUSION_SCREEN_FREE',
    scope: {
      checks: CHECKS_GIVEN,
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
    note: '本结果只覆盖「联系方式一致」与「项目成员交叉」两项跨家交叉比对；'
      + '其余线索类型见 checks_withheld，本次未执行。命中只是**客观线索**，不是串通的认定。',
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
