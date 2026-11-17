#!/usr/bin/env node
/**
 * drug-cold-chain-check-full.js —— 药品冷链温控与出入库记录核对引擎（订阅版 / 买断版；确定性、纯 Node 标准库）。
 *
 * 真实痛点（药店 / 医药商业 / 疫苗点的质量管理员与药师，**每月**必做，GSP 与《药品经营质量管理规范》要求）：
 *   冷藏药品（2–8℃）、阴凉库（≤20℃）、冷冻（-20℃ 以下）在**收货、储存、运输**全程都要有温控记录：
 *   · 收货要记录运输温度与到货温度；
 *   · 储存要按小时/按次记录库温（按该设施的应记录频次记，缺一个时点就是「温控记录断档」）；
 *   · 冷链运输要有在途温度曲线；
 *   · **超温要有处理与评估记录**（谁处理的、什么时候处理的、评估结论是什么）。
 *   GSP 检查与药监飞行检查最常见的整改项，就是「温控记录断档」「超温没处理」「冷链药品与常温药品混放」。
 *   质量管理员/药师每月必须核：温控记录连续性、超温报警与处理闭环、冷链品种与储存条件匹配、出入库与库存勾稽。
 *
 * 本文件是**订阅版（买断版）**：在本包六项逐行核对之上，多出**超温处理闭环（含处理时长）、
 * 冷链与储存条件匹配、运输在途温度、超温批次追溯、分设施×分品种汇总清单**这五类能力。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定药品本身是否因超温而失效、不判定 GSP 认证或药监飞检的结论、不联网核验批号与药品追溯码、
 *          不读 .xlsx/.pdf 原件或温控仪原始曲线文件；材料不足**一律不给结论**。
 *
 * ⚠️ 免费包由 `tools/strip_free_engine.py` 从本文件摘出，所以这里只用**形态 B**：
 *    · 付费开关**只在入口 `run` 里声明一次**，付费检查一律包在同一个开关的 `if` 块里；
 *    · **不要**留「以下为订阅版才执行的检查」那类 MARKER —— 两种形态并存时摘除工具会走形态 A，
 *      把免费检查也整块删掉（本仓库第 236 轮踩过）；
 *    · 写注释时**不要复述开关那一行的源码**：摘除后的残渣断言是**纯字符串包含**判断，复述会被判「没删干净」。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '温控记录连续性（按 设施编号+记录日期 比对：按该设施的应记录频次点名缺失的时点，并点名整天没有记录的日期）',
  '温度区间合规（记录温度是否落在该设施要求下限~要求上限之间，超限给出偏差值与该行原文；上下限填颠倒了也报）',
  '出入库数量勾稽（逐品种逐批号：期初库存 + 入库数量 − 出库数量 = 期末库存；同一品种批号前后时点的结存也要接得上）',
  '同一设施同一时间点重复记录（设施编号+记录日期+记录时间+品种+批号 完全重复即点名）',
  '合计行逐列复核（表里有 合计/小计 行时：期初库存/入库数量/出库数量/期末库存 须逐列等于明细行之和）',
  '空白/占位符与格式检测（关键字段空白或占位符、温度非数字、温度列表头缺单位、记录日期时间格式非法、报警状态/设施类型取值非法、数量为负或无法解析）',
];

const CHECKS_WITHHELD = [
  '超温处理闭环（报警状态=超温 却缺处理人/处理日期/评估结论；温度已超限但报警状态没标超温；处理时长超过 24 小时时限）',
  '冷链与储存条件匹配（品种要求储存条件 与 所在设施类型 不一致，如冷藏药品放进阴凉库）',
  '运输在途温度（运输温度/到货温度 超出该设施要求区间，给出偏差值与连续超温时段时长）',
  '超温批次追溯（同一批号在超温时段有出入库记录 ⇒ 点名批号与数量，供召回判断）',
  '分设施×分品种汇总清单（按超温次数与最大偏差排序，给出可整改动作）—— 结果里的 consolidated_actions 就是这份清单',
];

const OUT_OF_SCOPE = [
  '判定药品本身是否因超温而失效（那是质量部门与药品检验的职责），本工具只核记录是否连续、是否超限、处理与评估字段是否闭环',
  '判定 GSP 认证是否通过、药监飞行检查是否合格（那是药品监督管理部门的认定权），本工具只按写明的口径核这张台账的字面一致性',
  '联网核对批号真伪、疫苗批签发信息或药品追溯码流向（本工具不联网）',
  '读取 .xlsx / .pdf 原件、温控仪原始曲线文件或冷链温度记录仪导出文件；材料不足一律不给结论',
];

// 样例：一张**干净**的冷链温控与出入库合并台账 —— 4 个设施（冷藏库/阴凉库/冷冻库/冷藏车）、
// 记录时点按各自应记录频次一个不缺、温度全在要求区间内、逐行勾稽与合计行都算得平、没有重复记录。
// 批号是编造格式（B2026-xxxx），不是任何真实批号；文内不含身份证号与统一社会信用代码。
const SAMPLE_TEXT = [
  '设施编号\t设施名称\t设施类型\t要求下限(℃)\t要求上限(℃)\t记录日期\t记录时间\t记录温度(℃)\t应记录频次\t品种\t品种要求储存条件\t批号\t期初库存\t入库数量\t出库数量\t期末库存\t报警状态\t报警时间\t处理人\t处理日期\t评估结论\t运输温度(℃)\t到货温度(℃)\t备注',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-01\t00:00\t4.2\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t120\t0\t0\t120\t正常\t-\t-\t-\t-\t-\t-\t月度起始结存',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-01\t06:00\t3.8\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t120\t0\t0\t120\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-01\t12:00\t5.6\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t120\t30\t0\t150\t正常\t-\t-\t-\t-\t-\t-\t当日入库30盒',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-01\t18:00\t4.9\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t150\t0\t0\t150\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-02\t00:00\t5.1\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t150\t0\t0\t150\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-02\t06:00\t4.4\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t150\t0\t20\t130\t正常\t-\t-\t-\t-\t-\t-\t出库20盒至门诊药房',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-02\t12:00\t6.0\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t130\t0\t0\t130\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LL-01\t冷藏库1号库\t冷藏库\t2\t8\t2026-04-02\t18:00\t3.6\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0413\t130\t0\t0\t130\t正常\t-\t-\t-\t-\t-\t-\t-',
  'YL-01\t阴凉库2号库\t阴凉库\t0\t20\t2026-04-01\t08:00\t17.5\t每日2次\t维生素C片\t阴凉(≤20℃)\tB2026-0388\t300\t0\t0\t300\t正常\t-\t-\t-\t-\t-\t-\t-',
  'YL-01\t阴凉库2号库\t阴凉库\t0\t20\t2026-04-01\t16:00\t19.2\t每日2次\t维生素C片\t阴凉(≤20℃)\tB2026-0388\t300\t100\t0\t400\t正常\t-\t-\t-\t-\t-\t-\t当日入库100瓶',
  'YL-01\t阴凉库2号库\t阴凉库\t0\t20\t2026-04-02\t08:00\t18.4\t每日2次\t维生素C片\t阴凉(≤20℃)\tB2026-0388\t400\t0\t50\t350\t正常\t-\t-\t-\t-\t-\t-\t出库50瓶',
  'YL-01\t阴凉库2号库\t阴凉库\t0\t20\t2026-04-02\t16:00\t16.8\t每日2次\t维生素C片\t阴凉(≤20℃)\tB2026-0388\t350\t0\t0\t350\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LD-01\t冷冻库3号库\t冷冻库\t-30\t-20\t2026-04-01\t09:00\t-24.5\t每日1次\t核酸检测试剂盒\t冷冻(-20℃以下)\tB2026-0521\t60\t0\t0\t60\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LD-01\t冷冻库3号库\t冷冻库\t-30\t-20\t2026-04-02\t09:00\t-22.8\t每日1次\t核酸检测试剂盒\t冷冻(-20℃以下)\tB2026-0521\t60\t0\t0\t60\t正常\t-\t-\t-\t-\t-\t-\t-',
  'LC-01\t冷藏车1号车\t冷藏车\t2\t8\t2026-04-02\t00:00\t4.5\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0414\t0\t40\t0\t40\t正常\t-\t-\t-\t-\t-\t-\t途中药店配送',
  'LC-01\t冷藏车1号车\t冷藏车\t2\t8\t2026-04-02\t06:00\t5.0\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0414\t40\t0\t0\t40\t正常\t-\t-\t-\t-\t4.8\t5.5\t在途温控记录',
  'LC-01\t冷藏车1号车\t冷藏车\t2\t8\t2026-04-02\t12:00\t6.2\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0414\t40\t0\t0\t40\t正常\t-\t-\t-\t-\t5.0\t6.2\t到货验收温控记录',
  'LC-01\t冷藏车1号车\t冷藏车\t2\t8\t2026-04-02\t18:00\t4.1\t每6小时\t重组人胰岛素注射液\t冷藏(2-8℃)\tB2026-0414\t40\t0\t0\t40\t正常\t-\t-\t-\t-\t-\t-\t-',
  '合计\t-\t-\t-\t-\t-\t-\t-\t-\t合计\t-\t-\t2660\t170\t70\t2760\t-\t-\t-\t-\t-\t-\t-\t明细行合计',
].join('\n');

const TOL = 0.01;

// 超温处理时限（小时）：超温报警到处理日期超过这个时长就点名
const HANDLE_LIMIT_HOURS = 24;

const FACILITY_TYPES = ['冷藏库', '阴凉库', '冷冻库', '冷藏车'];
const FACILITY_FREQ = { 冷藏库: '每6小时', 阴凉库: '每日2次', 冷冻库: '每日1次', 冷藏车: '每6小时' };

const ALARM_OK = ['正常', '未报警', '无', '无报警', '不报警'];
const ALARM_OVER = ['超温', '超温报警', '温度超标', '高温报警', '低温报警', '高低温报警', '超标'];
const ALARM_WARN = ['预警', '温度预警', '接近上限', '接近下限'];

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'facilityNo', 'facilityName', 'facilityType', 'tempMin', 'tempMax',
  'recordDate', 'recordTime', 'recordTemp',
  'variety', 'batchNo', 'openQty', 'inQty', 'outQty', 'closeQty', 'alarmStatus',
];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['facilityNo', '设施编号'],
  ['facilityName', '设施名称'],
  ['facilityType', '设施类型'],
  ['tempMin', '要求下限(℃)'],
  ['tempMax', '要求上限(℃)'],
  ['recordDate', '记录日期'],
  ['recordTime', '记录时间'],
  ['recordTemp', '记录温度(℃)'],
  ['variety', '品种'],
  ['batchNo', '批号'],
  ['openQty', '期初库存'],
  ['inQty', '入库数量'],
  ['outQty', '出库数量'],
  ['closeQty', '期末库存'],
  ['alarmStatus', '报警状态'],
];

// 温度类列（表头必须写单位；单元格值要能解析成数字）
const TEMP_ROLES = ['tempMin', 'tempMax', 'recordTemp', 'transportTemp', 'arrivalTemp'];

// 数量类列（不得为负、必须能解析）
const QTY_ROLES = [
  ['openQty', '期初库存'],
  ['inQty', '入库数量'],
  ['outQty', '出库数量'],
  ['closeQty', '期末库存'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表尤其注意：「品种要求储存条件」必须排在「品种」之前；「运输温度/到货温度」必须排在
//    带兜底关键词「温度」的「记录温度」之前；「报警时间」必须排在带兜底关键词「报警」的「报警状态」之前。
const ROLES = {
  facilityNo: ['设施编号', '库房编号', '设备编号', '设施代码', '设施编码'],
  facilityName: ['设施名称', '库房名称', '设备名称', '设施名'],
  facilityType: ['设施类型', '库房类型', '设备类型', '设施类别'],
  tempMin: ['要求下限', '温度下限', '下限温度', '最低温度', '下限'],
  tempMax: ['要求上限', '温度上限', '上限温度', '最高温度', '上限'],
  transportTemp: ['运输温度', '在途温度', '途中温度'],
  arrivalTemp: ['到货温度', '收货温度', '到货时温度'],
  recordTemp: ['记录温度', '实测温度', '监测温度', '库温', '温度'],
  recordDate: ['记录日期', '温控日期', '监测日期', '记录日'],
  recordTime: ['记录时间', '温控时间', '监测时间', '采集时间', '记录时刻'],
  recordFreq: ['应记录频次', '记录频次', '监测频次', '频次'],
  storageReq: ['品种要求储存条件', '要求储存条件', '储存条件', '储运条件', '存储条件'],
  variety: ['品种名称', '品种', '品名', '药品名称', '商品名称'],
  batchNo: ['批号', '生产批号', '批次号', '批次'],
  openQty: ['期初库存', '期初数量', '上期结存', '期初结存', '期初'],
  inQty: ['入库数量', '入库量', '入库数', '入库'],
  outQty: ['出库数量', '出库量', '出库数', '出库'],
  closeQty: ['期末库存', '期末数量', '本期结存', '期末结存', '期末'],
  alarmTime: ['报警时间', '报警时刻', '报警开始时间'],
  alarmStatus: ['报警状态', '报警标志', '超温状态', '温度状态', '报警'],
  handler: ['处理人', '处理人员', '处置人', '处理责任人'],
  handleDate: ['处理日期', '处置日期', '处理时间', '处置时间', '处理完成日期'],
  assessConc: ['评估结论', '评估结果', '处理结论', '处置结论'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  facilityNo: '设施编号',
  facilityName: '设施名称',
  facilityType: '设施类型',
  tempMin: '要求下限(℃)',
  tempMax: '要求上限(℃)',
  recordDate: '记录日期',
  recordTime: '记录时间',
  recordTemp: '记录温度(℃)',
  recordFreq: '应记录频次',
  variety: '品种',
  storageReq: '品种要求储存条件',
  batchNo: '批号',
  openQty: '期初库存',
  inQty: '入库数量',
  outQty: '出库数量',
  closeQty: '期末库存',
  alarmStatus: '报警状态',
  alarmTime: '报警时间',
  handler: '处理人',
  handleDate: '处理日期',
  assessConc: '评估结论',
  transportTemp: '运输温度(℃)',
  arrivalTemp: '到货温度(℃)',
  note: '备注',
};

const SUM_ROLES = ['openQty', 'inQty', 'outQty', 'closeQty'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「合规」，也不说「不合规」。',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
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

const pad2 = (n) => (n < 10 ? '0' + n : String(n));

/** 温度：允许 5.2 / 5.2℃ / 5.2°C / 25度 / -24.5，其余一律判「看不懂」 */
function normTemp(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim()
    .replace(/[℃°C摄氏氏度\s]/g, '')
    .replace(/[－—–]/g, '-');
  if (!s) return null;
  return normNumber(s);
}

/** 日期：2026-04-01 / 2026/4/1 / 2026.04.01 / 20260401 / 2026年4月1日 ⇒ 'YYYY-MM-DD' */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (!s) return null;
  let m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return `${y}-${pad2(mo)}-${pad2(d)}`;
}

/** 时间：09:00 / 9:00 / 09:00:00 / 2026-04-01 09:00 ⇒ 'HH:MM' */
function normTime(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (!s) return null;
  const parts = s.split(/\s+/);
  const tail = parts[parts.length - 1];
  const m = /^(\d{1,2})[:：时](\d{1,2})(?:[:：分]\d{1,2})?秒?$/.exec(tail);
  if (!m) return null;
  const h = Number(m[1]);
  const mi = Number(m[2]);
  if (h > 23 || mi > 59) return null;
  return `${pad2(h)}:${pad2(mi)}`;
}

/** 日期时间 ⇒ UTC 毫秒（用于算处理时长）；解析不了返回 null */
function parseDateTime(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (!s) return null;
  const dm = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?/.exec(s);
  if (!dm) return null;
  const y = Number(dm[1]);
  const mo = Number(dm[2]);
  const d = Number(dm[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  let h = 0;
  let mi = 0;
  const tm = /(\d{1,2})[:：](\d{1,2})/.exec(s.slice(dm[0].length));
  if (tm) {
    const hh = Number(tm[1]);
    const mm = Number(tm[2]);
    if (hh <= 23 && mm <= 59) { h = hh; mi = mm; }
  }
  return Date.UTC(y, mo - 1, d, h, mi);
}

function fmtDT(ms) {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())} `
    + `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`;
}

function dateToMs(d) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(d));
  if (!m) return null;
  return Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
}

function msToDate(ms) {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`;
}

/** 报警状态归一：ok / over / warn / illegal / blank */
function alarmStateOf(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (!s || /^[-—–]+$/.test(s)) return { state: 'blank', raw: s };
  if (ALARM_OVER.indexOf(s) >= 0) return { state: 'over', raw: s };
  if (ALARM_OK.indexOf(s) >= 0) return { state: 'ok', raw: s };
  if (ALARM_WARN.indexOf(s) >= 0) return { state: 'warn', raw: s };
  return { state: 'illegal', raw: s };
}

function facilityTypeOf(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (!s) return null;
  for (const t of FACILITY_TYPES) {
    if (s === t || s.indexOf(t) >= 0) return t;
  }
  return null;
}

/** 设施类型 ⇒ 应记录频次默认值（表里有「应记录频次」列时以列为准） */
function defaultFreq(raw) {
  const t = facilityTypeOf(raw);
  return t ? FACILITY_FREQ[t] : '';
}

function hourSlots(step) {
  const out = [];
  for (let h = 0; h < 24; h += step) out.push(`${pad2(h)}:00`);
  return out;
}

// 应记录频次 ⇒ 应记录的时点序列（顺序：更具体的写法排在前面）
const FREQ_PLANS = [
  { re: /每小时|每\s*1\s*小时|1\s*小时\s*1\s*次/, label: '每小时', slots: hourSlots(1) },
  { re: /每\s*2\s*小时/, label: '每2小时', slots: hourSlots(2) },
  { re: /每\s*3\s*小时/, label: '每3小时', slots: hourSlots(3) },
  { re: /每\s*4\s*小时/, label: '每4小时', slots: hourSlots(4) },
  { re: /每\s*6\s*小时/, label: '每6小时', slots: hourSlots(6) },
  { re: /每\s*8\s*小时/, label: '每8小时', slots: hourSlots(8) },
  { re: /每\s*12\s*小时/, label: '每12小时', slots: hourSlots(12) },
  { re: /每日\s*3\s*次|每天\s*3\s*次|每日三次/, label: '每日3次', slots: ['08:00', '14:00', '20:00'] },
  { re: /每日\s*2\s*次|每天\s*2\s*次|每日两次/, label: '每日2次', slots: ['08:00', '16:00'] },
  { re: /每日\s*1\s*次|每天\s*1\s*次|每日一次/, label: '每日1次', slots: ['09:00'] },
];

function freqPlan(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (!s) return null;
  for (const p of FREQ_PLANS) {
    if (p.re.test(s)) return { label: p.label, slots: p.slots.slice() };
  }
  return null;
}

function isTotalRow(it) {
  const v = [it.facilityNo, it.facilityName, it.variety]
    .map((x) => String(x === undefined || x === null ? '' : x).trim());
  return v.some((x) => x !== '' && x.indexOf('合计') >= 0);
}

function pick(list) {
  for (const v of list) {
    if (!isBlank(v)) return String(v).trim();
  }
  return '';
}

function facLabel(it) {
  const no = String(it.facilityNo === undefined || it.facilityNo === null ? '' : it.facilityNo).trim();
  const name = String(it.facilityName === undefined || it.facilityName === null ? '' : it.facilityName).trim();
  return [no, name].filter((x) => x && x !== '-').join(' ') || '未标注设施';
}

function who(it) {
  const d = String(it.recordDate === undefined || it.recordDate === null ? '' : it.recordDate).trim();
  const tm = String(it.recordTime === undefined || it.recordTime === null ? '' : it.recordTime).trim();
  const v = String(it.variety === undefined || it.variety === null ? '' : it.variety).trim();
  const b = String(it.batchNo === undefined || it.batchNo === null ? '' : it.batchNo).trim();
  return `第 ${it.line} 行「${facLabel(it)} ${d} ${tm}｜${v || '未标注品种'} ${b || '未标注批号'}」`;
}

function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    evidence: String(it.raw === undefined || it.raw === null ? '' : it.raw).trim(),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

function findingAt(line, level, category, evidence, message, advice) {
  const f = {
    level,
    category,
    line,
    evidence: String(evidence == null ? '' : evidence).trim(),
    message,
  };
  if (advice) f.advice = advice;
  return f;
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      if (isTotalRow(it)) return acc;             // 合计行不参与「明细合计」，否则会自己加自己
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function qty(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return String(v);
}

/* ============================ 本包检查（六项） ============================ */

/** 1. 温控记录连续性：按 设施编号+记录日期 → 按时点频次点名缺的时点，并点名整天没有记录的日期 */
function checkContinuity(items) {
  const out = [];
  const data = items.filter((it) => !isTotalRow(it));
  const byFac = new Map();
  for (const it of data) {
    const key = (String(it.facilityNo === undefined || it.facilityNo === null ? '' : it.facilityNo).trim())
      || (String(it.facilityName === undefined || it.facilityName === null ? '' : it.facilityName).trim());
    if (!key) continue;                            // 交给「关键字段缺失」
    if (!byFac.has(key)) byFac.set(key, []);
    byFac.get(key).push(it);
  }
  for (const [, rows] of byFac) {
    const first = rows[0];
    const freqFromCol = pick(rows.map((r) => r.recordFreq));
    const freq = freqFromCol || defaultFreq(first.facilityType);
    const freqNote = freqFromCol
      ? `应记录频次「${freqFromCol}」`
      : `表里没填应记录频次，按「${String(first.facilityType).trim() || '未标注设施类型'}」的默认口径按${freq || '每日1次'}`;
    const plan = freqPlan(freq);

    const byDate = new Map();
    for (const r of rows) {
      const d = normDate(r.recordDate);
      if (!d) continue;                            // 交给「日期时间格式」那一项
      if (!byDate.has(d)) byDate.set(d, []);
      byDate.get(d).push(r);
    }
    const dateList = [...byDate.keys()].sort();

    if (dateList.length >= 2) {
      const startMs = dateToMs(dateList[0]);
      const endMs = dateToMs(dateList[dateList.length - 1]);
      const gaps = [];
      if (startMs !== null && endMs !== null) {
        let guard = 0;
        for (let ms = startMs; ms <= endMs && guard < 400; ms += 86400000, guard += 1) {
          const d = msToDate(ms);
          if (!byDate.has(d)) gaps.push(d);
        }
      }
      if (gaps.length) {
        const shown = gaps.slice(0, 12).join('、');
        out.push(finding('P1', '温控记录连续性缺记录', first, undefined,
          `${facLabel(first)}：${dateList[0]} 至 ${dateList[dateList.length - 1]} 之间，`
          + `${shown}${gaps.length > 12 ? ` 等 ${gaps.length} 天` : ''} 这 ${gaps.length} 天**一条温控记录都没有**`
          + `（${freqNote}）。该设施本期共 ${rows.length} 行记录，最早一行是第 ${first.line} 行。`,
          '温控记录断档是 GSP 飞检最常见的整改项。先把断档日期的温控仪原始记录找出来补档；'
          + '确实没有记录的，要在「备注」里写明原因与当时的替代措施，不要事后手写补记一个数字。'));
      }
    }

    if (!plan) continue;
    for (const d of dateList) {
      const dayRows = byDate.get(d);
      const got = new Set();
      for (const r of dayRows) {
        const tt = normTime(r.recordTime);
        if (tt) got.add(tt);
      }
      const miss = plan.slots.filter((s) => !got.has(s));
      if (!miss.length) continue;
      const lines = dayRows.map((r) => r.line).join('、');
      out.push(finding('P1', '温控记录连续性缺记录', dayRows[0], undefined,
        `${facLabel(first)} 在 ${d}：${freqNote} ⇒ 应有 ${plan.slots.length} 个记录时点（${plan.slots.join(' / ')}），`
        + `实际只有 ${got.size} 个（${[...got].sort().join(' / ') || '无'}），缺 ${miss.join('、')}`
        + `（当天行号：第 ${lines} 行）。`,
        '按该设施已批准的温控监测频次补齐缺的时点；冷藏库/冷藏车通常是自动监测每 5 分钟一次，'
        + '手工台账至少要把批准频次的时点记全，否则检查员会直接判「记录不连续」。'));
    }
  }
  return out;
}

/** 2. 温度区间合规：记录温度须落在要求下限~要求上限内；上下限填颠倒也报 */
function checkTempRange(items) {
  const out = [];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const t = normTemp(it.recordTemp);
    const min = normTemp(it.tempMin);
    const max = normTemp(it.tempMax);
    if (min !== null && max !== null && min > max + TOL) {
      out.push(finding('P0', '要求上下限填写颠倒', it, round2(min - max),
        `${who(it)}：要求下限 ${min}℃ 大于要求上限 ${max}℃ —— 上下限填颠倒了，这一行的区间判断没法做。`,
        '把要求下限/上限按该设施（或该品种）批准的温度区间重新填：冷藏库 2~8℃、阴凉库 0~20℃、'
        + '冷冻库 -30~-20℃ 这一类。填颠倒时本工具不猜你想表达什么，也不会硬套一个区间。'));
      continue;                                    // 颠倒时不做区间比较，避免一条错填报出两条
    }
    if (t === null || min === null || max === null) continue;   // 交给「温度无法解析 / 关键字段缺失」
    if (t >= min - TOL && t <= max + TOL) continue;
    const dev = round2(t < min ? t - min : t - max);
    out.push(finding('P0', '温度超出要求区间', it, dev,
      `${who(it)}：记录温度 ${t}℃ 超出要求区间 ${min}~${max}℃，偏差 ${dev > 0 ? '+' : ''}${dev}℃`
      + `（${t < min ? '低于下限' : '高于上限'}）。`,
      '先确认这不是抄错行；确认超温后必须走超温处理流程（隔离、评估、记录处理人与评估结论）。'
      + '本工具只报出偏差，不判断这批药能不能继续用。'));
  }
  return out;
}

/** 3. 出入库数量勾稽：逐行 期初+入−出=期末，且同品种同批号前后时点结存要接得上 */
function checkInOutBalance(items) {
  const out = [];
  const data = items.filter((it) => !isTotalRow(it));

  for (const it of data) {
    const o = normNumber(it.openQty);
    const i = normNumber(it.inQty);
    const u = normNumber(it.outQty);
    const c = normNumber(it.closeQty);
    if (o === null || i === null || u === null || c === null) continue;  // 交给「数量为负或无法解析」
    const diff = round2(o + i - u - c);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P0', '出入库数量不勾稽', it, diff,
      `${who(it)}：期初库存 ${qty(o)} + 入库数量 ${qty(i)} − 出库数量 ${qty(u)} = ${qty(round2(o + i - u))}，`
      + `但期末库存写的是 ${qty(c)}，差 ${qty(diff)}。`,
      '按批号把这一笔的入库单/出库单找出来对一遍：少记一张出库单、把赠品入库漏记、'
      + '或者期末库存是照上一行抄的，都会造成这个差额。'));
  }

  // 同一设施 + 同一品种 + 同一批号：上一时点的期末库存要等于本时点的期初库存
  const chain = new Map();
  for (const it of data) {
    const key = [
      String(it.facilityNo == null ? '' : it.facilityNo).trim(),
      String(it.variety == null ? '' : it.variety).trim(),
      String(it.batchNo == null ? '' : it.batchNo).trim(),
    ].join('|');
    if (key === '||') continue;
    if (!chain.has(key)) chain.set(key, []);
    chain.get(key).push(it);
  }
  for (const [, rows] of chain) {
    const sorted = rows.slice().sort((a, b) => {
      const da = normDate(a.recordDate) || '9999-99-99';
      const db = normDate(b.recordDate) || '9999-99-99';
      if (da !== db) return da < db ? -1 : 1;
      const ta = normTime(a.recordTime) || '99:99';
      const tb = normTime(b.recordTime) || '99:99';
      if (ta !== tb) return ta < tb ? -1 : 1;
      return a.line - b.line;
    });
    for (let k = 1; k < sorted.length; k += 1) {
      const prev = sorted[k - 1];
      const cur = sorted[k];
      const pc = normNumber(prev.closeQty);
      const co = normNumber(cur.openQty);
      if (pc === null || co === null) continue;
      const diff = round2(co - pc);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '出入库数量不勾稽', cur, diff,
        `${who(cur)}：同一设施同一品种同一批号的上一个时点是第 ${prev.line} 行（`
        + `${String(prev.recordDate).trim()} ${String(prev.recordTime).trim()}），那一行期末库存 ${qty(pc)}，`
        + `本行期初库存却是 ${qty(co)}，差 ${qty(diff)}。`,
        '逐时点接不上的结存，说明中间有未记录的出入库或抄错了行；'
        + '把这段时点的出入库单据补齐，或确认每次记录都抄的是同一个时点的账面结存。'));
    }
  }
  return out;
}

/** 4. 同一设施同一时间点重复记录 */
function checkDuplicateRecords(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const key = [
      String(it.facilityNo == null ? '' : it.facilityNo).trim(),
      String(it.recordDate == null ? '' : it.recordDate).trim(),
      normTime(it.recordTime) || String(it.recordTime == null ? '' : it.recordTime).trim(),
      String(it.variety == null ? '' : it.variety).trim(),
      String(it.batchNo == null ? '' : it.batchNo).trim(),
    ].join('|');
    if (key.replace(/\|/g, '') === '') continue;
    if (!seen.has(key)) { seen.set(key, it.line); continue; }
    out.push(finding('P1', '同一设施同一时点重复记录', it, undefined,
      `${who(it)}：设施编号+记录日期+记录时间+品种+批号 与第 ${seen.get(key)} 行**完全重复**。`,
      '同一时点同一批号只应有一条记录；确属两个时点写成了同一时间，请把时间改准；'
      + '确属重复登记，删掉多余那条 —— 重复记录会让连续性统计看起来「时点记全了」。'));
  }
  return out;
}

/** 5. 合计行逐列复核（数量类列） */
function checkTotalRow(items) {
  const out = [];
  const totals = items.filter((it) => isTotalRow(it));
  if (!totals.length) return out;
  const data = items.filter((it) => !isTotalRow(it));
  for (const tr of totals) {
    for (const role of SUM_ROLES) {
      const shown = normNumber(tr[role]);
      if (shown === null) continue;                // 合计行这列没填就不核这一列
      const sum = round2(data.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(shown - sum);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P0', '合计行复核不符', tr, diff,
        `第 ${tr.line} 行（${String(tr.facilityNo).trim()}/${String(tr.variety).trim()}）：`
        + `「${LABELS[role]}」合计写的是 ${qty(shown)}，明细行 ${data.length} 行逐行相加是 ${qty(sum)}，差 ${qty(diff)}。`,
        '合计行通常在 Excel 里是公式，被人手工改过之后就不会再重算；'
        + '重算这一列并确认合计行覆盖的明细范围（有没有把别的库房/别的月份的明细也算进去）。'));
    }
  }
  return out;
}

/** 6. 空白/占位符与格式检测 */
function checkFieldIntegrity(items, t) {
  const out = [];

  // 6.1 温度列表头必须带单位
  for (const c of t.cols) {
    if (!c.role || TEMP_ROLES.indexOf(c.role) < 0) continue;
    const h = String(c.header == null ? '' : c.header);
    if (/[℃°]|摄氏|华氏/.test(h)) continue;
    out.push(findingAt(1, 'P2', '温度列缺单位', h,
      `第 1 行表头「${h}」是温度列却没有写单位 —— 没有单位时「2~8」到底是摄氏度还是华氏度无法判定。`,
      `把表头写成「${LABELS[c.role] || '记录温度(℃)'}」这种带 ℃ 的形式；下限/上限、运输温度、到货温度同理。`));
  }

  for (const it of items) {
    if (isTotalRow(it)) continue;                  // 合计行不参与逐行字段检查

    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const role of ['tempMin', 'tempMax', 'recordTemp']) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normTemp(raw) === null) {
        out.push(finding('P1', '温度无法解析', it, undefined,
          `${who(it)}：「${LABELS[role]}」的值「${String(raw).trim()}」不是可识别的温度`
          + '（只认数字，可带 ℃ / °C / 度）。',
          '把温度改成纯数字形态（如 5.2 或 -24.5）再跑；'
          + '本工具不会把看不懂的值当成 0，也不会当成「没超温」。'));
      }
    }

    if (!isBlank(it.recordDate) && normDate(it.recordDate) === null) {
      out.push(finding('P1', '记录日期时间格式异常', it, undefined,
        `${who(it)}：「记录日期」的值「${String(it.recordDate).trim()}」不是可识别的日期`
        + '（认 2026-04-01 / 2026/4/1 / 2026.04.01 / 20260401）。',
        '统一用 YYYY-MM-DD 写日期；日期写成「4月1日」这类写法时，跨月跨年的连续性核对会直接失效。'));
    }
    if (!isBlank(it.recordTime) && normTime(it.recordTime) === null) {
      out.push(finding('P1', '记录日期时间格式异常', it, undefined,
        `${who(it)}：「记录时间」的值「${String(it.recordTime).trim()}」不是可识别的时间（认 HH:MM，24 小时制）。`,
        '把时间统一写成 24 小时制的 HH:MM（如 06:00）；写成「上午6点」或 25:00 这类值，时点连续性就核不了。'));
    }

    const alarm = alarmStateOf(it.alarmStatus);
    if (alarm.state === 'illegal') {
      out.push(finding('P1', '状态值非法', it, undefined,
        `${who(it)}：「报警状态」的值「${alarm.raw}」不是可识别的状态`
        + `（认 ${ALARM_OK.concat(ALARM_OVER, ALARM_WARN).join(' / ')}）。`,
        '报警状态是全表最重要的一列：超温了却没标「超温」，超温处理闭环这一项就永远查不出来。'
        + '按实际记录写「正常」或「超温」。'));
    }
    if (!isBlank(it.facilityType) && facilityTypeOf(it.facilityType) === null) {
      out.push(finding('P1', '状态值非法', it, undefined,
        `${who(it)}：「设施类型」的值「${String(it.facilityType).trim()}」不是可识别的类型`
        + `（认 ${FACILITY_TYPES.join(' / ')}）。`,
        '设施类型决定了要求温度区间与应记录频次，也决定了冷链品种能不能放进来；'
        + '按实际写成 冷藏库 / 阴凉库 / 冷冻库 / 冷藏车 之一。'));
    }

    for (const [role, label] of QTY_ROLES) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数量为负或无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数量（只认数字，可带千分位）。`,
          '把数量改成纯数字形态再跑；本工具不会把看不懂的值当成 0 —— 当成 0 会把勾稽「算平」。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数量为负或无法解析', it, n,
          `${who(it)}：「${label}」是负数（${qty(n)}）—— 库存类台账里出现负数，通常是出入库方向填反了，`
          + '或者把红字冲销直接写进了数量列。',
          '确认是红字冲销还是方向填反；确属冲销的请在「备注」写明并保留原始单据编号，别直接改成正数把账做平。'));
      }
    }
  }
  return out;
}

/* ============================ 订阅版检查 ============================ */

/** 付费：该行是否处于超温状态，以及最大偏差（记录温度 / 报警状态 / 运输与到货温度） */
function overTempInfo(it, ctx) {
  if (isTotalRow(it)) return { over: false, dev: 0, why: '' };
  const temp = normTemp(it.recordTemp);
  const min = normTemp(it.tempMin);
  const max = normTemp(it.tempMax);
  const alarm = alarmStateOf(it.alarmStatus);
  const reasons = [];
  let dev = 0;
  const inRange = min !== null && max !== null && min <= max + TOL;
  if (temp !== null && inRange) {
    if (temp < min - TOL) {
      dev = round2(temp - min);
      reasons.push(`记录温度 ${temp}℃ 低于要求下限 ${min}℃（偏差 ${dev}℃）`);
    } else if (temp > max + TOL) {
      dev = round2(temp - max);
      reasons.push(`记录温度 ${temp}℃ 高于要求上限 ${max}℃（偏差 +${dev}℃）`);
    }
  }
  if (alarm.state === 'over') reasons.push(`报警状态「${alarm.raw}」`);
  if (ctx && ctx.hasTransport && inRange) {
    const pairs = [['运输温度', normTemp(it.transportTemp)], ['到货温度', normTemp(it.arrivalTemp)]];
    for (const [label, v] of pairs) {
      if (v === null) continue;
      if (v < min - TOL) {
        const d = round2(v - min);
        if (Math.abs(d) > Math.abs(dev)) dev = d;
        reasons.push(`${label} ${v}℃ 低于要求下限 ${min}℃（偏差 ${d}℃）`);
      } else if (v > max + TOL) {
        const d = round2(v - max);
        if (Math.abs(d) > Math.abs(dev)) dev = d;
        reasons.push(`${label} ${v}℃ 高于要求上限 ${max}℃（偏差 +${d}℃）`);
      }
    }
  }
  return { over: reasons.length > 0, dev, why: reasons.join('；') };
}

/** 付费：算「品种要求储存条件」的类别（冷冻 / 阴凉 / 冷藏 / 常温） */
function storageToken(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (!s) return null;
  if (s.indexOf('冷冻') >= 0 || s.indexOf('冰冻') >= 0) return '冷冻';
  if (s.indexOf('阴凉') >= 0) return '阴凉';
  if (s.indexOf('冷藏') >= 0 || s.indexOf('冷处') >= 0
    || s.indexOf('2-8') >= 0 || s.indexOf('2~8') >= 0) return '冷藏';
  if (s.indexOf('常温') >= 0 || s.indexOf('室温') >= 0) return '常温';
  return null;
}

/** 付费：设施类型 ⇒ 能接受的储存条件类别（冷藏车按冷藏算） */
function facilityStorageToken(raw) {
  const t = facilityTypeOf(raw);
  if (!t) return null;
  if (t === '冷藏库' || t === '冷藏车') return '冷藏';
  if (t === '阴凉库') return '阴凉';
  if (t === '冷冻库') return '冷冻';
  return null;
}

/** 付费 ①：超温处理闭环（缺处理人/处理日期/评估结论、超温未报警、处理时长超时限） */
function checkOverTempClosure(it, ctx) {
  if (isTotalRow(it)) return [];
  const out = [];
  const alarm = alarmStateOf(it.alarmStatus);
  const info = overTempInfo(it, ctx);

  // 闭环针对的是**库温/储存温度**超限：在途温度超限由「运输在途温度」那一项单独报，不在这里重复报
  const temp = normTemp(it.recordTemp);
  const min = normTemp(it.tempMin);
  const max = normTemp(it.tempMax);
  let storeDev = 0;
  let storeWhy = '';
  if (temp !== null && min !== null && max !== null && min <= max + TOL) {
    if (temp < min - TOL) {
      storeDev = round2(temp - min);
      storeWhy = `记录温度 ${temp}℃ 低于要求下限 ${min}℃（偏差 ${storeDev}℃）`;
    } else if (temp > max + TOL) {
      storeDev = round2(temp - max);
      storeWhy = `记录温度 ${temp}℃ 高于要求上限 ${max}℃（偏差 +${storeDev}℃）`;
    }
  }

  if (alarm.state === 'over') {
    const miss = [];
    if (isBlank(it.handler)) miss.push('处理人');
    if (isBlank(it.handleDate)) miss.push('处理日期');
    if (isBlank(it.assessConc)) miss.push('评估结论');
    if (miss.length) {
      out.push(finding('P0', '超温处理未闭环', it, (storeDev || info.dev) || undefined,
        `${who(it)}：报警状态「${alarm.raw}」，但 ${miss.join('、')} 是空的`
        + `（本行超温依据：${storeWhy || '报警状态标注为超温'}）—— 超温处理没有闭环。`,
        '超温处理闭环至少要留下三样东西：谁处理的、什么时候处理的、评估结论是什么（能否继续销售使用）。'
        + 'GSP 飞检看的就是这三样；只有一行「超温」而没有处理记录，等于没处理。'));
    }
    const startRaw = String(it.alarmTime == null ? '' : it.alarmTime).trim();
    const endRaw = String(it.handleDate == null ? '' : it.handleDate).trim();
    const start = parseDateTime(startRaw);
    let end = parseDateTime(endRaw);
    // ⚠️ 处理日期通常只写到「日」（没有时分）⇒ 按**当日结束**算：
    //    否则「04-01 09:00 报警、04-01 处理」会被算成 −9 小时，当天处理反而报「时间顺序倒了」。
    if (end !== null && !/\d{1,2}[:：]\d{1,2}/.test(endRaw)) end += (23 * 3600000 + 59 * 60000);
    if (start !== null && end !== null) {
      const hours = round2((end - start) / 3600000);
      if (hours > HANDLE_LIMIT_HOURS) {
        out.push(finding('P1', '超温处理未闭环', it, undefined,
          `${who(it)}：超温报警发生在 ${fmtDT(start)}，处理日期是 ${fmtDT(end)}，处理时长约 ${hours} 小时，`
          + `超过 ${HANDLE_LIMIT_HOURS} 小时时限。`,
          '超温后药品要**立即**隔离并挂暂停销售标识，处理与评估不能拖到第二天甚至下周；'
          + '时限按本企业质量文件规定的时限填，本工具用的是 24 小时这条通用口径。'));
      } else if (hours < 0) {
        out.push(finding('P1', '超温处理未闭环', it, undefined,
          `${who(it)}：报警时间 ${fmtDT(start)} 晚于处理日期 ${fmtDT(end)} —— 处理记录的时间顺序倒了。`,
          '处理日期不可能早于报警时间；先确认报警时间是不是抄了下一次的，或处理日期写错月份。'));
      }
    }
  } else if (storeWhy) {
    out.push(finding('P0', '超温处理未闭环', it, storeDev,
      `${who(it)}：温度已经不在要求区间内（${storeWhy}），但报警状态写的是「${alarm.raw || '(空)'}」`
      + '—— 超温没有报警，报警与处理链在这里就断了。',
      '温控仪报警后必须人工在台账上把报警状态标出来，否则「超温处理闭环」这一项在台账上永远是空白。'
      + '先查温控仪的报警记录，确认是漏标还是设备没报警。'));
  }
  return out;
}

/** 付费 ②：冷链与储存条件匹配（品种要求储存条件 vs 所在设施类型） */
function checkStorageMatch(it, ctx) {
  if (isTotalRow(it)) return [];
  if (!ctx || !ctx.hasStorageReq) return [];
  const need = storageToken(it.storageReq);
  const can = facilityStorageToken(it.facilityType);
  if (!need || !can) return [];
  if (need === can) return [];
  if (need === '常温') {
    return [finding('P2', '冷链储存条件不匹配', it, undefined,
      `${who(it)}：「${String(it.storageReq).trim()}」标注为常温品种，却放在${String(it.facilityType).trim()}里`
      + '—— 常温品种长期占用冷链库位，会挤占真正的冷链库容。',
      '把常温品种移出冷链库位；冷链库位紧张时优先保证 2~8℃ 冷藏药品与疫苗。')];
  }
  return [finding('P0', '冷链储存条件不匹配', it, undefined,
    `${who(it)}：品种要求储存条件是「${String(it.storageReq).trim()}」（按 ${need} 口径），`
    + `但所在设施类型是「${String(it.facilityType).trim()}」（只能按 ${can} 口径储存）—— 冷链药品与储存条件不匹配。`,
    '「冷链药品与常温药品混放」是 GSP 飞检最常见的整改项之一。先把该批号移到匹配的库区/设备，'
    + '再核这段混放时间的记录是否完整；混放期间的温度记录要单独归档备查。')];
}

/** 付费 ③：运输在途温度（运输温度 / 到货温度 超限，给偏差值与连续超温时段时长） */
function checkTransportExcursion(items, ctx) {
  const out = [];
  if (!ctx || !ctx.hasTransport) return out;
  const groups = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const t1 = normTemp(it.transportTemp);
    const t2 = normTemp(it.arrivalTemp);
    if (t1 === null && t2 === null) continue;             // 这一行没有运输/到货温度记录，不核
    const min = normTemp(it.tempMin);
    const max = normTemp(it.tempMax);
    if (min === null || max === null || min > max + TOL) continue;
    const bad = [];
    for (const pair of [['运输温度', t1], ['到货温度', t2]]) {
      const label = pair[0];
      const v = pair[1];
      if (v === null) continue;
      if (v < min - TOL) bad.push({ label, v, dev: round2(v - min) });
      else if (v > max + TOL) bad.push({ label, v, dev: round2(v - max) });
    }
    if (t1 === null || t2 === null) {
      const which = t1 === null ? '运输温度(℃)' : '到货温度(℃)';
      out.push(finding('P1', '运输在途温度超限', it, undefined,
        `${who(it)}：这一行填了冷链运输温控记录，但「${which}」是空的 —— 收货环节的温度记录不完整。`,
        '冷链药品收货必须同时记录**运输温度**与**到货温度**，两者缺一都不能证明在途温控达标；'
        + '把运输温度记录仪（或随货温度计）上的读数补全。'));
    }
    if (!bad.length) continue;
    const key = `${String(it.facilityNo).trim()}|${String(it.batchNo).trim()}`;
    if (!groups.has(key)) groups.set(key, { first: it, items: [] });
    groups.get(key).items.push({ it, bad });
  }

  for (const [, g] of groups) {
    const first = g.first;
    const min = normTemp(first.tempMin);
    const max = normTemp(first.tempMax);
    let dev = 0;
    const parts = [];
    const times = [];
    for (const rec of g.items) {
      for (const b of rec.bad) {
        parts.push(`${b.label} ${b.v}℃（偏差 ${b.dev > 0 ? '+' : ''}${b.dev}℃）`);
        if (Math.abs(b.dev) > Math.abs(dev)) dev = b.dev;
      }
      const ms = parseDateTime(`${String(rec.it.recordDate).trim()} ${String(rec.it.recordTime).trim()}`);
      if (ms !== null) times.push(ms);
    }
    let span = '';
    if (times.length >= 2) {
      const sorted = times.slice().sort((a, b) => a - b);
      const hours = round2((sorted[sorted.length - 1] - sorted[0]) / 3600000);
      span = `；连续超温时段 ${fmtDT(sorted[0])} 至 ${fmtDT(sorted[sorted.length - 1])}，约 ${hours} 小时`;
    } else if (times.length === 1) {
      span = `；本行记录时点 ${fmtDT(times[0])}（只有这一个时点有记录，连续时长无法计算，需补在途温度曲线）`;
    }
    out.push(finding('P0', '运输在途温度超限', first, dev,
      `${who(first)}：批号「${String(first.batchNo).trim()}」的在途/到货温度超出要求区间 ${min}~${max}℃`
      + ` —— ${parts.join('、')}${span}。`,
      '冷链运输超温要按超温药品流程处理：先看运输温度记录仪的完整曲线确认超温持续时间，'
      + '再评估该批号能否继续使用并留书面结论；只有单个到货温度没有在途曲线时，要补记录仪导出文件。'));
  }
  return out;
}

/** 付费 ④：超温批次追溯（超温时段有出入库 ⇒ 点名批号与数量，供召回判断） */
function checkExcursionTrace(items, ctx) {
  const out = [];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const info = overTempInfo(it, ctx);
    if (!info.over) continue;
    const inQ = normNumber(it.inQty);
    const outQ = normNumber(it.outQty);
    const moved = (inQ !== null && inQ > 0) || (outQ !== null && outQ > 0);
    if (!moved) continue;
    const b = String(it.batchNo == null ? '' : it.batchNo).trim() || '(未填批号)';
    out.push(finding('P0', '超温批次出入库追溯', it, info.dev || undefined,
      `${who(it)}：批号「${b}」在超温时段发生了出入库 —— 入库数量 ${qty(inQ)}、出库数量 ${qty(outQ)}`
      + `（超温依据：${info.why || '报警状态标注为超温'}）。`,
      '这一步是**召回判断的输入**：超温时段有出库的批号，要顺着批号追到下游客户/门店/使用单位，'
      + '并核对这段时点在库与已发出的数量；只在库超温没出库的，隔离并做评估即可。'
      + '本工具只点名批号与数量，不判定该批号是否需要召回。'));
  }
  return out;
}

/** 付费 ⑤-a：分设施 × 分品种汇总 */
function buildFacilityVarietyRollup(items, ctx) {
  const map = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const no = String(it.facilityNo == null ? '' : it.facilityNo).trim();
    const name = String(it.facilityName == null ? '' : it.facilityName).trim();
    const variety = String(it.variety == null ? '' : it.variety).trim();
    const key = `${no}|${variety}`;
    if (!map.has(key)) {
      map.set(key, {
        facility_no: no,
        facility_name: name,
        facility_type: String(it.facilityType == null ? '' : it.facilityType).trim(),
        variety,
        rows: 0,
        over_count: 0,
        max_dev: 0,
        in_qty: 0,
        out_qty: 0,
      });
    }
    const b = map.get(key);
    b.rows += 1;
    b.in_qty = round2(b.in_qty + num(it, 'inQty'));
    b.out_qty = round2(b.out_qty + num(it, 'outQty'));
    const info = overTempInfo(it, ctx);
    if (info.over) {
      b.over_count += 1;
      if (Math.abs(info.dev) > Math.abs(b.max_dev)) b.max_dev = info.dev;
    }
  }
  const list = [...map.values()].sort((a, b) => (b.over_count - a.over_count)
    || (Math.abs(b.max_dev) - Math.abs(a.max_dev))
    || String(a.facility_no).localeCompare(String(b.facility_no))
    || String(a.variety).localeCompare(String(b.variety)));
  const total = list.reduce((acc, r) => {
    acc.facility_variety_pairs += 1;
    acc.rows += r.rows;
    acc.over_count += r.over_count;
    if (Math.abs(r.max_dev) > Math.abs(acc.max_dev)) acc.max_dev = r.max_dev;
    acc.in_qty = round2(acc.in_qty + r.in_qty);
    acc.out_qty = round2(acc.out_qty + r.out_qty);
    return acc;
  }, { facility_variety_pairs: 0, rows: 0, over_count: 0, max_dev: 0, in_qty: 0, out_qty: 0 });
  return { by_facility_variety: list, total };
}

/** 付费 ⑤-b：按超温次数与最大偏差排序的可整改清单 */
function buildConsolidatedActions(rollup) {
  if (!rollup || !Array.isArray(rollup.by_facility_variety)) return [];
  return rollup.by_facility_variety
    .filter((r) => r.over_count > 0 || Math.abs(r.max_dev) > TOL)
    .map((r, i) => ({
      seq: i + 1,
      facility_no: r.facility_no,
      facility_name: r.facility_name,
      variety: r.variety,
      over_count: r.over_count,
      max_dev: r.max_dev,
      abs_dev: round2(Math.abs(r.max_dev)),
      in_qty: r.in_qty,
      out_qty: r.out_qty,
      action: `${r.facility_name || r.facility_no} 的「${r.variety}」本期超温 ${r.over_count} 次、`
        + `最大偏差 ${r.max_dev}℃：先调这两个时点的温控仪原始曲线确认超温持续多久，`
        + '再核该批号是否已按超温药品流程隔离并留下书面评估结论；'
        + '记录缺口的时点用温控仪原始打印小票补档，不要事后手写补记一个「看着正常」的数字。',
    }));
}

/** 付费：看这次的材料里有没有付费检查需要的那几列（没有就说清楚哪一项没跑，而不是假装跑过） */
function buildPaidContext(items, t) {
  const has = (role) => t.cols.some((c) => c.role === role);
  const hasAnyValue = (role) => items.some((it) => !isTotalRow(it) && !isBlank(it[role]));
  const ctx = {
    hasStorageReq: has('storageReq') && hasAnyValue('storageReq'),
    hasTransport: (has('transportTemp') || has('arrivalTemp'))
      && (hasAnyValue('transportTemp') || hasAnyValue('arrivalTemp')),
    hasHandler: has('handler') || has('handleDate') || has('assessConc'),
    hasAlarmTime: has('alarmTime'),
  };
  const missing = [];
  if (!ctx.hasStorageReq) missing.push(`${LABELS.storageReq}（冷链与储存条件匹配需要这一列）`);
  if (!ctx.hasHandler) missing.push(`${LABELS.handler}/${LABELS.handleDate}/${LABELS.assessConc}（超温处理闭环需要这三列）`);
  if (!ctx.hasAlarmTime) missing.push(`${LABELS.alarmTime}（超温处理时长需要这一列）`);
  if (!ctx.hasTransport) missing.push(`${LABELS.transportTemp}/${LABELS.arrivalTemp}（运输在途温度核对需要这两列）`);
  ctx.missing = missing;
  return ctx;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的药品冷链温控与出入库记录台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的药品冷链温控与出入库记录台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的药品冷链温控与出入库记录台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行温控/出入库明细（现在只有表头，没有可核对的明细行）']);
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const findings = [];
  const notRun = [];
  const dataRows = t.items.filter((it) => !isTotalRow(it));

  for (const f of checkContinuity(t.items)) findings.push(f);
  for (const f of checkTempRange(t.items)) findings.push(f);
  for (const f of checkInOutBalance(t.items)) findings.push(f);
  for (const f of checkDuplicateRecords(t.items)) findings.push(f);
  for (const f of checkTotalRow(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items, t)) findings.push(f);

  let rollup = null;
  let actions = null;
  const paidContext = buildPaidContext(t.items, t);
  if (paid) {
    for (const it of t.items) {
      for (const f of checkOverTempClosure(it, paidContext)) findings.push(f);
      for (const f of checkStorageMatch(it, paidContext)) findings.push(f);
    }
    for (const f of checkTransportExcursion(t.items, paidContext)) findings.push(f);
    for (const f of checkExcursionTrace(t.items, paidContext)) findings.push(f);
    rollup = buildFacilityVarietyRollup(t.items, paidContext);
    actions = buildConsolidatedActions(rollup);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const balances = round2(
    (t.totals.openQty || 0) + (t.totals.inQty || 0) - (t.totals.outQty || 0) - (t.totals.closeQty || 0),
  );
  const result = {
    findings,
    summary: {
      rows: t.items.length,
      data_rows: dataRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      open_total: t.totals.openQty,
      in_total: t.totals.inQty,
      out_total: t.totals.outQty,
      close_total: t.totals.closeQty,
      balance_diff: balances,
      basis: '温控记录按 设施编号+记录日期 比对，时点按该设施的应记录频次（或设施类型默认口径）核对；'
        + '记录温度须落在该设施要求下限~要求上限之间；逐行 期初库存+入库数量−出库数量=期末库存，'
        + '同一设施同一品种同一批号前后时点的结存也要接得上；同一设施同一时间点同一品种批号不得重复记录；'
        + '有 合计/小计 行时数量类列须等于明细行之和；字段空白、温度非数字、日期时间格式、状态取值都要能看懂。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得平、记录时点没缺、'
      + '字段能看懂**，不代表这批药品的质量是否合格，也不代表 GSP 认证或药监飞行检查的结论 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    data_rows: dataRows.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    facilities: new Set(dataRows.map((it) => String(it.facilityNo == null ? '' : it.facilityNo).trim())).size,
    varieties: new Set(dataRows.map((it) => String(it.variety == null ? '' : it.variety).trim())).size,
    open_total: t.totals.openQty,
    in_total: t.totals.inQty,
    out_total: t.totals.outQty,
    close_total: t.totals.closeQty,
    balance_diff: balances,
  };
  result.scope = scope;

  if (paid) {
    result.rollup = rollup;
    result.consolidated_actions = actions;
    if (paidContext.missing.length) result.paid_columns_missing = paidContext.missing;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
