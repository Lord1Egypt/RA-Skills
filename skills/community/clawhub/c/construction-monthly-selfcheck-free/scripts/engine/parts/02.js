#!/usr/bin/env node
/**
 * progress-payment-check.js —— 工程进度款与质保金核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**施工/工程类企业每月报进度款，都要按合同约定算一遍**：
 *   ① 本期应付进度款 = 本期完成产值 × 进度款比例（常见 80%）
 *   ② 本期扣质保金   = 本期应付进度款 × 质保金比例（常见 3%~5%）
 *   ③ 本期实付       = 本期应付进度款 − 本期扣质保金
 * 单笔金额动辄几十上百万，比例用错一个小数点就是几万块；而且**累计完成产值与合同金额的勾稽**
 * 直接关系到"有没有超付"。这些都是**纯算术**，但几十个标段人眼核不动。
 *
 * 与已有能力的区别：`three-way-match` 核的是采购三单（订单/入库/发票）匹配；
 * `platform-settlement-check` 核电商平台结算单；**本能力核的是工程进度款与质保金**，口径完全不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判工程实体、不调用大模型；材料不足不给结论；不给法律/造价意见。
 */
'use strict';

const CHECKS_GIVEN = [
  '本期应付进度款勾稽（本期完成产值 × 进度款比例）',
  '本期扣质保金勾稽（本期应付进度款 × 质保金比例）',
  '本期实付勾稽（本期应付进度款 − 本期扣质保金）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复标段/合同行检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '累计完成产值超过合同金额检测（超合同/超付风险）',
  '累计完成产值小于本期完成产值检测（累计与本期倒挂）',
  '进度款比例超出 0~100% 检测',
  '质保金比例超出 0~5% 常见区间检测',
  '本期实付为负检测',
];

const OUT_OF_SCOPE = [
  '判断工程实体是否真的完成了这些产值（那是监理计量与现场签证的事）',
  '处理甲供材、暂列金额、变更签证、索赔与罚款的抵扣（请先算进本期完成产值或另列）',
  '处理多级分包与总包代扣税（口径差异大，需按合同逐条确认）',
  '判断质保金比例是否合法（那是合同与招投标文件的事）',
  '给出造价或法律意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '标段\t合同金额\t本期完成产值\t累计完成产值\t进度款比例\t本期应付进度款\t质保金比例\t本期扣质保金\t本期实付',
  'A标段\t5000000.00\t800000.00\t3200000.00\t80%\t640000.00\t3%\t19200.00\t620800.00',
  'B标段\t3000000.00\t400000.00\t2400000.00\t80%\t320000.00\t5%\t16000.00\t304000.00',
  '合计\t8000000.00\t1200000.00\t5600000.00\t\t960000.00\t\t35200.00\t924800.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  party: ['标段', '项目名称', '合同名称', '工程', '单位'],
  contract: ['合同金额', '合同价', '签约合同价'],
  periodValue: ['本期完成产值', '本期产值', '本期完成'],
  totalValue: ['累计完成产值', '累计产值', '累计完成'],
  progressRate: ['进度款比例', '支付比例', '付款比例'],
  payable: ['本期应付进度款', '本期应付', '应付进度款'],
  retentionRate: ['质保金比例', '质保金率', '保修金比例'],
  retention: ['本期扣质保金', '本期质保金', '扣质保金'],
  paid: ['本期实付', '实付金额', '本期支付'],
};

const LABELS = {
  party: '标段', contract: '合同金额', periodValue: '本期完成产值', totalValue: '累计完成产值',
  progressRate: '进度款比例', payable: '本期应付进度款', retentionRate: '质保金比例',
  retention: '本期扣质保金', paid: '本期实付',
};

const REQUIRED = ['party', 'contract', 'periodValue', 'totalValue', 'progressRate',
  'payable', 'retentionRate', 'retention', 'paid'];
const SUM_ROLES = ['contract', 'periodValue', 'totalValue', 'payable', 'retention', 'paid'];

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
const who = (it) => `标段「${it.byRole.party || '(未命名)'}」`;

function checkPayable(it) {
  const value = num(it, 'periodValue');
  const rate = num(it, 'progressRate');
  const stated = num(it, 'payable');
  if (value === null || rate === null || stated === null) return null;
  const expect = round2(value * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应付进度款与复算不符', line: it.line,
    message: `${who(it)}的本期应付进度款是 ${stated.toFixed(2)}，`
      + `按 本期完成产值 ${value.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '进度款比例按合同约定（常见 80%）；比例或产值录错都会直接放大成钱。',
  };
}

function checkRetention(it) {
  const payable = num(it, 'payable');
  const rate = num(it, 'retentionRate');
  const stated = num(it, 'retention');
  if (payable === null || rate === null || stated === null) return null;
  const expect = round2(payable * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期扣质保金与复算不符', line: it.line,
    message: `${who(it)}的本期扣质保金是 ${stated.toFixed(2)}，`
      + `按 本期应付进度款 ${payable.toFixed(2)} × ${rate}% 复算应为 ${expect.toFixed(2)}。`,
    advice: '质保金一般按**本期应付进度款**乘比例扣留（不是按产值直接乘）；口径要先与合同对齐。',
  };
}

function checkPaid(it) {
  const payable = num(it, 'payable');
  const retention = num(it, 'retention');
  const stated = num(it, 'paid');
  if (payable === null || retention === null || stated === null) return null;
  const expect = round2(payable - retention);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期实付与复算不符', line: it.line,
    message: `${who(it)}的本期实付是 ${stated.toFixed(2)}，`
      + `按 本期应付进度款 ${payable.toFixed(2)} − 本期扣质保金 ${retention.toFixed(2)} 应为 ${expect.toFixed(2)}。`,
    advice: '实付 = 应付 − 质保金（若另有代扣税、水电费、罚款，应先在本表里显式列出来）。',
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
        advice: '要么明细行漏了标段，要么合计行没跟着更新。',
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
        level: 'P1', category: '同一标段出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一标段分次报量是正常的；但若本表按标段汇总，重复行会让应付与实付一起翻倍。',
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
          advice: '缺这一格这笔进度款就算不出来；补齐前本工具不会用 0 或默认值替你填。',
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
      '含表头的进度款支付计算表（要能认出「合同金额」「本期完成产值」「累计完成产值」'
      + '「进度款比例」「本期应付进度款」「质保金比例」「本期扣质保金」「本期实付」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从计量支付台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个标段的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkPayable(it); if (a) findings.push(a);
    const b = checkRetention(it); if (b) findings.push(b);
    const c = checkPaid(it); if (c) findings.push(c);
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

  const result = {
    findings,
    summary: {
      sections: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      contract_total: sumOf('contract'),
      period_value_total: sumOf('periodValue'),
      payable_total: sumOf('payable'),
      retention_total: sumOf('retention'),
      paid_total: sumOf('paid'),
      basis: '本期应付进度款 = 本期完成产值 × 进度款比例；本期扣质保金 = 本期应付进度款 × 质保金比例；'
        + '本期实付 = 本期应付进度款 − 本期扣质保金；合计行逐列复核。',
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
      + '不代表产值计量真实、也不代表合同约定本身合理 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
