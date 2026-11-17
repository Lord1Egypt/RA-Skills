/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cost-allocation-check.js —— 在产品与完工产品成本分配核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有在产品（在制）的制造企业**，在**月度成本计算与结转、
 * 以及年度审计 / 税务检查提供成本计算底稿之前**。成本会计要把
 * 「期初在产品成本 + 本期投入」在「完工产品」与「期末在产品」之间分掉，
 * 并逐行维护十来个数字列；审计与税务盯的就是这些列能不能**逐列对上、总量守恒**。
 *
 * 核心可算关系（都能手算复现）：
 *   本期投入合计 = 本期投入材料 + 本期投入人工 + 本期投入制造费用
 *   完工产品成本 + 期末在产品成本 = 期初在产品成本 + 本期投入合计   （成本守恒）
 *   单位完工成本 = 完工产品成本 ÷ 完工数量（同工序之间可比）
 *   合计行的每个数字列 = 明细逐行相加（9 个数字列）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。
 * 材料不足（空文本 / 认不出表头 / 没有数据行）时**绝不给结论**；
 * **只是缺个别列**时照常执行，并如实报「列缺失」——缺列不等于材料不足。
 * ⚠️ 本工具**不判断**该用哪种分配方法、约当完工率定得准不准、定额是否合理（属于成本会计判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过 6 次的坑）。
   `完工产品成本` / `在产品数量` / `期初在产品成本` / `期末在产品成本` 里都含 `产品`；
   `本期投入材料` 里含 `材料`；`在产品数量` 里含 `产品` 与 `数量`。
   若键里带裸词 `产品` 的角色排在前面，这些列会被它**整列抢走**
   ⇒ 数量与成本全读到空（`header_map_check` 会拦，样例直接失去结论）。 */
const ROLES = {
  // ① 带限定语的成本列：必须先于任何含裸词「产品」「成本」的角色
  beginWip: ['期初在产品成本', '期初在产品', '期初在制成本'],
  endWip: ['期末在产品成本', '期末在产品', '期末在制成本'],
  finishedCost: ['完工产品成本', '完工产成品成本', '产成品成本', '完工成本'],
  // ② 本期三段投入：必须先于任何含裸词「材料」「人工」「制造费用」「合计」的角色
  matIn: ['本期投入材料', '本期材料', '直接材料'],
  laborIn: ['本期投入人工', '本期人工', '直接人工'],
  ohIn: ['本期投入制造费用', '本期制造费用', '制造费用'],
  inTotal: ['本期投入合计', '本期投入总额', '投入合计'],
  // ③ 数量列（`在产品数量` 含裸词「产品」，必须早于 product；`期末数量` 类必须晚于 endWip）
  wipQty: ['在产品数量', '在产品约当产量', '约当产量合计', '期末在产品数量'],
  finishedQty: ['完工数量', '完工产量', '产成品数量'],
  // ④ 只有当「数量口径」两列真的存在时才会用到的可选列（样例里没有）
  beginQty: ['期初数量', '期初结存数量', '期初完工入库数量'],
  inputQty: ['本期投入数量', '本期完工入库数量', '本期生产数量'],
  // ⑤ 裸词兜底：只能排在最后
  product: ['产品/批次', '产品批次', '批次号', '批次', '产品'],
  process: ['工序或车间', '工序', '车间'],
  method: ['分配方法', '分配方式', '计价方法'],
};

const LABELS = {
  product: '产品/批次', process: '工序或车间', beginWip: '期初在产品成本',
  matIn: '本期投入材料', laborIn: '本期投入人工', ohIn: '本期投入制造费用',
  inTotal: '本期投入合计', finishedQty: '完工数量', wipQty: '在产品数量',
  finishedCost: '完工产品成本', endWip: '期末在产品成本', method: '分配方法',
  beginQty: '期初数量', inputQty: '本期投入数量',
};

/* 必需列：全表的 12 列。缺列**不阻断执行**，只报一条「列缺失」。 */
const REQUIRED = [
  'product', 'process', 'beginWip', 'matIn', 'laborIn', 'ohIn', 'inTotal',
  'finishedQty', 'wipQty', 'finishedCost', 'endWip', 'method',
];
/* 合计行要逐列复核的数字列（9 列） */
const SUM_ROLES = [
  'beginWip', 'matIn', 'laborIn', 'ohIn', 'inTotal',
  'finishedQty', 'wipQty', 'finishedCost', 'endWip',
];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**，且只有一种写法（形态 B：布尔常量 + `if` 块）：
   `strip_free_engine` 按「顶部赋值为 Boolean(…) 的那一行 + `if` 块」识别并整块摘掉付费语句，
   再迭代删掉只被付费语句引用的函数。写成别的形式（数组 `.some()`、`payload.xxx` 直接判断）
   会**留下开关不删** ⇒ 泄漏守卫报「免费引擎里仍留着付费开关」。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（期初 / 材料 / 人工 / 制造费用 / 投入合计 / 完工数量 / 在产品数量 / 完工产品成本 / 期末在产品成本）',
  '同一「产品/批次 + 工序或车间」重复行检测',
  '本期投入合计 = 本期投入材料 + 本期投入人工 + 本期投入制造费用',
  '完工产品成本 + 期末在产品成本 = 期初在产品成本 + 本期投入合计（成本守恒）',
  '完工数量 + 在产品数量 ≤ 0 时不给分配结论（数量缺失/为零）',
  '完工产品成本为负或期末在产品成本为负检测',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '分配方法不在常见口径（约当产量法 / 定额比例法 / 在产品按定额成本计算 / 不计算在产品成本）提示',
  '单位完工成本 = 完工产品成本 ÷ 完工数量，与其所在工序平均值偏离超过 30% 提示',
  '在产品数量 > 0 但期末在产品成本为 0（漏留在产品）检测',
  '完工数量 > 期初数量 + 本期投入数量（数量口径缺失）提示',
  '期初在产品成本占本期投入合计比例超过 50% 提示（期初异常大）',
];

const OUT_OF_SCOPE = [
  '判断该用哪种分配方法、约当完工率/投料程度定得准不准（属于成本会计判断）',
  '重算定额成本、工时定额、材料定额本身是否合理（需要工艺与定额底稿）',
  '核对领料单、工时记录、制造费用明细账的**真伪**，或与 ERP / MES 的逐行明细比对',
  '读取 ERP / 成本核算系统 / Excel 的原始文件（需要你先导出成文本贴进来）',
  '判断成本分配对所得税、存货跌价准备的影响（属于税务与会计估计判断）',
];

const SAMPLE_TEXT = [
  '产品/批次\t工序或车间\t期初在产品成本\t本期投入材料\t本期投入人工\t本期投入制造费用\t本期投入合计\t完工数量\t在产品数量\t完工产品成本\t期末在产品成本\t分配方法',
  '甲产品\t一车间\t100000\t300000\t120000\t80000\t500000\t800\t200\t480000\t120000\t约当产量法',
  '乙产品\t二车间\t50000\t150000\t60000\t40000\t250000\t500\t100\t240000\t60000\t约当产量法',
  '合计\t\t150000\t450000\t180000\t120000\t750000\t1300\t300\t720000\t180000\t',
].join('\n');

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（缺个别列不算材料不足，照常执行并报列缺失）。',
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
const show = (v) => (v === null || v === undefined ? '(空)' : String(v));
const who = (it) => {
  const a = String(it.product || '').trim();
  const b = String(it.process || '').trim();
  if (a && b) return `${a} / ${b}`;
  if (a) return a;
  if (b) return b;
  return `第 ${it.line} 行`;
};

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [], cols: [] };
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
  return { items, totals, missingColumns, header, cols };
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
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但 ${n} 行明细逐行相加是 ${sum}（差 ${round2(stated - sum)}）`,
        evidence: `合计行${LABELS[role]}=${stated}；明细合计=${sum}；参与相加行数=${n}`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = `${String(it.product || '').trim()}|${String(it.process || '').trim()}`;
    if (key === '|') continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「产品/批次 + 工序或车间」完全相同 —— 可能重复计入`,
        evidence: `产品/批次=${show(it.product)}；工序或车间=${show(it.process)}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkInTotal(it) {
  const tot = normNumber(it.inTotal);
  const mat = normNumber(it.matIn);
  const lab = normNumber(it.laborIn);
  const oh = normNumber(it.ohIn);
  if (tot === null || mat === null || lab === null || oh === null) return null;
  const sum = round2(mat + lab + oh);
  if (Math.abs(sum - tot) > TOL) {
    return {
      line: it.line, level: 'P0', category: '本期投入合计不符',
      message: `${who(it)} 本期投入合计填 ${tot}，但材料 ${mat} + 人工 ${lab} + 制造费用 ${oh} = ${sum}（差 ${round2(tot - sum)}）`,
      evidence: `本期投入合计=${tot}；材料+人工+制造费用=${sum}；差=${round2(tot - sum)}`,
    };
  }
  return null;
}

function checkCostConservation(it) {
  const bw = normNumber(it.beginWip);
  const tot = normNumber(it.inTotal);
  const fc = normNumber(it.finishedCost);
  const ew = normNumber(it.endWip);
  if (bw === null || tot === null || fc === null || ew === null) return null;
  const left = round2(fc + ew);
  const right = round2(bw + tot);
  if (Math.abs(left - right) > TOL) {
    return {
      line: it.line, level: 'P0', category: '成本守恒不符',
      message: `${who(it)} 完工产品成本 ${fc} + 期末在产品成本 ${ew} = ${left}，但期初在产品成本 ${bw} + 本期投入合计 ${tot} = ${right}（差 ${round2(left - right)}）`,
      evidence: `完工+期末=${left}；期初+本期投入=${right}；差=${round2(left - right)}`,
    };
  }
  return null;
}

function checkQtyMissing(it) {
  const fq = normNumber(it.finishedQty);
  const wq = normNumber(it.wipQty);
  if (fq === null && wq === null) {
    return {
      line: it.line, level: 'P1', category: '数量缺失或为零',
      message: `${who(it)} 完工数量与在产品数量都读不出数字 —— 数量缺失，不给分配结论`,
      evidence: `完工数量=${show(it.finishedQty)}；在产品数量=${show(it.wipQty)}`,
    };
  }
  const sum = round2((fq || 0) + (wq || 0));
  if (sum <= 0) {
    return {
      line: it.line, level: 'P1', category: '数量缺失或为零',
      message: `${who(it)} 完工数量 ${show(fq)} + 在产品数量 ${show(wq)} = ${sum}（≤0）—— 数量缺失/为零，不给分配结论`,
      evidence: `完工数量=${show(fq)}；在产品数量=${show(wq)}；数量合计=${sum}`,
    };
  }
  return null;
}

function checkNegativeCost(it) {
  const fc = normNumber(it.finishedCost);
  const ew = normNumber(it.endWip);
  const bad = [];
  if (fc !== null && fc < 0) bad.push(`完工产品成本=${fc}`);
  if (ew !== null && ew < 0) bad.push(`期末在产品成本=${ew}`);
  if (!bad.length) return null;
  return {
    line: it.line, level: 'P0', category: '成本为负',
    message: `${who(it)} 出现负数成本：${bad.join('；')} —— 分配表里成本不应为负`,
    evidence: bad.join('；'),
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 缺列不影响其余检查继续执行`,
      evidence: `表头=${header.join('|')}；缺失列=${missingColumns.join(',')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一格无法核对`,
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
  if (text.trim() === '') return insufficient(['成本分配表文本为空：请把带表头的 Tab 分隔成本分配表贴进来']);

  const { items, totals, missingColumns, header, cols } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可以有）']);
  }
  const mapped = cols.filter((c) => c.role).length;
  if (mapped === 0) {
    return insufficient([
      '认不出表头：列名里要能看到「产品/批次」「工序或车间」「完工产品成本」「期末在产品成本」等字样',
      '未能识别的必需列：' + REQUIRED.map((r) => LABELS[r]).join('、'),
    ]);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkInTotal(it), checkCostConservation(it), checkQtyMissing(it), checkNegativeCost(it)];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  let notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0,
        p1,
        p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
