#!/usr/bin/env node
/**
 * franchise-royalty-check.js —— 加盟抽成与最低保底核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**做连锁/加盟的每月要向每个加盟商出结算单**，而规则里有一条最容易错：
 *   ① 抽成额   = 本月营业额 × 抽成率
 *   ② 广告基金 = 本月营业额 × 广告基金率
 *   ③ **应缴合计 = max(抽成额, 最低保底) + 广告基金**   ← 「**取大**」这一步
 * 营业额没达标时按保底收、达标了按抽成收 —— **取大取小写反、保底忘了加广告基金、
 * 或者干脆把保底当成"额外加一笔"**，都会让账单算错；加盟商一多，人眼核不动。
 *
 * 与已有能力的区别：`commission-check` 核**销售提成**（发给员工/代理的）、`ota-commission-check` 核**渠道佣金**；
 * 本能力核的是**向加盟商收取的抽成与最低保底**（方向相反、且含"取大"规则）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查加盟合同、不调用大模型；材料不足不给结论；不给法律意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '抽成额勾稽（本月营业额 × 抽成率）',
  '广告基金勾稽（本月营业额 × 广告基金率）',
  '应缴合计勾稽（**max(抽成额, 最低保底)** + 广告基金）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复加盟商检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '抽成率超出 0~20% 检测',
  '广告基金率超出 0~10% 检测',
  '本月营业额非正检测',
  '最低保底为负检测',
  '应缴合计为负或小于广告基金检测',
];

const OUT_OF_SCOPE = [
  '判断抽成率、保底、广告基金比例是否符合加盟合同',
  '处理阶梯抽成（按营业额分档）与超额累进（请先把适用档的抽成率算好再填）',
  '处理保证金、装修补贴、返利与年度清算',
  '判断收入确认与开票口径；给出法律或税务意见',
  '读取 .xlsx 或加盟商报表（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '加盟商\t本月营业额\t抽成率\t抽成额\t最低保底\t广告基金率\t广告基金\t应缴合计',
  'A店\t200000.00\t5%\t10000.00\t8000.00\t2%\t4000.00\t14000.00',
  'B店\t100000.00\t5%\t5000.00\t8000.00\t2%\t2000.00\t10000.00',
  '合计\t300000.00\t\t15000.00\t\t\t6000.00\t24000.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['加盟商', '门店', '客户名称', '店铺'],
  revenue: ['本月营业额', '营业额', '销售额'],
  // ⚠️ 顺序即优先级（更具体在前）：`抽成率` 必须在 `抽成额` 之前，`广告基金率` 必须在 `广告基金` 之前 ——
  //    否则宽泛别名会把带"率"的那列抢走（本仓库第五次踩这类坑，靠发版前的 header_map_check 拦下）。
  rate: ['抽成率', '提成率', '抽成比例'],
  commission: ['抽成额', '提成额', '抽成金额'],
  minGuarantee: ['最低保底', '保底额', '最低抽成'],
  fundRate: ['广告基金率', '基金率'],
  fund: ['广告基金', '市场基金'],
  total: ['应缴合计', '应缴金额', '结算额'],
};

const LABELS = {
  party: '加盟商', revenue: '本月营业额', rate: '抽成率', commission: '抽成额',
  minGuarantee: '最低保底', fundRate: '广告基金率', fund: '广告基金', total: '应缴合计',
};

const REQUIRED = ['party', 'revenue', 'rate', 'commission', 'minGuarantee', 'fundRate', 'fund', 'total'];
const SUM_ROLES = ['revenue', 'commission', 'fund', 'total'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
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
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
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
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `加盟商「${it.byRole.party || '(未命名)'}」`;

function checkCommission(it) {
  const revenue = num(it, 'revenue');
  const rate = num(it, 'rate');
  const stated = num(it, 'commission');
  if (revenue === null || rate === null || stated === null) return null;
  const expect = round2(revenue * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '抽成额与复算不符', line: it.line,
    message: `${who(it)}的抽成额是 ${stated.toFixed(2)}，按 本月营业额 ${revenue.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '抽成率常按合同分档；要确认本期适用哪一档，以及"营业额"的统计口径（含不含税、含不含外卖）。',
  };
}

function checkFund(it) {
  const revenue = num(it, 'revenue');
  const rate = num(it, 'fundRate');
  const stated = num(it, 'fund');
  if (revenue === null || rate === null || stated === null) return null;
  const expect = round2(revenue * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '广告基金与复算不符', line: it.line,
    message: `${who(it)}的广告基金是 ${stated.toFixed(2)}，按 本月营业额 ${revenue.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '广告基金按营业额计提，与保底无关；**不要因为它小而略过**。',
  };
}

function checkTotal(it) {
  const commission = num(it, 'commission');
  const minG = num(it, 'minGuarantee');
  const fund = num(it, 'fund');
  const stated = num(it, 'total');
  if (commission === null || minG === null || fund === null || stated === null) return null;
  const base = Math.max(commission, minG);
  const expect = round2(base + fund);
  if (Math.abs(expect - stated) <= TOL) return null;
  const used = commission >= minG ? '抽成额' : '最低保底';
  return {
    level: 'P0', category: '应缴合计与复算不符', line: it.line,
    message: `${who(it)}的应缴合计是 ${stated.toFixed(2)}，`
      + `按 **max(抽成额 ${commission.toFixed(2)}, 最低保底 ${minG.toFixed(2)}) = ${base.toFixed(2)}**（本期取 ${used}）`
      + ` + 广告基金 ${fund.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '规则是「**抽成与保底取大，再加广告基金**」；常见错法：取小、把保底额外加上、或漏加广告基金。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '注意：**最低保底与各比例不能相加**（合计行里应为空），只有金额类列才求和。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一加盟商出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '多门店分行是正常的；但若本表按加盟商汇总，重复行会让营业额与应缴一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔结算就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的加盟结算表（要能认出「本月营业额」「抽成率」「抽成额」「最低保底」'
      + '「广告基金率」「广告基金」「应缴合计」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从加盟结算台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个加盟商的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkCommission(it); if (a) findings.push(a);
    const b = checkFund(it); if (b) findings.push(b);
    const c = checkTotal(it); if (c) findings.push(c);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const guaranteed = t.items.filter((it) => {
    const c = num(it, 'commission'); const m = num(it, 'minGuarantee');
    return c !== null && m !== null && m > c;
  }).length;

  const result = {
    findings,
    summary: {
      franchisees: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      revenue_total: sumOf('revenue'),
      commission_total: sumOf('commission'),
      fund_total: sumOf('fund'),
      payable_total: sumOf('total'),
      on_guarantee: guaranteed,
      basis: '抽成额 = 本月营业额 × 抽成率；广告基金 = 本月营业额 × 广告基金率；'
        + '应缴合计 = **max(抽成额, 最低保底)** + 广告基金；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表合同约定的比例合理、也不代表营业额口径与合同一致 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
