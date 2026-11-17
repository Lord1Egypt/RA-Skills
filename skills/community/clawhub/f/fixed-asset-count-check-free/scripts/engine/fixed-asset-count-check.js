/**
 * fixed-asset-count-check.js —— 固定资产盘点账实核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每年至少一次（多数企业年中+年末各一次）盘点固定资产**，
 * 财务拿「固定资产台账」与「盘点表」对：盘盈盘亏是多少、净值算得对不对、有没有重复编号。
 * 这三件事**完全能算出来对错**，而且盘亏直接牵涉资产损失税前扣除与责任人处理。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   净值 = 原值 − 累计折旧
 *   盘盈盘亏 = 实盘数量 − 账面数量（正=盘盈，负=盘亏）
 *   月折旧额 = (原值 − 预计残值) ÷ 使用月数
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '净值勾稽（原值 − 累计折旧 = 账面净值）',
  '盘盈盘亏与数量差一致（实盘 − 账面）',
  '合计行逐列复核',
  '资产编号重复检测',
  '空白与占位符检测',
  '原值或累计折旧为负检测',
];

const CHECKS_WITHHELD = [
  '累计折旧超过原值检测',
  '月折旧额与（原值 − 残值）÷ 使用月数 勾稽',
  '盘点日期早于入账日期检测',
  '使用状态与盘亏矛盾检测（在用却有盘亏）',
  '数量为负或非整数检测',
];

const OUT_OF_SCOPE = [
  '判断资产分类、折旧年限与残值率是否符合税法与会计政策（以企业政策与税法为准）',
  '处理资产减值、评估增值、在建工程转固时点判断',
  '读取 ERP/固定资产模块导出文件（需要你先导出成文本贴进来）',
  '认定盘亏责任与税前扣除资料（属于税务与内控职责）',
];

const SAMPLE_TEXT = [
  '资产编号\t资产名称\t使用部门\t入账日期\t盘点日期\t原值\t预计残值\t累计折旧\t账面净值\t使用月数\t月折旧额\t账面数量\t实盘数量\t使用状态',
  'GD-001\t数控车床\t生产一车间\t2022-03-15\t2026-06-30\t480000.00\t0.00\t168000.00\t312000.00\t120\t4000.00\t2\t2\t在用',
  'GD-002\t叉车\t物流部\t2023-01-10\t2026-06-30\t120000.00\t0.00\t42000.00\t78000.00\t120\t1000.00\t1\t1\t在用',
  'GD-003\t办公电脑（批次）\t行政部\t2024-05-20\t2026-06-30\t96000.00\t0.00\t38400.00\t57600.00\t60\t1600.00\t12\t12\t在用',
  '合计\t\t\t\t\t696000.00\t0.00\t248400.00\t447600.00\t\t\t15\t15\t',
].join('\n');

const TOL = 0.01;
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  code: ['资产编号', '资产编码', '卡片编号', '编号'],
  name: ['资产名称', '名称'],
  dept: ['使用部门', '部门', '存放地点'],
  bookDate: ['入账日期', '购置日期', '启用日期'],
  countDate: ['盘点日期', '盘点基准日'],
  cost: ['原值', '资产原值', '购置原值'],
  residual: ['预计残值', '残值'],
  deprec: ['累计折旧', '已提折旧'],
  usefulMonths: ['使用月数', '折旧月数', '预计使用月数'],
  monthlyDeprec: ['月折旧额', '每月折旧额'],
  netValue: ['账面净值', '净值'],
  bookQty: ['账面数量', '账面数'],
  realQty: ['实盘数量', '实盘数', '盘点数量'],
  status: ['使用状态', '状态'],
};

const LABELS = {
  code: '资产编号', name: '资产名称', dept: '使用部门', bookDate: '入账日期', countDate: '盘点日期',
  cost: '原值', residual: '预计残值', deprec: '累计折旧', usefulMonths: '使用月数',
  monthlyDeprec: '月折旧额', netValue: '账面净值', bookQty: '账面数量',
  realQty: '实盘数量', status: '使用状态',
};

const REQUIRED = ['code', 'cost', 'deprec', 'netValue', 'bookQty', 'realQty'];
const SUM_ROLES = ['cost', 'deprec', 'netValue', 'bookQty', 'realQty'];

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
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const who = (it) => (it && it.code ? `${String(it.code).trim()}` : `第 ${it && it.line} 行`);

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkNetValue(it) {
  const cost = normNumber(it.cost); const dep = normNumber(it.deprec); const net = normNumber(it.netValue);
  if (cost === null || dep === null || net === null) return null;
  const want = round2(cost - dep);
  if (Math.abs(want - net) > TOL) {
    return {
      line: it.line, level: 'P0', category: '净值勾稽',
      message: `${who(it)} 账面净值 ${net} ≠ 原值 ${cost} − 累计折旧 ${dep} = ${want}`,
      evidence: `原值=${cost}；累计折旧=${dep}；账面净值=${net}；应为 ${want}`,
    };
  }
  return null;
}

function checkQuantityDiff(it) {
  const book = normNumber(it.bookQty); const real = normNumber(it.realQty);
  if (book === null || real === null) return null;
  const diff = round2(real - book);
  if (Math.abs(diff) > 1e-9) {
    const kind = diff > 0 ? '盘盈' : '盘亏';
    return {
      line: it.line, level: 'P1', category: '盘盈盘亏',
      message: `${who(it)} ${kind} ${Math.abs(diff)}（账面 ${book}，实盘 ${real}）`,
      evidence: `账面数量=${book}；实盘数量=${real}；差额=${diff}`,
    };
  }
  return null;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const declared = normNumber(totals.row[role]);
  if (declared === null) return out;
  let sum = 0; let n = 0;
  for (const it of items) { const v = normNumber(it[role]); if (v !== null) { sum += v; n += 1; } }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(sum - declared) > TOL) {
    out.push({
      line: totals.line, level: 'P1', category: '合计复核',
      message: `合计行「${LABELS[role]}」填 ${declared}，但明细逐行相加是 ${sum}`,
      evidence: `合计=${declared}；明细合计=${sum}（${n} 行）`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = []; const seen = new Map();
  for (const it of items) {
    const k = String(it.code || '').trim();
    if (!k) continue;
    if (seen.has(k)) {
      out.push({
        line: it.line, level: 'P1', category: '重复资产',
        message: `资产编号 ${k} 出现两次（第 ${seen.get(k)} 行与第 ${it.line} 行）`,
        evidence: `编号=${k}；首次出现在第 ${seen.get(k)} 行`,
      });
    } else seen.set(k, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  const watch = ['cost', 'deprec', 'netValue', 'bookQty', 'realQty'];
  for (const it of items) {
    const miss = watch.filter((r) => isBlank(it[r]));
    if (miss.length) {
      out.push({
        line: it.line, level: 'P1', category: '空白字段',
        message: `${who(it)} 有 ${miss.length} 个关键字段没填：${miss.map((r) => LABELS[r]).join('、')}`,
        evidence: `缺失列=${miss.map((r) => LABELS[r]).join('、')}`,
      });
    }
  }
  return out;
}

function checkNegatives(it) {
  const out = [];
  for (const r of ['cost', 'deprec']) {
    const v = normNumber(it[r]);
    if (v !== null && v < 0) {
      out.push({
        line: it.line, level: 'P0', category: '负数异常',
        message: `${who(it)} 的「${LABELS[r]}」是负数 ${v}`,
        evidence: `${LABELS[r]}=${v}`,
      });
    }
  }
  return out;
}

/* ====================== 完整档（付费）检查项（不进免费包） ====================== */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到盘点表正文（text）—— 请把「资产编号 / 原值 / 累计折旧 / 账面净值 / 账面数量 / 实盘数量」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `盘点表缺少必需列：${t.missingColumns.map((r) => LABELS[r]).join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) return insufficient('表里只有表头，没有任何资产明细行');

  const findings = [];
  for (const it of t.items) {
    const a = checkNetValue(it); if (a) findings.push(a);
    const b = checkQuantityDiff(it); if (b) findings.push(b);
    for (const f of checkNegatives(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let netTotal = 0; let gain = 0; let loss = 0;
  for (const it of t.items) {
    const v = normNumber(it.netValue); if (v !== null) netTotal += v;
    const book = normNumber(it.bookQty); const real = normNumber(it.realQty);
    if (book !== null && real !== null) {
      const d = round2(real - book);
      if (d > 0) gain += d; else loss += -d;
    }
  }

  return {
    status: 'success',
    result: {
      status: 'success',
      service_type: 'FIXED_ASSET_COUNT_CHECK',
      scope: {
        checks: CHECKS_GIVEN.slice(),
        checks_not_run: notRun,
        assets: t.items.length,
        net_value_total: round2(netTotal),
        gain_qty: round2(gain),
        loss_qty: round2(loss),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
      findings,
      summary: {
        assets: t.items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
        omitted: 0,
      },
      checks_out_of_scope: OUT_OF_SCOPE,
      note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
      disclaimer: '只核"原值 − 累计折旧 = 净值""实盘 − 账面 = 盘盈盘亏"这类内部勾稽；'
        + '**不判断资产分类、折旧年限与残值率是否合规**；结论可由第三方用同一份输入复算。',
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
