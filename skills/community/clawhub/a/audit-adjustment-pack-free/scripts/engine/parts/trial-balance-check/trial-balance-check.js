#!/usr/bin/env node
/**
 * trial-balance-check.js —— 试算平衡与期末结转核对（免费档 / 完整档共用源码）
 *
 * 真实痛点：**每家公司每月结账、每年审计前都必须先做试算平衡**。
 * 会计把总账/明细账导成一张「科目余额表」，要同时成立这几条：
 *   ① 资产负债类逐行：期末余额 = 期初余额 + 本期借方发生额 − 本期贷方发生额
 *   ② 损益类每月结转后：期末余额必须为 0（收入/成本/费用都结转到本年利润）
 *   ③ 三处借贷平衡：期初余额合计 = 0、本期借方发生额合计 = 本期贷方发生额合计、期末余额合计 = 0
 *   ④ 一级科目 = 其直接下级科目之和（科目层级小计）
 *   ⑤ 明细账与总账勾稽：表里的合计行 = 各一级科目之行之和
 * 这五条全是加减法，但科目一多、层级一深，人眼极易漏；**一笔借贷不平会带着错一路进报表**，
 * 所以它是"每月必须做、且完全能算出来对错"的典型。
 *
 * 与已有能力的区别：`invoice-consistency-check` 核发票本身、`vat-burden-check` 核申报口径的进销项；
 * 本能力核的是**账套自己的试算平衡与期末结转**（科目余额表内部勾稽），层面完全不同。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * 不发起任何网络请求（没有 fetch / http / https / net / dns / tls）。
 *
 * 金额口径（必须一致，否则会误判）：**借贷方向带符号填列 —— 借方余额为正、贷方余额为负**，
 * 本期借方/贷方发生额两列都填正数；发生额列请用**结转后口径**（含损益结转分录）。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查科目体系、不调用大模型；材料不足**绝不给结论**；不给会计政策意见。
 *
 * 免费档执行 7 项；完整档追加的 3 项见 CHECKS_WITHHELD（归因 + 结账前处理清单）。
 */

'use strict';

const CHECKS_GIVEN = [
  '资产负债类逐行复算（期末余额 = 期初余额 + 本期借方发生额 − 本期贷方发生额）',
  '损益类期末结转为零（期末余额必须为 0；发生额列应是含结转分录的结转后口径）',
  '借方合计与贷方合计相等（期初余额合计、本期发生额合计、期末余额合计三个口径）',
  '明细账与总账勾稽（表里的合计行 = 各一级科目行之和）',
  '科目层级小计（上级科目 = 其直接下级科目之和，逐列复核）',
  '重复科目检测（同一科目编码出现多行）',
  '空缺与非法值（必填列为空、占位符、非数字、科目类别无法识别）',
];

const CHECKS_WITHHELD = [
  '结账前不平差额归因（漏记 / 重复记账 / 科目串户 / 结转未做 / 方向反了，逐条给出证据行号）',
  '无法用行级证据归因的差额如实标为「待人工确认」并单列残余金额（不硬套原因）',
  '结账前处理清单（按金额排序的调整分录，写明借/贷科目与金额，每条都带原文行号）',
];

const OUT_OF_SCOPE = [
  '判断科目使用是否正确、科目体系是否应当调整（那是会计政策与制度的事）',
  '合并多套账、跨年度调整与追溯重述（只核你贴进来的这一张表）',
  '判断未达账项、暂估冲回、坏账核销等账外事项',
  '读取 Excel 或财务软件账套文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '科目编码\t科目名称\t科目类别\t期初余额\t本期借方发生额\t本期贷方发生额\t期末余额',
  '1001\t库存现金\t资产\t20000.00\t20000.00\t15000.00\t25000.00',
  '1002\t银行存款\t资产\t430000.00\t330000.00\t345000.00\t415000.00',
  '1122\t应收账款\t资产\t150000.00\t100000.00\t30000.00\t220000.00',
  '1122.01\t应收账款—甲公司\t资产\t100000.00\t80000.00\t30000.00\t150000.00',
  '1122.02\t应收账款—乙公司\t资产\t50000.00\t20000.00\t0.00\t70000.00',
  '2202\t应付账款\t负债\t-150000.00\t250000.00\t250000.00\t-150000.00',
  '2211\t应付职工薪酬\t负债\t-50000.00\t70000.00\t70000.00\t-50000.00',
  '4001\t实收资本\t权益\t-400000.00\t0.00\t0.00\t-400000.00',
  '4103\t本年利润\t权益\t0.00\t340000.00\t400000.00\t-60000.00',
  '6001\t主营业务收入\t损益\t0.00\t400000.00\t400000.00\t0.00',
  '6401\t主营业务成本\t损益\t0.00\t250000.00\t250000.00\t0.00',
  '6602\t管理费用\t损益\t0.00\t90000.00\t90000.00\t0.00',
  '合计\t合计\t\t0.00\t1850000.00\t1850000.00\t0.00',
].join('\n');

const TOL = 0.01;
const BALANCE_CLASS = '资产负债';
const PNL_CLASS = '损益';

// ⚠️ 关键词顺序即优先级：更具体的词必须排在更宽泛的词前面（本仓库踩过两次的坑，
//    见 tools/header_map_check.py）。这里「科目类别」必须排在「科目」前面，否则它会被
//    宽泛的「科目」抢走 name 角色，类别列静默不参与检查。
const ROLES = {
  code: ['科目编码', '科目代码', '科目编号'],
  cls: ['科目类别', '科目属性', '科目性质', '类别'],
  name: ['科目名称', '会计科目', '科目'],
  opening: ['期初余额', '期初'],
  debit: ['本期借方发生额', '本期借方', '借方发生额', '借方'],
  credit: ['本期贷方发生额', '本期贷方', '贷方发生额', '贷方'],
  closing: ['期末余额', '期末'],
};

const LABELS = {
  code: '科目编码', name: '科目名称', cls: '科目类别',
  opening: '期初余额', debit: '本期借方发生额', credit: '本期贷方发生额', closing: '期末余额',
};

const REQUIRED = ['code', 'name', 'cls', 'opening', 'debit', 'credit', 'closing'];
const AMOUNT_ROLES = ['opening', 'debit', 'credit', 'closing'];
const TOTAL_ROW_RE = /^(合计|总计|total)/i;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;
const PNL_WORDS = ['损益', '收入', '费用', '利润表'];
const BS_WORDS = ['资产负债', '资产', '负债', '所有者权益', '权益', '成本'];

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return {
      error: 'no_header',
      missingRoles: missingRoles.map((r) => LABELS[r]),
      headers: cols.map((c) => c.header),
    };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (TOTAL_ROW_RE.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const rawOf = (it, role) => String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
const codeOf = (it) => rawOf(it, 'code');
const nameOf = (it) => rawOf(it, 'name') || `第 ${it.line} 行科目`;
const who = (it) => `「${nameOf(it)}」（科目编码 ${codeOf(it) || '空'}）`;

function classOf(it) {
  const raw = rawOf(it, 'cls');
  if (!raw) return 'unknown';
  if (PNL_WORDS.some((w) => raw.indexOf(w) >= 0)) return PNL_CLASS;
  if (BS_WORDS.some((w) => raw.indexOf(w) >= 0)) return BALANCE_CLASS;
  return 'unknown';
}

function normCode(raw) {
  return String(raw === undefined || raw === null ? '' : raw).replace(/[^0-9A-Za-z]/g, '');
}

/** 科目层级：父行 = 直接下级行之和（编码前缀判定，兼容 1122.01 与 112201 两种写法） */
function hierarchyOf(items) {
  const entries = items.map((it) => ({ it, code: normCode(codeOf(it)) })).filter((e) => e.code !== '');
  const parentOf = new Map();
  for (const e of entries) {
    let best = null;
    for (const p of entries) {
      if (p === e) continue;
      if (e.code.length > p.code.length && e.code.indexOf(p.code) === 0) {
        if (!best || p.code.length > best.code.length) best = p;
      }
    }
    if (best) parentOf.set(e.it, best.it);
  }
  const childrenOf = new Map();
  for (const e of entries) {
    const p = parentOf.get(e.it);
    if (!p) continue;
    if (!childrenOf.has(p)) childrenOf.set(p, []);
    childrenOf.get(p).push(e.it);
  }
  const top = entries.filter((e) => !parentOf.get(e.it)).map((e) => e.it);
  return { parentOf, childrenOf, top };
}

function sumOf(rows, role) {
  return round2(rows.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
}

/* ===== 免费档执行 7 项（第 1 个 check 函数即变异测试的锚点，不要挪走） ===== */

function checkRowBalance(it) {
  if (classOf(it) !== BALANCE_CLASS) return null;
  const opening = num(it, 'opening');
  const debit = num(it, 'debit');
  const credit = num(it, 'credit');
  const stated = num(it, 'closing');
  if (opening === null || debit === null || credit === null || stated === null) return null;
  const expect = round2(opening + debit - credit);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '资产负债类余额复算不符', line: it.line,
    message: `${who(it)}第 ${it.line} 行的期末余额是 ${stated.toFixed(2)}，`
      + `按 期初余额 ${opening.toFixed(2)} + 本期借方发生额 ${debit.toFixed(2)} − 本期贷方发生额 ${credit.toFixed(2)} = ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '资产负债类科目只有这一条恒等式。对不上先看是不是漏了一笔发生额、或者借贷两列记反了。',
  };
}

function checkProfitLossClose(it) {
  if (classOf(it) !== PNL_CLASS) return null;
  const stated = num(it, 'closing');
  if (stated === null) return null;
  const debit = num(it, 'debit');
  const credit = num(it, 'credit');
  if (Math.abs(stated) > TOL) {
    return {
      level: 'P0', category: '损益类期末结转异常', line: it.line,
      message: `${who(it)}是损益类科目，结转后期末余额必须为 0，第 ${it.line} 行填的是 ${stated.toFixed(2)}。`,
      advice: '损益类每月结账都要结转到本年利润，结转后余额为 0；余额留在表里说明期末结转分录没做。',
    };
  }
  if (debit !== null && credit !== null && Math.abs(debit - credit) > TOL) {
    return {
      level: 'P1', category: '损益类期末结转异常', line: it.line,
      message: `${who(it)}第 ${it.line} 行的期末余额是 0，但本期借方发生额 ${debit.toFixed(2)} 与贷方发生额 ${credit.toFixed(2)} 不等`
        + `（相差 ${round2(debit - credit).toFixed(2)}），说明发生额列没有含结转分录。`,
      advice: '请用「结转后」口径导出发生额（借、贷两列都含结转分录）；否则借贷合计不会相等，后续复算也会跟着错。',
    };
  }
  return null;
}

function checkDebitCreditTotals(t) {
  const out = [];
  const h = hierarchyOf(t.items);
  const topLines = h.top.map((it) => it.line).join('、');
  // 科目编码整列缺失时没有"一级科目行"→ 退回到全部明细行的行号，绝不让取行号这一步抛错
  const anchorLine = t.totals.length ? t.totals[0].line
    : (h.top.length ? h.top[0].line : t.items[0].line);
  const opening = sumOf(h.top, 'opening');
  const debit = sumOf(h.top, 'debit');
  const credit = sumOf(h.top, 'credit');
  const closing = sumOf(h.top, 'closing');
  if (Math.abs(debit - credit) > TOL) {
    out.push({
      level: 'P0', category: '借贷合计不平', line: anchorLine,
      message: `本期借方发生额合计 ${debit.toFixed(2)} ≠ 本期贷方发生额合计 ${credit.toFixed(2)}，`
        + `相差 ${round2(debit - credit).toFixed(2)}（口径：一级科目行 第 ${topLines || anchorLine} 行，下级科目不重复计入）。`,
      advice: '借贷不平衡是试算平衡表的头号红灯：要么有单边分录，要么发生额被重复/漏计。',
    });
  }
  if (Math.abs(opening) > TOL) {
    out.push({
      level: 'P0', category: '借贷合计不平', line: anchorLine,
      message: `期初余额合计是 ${opening.toFixed(2)}，借贷两方应当相等（借方为正、贷方为负，合计应为 0）。`,
      advice: '期初不平说明上期期末就没平，或者本表漏了某些科目；先处理期初再往本月看。',
    });
  }
  if (Math.abs(closing) > TOL) {
    out.push({
      level: 'P0', category: '借贷合计不平', line: anchorLine,
      message: `期末余额合计是 ${closing.toFixed(2)}，借贷两方应当相等（借方为正、贷方为负，合计应为 0）。`,
      advice: '期末不平说明本月账没平；先查不符合恒等式的科目行，再看发生额借贷是否相等。',
    });
  }
  for (const row of t.totals) {
    for (const role of AMOUNT_ROLES) {
      const stated = num(row, role);
      if (stated === null) continue;
      const sum = sumOf(h.top, role);
      if (Math.abs(sum - stated) > TOL) {
        out.push({
          level: 'P0', category: '借贷合计不平', line: row.line,
          message: `第 ${row.line} 行合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，`
            + `各一级科目行（第 ${topLines || anchorLine} 行）相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
          advice: '合计行要么漏了科目，要么没跟着更新；它必须等于各一级科目行之和。',
        });
      }
    }
  }
  return out;
}

function checkHierarchy(t) {
  const out = [];
  const h = hierarchyOf(t.items);
  for (const [parent, kids] of h.childrenOf) {
    const kidLines = kids.map((k) => k.line).join('、');
    for (const role of AMOUNT_ROLES) {
      const stated = num(parent, role);
      if (stated === null) continue;
      const sum = sumOf(kids, role);
      if (Math.abs(sum - stated) > TOL) {
        out.push({
          level: 'P0', category: '科目层级小计不符', line: parent.line,
          message: `${who(parent)}第 ${parent.line} 行的「${LABELS[role]}」是 ${stated.toFixed(2)}，`
            + `但其直接下级（第 ${kidLines} 行）相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
          advice: '上级科目要么等于下级之和，要么就不该单独占一行；两者同时出现时，上级行不能重复参与合计。',
        });
      }
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = codeOf(it);
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复科目', line: it.line,
        message: `科目编码「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现（${nameOf(it)}）。`,
        advice: '同一科目编码出现两行，合计与层级小计都会被重复计入；请合并成一行，或确认是不是明细编码写重了。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = rawOf(it, role);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '空缺与非法值', line: it.line,
          message: `${who(it)}第 ${it.line} 行的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
        continue;
      }
      if (role !== 'code' && role !== 'name' && role !== 'cls' && num(it, role) === null) {
        out.push({
          level: 'P0', category: '空缺与非法值', line: it.line,
          message: `${who(it)}第 ${it.line} 行的「${LABELS[role]}」不是数字（填的是「${s}」）。`,
          advice: '金额列只能填数字（可带千分位与正负号）；中文备注、括号负数写法都要先转成规范数字。',
        });
      }
    }
    const cls = rawOf(it, 'cls');
    if (cls !== '' && classOf(it) === 'unknown') {
      out.push({
        level: 'P1', category: '空缺与非法值', line: it.line,
        message: `${who(it)}第 ${it.line} 行的「科目类别」是「${cls}」，认不出是资产负债类还是损益类。`,
        advice: '科目类别只认「资产 / 负债 / 权益（所有者权益）/ 损益（收入、费用）」这类写法，请照会计口径填。',
      });
    }
  }
  return out;
}

/* ===== 以下为完整档追加：不平差额归因 + 结账前处理清单（免费包整块被摘掉） ===== */

function run(payload) {
  if (payload === null || payload === undefined || typeof payload !== 'object' || Array.isArray(payload)) {
    return insufficient(['入参（一个对象，形如 {"text": "……"}）']);
  }
  const text = typeof payload.text === 'string' ? payload.text
    : (typeof payload.content === 'string' ? payload.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：总账/明细账试算平衡表的表头与各行（从 Excel 复制成文本，Tab 分隔最稳）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '一张带表头的科目余额表 / 试算平衡表（要能认出「科目编码」「科目名称」「科目类别」'
      + '「期初余额」「本期借方发生额」「本期贷方发生额」「期末余额」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      `本次读到的表头是：${(t.headers || []).join(' / ')}`,
      '请连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行科目明细（现在只有表头，或只有合计行）—— 没有明细行就无从复算']);
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkRowBalance(it); if (a) findings.push(a);
    const b = checkProfitLossClose(it); if (b) findings.push(b);
  }
  for (const f of checkDebitCreditTotals(t)) findings.push(f);
  for (const f of checkHierarchy(t)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  let executed = CHECKS_GIVEN.slice();
  notRun.push.apply(notRun, CHECKS_WITHHELD);
  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const h = hierarchyOf(t.items);
  const summary = {
    rows: t.items.length,
    top_level_rows: h.top.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    verdict: findings.some((f) => f.level === 'P0') ? 'ERROR_FOUND'
      : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
    omitted: 0,
  };

  const result = {
    status: 'success',
    scope: {
      checks: executed,
      checks_not_run: notRun,
      rows: t.items.length,
      top_level_rows: h.top.length,
      ledger_totals: {
        opening_total: sumOf(h.top, 'opening'),
        debit_total: sumOf(h.top, 'debit'),
        credit_total: sumOf(h.top, 'credit'),
        closing_total: sumOf(h.top, 'closing'),
      },
      tolerance: TOL,
      amount_convention: '借贷方向带符号：借方余额为正、贷方余额为负；本期借方/贷方发生额两列都填正数；发生额用结转后口径（含损益结转分录）',
      executed_locally: true,
      network_used: false,
    },
    findings: findings,
    summary: summary,
    checks_given: executed,
    checks_out_of_scope: OUT_OF_SCOPE,
    columns: t.cols.map((c) => c.header),
    note: executed.length === CHECKS_GIVEN.length
      ? `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run（它们不会被执行，也不会被伪造出来）。`
      : `本版本执行全部 ${executed.length} 项检查（免费档 ${CHECKS_GIVEN.length} 项 + 完整档追加 ${CHECKS_WITHHELD.length} 项）。`,
    disclaimer: '只核这张科目余额表内部的算术勾稽（逐行复算、期末结转、借贷合计、层级小计）；'
      + '不判断科目使用是否正确、也不判断账外事项。每条结论都带原文行号，可被第三方用同一份输入复算。',
  };
  if (findings.length === 0) {
    result.note += ' 本次实际执行的全部检查项都通过了；这只说明这张表按上面写明的口径算得对。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, classOf, normCode, hierarchyOf, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, AMOUNT_ROLES, REQUIRED, TOL,
};
