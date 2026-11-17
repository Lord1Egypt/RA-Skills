/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * equity-method-investment-check.js —— 长期股权投资权益法核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**对联营/合营企业采用权益法核算的公司**，在**每月结账、
 * 季度报表编制、以及年度审计提供长期股权投资底稿之前**。会计要把"被投资方净利润 ×
 * 持股比例"确认成投资收益，并按权益法滚动期末账面价值；审计与监管盯的就是这张表
 * 能不能**逐列滚动对上、合计行能不能对上、比例有没有用错**。
 *
 * 核心可算关系（都能手算复现）：
 *   期末账面价值 = 期初账面价值 + 本期投资收益 + 本期其他综合收益 + 本期其他权益变动
 *                  − 本期宣告分红 + 本期新增投资
 *   本期投资收益 = 被投资方净利润 × 持股比例（或"投资方享有比例"）
 *   合计行 = 明细各行逐列相加
 *   持股比例 ≤ 50%（> 50% 应纳入合并范围，不能再按权益法）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该不该用权益法（重大影响/共同控制的认定）、也不判断分红是否合规，
 *    那属于会计与审计判断。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**（本仓库踩过 4 次的坑）。
   `本期投资收益` 里含 `投资收益`；`期末账面价值`/`期初账面价值` 都含 `账面价值`；
   `本期宣告分红` 里含"分红"；`投资方享有比例` 里含"比例"。
   若裸词排在前面，这些列会被**抢走并互相覆盖** ⇒ 算错但**不会报缺列**，
   只能靠 `tools/header_map_check.py` 的"识别出的表头数 > 解析出的列数"判据拦住。 */
const ROLES = {
  investee: ['被投资单位', '被投资方名称', '被投资公司'],
  sharePct: ['持股比例', '持股百分比', '股权比例'],
  bookBegin: ['期初账面价值', '期初余额', '期初投资账面价值'],
  invIncome: ['本期投资收益', '投资收益'],
  oci: ['本期其他综合收益', '其他综合收益'],
  equityOther: ['本期其他权益变动', '其他权益变动'],
  dividend: ['本期宣告分红', '宣告分红', '本期分红'],
  newInvest: ['本期新增投资', '新增投资'],
  bookEnd: ['期末账面价值', '期末余额', '期末投资账面价值'],
  netProfit: ['被投资方净利润', '被投资单位净利润', '被投资方净利'],
  shareRatio: ['投资方享有比例', '享有比例'],
};

const LABELS = {
  investee: '被投资单位',
  sharePct: '持股比例',
  bookBegin: '期初账面价值',
  invIncome: '本期投资收益',
  oci: '本期其他综合收益',
  equityOther: '本期其他权益变动',
  dividend: '本期宣告分红',
  newInvest: '本期新增投资',
  bookEnd: '期末账面价值',
  netProfit: '被投资方净利润',
  shareRatio: '投资方享有比例',
};

/* 空白/占位符检查只盯"缺了就没法核"的那几列：被投资单位 + 三个金额（期初/期末/被投资方净利润）。
   `本期投资收益` 已经在第 4 项里单独核，不重复报。 */
const REQUIRED = ['investee', 'sharePct', 'bookBegin', 'bookEnd', 'netProfit'];
const SUM_ROLES = ['bookBegin', 'invIncome', 'oci', 'equityOther', 'dividend', 'newInvest', 'bookEnd'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按那一行识别并摘掉付费语句；写成别的形式（例：数组的 `.some()`）
   会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
   写了字面量就会被当成"没删干净"而整包跳过（本仓库踩过）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（期初 / 投资收益 / 其他综合收益 / 其他权益变动 / 宣告分红 / 新增投资 / 期末）',
  '同一被投资单位重复行检测',
  '权益法滚动：期末 = 期初 + 投资收益 + 其他综合收益 + 其他权益变动 − 宣告分红 + 新增投资',
  '本期投资收益 = 被投资方净利润 × 持股比例（优先用投资方享有比例）',
  '持股比例 > 50% 却仍按权益法（应纳入合并范围）检测',
  '本期宣告分红为负检测',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '期末账面价值为负检测',
  '投资收益为负但被投资方净利润为正（或反之）口径提示',
  '持股比例不在 20%~50% 区间提示（权益法通常适用区间）',
  '长期股权投资账面价值超过被投资方净利润 × 比例 × 3 倍提示',
  '本期新增投资但持股比例未变提示',
];

const OUT_OF_SCOPE = [
  '判断某个被投资单位**该不该**用权益法（重大影响 / 共同控制的认定属于会计判断）',
  '判断持股比例本身填得对不对（以工商登记 / 投资协议为准，本工具只按你填的数算）',
  '代替审计程序，也不出具审计或鉴证意见',
  '核对被投资方净利润的真伪，或与投资方、被投资方的账簿逐笔比对',
  '读取 ERP / 合并报表系统的导出文件（需要你先导出成文本贴进来）',
  '判断权益法核算对所得税、递延所得税的影响（属于税务判断）',
];

/* 样例是**干净稿**：两档跑出来都必须 0 条发现。
   数字按下列 12 条规则反推（都能手算复核）：
     · 甲：1200000 = 4000000 × 30%；3600000 = 3000000 + 1200000 − 600000；
           3600000 ≤ 4000000 × 30% × 3 = 3600000（**取等号，刚好不报"3 倍"提示**）；
     · 乙：500000 = 2000000 × 25%；1400000 = 1000000 + 500000 − 100000；
           1400000 ≤ 2000000 × 25% × 3 = 1500000；
     · 合计行 = 明细逐列相加（期初 4000000 / 投资收益 1700000 / 分红 700000 /
       期末 5000000 / 被投资方净利润 6000000）；
     · 两行比例都在 20%~50%（不触发"超 50%"与"不在区间"），
       分红为正（不触发"分红为负"），账面价值与净利润同向为正（不触发方向提示与负值检测），
       新增投资均为 0（不触发"新增投资但比例未变"）。 */
const SAMPLE_TEXT = [
  '被投资单位\t持股比例\t期初账面价值\t本期投资收益\t本期其他综合收益\t本期其他权益变动\t本期宣告分红\t本期新增投资\t期末账面价值\t被投资方净利润\t投资方享有比例',
  '被投资单位甲\t30%\t3000000\t1200000\t0\t0\t600000\t0\t3600000\t4000000\t30%',
  '被投资单位乙\t25%\t1000000\t500000\t0\t0\t100000\t0\t1400000\t2000000\t25%',
  '合计\t\t4000000\t1700000\t0\t0\t700000\t0\t5000000\t6000000\t',
].join('\n');

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

/** 持股比例：`30%` / `0.3` / `30` 都换算成"百分数"（30 表示 30%）；认不出返回 null。 */
function percentOf(raw) {
  const n = normNumber(raw);
  if (n === null) return null;
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (s.endsWith('%')) return round2(n);
  if (n > 0 && n <= 1) return round2(n * 100);
  return round2(n);
}

const who = (it) => {
  const n = String(it.investee || '').trim();
  return n ? n : `第 ${it.line} 行`;
};
/** 计算用的比例：优先"投资方享有比例"，没填就用"持股比例"。 */
const ratioOf = (it) => {
  const own = percentOf(it.shareRatio);
  if (own !== null) return own;
  return percentOf(it.sharePct);
};
const num = (it, role) => normNumber(it[role]);

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
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

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P0', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicateInvestee(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.investee || '').replace(/\s/g, '');
    if (!key || isBlank(key)) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「被投资单位」完全相同 —— 可能重复计入`,
        evidence: `被投资单位=${it.investee}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkRollForward(it) {
  const begin = num(it, 'bookBegin');
  const income = num(it, 'invIncome');
  const oci = num(it, 'oci');
  const eqOther = num(it, 'equityOther');
  const div = num(it, 'dividend');
  const add = num(it, 'newInvest');
  const end = num(it, 'bookEnd');
  if ([begin, income, oci, eqOther, div, add, end].some((v) => v === null)) return null;
  /* 关键列（期初 / 期末）空白时由第 7 项报空白，这里不重复报 */
  if (isBlank(it.bookBegin) || isBlank(it.bookEnd)) return null;
  const should = round2(begin + income + oci + eqOther - div + add);
  if (Math.abs(should - end) > TOL) {
    return {
      line: it.line, level: 'P0', category: '权益法滚动不平',
      message: `${who(it)} 期末账面价值填 ${end}，但按权益法滚动应为 ${should}`
        + `（${begin} + ${income} + ${oci} + ${eqOther} − ${div} + ${add}）`,
      evidence: `期初=${begin}；投资收益=${income}；其他综合收益=${oci}；其他权益变动=${eqOther}；`
        + `宣告分红=${div}；新增投资=${add}；报表期末=${end}；应为=${should}；差异=${round2(end - should)}`,
    };
  }
  return null;
}

function checkInvIncomeVsProfit(it) {
  const income = num(it, 'invIncome');
  const profit = num(it, 'netProfit');
  const pct = ratioOf(it);
  if (income === null || profit === null || pct === null) return null;
  if (isBlank(it.invIncome) || isBlank(it.netProfit)) return null;
  const should = round2(profit * pct / 100);
  if (Math.abs(should - income) > TOL) {
    return {
      line: it.line, level: 'P0', category: '投资收益与净利润不匹配',
      message: `${who(it)} 本期投资收益填 ${income}，但被投资方净利润 ${profit} × ${pct}% 应为 ${should}`,
      evidence: `被投资方净利润=${profit}；比例=${pct}%；按比例应为=${should}；报表投资收益=${income}；`
        + `差异=${round2(income - should)}`,
    };
  }
  return null;
}

function checkRatioOver50(it) {
  const pct = percentOf(it.sharePct);
  if (pct === null || isBlank(it.sharePct)) return null;
  if (pct > 50) {
    return {
      line: it.line, level: 'P0', category: '持股比例超 50% 仍按权益法',
      message: `${who(it)} 持股比例 ${pct}% 已超过 50%，应当纳入合并范围（按成本法/合并报表处理），不能再按权益法核算`,
      evidence: `持股比例=${pct}%；阈值=50%`,
    };
  }
  return null;
}

function checkNegativeDividend(it) {
  const div = num(it, 'dividend');
  if (div === null || div >= 0) return null;
  return {
    line: it.line, level: 'P1', category: '宣告分红为负',
    message: `${who(it)} 本期宣告分红为 ${div}（负数）—— 负数通常应作为分红冲回或红冲单独反映`,
    evidence: `本期宣告分红=${div}`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把长期股权投资权益法核算表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  /* 「认不出表头」= 连**被投资单位**这一列都没认出来 ⇒ 连哪一行属于谁都定不了，不给结论。
     只是少了个别列（例如没有「被投资方净利润」）时**仍然执行**，并如实报「列缺失」——
     那是"查得到的问题"，不该退化成"什么都没有"。 */
  if (missingColumns.indexOf('investee') >= 0) {
    return insufficient(missingColumns.map((r) => `认不出必需列「${LABELS[r]}」：第一行必须是表头（Tab 分隔），且表头里要有这一列`));
  }
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（只有合计行不行）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const f of checkDuplicateInvestee(items)) findings.push(f);
  for (const it of items) {
    const one = [checkRollForward(it), checkInvIncomeVsProfit(it), checkRatioOver50(it), checkNegativeDividend(it)];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        book_begin_total: round2(items.reduce((n, it) => n + (num(it, 'bookBegin') || 0), 0)),
        book_end_total: round2(items.reduce((n, it) => n + (num(it, 'bookEnd') || 0), 0)),
        income_total: round2(items.reduce((n, it) => n + (num(it, 'invIncome') || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, percentOf, checkRollForward, checkInvIncomeVsProfit, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
