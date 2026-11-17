#!/usr/bin/env node
/**
 * medical-device-traceability-check.js —— 医疗器械 UDI 与出入库追溯核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点（医院设备科 / 器械经营企业**每月**必做）：
 *   ① 采购入库要登记 UDI-DI（产品标识）与 UDI-PI（生产标识：批号/序列号、有效期至），
 *      出库/使用要能**反向追溯到科室或患者**；
 *   ② 植入介入类器械还要留存使用登记（谁用了、用在哪台手术、给了哪个患者）；
 *   ③ 飞检与医保检查最常见的整改项就是「UDI 不完整」「批号与实物不符」
 *      「效期过期仍在用」「追溯链条断在某个环节」；
 *   ④ 每月必须核：UDI 完整性、批号序列号一致性、效期、出入库勾稽、追溯链完整性。
 *
 * 本文件是**同源引擎**：本包 6 项与订阅版追加的 5 项都写在这一份源码里。
 *   · 免费包里的 `medical-device-traceability-check.js` 由 `tools/strip_free_engine.py`
 *     从本文件**摘出**，那是一份**本包子集**：订阅版追加的 5 项连实现一起摘掉，免费包里没有它们；
 *   · 买断包里的 `medical-device-traceability-check-full.js` 就是本文件，入口一律按**订阅版**跑。
 *   `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定器械质量与能否继续使用、不联网核验 UDI/注册证真伪、不做法规条款级合规判定、
 *          不读 .xlsx/.pdf/图片原件；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  'UDI 完整性（逐行点名 UDI-DI 缺失、UDI-PI 缺批号或序列号、UDI-PI 缺有效期至）',
  '出入库数量勾稽（逐行复算 期初库存 + 入库数量 − 出库数量 = 期末库存，差额不为零即列出）',
  '效期核对（核对日期 ≤ 有效期至；已过期或临期 30 天内即报出并给天数）',
  '同一 UDI-DI + 同一批号或序列号重复登记检测',
  '合计行逐列复核（数量类列：期初库存 / 入库数量 / 出库数量 / 期末库存 与明细逐列相加对比）',
  '关键字段与数量合法性（产品名称/规格型号/注册证号/生产厂家/库位/核对日期空缺、日期格式、数量为负或无法解析、状态值非法）',
];

const CHECKS_WITHHELD = [
  '追溯链完整性（出库记录缺少使用科室/患者去向即点名断链环节，植入介入类必须留存使用登记）',
  '注册证有效期覆盖（入库或使用日期超出注册证有效期 ⇒ 点名「过期注册证仍在流转」）',
  '效期与库龄（入库日期到核对日期超过本行给出的库龄阈值且期末仍在库 ⇒ 提示）',
  '同一批号跨库位/跨供应商（防串货、防混批 ⇒ 逐批号点名）',
  '分科室 × 分器械类别的汇总清单（按追溯缺口与效期风险排序，给出可整改动作）+ 逐条整改清单',
];

const OUT_OF_SCOPE = [
  '判定器械本身质量是否合格、能否继续使用（那是医疗器械质量管理与不良事件监测的职责），本工具只核台账字面与算术',
  '联网核验 UDI-DI / 注册证号真伪，或比对国家药监局 UDI 数据库（本工具不联网、不读数据库）',
  '做法规条款级合规判定（逐条判定是否符合《医疗器械唯一标识系统规则》等条款），本工具只做表内逐行核对',
  '读取 .xlsx / .pdf / 图片原件，或识别随货同行单、发票、灭菌批号标签上的内容',
  '判定植入器械使用登记是否已上报、是否构成需要报告的不良事件',
];

// 样例：一张**干净**的医疗器械 UDI 与出入库追溯台账 —— 四个品种（含一个植入介入类），
// UDI-DI 与 UDI-PI（批号/序列号 + 有效期至）齐全、期初+入库−出库=期末、效期都不在 30 天内、
// 批号不重复、合计行与明细逐列相等、出库都写了使用科室/患者去向（植入类写「骨科/患者A」掩码）、
// 注册证都在有效期内、库龄都没超本行给的阈值。
const SAMPLE_TEXT = [
  'UDI-DI\t产品名称\t规格型号\t批号或序列号\t有效期至\t注册证号\t生产厂家\t期初库存\t入库数量\t出库数量\t期末库存\t库位\t核对日期\t注册证有效期至\t入库日期\t库龄阈值天数\t供应商\t器械类别\t使用科室或患者去向\t状态',
  'UDI-2026-000101\t一次性使用无菌注射器\t5ml\tLOT-A2601\t2027-12-31\t国械注准20263000101\t华康医疗器械（示例）有限公司\t0\t200\t120\t80\tA区-常温架1\t2026-07-01\t2030-12-31\t2026-03-10\t180\t华东医械（示例）有限公司\t低值耗材\t手术室\t在库',
  'UDI-2026-000102\t医用外科口罩\t17.5cm×9.5cm\tLOT-B2602\t2026-08-31\t国械注准20263000102\t华康医疗器械（示例）有限公司\t100\t300\t300\t100\tA区-常温架2\t2026-07-01\t2030-12-31\t2026-02-05\t180\t华东医械（示例）有限公司\t低值耗材\t消毒供应中心\t在库',
  'UDI-2026-000103\t椎间融合器\tPEEK-8mm\tSN-IMP-2603\t2028-05-31\t国械注准20263000103\t弘康骨科器械（示例）有限公司\t0\t20\t18\t2\tB区-植入器械专柜\t2026-07-01\t2031-06-30\t2026-01-15\t365\t弘康医械（示例）有限公司\t植入介入类\t骨科/患者A\t在库',
  'UDI-2026-000104\t一次性使用输液器\t0.7×25mm\tLOT-C2604\t2026-09-30\t国械注准20263000104\t华康医疗器械（示例）有限公司\t50\t0\t30\t20\tC区-常温架3\t2026-07-01\t2030-12-31\t2026-04-20\t120\t华东医械（示例）有限公司\t低值耗材\t输液室\t在库',
  '合计\t-\t-\t-\t-\t-\t-\t150\t520\t468\t202\t-\t-\t-\t-\t-\t-\t-\t-\t-',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = ['udiDi', 'productName', 'specModel', 'batchNo', 'expiry', 'regCertNo',
  'manufacturer', 'openQty', 'inQty', 'outQty', 'closeQty', 'location', 'checkDate'];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const CELL_REQUIRED = [
  ['productName', '产品名称'],
  ['specModel', '规格型号'],
  ['regCertNo', '注册证号'],
  ['manufacturer', '生产厂家'],
  ['location', '库位'],
  ['checkDate', '核对日期'],
];

// 数量列（勾稽、为负、无法解析都用它）
const QTY_FIELDS = [
  ['openQty', '期初库存'],
  ['inQty', '入库数量'],
  ['outQty', '出库数量'],
  ['closeQty', '期末库存'],
];

// 日期列（格式合法性；有效期至/核对日期是必需列，入库日期与注册证有效期至是订阅版才会用到的列）
const DATE_FIELDS = [
  ['expiry', '有效期至'],
  ['checkDate', '核对日期'],
  ['inDate', '入库日期'],
  ['regCertExpiry', '注册证有效期至'],
];

// 状态列允许的取值（列存在时校验；列不存在只记「没做」，不猜）
const STATUS_ALLOWED = ['在库', '在用', '已出库', '已使用', '已退回', '已报废', '待验', '停用'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本例的雷区：「入库日期」会被「入库」抢走、「注册证有效期至」会被「有效期」抢走 ——
//    所以 inDate 必须排在 inQty/outQty 之前，regCertExpiry 必须排在 expiry 之前。
const ROLES = {
  udiDi: ['UDI-DI', 'UDI DI', 'UDI'],
  productName: ['产品名称', '器械名称', '品名', '名称'],
  specModel: ['规格型号', '规格', '型号'],
  batchNo: ['批号或序列号', '批号/序列号', '生产批号', '批号', '序列号'],
  regCertExpiry: ['注册证有效期至', '注册证有效期', '注册证到期日'],
  regCertNo: ['注册证号', '注册证编号', '医疗器械注册证'],
  expiry: ['有效期至', '有效期', '失效日期', '效期'],
  inDate: ['入库日期', '入库时间', '到货日期', '采购日期'],
  checkDate: ['核对日期', '盘点日期', '核对基准日', '截止日期'],
  ageLimit: ['库龄阈值天数', '库龄阈值', '库龄上限', '滞留天数'],
  manufacturer: ['生产厂家', '生产企业', '厂商', '厂家'],
  openQty: ['期初库存', '期初结存', '期初数量', '期初'],
  inQty: ['入库数量', '本期入库', '入库数', '入库'],
  outQty: ['出库数量', '本期出库', '出库数', '出库'],
  closeQty: ['期末库存', '期末结存', '期末数量', '期末'],
  location: ['库位', '货位', '存放位置', '库房'],
  supplier: ['供应商', '供货单位', '供货商', '供应单位'],
  category: ['器械类别', '产品类别', '管理类别', '器械分类'],
  dest: ['使用科室或患者去向', '使用科室', '患者去向', '领用科室', '出库去向', '去向'],
  status: ['状态', '记录状态', '使用状态'],
};

const LABELS = {
  udiDi: 'UDI-DI',
  productName: '产品名称',
  specModel: '规格型号',
  batchNo: '批号或序列号',
  regCertExpiry: '注册证有效期至',
  regCertNo: '注册证号',
  expiry: '有效期至',
  inDate: '入库日期',
  checkDate: '核对日期',
  ageLimit: '库龄阈值天数',
  manufacturer: '生产厂家',
  openQty: '期初库存',
  inQty: '入库数量',
  outQty: '出库数量',
  closeQty: '期末库存',
  location: '库位',
  supplier: '供应商',
  category: '器械类别',
  dest: '使用科室或患者去向',
  status: '状态',
};

const SUM_ROLES = ['openQty', 'inQty', 'outQty', 'closeQty'];

const TOTALS_RE = /^(合计|总计|小计|汇总)$/;

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「一致」，也不说「不一致」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|未知)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D / YYYY年M月D日；其余（含不存在的日期）一律 null */
function parseDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim()
    .replace(/[年月]/g, '-')
    .replace(/日/g, '')
    .replace(/[./]/g, '-');
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return dt;
}

/** b − a 的天数（正数 = b 在 a 之后） */
function daysBetween(a, b) {
  return Math.round((b.getTime() - a.getTime()) / 86400000);
}

function isTotalsRow(cells) {
  return cells.some((c) => TOTALS_RE.test(String(c == null ? '' : c).trim()));
}

/** 解析成 {header, cols, items, totalsRow, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totalsRow: null, totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  let totalsRow = null;
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    if (isTotalsRow(cells)) { totalsRow = it; continue; }
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totalsRow,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

function num(it, role) {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
}

function who(it) {
  const name = String(it.productName == null ? '' : it.productName).trim();
  const udi = String(it.udiDi == null ? '' : it.udiDi).trim();
  const batch = String(it.batchNo == null ? '' : it.batchNo).trim();
  const tail = [udi, batch].filter((s) => s !== '').join('｜');
  return `第 ${it.line} 行「${name || '(未填产品名称)'}${tail ? '｜' + tail : ''}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    evidence: String(it.raw == null ? '' : it.raw).trim(),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

const qty = (n) => String(round2(n));

/* ============================ 本包检查（六项） ============================ */

/** 1. UDI 完整性：UDI-DI 与 UDI-PI（批号或序列号、有效期至）逐行点名 */
function checkUdiCompleteness(items) {
  const out = [];
  for (const it of items) {
    if (isBlank(it.udiDi)) {
      out.push(finding('P0', 'UDI-DI 缺失', it, undefined,
        `${who(it)}：UDI-DI（产品标识）这一栏是空的或占位符 —— 这条记录没有产品标识可用。`,
        '从器械标签/包装上抄录 UDI-DI（产品标识）补进这一行；缺 UDI-DI 时这条记录无法与国家药监局 UDI 数据库对上。'));
    }
    if (isBlank(it.batchNo)) {
      out.push(finding('P0', 'UDI-PI 缺失（批号或序列号）', it, undefined,
        `${who(it)}：UDI-PI（生产标识）里的「批号或序列号」是空的 —— 同一个 UDI-DI 下的多批器械就此分不开。`,
        '按实物标签补上批号或序列号；植入介入类通常用序列号，逐件可追。'));
    }
    if (isBlank(it.expiry)) {
      out.push(finding('P0', 'UDI-PI 缺失（有效期至）', it, undefined,
        `${who(it)}：UDI-PI（生产标识）里的「有效期至」是空的 —— 效期核对这一项在这行做不了。`,
        '补上有效期至（YYYY-MM-DD）；确无有效期的器械请在备注写明并保留原值，不要留空。'));
    }
  }
  return out;
}

/** 2. 出入库数量勾稽：期初 + 入库 − 出库 = 期末（逐 UDI 逐批号，就是逐行） */
function checkStockBalance(items) {
  const out = [];
  for (const it of items) {
    const open = normNumber(it.openQty);
    const inn = normNumber(it.inQty);
    const o = normNumber(it.outQty);
    const close = normNumber(it.closeQty);
    if (open === null || inn === null || o === null || close === null) continue;
    const expect = round2(open + inn - o);
    const diff = round2(close - expect);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '出入库数量不勾稽', it, diff,
      `${who(it)}：期初库存 ${qty(open)} + 入库 ${qty(inn)} − 出库 ${qty(o)} = ${qty(expect)}，`
      + `但期末库存写的是 ${qty(close)}，差 ${qty(diff)}。`,
      '按同一 UDI + 同一批号逐笔对出入库单据：常见原因是出库单漏登记、退货/报损没入账，或期末数是盘点后手工改的。'));
  }
  return out;
}

/** 3. 效期核对：核对日期 ≤ 有效期至（过期 / 临期 30 天内都报出来并给天数） */
function checkExpiry(items) {
  const out = [];
  for (const it of items) {
    const exp = parseDate(it.expiry);
    const base = parseDate(it.checkDate);
    if (exp === null || base === null) continue;
    const days = daysBetween(base, exp);
    const expRaw = String(it.expiry).trim();
    const baseRaw = String(it.checkDate).trim();
    if (days < 0) {
      out.push(finding('P0', '效期已过', it, days,
        `${who(it)}：有效期至 ${expRaw}，核对基准日 ${baseRaw} —— 已过期 ${Math.abs(days)} 天，按口径不得继续在库或使用。`,
        '先隔离实物并锁定库位，再走不合格品/退货流程；同时查这批有没有已经出库到临床，已使用的要走上报流程。'));
    } else if (days <= 30) {
      out.push(finding('P1', '效期临期（30 天内）', it, days,
        `${who(it)}：有效期至 ${expRaw}，核对基准日 ${baseRaw} —— 只剩 ${days} 天（临期 30 天内）。`,
        '按先进先出安排先用；本期内用不完的做换货/退货或调剂到其他院区，别让它放到过期。'));
    }
  }
  return out;
}

/** 4. 同一 UDI-DI + 同一批号或序列号重复登记 */
function checkDuplicateRegistration(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const udi = String(it.udiDi == null ? '' : it.udiDi).trim();
    const batch = String(it.batchNo == null ? '' : it.batchNo).trim();
    if (!udi || !batch) continue;
    const key = udi + '|' + batch;
    if (seen.has(key)) {
      out.push(finding('P0', '同一 UDI+批号重复登记', it, undefined,
        `${who(it)}：UDI-DI「${udi}」+ 批号「${batch}」在第 ${seen.get(key)} 行已经登记过一次 —— 同一条器械追溯记录重复登记。`,
        '同一 UDI + 同一批号在本期只应有一条出入库勾稽记录；分批到货请拆成不同批号，或把两次数量并入同一行。'));
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 5. 合计行逐列复核（数量类列：合计行写的数必须等于明细逐列相加） */
function checkTotalsRow(totalsRow, totals) {
  const out = [];
  if (!totalsRow) return out;
  for (const [role, label] of QTY_FIELDS) {
    const declared = normNumber(totalsRow[role]);
    if (declared === null) continue;
    const computed = totals[role];
    const diff = round2(declared - computed);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P1', '合计行与明细不符', totalsRow, diff,
      `第 ${totalsRow.line} 行合计行的「${label}」写的是 ${qty(declared)}，`
      + `但上面明细逐行相加是 ${qty(computed)}，差 ${qty(diff)}。`,
      '合计行要用公式（SUM）跟着明细走，不要手工填；先确认有没有明细行被漏抄或被重复抄。'));
  }
  return out;
}

/** 6. 关键字段与数量合法性（空缺、日期格式、数量为负/无法解析、状态值非法） */
function checkFieldIntegrity(items, rolesPresent) {
  const out = [];
  for (const it of items) {
    const miss = CELL_REQUIRED.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    for (const [role, label] of QTY_FIELDS) {
      if (isBlank(it[role])) miss.push(label);
    }
    if (rolesPresent.has('status') && isBlank(it.status)) miss.push('状态');
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑。本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of QTY_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数量无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数量（只认数字、千分位、括号负数）。`,
          '把数量改成纯数字形态（如 200）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数量为负', it, n,
          `${who(it)}：「${label}」是负数（${qty(n)}）—— 出入库台账里出现负数通常是填反了方向，或写成了红字冲销。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      }
    }
    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (parseDate(raw) === null) {
        out.push(finding('P1', '日期格式无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D / YYYY年M月D日）。',
          '改成 YYYY-MM-DD 再跑；本工具不会把看不懂的日期当成没过期、也不会当成没登记。'));
      }
    }
    const st = String(it.status == null ? '' : it.status).trim();
    if (st !== '' && !isBlank(it.status) && STATUS_ALLOWED.indexOf(st) < 0) {
      out.push(finding('P1', '状态值非法', it, undefined,
        `${who(it)}：状态值「${st}」不在允许的取值里（${STATUS_ALLOWED.join(' / ')}）。`,
        '按台账口径把状态改成允许值之一；状态写错会让「在库 / 已出库」的勾稽完全对不上。'));
    }
  }
  return out;
}

/* ============================ 订阅版追加的检查（付费） ============================ */

/** 付费 1. 追溯链完整性：出库了却没有使用科室/患者去向 ⇒ 点名断链环节（植入介入类必须留存使用登记） */
function checkTraceChain(it, hasDest) {
  const out = [];
  if (!hasDest) return out;
  const o = normNumber(it.outQty);
  if (o === null || o <= 0) return out;
  const dest = String(it.dest == null ? '' : it.dest).trim();
  if (dest !== '' && !isBlank(it.dest)) return out;
  const cat = String(it.category == null ? '' : it.category).trim();
  const implant = /植入|介入/.test(cat);
  out.push(finding(implant ? 'P0' : 'P1', '追溯链断链（缺少使用科室/患者去向）', it, undefined,
    `${who(it)}：出库 ${qty(o)} 件，但「使用科室或患者去向」是空的 —— 追溯链断在**出库环节**：`
    + `往回查得到货，往前查不到给了谁用${implant ? `（器械类别「${cat}」属植入介入类，必须留存使用登记）` : ''}。`,
    '按出库单补使用科室；植入介入类还要补患者标识（用患者A/患者B 这类掩码或院内病历号，不要写身份证号）。'));
  return out;
}

/** 付费 2. 注册证有效期覆盖：入库或使用（核对）日期 ≤ 注册证有效期至 */
function checkRegCertCoverage(it) {
  const out = [];
  const cert = parseDate(it.regCertExpiry);
  if (cert === null) return out;
  const hits = [];
  const inD = parseDate(it.inDate);
  if (inD !== null && daysBetween(cert, inD) > 0) hits.push(`入库日期 ${String(it.inDate).trim()}`);
  const o = normNumber(it.outQty);
  const chk = parseDate(it.checkDate);
  if (o !== null && o > 0 && chk !== null && daysBetween(cert, chk) > 0) {
    hits.push(`使用（核对）日期 ${String(it.checkDate).trim()}`);
  }
  if (!hits.length) return out;
  out.push(finding('P0', '注册证过期仍在流转', it, undefined,
    `${who(it)}：注册证有效期至 ${String(it.regCertExpiry).trim()}，但 ${hits.join('、')} 已经超出注册证有效期 —— 过期证照下的器械仍在流转/使用。`,
    '停用并锁定这批器械，核对是否有延续注册的新证；新证未下发前不得继续出库使用，已使用的要补追溯登记。'));
  return out;
}

/** 付费 3. 效期与库龄：入库日期到核对日期超过本行给的库龄阈值，且期末仍在库 */
function checkShelfAge(it) {
  const out = [];
  const inD = parseDate(it.inDate);
  const chk = parseDate(it.checkDate);
  const limit = normNumber(it.ageLimit);
  const close = normNumber(it.closeQty);
  if (inD === null || chk === null || limit === null) return out;
  if (close === null || close <= 0) return out;
  const age = daysBetween(inD, chk);
  if (age <= limit) return out;
  out.push(finding('P2', '库龄超阈值仍在库', it, age,
    `${who(it)}：${String(it.inDate).trim()} 入库、${String(it.checkDate).trim()} 核对 —— 在库库龄 ${age} 天，`
    + `超过本行给的库龄阈值 ${qty(limit)} 天，且期末仍在库 ${qty(close)} 件。`,
    '按周转/先进先出安排动用或调剂；长期不动的要盘实数量，避免放到效期临界才处理。'));
  return out;
}

/** 付费 4. 同一批号跨库位 / 跨供应商（防串货、防混批） */
function checkBatchCrossLocation(items) {
  const out = [];
  const byBatch = new Map();
  for (const it of items) {
    const batch = String(it.batchNo == null ? '' : it.batchNo).trim();
    if (!batch) continue;
    if (!byBatch.has(batch)) byBatch.set(batch, []);
    byBatch.get(batch).push(it);
  }
  for (const [batch, list] of byBatch) {
    if (list.length < 2) continue;
    const sups = new Set();
    const locs = new Set();
    for (const it of list) {
      const s = String(it.supplier == null ? '' : it.supplier).trim();
      const l = String(it.location == null ? '' : it.location).trim();
      if (s !== '' && !isBlank(it.supplier)) sups.add(s);
      if (l !== '' && !isBlank(it.location)) locs.add(l);
    }
    const crossSup = sups.size >= 2;
    const crossLoc = locs.size >= 2;
    if (!crossSup && !crossLoc) continue;
    const last = list[list.length - 1];
    const lines = list.map((it) => it.line).join('、');
    const parts = [];
    if (crossSup) parts.push(`跨 ${sups.size} 个供应商（${[...sups].join('、')}）`);
    if (crossLoc) parts.push(`跨 ${locs.size} 个库位（${[...locs].join('、')}）`);
    out.push(finding('P1', '同一批号跨库位或跨供应商', last, undefined,
      `批号「${batch}」在 ${list.length} 行里出现，${parts.join('，')}（第 ${lines} 行）—— `
      + '同一批号分散在多处，存在串货 / 混批风险，出问题时无法定位到唯一来源。',
      '把同一批号归到同一库位，并核对供应商随货同行单；确属分批采购的请拆分批号或加子批号（如 LOT-B2602-A）。'));
  }
  return out;
}

/** 付费 5-a. 一个科室 × 一个器械类别的可整改动作 */
function buildGroupAction(g) {
  const parts = [];
  if (g.chain_gaps > 0) parts.push(`补 ${g.chain_gaps} 行出库记录的「使用科室/患者去向」，把出库环节的断链接上`);
  if (g.expiry_risks > 0) parts.push(`处理 ${g.expiry_risks} 行效期风险（过期隔离、临期先用或换货）`);
  if (g.cert_risks > 0) parts.push(`核对 ${g.cert_risks} 行注册证过期仍在流转的器械并停用`);
  if (!parts.length) parts.push('本期无追溯缺口与效期风险，按常规盘点复核数量即可');
  return parts.join('；') + '。';
}

/** 付费 5-b. 分科室 × 分器械类别的汇总清单（按追溯缺口与效期风险排序）+ 逐条整改清单 */
function buildConsolidation(items, findings) {
  const riskByLine = new Map();
  for (const f of findings) {
    const cur = riskByLine.get(f.line) || { chain: 0, expiry: 0, cert: 0 };
    if (f.category === '追溯链断链（缺少使用科室/患者去向）') cur.chain += 1;
    else if (f.category === '效期已过' || f.category === '效期临期（30 天内）') cur.expiry += 1;
    else if (f.category === '注册证过期仍在流转') cur.cert += 1;
    riskByLine.set(f.line, cur);
  }
  const groups = new Map();
  for (const it of items) {
    const dept = String(it.dest == null ? '' : it.dest).trim() || '(未填使用科室/去向)';
    const cat = String(it.category == null ? '' : it.category).trim() || '(未填器械类别)';
    const key = dept + '|' + cat;
    if (!groups.has(key)) {
      groups.set(key, {
        dept: dept, category: cat, rows: 0, qty_in: 0, qty_out: 0, qty_close: 0,
        chain_gaps: 0, expiry_risks: 0, cert_risks: 0, risk_score: 0, lines: [],
      });
    }
    const g = groups.get(key);
    g.rows += 1;
    g.qty_in = round2(g.qty_in + num(it, 'inQty'));
    g.qty_out = round2(g.qty_out + num(it, 'outQty'));
    g.qty_close = round2(g.qty_close + num(it, 'closeQty'));
    g.lines.push(it.line);
    const r = riskByLine.get(it.line);
    if (r) {
      g.chain_gaps += r.chain;
      g.expiry_risks += r.expiry;
      g.cert_risks += r.cert;
    }
  }
  const list = [...groups.values()].map((g) => Object.assign({}, g, {
    risk_score: g.chain_gaps * 3 + g.expiry_risks * 2 + g.cert_risks * 2,
    action: buildGroupAction(g),
  }));
  list.sort((a, b) => (b.risk_score - a.risk_score)
    || String(a.dept).localeCompare(String(b.dept))
    || String(a.category).localeCompare(String(b.category)));

  const actions = [];
  for (const g of list) {
    if (g.risk_score <= 0) continue;
    actions.push({
      seq: actions.length + 1,
      scope: g.dept + ' × ' + g.category,
      kind: g.chain_gaps > 0 ? '追溯缺口' : (g.expiry_risks > 0 ? '效期风险' : '证照风险'),
      level: g.chain_gaps > 0 ? 'P0' : 'P1',
      risk_score: g.risk_score,
      lines: g.lines.slice(),
      action: g.action,
    });
  }

  const total = items.reduce((acc, it) => {
    acc.rows += 1;
    acc.qty_in = round2(acc.qty_in + num(it, 'inQty'));
    acc.qty_out = round2(acc.qty_out + num(it, 'outQty'));
    acc.qty_close = round2(acc.qty_close + num(it, 'closeQty'));
    return acc;
  }, { rows: 0, qty_in: 0, qty_out: 0, qty_close: 0 });

  return { by_dept_category: list, actions: actions, total: total };
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  const needAll = REQUIRED_ROLES.map((r) => LABELS[r]);
  if (!String(text).trim()) {
    return insufficient([`原文（text）：一张含表头的医疗器械 UDI 与出入库追溯台账（至少要有「${needAll.join('」「')}」这些列）`]);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient([`原文（text）：一张含表头的医疗器械 UDI 与出入库追溯台账（至少要有「${needAll.join('」「')}」这些列）`]);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的医疗器械 UDI 与出入库追溯台账（至少要能认出「${needAll.join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行器械出入库明细（现在只有表头或只有合计行，没有可核对的明细行）']);
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const rolesPresent = new Set(t.cols.filter((c) => c.role).map((c) => c.role));
  const findings = [];
  const notRun = [];
  const checksSkipped = [];

  for (const f of checkUdiCompleteness(t.items)) findings.push(f);
  for (const f of checkStockBalance(t.items)) findings.push(f);
  for (const f of checkExpiry(t.items)) findings.push(f);
  for (const f of checkDuplicateRegistration(t.items)) findings.push(f);
  for (const f of checkTotalsRow(t.totalsRow, t.totals)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items, rolesPresent)) findings.push(f);

  if (!t.totalsRow) {
    checksSkipped.push('合计行逐列复核（数量类列）：材料里没有「合计 / 总计」行，这一项没有可复核的对象');
  }
  if (!rolesPresent.has('status')) {
    checksSkipped.push('状态值非法检测：材料里没有「状态」列，这一项没有可检查的对象');
  }

  if (paid) {
    if (!rolesPresent.has('dest')) {
      checksSkipped.push('追溯链完整性：材料里没有「使用科室或患者去向」列，出库去向无法核对');
    }
    if (!rolesPresent.has('inDate')) {
      checksSkipped.push('效期与库龄：材料里没有「入库日期」列，库龄算不出来');
    }
    if (!rolesPresent.has('supplier')) {
      checksSkipped.push('同一批号跨库位/跨供应商：材料里没有「供应商」列，本次只能按库位判断，跨供应商未能核对');
    }
    for (const it of t.items) {
      for (const f of checkTraceChain(it, rolesPresent.has('dest'))) findings.push(f);
      for (const f of checkRegCertCoverage(it)) findings.push(f);
      for (const f of checkShelfAge(it)) findings.push(f);
    }
    for (const f of checkBatchCrossLocation(t.items)) findings.push(f);
    // 挂在解析结果对象上转交给下面（这样本包摘掉付费块后不留任何付费残留）
    t.consolidation = buildConsolidation(t.items, findings);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const openTotal = t.totals.openQty;
  const inTotal = t.totals.inQty;
  const outTotal = t.totals.outQty;
  const closeTotal = t.totals.closeQty;
  const expectClose = round2(openTotal + inTotal - outTotal);
  const balanceDiff = round2(closeTotal - expectClose);

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      qty_open_total: openTotal,
      qty_in_total: inTotal,
      qty_out_total: outTotal,
      qty_close_total: closeTotal,
      balance_diff_total: balanceDiff,
      basis: 'UDI 完整性按 UDI-DI 与 UDI-PI（批号或序列号、有效期至）逐行点名；'
        + '出入库按 期初库存 + 入库数量 − 出库数量 = 期末库存 逐行复算；'
        + '效期按 核对日期 ≤ 有效期至 判定，过期与临期 30 天内都给天数；'
        + '同一 UDI-DI + 同一批号在表内只应出现一次；合计行的数量类列必须等于明细逐列相加。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (checksSkipped.length) result.checks_skipped = checksSkipped;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、该点的列都点得到**，'
      + '不代表器械质量合格、UDI 与注册证真伪已经核验、或追溯记录满足具体法规条款 —— 那些不在本工具范围内。';
  }

  result.scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    checks_skipped: checksSkipped,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    totals_row_found: Boolean(t.totalsRow),
    qty_open_total: openTotal,
    qty_in_total: inTotal,
    qty_out_total: outTotal,
    qty_close_total: closeTotal,
    balance_diff_total: balanceDiff,
    expired_count: findings.filter((f) => f.category === '效期已过').length,
    near_expiry_count: findings.filter((f) => f.category === '效期临期（30 天内）').length,
  };

  if (paid) {
    result.consolidated = t.consolidation.by_dept_category;
    result.consolidated_actions = t.consolidation.actions;
    result.consolidated_total = t.consolidation.total;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
