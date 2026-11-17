/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * contract-asset-liability-aging-check-full.js —— 合同资产与合同负债账龄核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**按履约进度确认收入、或按合同预收款项的企业**，
 * 在**每月结账 / 出具报表之前**、以及**年度审计提供底稿时**，要把"合同资产 / 合同负债"台账核一遍。
 * 新收入准则下同一个合同既可能"先干活后收款"（合同资产）、也可能"先收款后干活"（合同负债）：
 * 台账要能**逐行滚动对上**，并且同一个合同**不应同时**在两边都挂余额（该重分类的必须重分类）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末合同资产 = 期初合同资产 + 本期新增合同资产 − 本期结转收入
 *   期末合同负债 = 期初合同负债 + 本期新增合同负债 − 本期确认收入
 *   明细逐行相加 = 合计行（表头里的**全部金额列**）
 *   本期结转收入 ≤ 期初合同资产 + 本期新增合同资产（不能超结转）
 *   本期确认收入 ≤ 期初合同负债 + 本期新增合同负债（不能超确认）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔款项到底该记合同资产还是合同负债、也不判断履约进度是否恰当（那属于会计判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**，不读环境变量。
 */

/* ⛔ 顺序即优先级：**带限定语的完整列名必须排在裸词前面**（本仓库踩过 6 次的坑）。
   表头有 `期初合同资产` / `本期新增合同资产` / `本期结转收入` / `期末合同资产`，
   以及 `期初合同负债` / `本期新增合同负债` / `本期确认收入` / `期末合同负债` —— 8 个列名两两互相包含。
   `roleOf` 命中**第一个**匹配上的角色，所以：
     · 每个角色的别名数组里，**完整列名排最前**，裸词（`合同资产` / `合同负债` / `账龄`）排最后；
     · 裸词只许放在**该族最后一个角色**里（`合同资产` 只挂在 assetEnd、`合同负债` 只挂在 liabEnd），
       否则它会抢走 `期初/本期新增` 的列 —— 抢走的表现是"列静默不参与检查"，不报错，最难发现。 */
const ROLES = {
  contractNo: ['合同编号', '合同号', '合同代码'],
  party: ['客户/供应商', '客户或供应商', '客户名称', '供应商名称', '客户', '供应商'],
  project: ['项目名称', '项目'],
  /* 合同资产族：期初 → 新增 → 结转 → 期末（顺序即优先级，别调换） */
  assetBegin: ['期初合同资产', '合同资产期初', '期初资产'],
  assetAdd: ['本期新增合同资产', '本期增加合同资产', '新增合同资产'],
  assetCarry: ['本期结转收入', '本期结转', '结转收入'],
  assetEnd: ['期末合同资产', '合同资产期末', '期末资产', '合同资产'],
  /* 合同负债族：期初 → 新增 → 确认 → 期末（顺序即优先级，别调换） */
  liabBegin: ['期初合同负债', '合同负债期初', '期初负债'],
  liabAdd: ['本期新增合同负债', '本期增加合同负债', '新增合同负债'],
  liabRecog: ['本期确认收入', '本期确认', '确认收入'],
  liabEnd: ['期末合同负债', '合同负债期末', '期末负债', '合同负债'],
  agingDays: ['账龄天数', '账龄（天）', '账龄(天)', '账龄', '天数'],
};

const LABELS = {
  contractNo: '合同编号', party: '客户/供应商', project: '项目',
  assetBegin: '期初合同资产', assetAdd: '本期新增合同资产', assetCarry: '本期结转收入',
  assetEnd: '期末合同资产', liabBegin: '期初合同负债', liabAdd: '本期新增合同负债',
  liabRecog: '本期确认收入', liabEnd: '期末合同负债', agingDays: '账龄天数',
};

/* 必需列：核心滚动关系 + 重复检测 + 账龄都要用到它们。
   缺任何一列都**照常给结论**，只在第 1 行报一条「列缺失」并跳过依赖它的检查（不做任何默认值代入）。 */
const REQUIRED = [
  'contractNo', 'assetBegin', 'assetAdd', 'assetCarry', 'assetEnd',
  'liabBegin', 'liabAdd', 'liabRecog', 'liabEnd', 'agingDays',
];

/* 要逐列做「明细相加 = 合计」的金额列：表头里全部 8 个金额列（合同资产 4 + 合同负债 4）。 */
const SUM_ROLES = [
  'assetBegin', 'assetAdd', 'assetCarry', 'assetEnd',
  'liabBegin', 'liabAdd', 'liabRecog', 'liabEnd',
];

const TOTAL_WORDS = /^(合计|总计|小计|合计数?|累计)$/;
const TOL = 0.01;

/* ⚠️ 付费开关**只声明一次**，且只用 `Boolean(...)` 这一种写法：`strip_free_engine` 按
   「开关行 + 付费分支」识别并整块摘掉；写成别的形态（例：数组的 .some()）会**留下开关不删**
   ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出开关那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本仓库实测踩到）。
   ⛔ 形态 A（MARKER 整块）与形态 B（内联分支）**只许出现一个**：两个同时出现时
      `strip_free_engine` 会走形态 A，把免费检查也整块删掉（第 236 轮踩过）。本引擎用**形态 B**。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（期初 / 本期新增 / 本期结转 / 期末 的合同资产与合同负债，表头里全部 8 个金额列：明细逐行相加 = 合计）',
  '同一「合同编号」重复行检测',
  '期末合同资产 = 期初合同资产 + 本期新增合同资产 − 本期结转收入（不符报 P0）',
  '期末合同负债 = 期初合同负债 + 本期新增合同负债 − 本期确认收入（不符报 P0）',
  '同一合同同时挂「期末合同资产」与「期末合同负债」（应重分类到对方，报 P1）',
  '账龄天数为负（报 P1）',
  '空白与占位符检测（含必需列缺失；只缺个别列仍照常给结论并报「列缺失」）',
];

const CHECKS_WITHHELD = [
  '账龄超过 365 天的合同资产 / 合同负债提示（长期挂账，P2）',
  '期末合同资产或期末合同负债为负（报 P0）',
  '本期结转收入 > 期初合同资产 + 本期新增合同资产（超结转，报 P0）',
  '本期确认收入 > 期初合同负债 + 本期新增合同负债（超确认，报 P0）',
  '账龄 ≤ 0 但期末仍有余额（本期新增却没填账龄，报 P2）',
];

const OUT_OF_SCOPE = [
  '判断某笔款项**实质上**该记合同资产还是合同负债（要看合同条款与履约进度，属于会计判断）',
  '判断履约进度、收入确认时点或金额是否恰当（属于会计判断与估计）',
  '按账龄计提合同资产减值准备（减值迹象与比例属于会计估计判断）',
  '核对合同、发票、结算单的**真伪**，或与业务系统的逐行明细比对',
  '代替审计程序，也不出具审计或鉴证意见',
  '读取 ERP / 财务系统的导出文件（需要你先导出成文本贴进来）',
];

/* 干净样例：两档都必须 0 条发现。
   逐行验证：350000 = 300000+200000−150000；0 = 0+0−0；30000 = 100000+50000−120000；
            520000 = 500000+200000−180000；每行都没有同时两边挂余额；账龄 120/90/200 全为正。 */
const SAMPLE_TEXT = [
  '合同编号\t客户/供应商\t项目\t期初合同资产\t本期新增合同资产\t本期结转收入\t期末合同资产\t期初合同负债\t本期新增合同负债\t本期确认收入\t期末合同负债\t账龄天数',
  'HT-2026-001\t甲客户\t系统集成\t300000\t200000\t150000\t350000\t0\t0\t0\t0\t120',
  'HT-2026-002\t乙客户\t设备安装\t0\t0\t0\t0\t500000\t200000\t180000\t520000\t90',
  'HT-2026-003\t丙供应商\t运维服务\t100000\t50000\t120000\t30000\t0\t0\t0\t0\t200',
  '合计\t\t\t400000\t250000\t270000\t380000\t500000\t200000\t180000\t520000\t',
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

const who = (it) => {
  const no = String(it.contractNo || '').trim();
  if (!no) return `第 ${it.line} 行`;
  const p = String(it.party || '').trim();
  return p ? `${no}（${p}）` : `${no}`;
};

/* 期末两边的余额（供"同时挂账 / 期末为负 / 账龄提示"共用）。 */
function endSides(it) {
  return { asset: normNumber(it.assetEnd), liab: normNumber(it.liabEnd) };
}

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
    const stated = num(totals.row, role);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = num(it, role);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细 ${n} 行逐行相加是 ${sum}（差 ${round2(stated - sum)}）`,
        evidence: `合计行=${stated}；明细逐行相加=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.contractNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「合同编号」完全相同（${key}）—— 可能重复计入`,
        evidence: `合同编号=${key}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkAssetRollForward(it) {
  const begin = num(it, 'assetBegin');
  const add = num(it, 'assetAdd');
  const carry = num(it, 'assetCarry');
  const end = num(it, 'assetEnd');
  if (begin === null || add === null || carry === null || end === null) return null;
  const expect = round2(begin + add - carry);
  if (Math.abs(end - expect) > TOL) {
    return {
      line: it.line, level: 'P0', category: '合同资产滚动不符',
      message: `${who(it)} 期末合同资产填 ${end}，但按「期初 ${begin} + 本期新增 ${add} − 本期结转 ${carry}」应为 ${expect}（差 ${round2(end - expect)}）`,
      evidence: `期初合同资产=${begin}；本期新增合同资产=${add}；本期结转收入=${carry}；应为=${expect}；填报=${end}`,
    };
  }
  return null;
}

function checkLiabilityRollForward(it) {
  const begin = num(it, 'liabBegin');
  const add = num(it, 'liabAdd');
  const recog = num(it, 'liabRecog');
  const end = num(it, 'liabEnd');
  if (begin === null || add === null || recog === null || end === null) return null;
  const expect = round2(begin + add - recog);
  if (Math.abs(end - expect) > TOL) {
    return {
      line: it.line, level: 'P0', category: '合同负债滚动不符',
      message: `${who(it)} 期末合同负债填 ${end}，但按「期初 ${begin} + 本期新增 ${add} − 本期确认 ${recog}」应为 ${expect}（差 ${round2(end - expect)}）`,
      evidence: `期初合同负债=${begin}；本期新增合同负债=${add}；本期确认收入=${recog}；应为=${expect}；填报=${end}`,
    };
  }
  return null;
}

function checkBothSides(it) {
  const s = endSides(it);
  if (s.asset === null || s.liab === null) return null;
  if (s.asset > TOL && s.liab > TOL) {
    return {
      line: it.line, level: 'P1', category: '同一合同两边同时挂账',
      message: `${who(it)} 期末合同资产 ${s.asset} 与期末合同负债 ${s.liab} 同时有余额 —— 同一合同不应两边都挂，应重分类到对方`,
      evidence: `期末合同资产=${s.asset}；期末合同负债=${s.liab}`,
    };
  }
  return null;
}

function checkNegativeAging(it) {
  const days = num(it, 'agingDays');
  if (days === null || days >= 0) return null;
  return {
    line: it.line, level: 'P1', category: '账龄天数为负',
    message: `${who(it)} 账龄天数填 ${days} 天（负数）—— 账龄不可能为负`,
    evidence: `账龄天数=${days}`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}（共 ${missingColumns.length} 列）—— 依赖这些列的项目本次跳过，其余检查照常出结论`,
      evidence: `表头=${header.join('|')}；缺少=${missingColumns.join('、')}`,
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
  if (text.trim() === '') {
    return insufficient(['材料文本为空：请把「合同资产与合同负债账龄核对」台账（含表头）贴进来']);
  }

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['没有明细行：第一行必须是表头，且至少有一行明细（「合计」行不能当明细）']);
  }
  if (!header.some((h) => roleOf(h))) {
    return insufficient(['认不出表头：第一行必须是列名（合同编号 / 期初合同资产 / 期末合同负债 / 账龄天数 …），Tab 分隔最稳']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [
      checkAssetRollForward(it),
      checkLiabilityRollForward(it),
      checkBothSides(it),
      checkNegativeAging(it),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
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
        asset_end_total: round2(items.reduce((n, it) => n + (num(it, 'assetEnd') || 0), 0)),
        liab_end_total: round2(items.reduce((n, it) => n + (num(it, 'liabEnd') || 0), 0)),
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
