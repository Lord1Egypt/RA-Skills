#!/usr/bin/env node
/**
 * secondary-water-supply-check-full.js —— 二次供水清洗消毒与水质检测核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：物业 / 供水管理单位对**二次供水**的水箱（水池）必须**每半年（180 天口径）清洗消毒一次**
 * 并做水质检测，台账每月 / 每季要向业主与卫生监督报一次。这本台账一旦出错，直接是**卫生监督处罚 + 水质事故**：
 *   ① 清洗周期超期：距上次清洗已过 180 天还没洗 —— 监管直接下整改 / 处罚；
 *   ② 检测项目缺失：常规指标子集没做全（缺菌落总数、缺总大肠菌群…），"其他项都合格"不能顶；
 *   ③ 检测结果超限值 / 低于限值：超标水样不得作为合格报告归档，必须复采复检并闭环；
 *   ④ 清洗单位资质与作业人员健康证：缺证 / 过期作业是直接处罚项；
 *   ⑤ 同一水箱同一天被登记成两次清洗（两套单位 / 人员打架）：追溯时说不清到底洗过没有；
 *   ⑥ 超期未清洗或未检测的水箱仍写着「在供水」、停用 / 废弃的水箱还出现在巡检记录里 —— 当天处置的 P0。
 * 所以每条结论都必须能拿原文行号 + 原文行内容复算。
 *
 * 本文件同时服务**订阅版（买断版）**与**本包**两个包：
 *   · 订阅版执行全部检查项（免费六项 + 追加五项）；
 *   · 本包只执行免费六项。追加项的实现由 `tools/strip_free_engine.py` 整块摘除，
 *     免费包里只留 `CHECKS_WITHHELD` 的**说明文本**，没有任何实现。
 *
 * 与同仓库另外三个跟"水 / 物业"有关的产品**不是一回事**（别混用）：
 *   · `utility-meter-reading-check` 核的是水电抄表与账单（表底、单价、用量、账单金额）；
 *   · `property-utility-apportionment-check` 核的是公共能耗在业主之间的分摊；
 *   · `wastewater-fee-check` 核的是污水处理费结算（水量勾稽、水质档位、超标扣款）；
 *   本产品核的是**二次供水水箱的清洗消毒周期 + 水质检测项目与限值**，既不抄表、也不分摊、也不算污水费。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定水箱容积 / 材质 / 消毒方式是否符合卫生规范、不判定水样采集与实验室检测过程是否规范、
 *          不判定现场是否真的洗过、不读 .xlsx / .pdf 原件、不联网核验清洗单位资质证书 / 健康证 / 检测报告真伪；
 *          材料不足**一律不给结论**（连「未发现问题」也不输出）。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '清洗周期覆盖（核对基准日 − 上次清洗日期 ≤ 180 天，超期逐水箱给出已超期天数；「下次清洗日期」与「上次清洗日期 + 180 天」逐水箱复算）',
  '检测项目齐全与限值判定（按水箱核对常规指标子集是否齐全；逐项判定检测结果是否超出上限 / 低于下限并给出倍数）',
  '清洗单位与作业人员健康证覆盖（清洗单位 / 清洗人员不得空缺；健康证有效期要覆盖本次清洗作业日，缺证或过期逐水箱点名）',
  '同一水箱同日重复清洗记录（同一水箱编号 + 同一上次清洗日期下出现互相矛盾的清洗单位或清洗人员）',
  '合计行逐列复核（水箱数 = 明细里不重复的水箱编号个数；检测项数 = 明细行数）',
  '字段合法性（关键字段缺失、日期格式非法、数值为负或为零、供水状态非法）',
];

const CHECKS_WITHHELD = [
  '超期未清洗或未检测仍在供水（供水状态=在供水，且清洗已超 180 天 / 检测已超 180 天 / 查不到有效检测日期；P0 并附超期天数）',
  '停用或已废弃水箱仍出现在巡检记录（跨表交叉：台账供水状态为停用 / 废弃，却在「巡检记录」段里出现，点巡检记录原文行号）',
  '检测结果超标未闭环（跨表交叉：台账里越过限值的项，到「复检记录」段核对复检日期与复检结果；缺复检或复检仍不合格逐条点名）',
  '消毒剂残留检测断档（跨表交叉：按「水箱 × 检测日期」逐次比对消毒剂残留记录，哪一次没有余氯 / 二氧化氯记录就点哪一次）',
  '分小区 × 分水箱（设施）汇总清单（按超期天数降序，每组给出可整改动作）与逐水箱整改清单（result.rollup / result.consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定二次供水水箱的容积、材质、内壁处理与消毒方式是否符合卫生规范（那是设计审查与卫生许可的口径，本工具只核台账日期与检测算术）',
  '判定水样采集 / 保存 / 运输 / 实验室检测过程是否规范、判定检测报告本身是否有效（那是 CMA / CNAS 检测机构与卫生监督部门的判定权）',
  '判定超期未清洗到底是物业没做还是做了没记、判定现场是否真的已经清洗或已经停水（本工具只核台账与巡检 / 复检记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验清洗单位资质证书 / 作业人员健康证 / 水质检测报告的真伪，替代卫生监督部门或供水管理单位的认定',
];

// 样例：一本**干净**的二次供水清洗消毒与水质检测台账 —— 2 个小区、3 个水箱、18 条检测记录：
// 清洗周期都在 180 天内、下次清洗日期复算一致、常规指标子集齐全且结果全在限值内、健康证都在有效期内、
// 水箱编号不重复、合计行与明细一致；三段跨表记录（消毒剂残留 / 巡检 / 复检）也都对得上。**全表零命中**。
const SAMPLE_TEXT = [
  '小区/项目名称\t水箱编号\t水箱名称\t上次清洗日期\t下次清洗日期\t清洗单位\t清洗人员\t健康证有效期\t检测日期\t检测项目\t检测结果\t限值\t单位\t供水状态\t水箱数\t检测项数\t核对基准日\t备注',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t色度\t5\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t浑浊度\t0.3\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\tpH\t7.2\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t游离余氯\t0.35\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t菌落总数\t20\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t色度\t6\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t浑浊度\t0.35\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\tpH\t7.1\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t游离余氯\t0.32\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t菌落总数\t25\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t色度\t5\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t浑浊度\t0.4\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\tpH\t7.0\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t游离余氯\t0.30\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t菌落总数\t30\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t3\t18\t2026-04-30\t2 个小区 3 个水箱 18 条检测记录由明细行汇总',
  '--- 消毒剂残留检测记录 ---',
  '水箱编号\t检测日期\t余氯(mg/L)\t二氧化氯(mg/L)',
  'SX-2026-01\t2026-03-18\t0.35\t—',
  'SX-2026-02\t2026-03-18\t0.32\t—',
  'SX-2026-03\t2026-04-08\t0.30\t—',
  '--- 巡检记录 ---',
  '水箱编号\t巡检日期\t巡检人\t巡检结果',
  'SX-2026-01\t2026-04-10\t赵国庆\t正常',
  'SX-2026-02\t2026-04-10\t赵国庆\t正常',
  'SX-2026-03\t2026-04-12\t孙明远\t正常',
  '--- 复检记录 ---',
  '水箱编号\t检测项目\t复检日期\t复检结果',
].join('\n');

const TOL = 0.01;

/** 二次供水水箱的法定清洗消毒周期：每半年（按 180 天口径核） */
const CLEAN_CYCLE_DAYS = 180;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'community', 'tankNo', 'lastCleanDate', 'cleanCompany', 'cleanStaff', 'healthCertExpiry',
  'testDate', 'testItem', 'testResult', 'limitValue', 'unit', 'nextCleanDate', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['community', '小区/项目名称'],
  ['tankNo', '水箱编号'],
  ['lastCleanDate', '上次清洗日期'],
  ['cleanCompany', '清洗单位'],
  ['cleanStaff', '清洗人员'],
  ['healthCertExpiry', '健康证有效期'],
  ['testDate', '检测日期'],
  ['testItem', '检测项目'],
  ['testResult', '检测结果'],
  ['limitValue', '限值'],
  ['unit', '单位'],
  ['nextCleanDate', '下次清洗日期'],
  ['checkDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['lastCleanDate', '上次清洗日期'],
  ['nextCleanDate', '下次清洗日期'],
  ['healthCertExpiry', '健康证有效期'],
  ['testDate', '检测日期'],
  ['checkDate', '核对基准日'],
];

// 数值列：[角色, 标签, 允许定性文字]
//   水箱数 / 检测项数 是纯数量（负数或 0 都不成立）；检测结果允许「未检出 / 阴性」这类定性描述。
const NUMBER_FIELDS = [
  ['tankCount', '水箱数', false],
  ['itemCount', '检测项数', false],
  ['testResult', '检测结果', true],
];

// 二次供水水质检测的**常规指标子集**：这 6 项少任何一项，这份检测报告在卫生监督眼里都不算做全
const REQUIRED_TEST_ITEMS = ['色度', '浑浊度', 'pH', '游离余氯', '菌落总数', '总大肠菌群'];

// 供水状态只认这三个值（二次供水水箱台账口径）
const SUPPLY_STATUSES = ['在供水', '停用', '废弃'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位：
//      · 「清洗单位」必须排在「单位」之前（否则被 unit 抢走）；
//      · 「下次清洗日期」必须排在「上次清洗日期」之前（后者的「清洗日期」会抢先命中）；
//      · 「水箱数」「检测项数」必须排在「水箱编号」「检测项目」之前；
//      · 「复检结果」「巡检结果」必须排在「检测结果」之前；
//      · 「检测日期」必须排在兜底的「日期」（recordDate）之前；
//      · 兜底的「日期」只能放在所有日期角色之后。
const ROLES = {
  tankCount: ['水箱数量', '水箱数', '设施数量'],
  itemCount: ['检测项目数', '检测项数', '检测项目合计'],
  community: ['小区/项目名称', '小区名称', '项目名称', '小区', '管理处'],
  tankNo: ['水箱编号', '水池编号', '水箱号', '设施编号'],
  tankName: ['水箱名称', '设施名称', '水箱位置'],
  nextCleanDate: ['下次清洗消毒日期', '下次清洗日期', '计划清洗日期', '下次清洗'],
  lastCleanDate: ['上次清洗消毒日期', '上次清洗日期', '最近一次清洗日期', '清洗日期', '上次清洗'],
  cleanCompany: ['清洗消毒单位', '清洗单位', '施工单位', '服务单位'],
  cleanStaff: ['清洗消毒人员', '清洗人员', '作业人员', '施工人员'],
  healthCertExpiry: ['健康证有效期至', '健康证有效期止', '健康证有效期', '健康证明有效期', '健康证到期日'],
  recheckDate: ['复检日期', '复查日期', '复检时间'],
  recheckResult: ['复检结果', '复查结果', '复检值'],
  recordResult: ['巡检结果', '巡检情况', '巡查结果'],
  testItem: ['检测项目', '检验项目', '水质检测项目'],
  testResult: ['检测结果', '检验结果', '检测值'],
  limitValue: ['限值', '标准限值', '限值要求', '标准值', '卫生标准'],
  testDate: ['检测日期', '检验日期', '采样日期', '检测时间'],
  unit: ['单位', '计量单位'],
  supplyStatus: ['供水状态', '水箱状态', '使用状态', '运行状态'],
  inspector: ['巡检人员', '巡检人', '巡检员'],
  recordDate: ['巡检日期', '巡查日期', '记录日期', '日期'],
  chlorineDioxide: ['二氧化氯'],
  chlorine: ['游离性余氯', '余氯'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明'],
};

const LABELS = {
  community: '小区/项目名称',
  tankNo: '水箱编号',
  tankName: '水箱名称',
  lastCleanDate: '上次清洗日期',
  nextCleanDate: '下次清洗日期',
  cleanCompany: '清洗单位',
  cleanStaff: '清洗人员',
  healthCertExpiry: '健康证有效期',
  testDate: '检测日期',
  testItem: '检测项目',
  testResult: '检测结果',
  limitValue: '限值',
  unit: '单位',
  supplyStatus: '供水状态',
  tankCount: '水箱数',
  itemCount: '检测项数',
  checkDate: '核对基准日',
  recheckDate: '复检日期',
  recheckResult: '复检结果',
  recordDate: '巡检日期',
  inspector: '巡检人',
  recordResult: '巡检结果',
  chlorine: '余氯',
  chlorineDioxide: '二氧化氯',
  note: '备注',
};

// 合计行要复核的数量类列：水箱数（不重复水箱个数）与检测项数（明细行数）
const SUM_ROLES = ['tankCount', 'itemCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「周期覆盖」，也不说「超期」。',
  };
}

/** 全角数字 / 全角符号 → 半角（物业与检测台账里很常见；认不出来就绝不猜） */
function toHalf(raw) {
  return String(raw)
    .replace(/[\uFF10-\uFF19]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\uFF0E/g, '.').replace(/\uFF0C/g, ',').replace(/\uFF0B/g, '+')
    .replace(/\uFF0D/g, '-').replace(/\uFF05/g, '%')
    .replace(/\uFF08/g, '(').replace(/\uFF09/g, ')')
    .replace(/\uFF1C/g, '<').replace(/\uFF1E/g, '>')
    .replace(/\u3000/g, ' ');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalf(String(raw)).trim().replace(/[¥￥,，\s]/g, '');
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
  const s = toHalf(String(v)).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalf(String(raw)).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
function isoOfDayNum(n) {
  return new Date(n * DAY_MS).toISOString().slice(0, 10);
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}
/** 日期 + 天数（清洗周期用**天**口径，避免 30 / 31 天换月带来的 1 天争议） */
function addDays(iso, n) {
  return isoOfDayNum(dayNum(iso) + n);
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = toHalf(String(header == null ? '' : header)).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/**
 * 合计行不是水箱明细：逐水箱检查要跳过它，只有「合计行逐列复核」那一项会用到它。
 * 合计行可能把「合计」写在小区 / 项目名称列（本台账的写法），也可能写在水箱编号 / 水箱名称列 —— 都要认出来。
 */
function isTotalRow(it) {
  const no = String(it.tankNo == null ? '' : it.tankNo).trim();
  const name = String(it.tankName == null ? '' : it.tankName).trim();
  const cm = String(it.community == null ? '' : it.community).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name) || TOTAL_LABEL.test(cm);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到一行 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
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
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  // 合计口径：水箱数 = 明细里不重复的水箱编号个数；检测项数 = 明细行数（不是逐行求和）
  const tanks = new Set(detail.map((it) => cell(it, 'tankNo')).filter(Boolean));
  const totals = { tankCount: tanks.size, itemCount: detail.length };
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

function who(it) {
  const name = cell(it, 'tankName');
  const no = cell(it, 'tankNo');
  const cm = cell(it, 'community');
  const label = name || no || '未命名水箱';
  const tail = name && no ? ' / ' + no : '';
  return `第 ${it.line} 行「${label}${tail}」${cm ? '（' + cm + '）' : ''}`;
}

function listShow(arr, max) {
  const n = max || 8;
  const a = arr.slice(0, n);
  return a.join('、') + (arr.length > n ? ' 等' : '');
}

/** 每条结论都带原文依据：行号 + 水箱编号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    tank_no: cell(it, 'tankNo'),
    community: cell(it, 'community'),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/** 把明细行按水箱编号分组（同一水箱的多条检测记录合成一组，逐水箱检查只报一次） */
function tankGroups(items) {
  const map = new Map();
  let seq = 0;
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'tankNo');
    let key = no;
    if (!key) { seq += 1; key = '(未填水箱编号)#' + seq; }
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(it);
  }
  return [...map.values()];
}

/** 一组行里第一个能认出来的日期 */
function firstDateOf(rows, role) {
  for (const r of rows) {
    const d = normDate(r[role]);
    if (d) return d;
  }
  return null;
}

/* ============================ 限值判定（本包第 ② 项用） ============================ */

/**
 * 解析「限值」单元格，支持四种真实形态：
 *   · 单个数字   15 / 100       ⇒ 上限（结果 ≤ 限值）
 *   · 区间       6.5~8.5        ⇒ 上下限都要满足（分隔符认 ~ ～ - — 至）
 *   · 带比较符   ≥0.05 / ≤15    ⇒ 只判下限 / 只判上限
 *   · 定性       不得检出        ⇒ 结果必须是 未检出 / 阴性 / 0
 */
function parseLimit(raw) {
  const s = toHalf(String(raw == null ? '' : raw)).replace(/\s/g, '');
  if (!s || /^[-—–]+$/.test(s)) return { kind: 'blank' };
  if (/不得检出|不应检出|不得验出|不得测出/.test(s)) return { kind: 'nodetect', raw: s };
  const cmp = /^([≥≤<>=]+)/.exec(s);
  const body = s.replace(/^[≥≤<>=]+/, '');
  const m = /^(-?\d+(?:\.\d+)?)\s*[~～\-—至]\s*(-?\d+(?:\.\d+)?)$/.exec(body);
  if (m) return { kind: 'range', lo: Number(m[1]), hi: Number(m[2]), raw: s };
  const n = normNumber(body);
  if (n === null) return { kind: 'unknown', raw: s };
  if (cmp) {
    if (/[≥>]/.test(cmp[1])) return { kind: 'min', v: n, raw: s };
    if (/[≤<]/.test(cmp[1])) return { kind: 'max', v: n, raw: s };
  }
  return { kind: 'max', v: n, raw: s };
}

const NEG_WORDS = /未检出|未测出|未验出|阴性|不检出|无检出/;
const POS_WORDS = /检出|阳性/;

/**
 * 判定「检测结果」是否在「限值」之内。返回 {verdict, ratio, why, value}：
 *   verdict: ok / over（越过上限，或"不得检出"却检出） / under（低于下限） / unknown（认不出来）
 *   ratio  : 越限倍数（结果 ÷ 上限）；低于下限时给「下限 ÷ 结果」的倍数
 */
function judgeResult(resultRaw, limitRaw) {
  const rRaw = String(resultRaw == null ? '' : resultRaw).trim();
  const lim = parseLimit(limitRaw);
  if (lim.kind === 'blank') return { verdict: 'unknown', why: '限值没填' };
  if (lim.kind === 'unknown') return { verdict: 'unknown', why: `限值「${lim.raw}」认不出是数字、区间还是比较符` };
  if (rRaw === '') return { verdict: 'unknown', why: '检测结果没填' };

  const rNum = normNumber(rRaw);
  const rNeg = NEG_WORDS.test(rRaw);
  const rPos = !rNeg && POS_WORDS.test(rRaw);

  if (lim.kind === 'nodetect') {
    if (rNeg) return { verdict: 'ok', value: 0 };
    if (rNum !== null) {
      return rNum > TOL
        ? { verdict: 'over', value: rNum, why: `限值是「不得检出」，但结果填了 ${rNum}` }
        : { verdict: 'ok', value: rNum };
    }
    if (rPos) return { verdict: 'over', value: rRaw, why: `限值是「不得检出」，但结果是「${rRaw}」` };
    return { verdict: 'unknown', why: `限值是「不得检出」，但结果「${rRaw}」看不出是检出还是未检出` };
  }

  const value = rNum !== null ? rNum : (rNeg ? 0 : null);
  if (value === null) return { verdict: 'unknown', why: `结果「${rRaw}」既不是数字，也不是未检出 / 阴性这类定性描述` };

  if (lim.kind === 'range') {
    if (value > lim.hi + TOL) return { verdict: 'over', ratio: round2(value / lim.hi), value, why: `超过区间上限 ${lim.hi}` };
    if (value < lim.lo - TOL) return { verdict: 'under', ratio: value > 0 ? round2(lim.lo / value) : undefined, value, why: `低于区间下限 ${lim.lo}` };
    return { verdict: 'ok', value };
  }
  if (lim.kind === 'min') {
    if (value < lim.v - TOL) return { verdict: 'under', ratio: value > 0 ? round2(lim.v / value) : undefined, value, why: `低于下限 ${lim.v}` };
    return { verdict: 'ok', value };
  }
  if (value > lim.v + TOL) return { verdict: 'over', ratio: lim.v > 0 ? round2(value / lim.v) : undefined, value, why: `超过限值 ${lim.v}` };
  return { verdict: 'ok', value };
}

/* ============================ 本包检查（六项） ============================ */

function checkCleanCycle(items, base) {
  // ① 清洗周期覆盖：核对基准日 − 上次清洗日期 ≤ 180 天，超期给天数；下次清洗日期按 +180 天逐水箱复算
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const last = firstDateOf(rows, 'lastCleanDate');
    const b = baseOf(first, base);
    if (last && b) {
      const elapsed = daysBetween(last, b);
      if (elapsed > CLEAN_CYCLE_DAYS) {
        const over = elapsed - CLEAN_CYCLE_DAYS;
        out.push(finding('P1', '清洗超期', first, over,
          `${who(first)}：上次清洗日期 ${last}，距核对基准日 ${b} 已经 ${elapsed} 天，`
          + `超过 ${CLEAN_CYCLE_DAYS} 天的半年清洗周期，**已超期 ${over} 天**`
          + `（该水箱在台账里有 ${rows.length} 条检测记录）。`,
          '二次供水水箱每半年必须清洗消毒一次：先按上面的天数排进本月清洗计划，'
          + '清洗完成后补做一次水质检测，并把新的「上次清洗日期 / 下次清洗日期」填回台账；别只改日期。'));
      }
    }
    const next = firstDateOf(rows, 'nextCleanDate');
    if (last && next) {
      const expect = addDays(last, CLEAN_CYCLE_DAYS);
      if (next !== expect) {
        const drift = daysBetween(expect, next);
        out.push(finding('P2', '清洗周期与下次清洗日期不符', first, drift,
          `${who(first)}：上次清洗日期 ${last} + ${CLEAN_CYCLE_DAYS} 天 = ${expect}，`
          + `但台账写的下次清洗日期是 ${next}，差 ${Math.abs(drift)} 天（复算值 − 台账值）。`,
          '两个字段只能有一个是对的：要么上次清洗日期抄错，要么下次清洗日期是照抄上一年 / 手工估的。'
          + '先拿清洗消毒记录单上的日期改正，再重跑。'));
      }
    }
  }
  return out;
}

function checkTestItemsAndLimits(items) {
  // ②-a 检测项目齐全：按水箱核对常规指标子集（缺哪一项就点哪一项）
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const have = [];
    for (const r of rows) {
      const t = cell(r, 'testItem');
      if (t && have.indexOf(t) < 0) have.push(t);
    }
    if (!have.length) continue;                     // 检测项目整列空 ⇒ 交给第 ⑥ 项逐行点名
    const miss = REQUIRED_TEST_ITEMS.filter((req) => !have.some((t) => t.indexOf(req) >= 0));
    if (miss.length) {
      out.push(finding('P1', '检测项目缺失', first, miss.length,
        `${who(first)}：这个水箱的定期水质检测一共只登记了 ${have.length} 项（${listShow(have, 6)}），`
        + `常规指标子集里缺这几项 —— ${miss.join('、')}。`,
        '二次供水的水质检测项目要覆盖卫生规范要求的常规指标子集：缺哪一项就先补采水样做哪一项；'
        + '缺项的检测报告在卫生监督眼里等于没做全，别用其他项都合格顶过去。'));
    }
  }

  // ②-b 逐项限值判定（越限就报，并给倍数）
  for (const it of items) {
    if (it.isTotal) continue;
    const raw = cell(it, 'testResult');
    const limRaw = cell(it, 'limitValue');
    if (isBlank(raw) || isBlank(limRaw)) continue;  // 缺谁交给第 ⑥ 项点名
    const j = judgeResult(raw, limRaw);
    const item = cell(it, 'testItem') || '(未填检测项目)';
    const unit = cell(it, 'unit');
    if (j.verdict === 'over') {
      out.push(finding('P0', '检测结果超限值', it, j.ratio,
        `${who(it)}：检测项目「${item}」的结果 ${raw}${unit ? ' ' + unit : ''} 越过了限值 ${limRaw}`
        + `（${j.why}${j.ratio !== undefined ? '，为限值的 ' + j.ratio + ' 倍' : ''}）。`,
        '超标水样不得作为合格报告归档：先同一样点、同一项目复采复检；'
        + '同时按超标项目倒查消毒与清洗环节，整改后重新检测并留痕，复检结果填进「复检记录」段。'));
    } else if (j.verdict === 'under') {
      out.push(finding('P1', '检测结果低于限值', it, j.ratio,
        `${who(it)}：检测项目「${item}」的结果 ${raw}${unit ? ' ' + unit : ''} 低于限值 ${limRaw}`
        + `（${j.why}${j.ratio !== undefined ? '，只有下限的 1/' + j.ratio : ''}）。`,
        '低于下限同样不合格：消毒剂残留不足会让管网末梢的余氯掉到保护线以下，'
        + '先查投加设备与投加量，再补做一次检测确认。'));
    }
  }
  return out;
}

function checkCleaningQualification(items, base) {
  // ③ 清洗单位 / 清洗人员 / 健康证：人员与单位不得空缺；健康证有效期必须覆盖本次清洗作业日
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const staff = cell(first, 'cleanStaff');
    const miss = [];
    if (isBlank(first.cleanCompany)) miss.push('清洗单位');
    if (isBlank(first.cleanStaff)) miss.push('清洗人员');
    if (miss.length) {
      out.push(finding('P1', '清洗单位或人员缺失', first, miss.length,
        `${who(first)}：${miss.join('、')}是空的 —— 清洗记录连是谁来洗的都点不出来。`,
        '二次供水清洗消毒必须由具备资质的清洗单位派人作业：把清洗单位全称与作业人员姓名补进台账，'
        + '并保留清洗消毒记录单（含单位盖章、作业日期、人员签到）。'));
    }

    const certRaw = first.healthCertExpiry;
    const work = firstDateOf(rows, 'lastCleanDate') || baseOf(first, base);
    if (isBlank(certRaw)) {
      out.push(finding('P1', '健康证过期或缺失', first, undefined,
        `${who(first)}：清洗人员 ${staff || '(未填)'} 的健康证有效期是空的 —— `
        + '台账里连到期日都点不出来，等于无法证明作业时持有效健康证。',
        '从事二次供水清洗消毒的人员必须持有效健康证：把姓名与健康证有效期逐水箱补进台账，'
        + '证件在别处的也要能在这本台账里点到。'));
    } else {
      const d = normDate(certRaw);
      if (d && work && daysBetween(d, work) > 0) {
        const over = daysBetween(d, work);
        out.push(finding('P0', '健康证过期或缺失', first, over,
          `${who(first)}：清洗人员 ${staff || '(未填)'} 的健康证有效期 ${d}，`
          + `早于本次清洗作业日 ${work}，**作业时已过期 ${over} 天**。`,
          '健康证过期期间不得从事二次供水清洗消毒作业：先安排体检换证或换持证人，'
          + '并把换证后的有效期填回台账。'));
      }
    }
  }
  return out;
}

function checkDuplicateCleaning(items) {
  // ④ 同一水箱 + 同一上次清洗日期下出现互相矛盾的清洗单位 / 清洗人员 ⇒ 同一天被登记成两次清洗
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'tankNo');
    const last = normDate(it.lastCleanDate);
    if (!no || !last) continue;
    const key = no + '|' + last;
    const company = cell(it, 'cleanCompany');
    const staff = cell(it, 'cleanStaff');
    if (!seen.has(key)) {
      seen.set(key, { line: it.line, company, staff });
      continue;
    }
    const p = seen.get(key);
    const conf = [];
    if (p.company && company && p.company !== company) {
      conf.push(`清洗单位「${p.company}」（第 ${p.line} 行）与「${company}」`);
    }
    if (p.staff && staff && p.staff !== staff) {
      conf.push(`清洗人员「${p.staff}」（第 ${p.line} 行）与「${staff}」`);
    }
    if (!conf.length) continue;
    out.push(finding('P0', '同一水箱同日重复清洗记录', it, conf.length,
      `${who(it)}：水箱编号 ${no} 的「上次清洗日期」都写着 ${last}，但清洗记录出现了互相矛盾的两套 —— `
      + `${conf.join('；')}。同一天被登记成两次清洗（或至少两套记录打架），追溯时说不清到底洗过没有。`,
      '一个水箱一次清洗只能有一条清洗记录：先找清洗消毒记录单核对当天的实际作业单位与人员，'
      + '删掉错的那一行，并把两套记录的来源写进备注（别只改一行了事）。'));
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：水箱数 = 不重复水箱编号个数；检测项数 = 明细行数
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const expected = {
    tankCount: new Set(detail.map((it) => cell(it, 'tankNo')).filter(Boolean)).size,
    itemCount: detail.length,
  };
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（个 / 项）写进了单元格里。'));
        continue;
      }
      const actual = expected[role];
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      const how = role === 'tankCount'
        ? `明细里不重复的水箱编号只有 ${actual} 个`
        : `明细一共 ${actual} 行`;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但${how}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须与明细对得上：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有把同一水箱的多条检测记录重复计数'
        + '（水箱数要按**不重复的水箱编号**数，不是按行数）。'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 关键字段缺失 / 日期格式非法 / 数值为负或为零 / 供水状态非法
  const out = [];
  for (const it of items) {
    if (!it.isTotal) {
      const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
      if (miss.length) {
        out.push(finding('P1', '关键字段缺失', it, miss.length,
          `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
          '空着的字段会让对应的核对整项做不了（例如限值空着就判不了超标、健康证空着就判不了覆盖）；'
          + '补全后重跑，本工具不会替你猜一个默认值。'));
      }
      for (const [role, label] of DATE_FIELDS) {
        const raw = it[role];
        if (isBlank(raw)) continue;
        if (normDate(raw) === null) {
          out.push(finding('P1', '日期格式非法', it, undefined,
            `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
            + '（只认 2026-04-30 / 2026/4/30 / 2026年4月30日 / 20260430 这几种形态）。',
            '把日期改成 2026-04-30 这种形态再跑；日期认不出来时本工具不会拿它去算清洗周期或超期天数。'));
        }
      }
      const st = cell(it, 'supplyStatus');
      if (st && SUPPLY_STATUSES.indexOf(st) < 0) {
        out.push(finding('P1', '供水状态非法', it, undefined,
          `${who(it)}：供水状态写的是「${st}」，不在允许的三个值里（${SUPPLY_STATUSES.join(' / ')}）。`,
          '供水状态会直接决定「超期未清洗仍在供水」这类结论：按实际状态改成 在供水 / 停用 / 废弃 之一。'));
      }
    }

    for (const [role, label, soft] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        if (soft) continue;                         // 检测结果允许「未检出 / 阴性」这类定性描述
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '数量必须是纯数字（如 3 / 18）；写成「三」「壹拾捌」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的数量出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && !soft) {
        out.push(finding('P1', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是 0 —— 数量为零说明这本台账根本没覆盖到任何水箱 / 检测记录，口径上不成立。`,
          '按实际覆盖范围填真实的个数；确实还没有水箱的要先确认这本台账是不是空表，别用 0 顶过去。'));
      }
    }
  }
  return out;
}

/* ============================ 订阅版检查（追加五项） ============================ */

/** 把主台账之后每一段 `--- 段名 ---` 单独当一张表解析（行号换回**全文**行号，才能对上原文） */
function parseSections(text) {
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  const found = [];
  let cur = null;
  for (let i = 0; i < lines.length; i++) {
    const m = SECTION_RE.exec(lines[i]);
    if (m) {
      cur = { name: m[1].trim(), lines: [], start: i + 2 };
      found.push(cur);
      continue;
    }
    if (!cur) continue;
    cur.lines.push(lines[i]);
  }
  const out = {};
  for (const s of found) {
    if (!s.lines.some((l) => String(l).trim() !== '')) continue;
    const t = parseTable(s.lines.join('\n'));
    for (const it of t.items) it.line += (s.start - 1);
    out[s.name] = t;
  }
  return out;
}

function findSection(sections, pattern) {
  for (const n of Object.keys(sections || {})) {
    if (pattern.test(n)) return { name: n, table: sections[n] };
  }
  return null;
}

function readDisinfectant(sections) {
  // 消毒剂残留检测记录：水箱编号 / 检测日期 / 余氯 / 二氧化氯
  const hit = findSection(sections, /消毒剂|残留|余氯|二氧化氯/);
  if (!hit) return { present: false, name: '', rows: [], missing: [] };
  const t = hit.table;
  const missing = [];
  if (!t.cols.some((c) => c.role === 'tankNo')) missing.push('水箱编号');
  if (!t.cols.some((c) => c.role === 'testDate')) missing.push('检测日期');
  const rows = (t.items || []).map((it) => ({
    line: it.line,
    tank_no: cell(it, 'tankNo'),
    date: normDate(it.testDate),
    date_raw: cell(it, 'testDate'),
    has_chlorine: !isBlank(it.chlorine),
    has_dioxide: !isBlank(it.chlorineDioxide),
    chlorine: cell(it, 'chlorine'),
    dioxide: cell(it, 'chlorineDioxide'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  return { present: true, name: hit.name, rows, missing };
}

function readPatrol(sections) {
  // 巡检记录：水箱编号 / 巡检日期 / 巡检人 / 巡检结果
  const hit = findSection(sections, /巡检|巡查/);
  if (!hit) return { present: false, name: '', rows: [], missing: [] };
  const t = hit.table;
  const missing = [];
  if (!t.cols.some((c) => c.role === 'tankNo')) missing.push('水箱编号');
  if (!t.cols.some((c) => c.role === 'recordDate')) missing.push('巡检日期');
  const rows = (t.items || []).map((it) => ({
    line: it.line,
    tank_no: cell(it, 'tankNo'),
    date: normDate(it.recordDate),
    date_raw: cell(it, 'recordDate'),
    inspector: cell(it, 'inspector'),
    result: cell(it, 'recordResult'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  return { present: true, name: hit.name, rows, missing };
}

function readRecheck(sections) {
  // 复检记录：水箱编号 / 检测项目 / 复检日期 / 复检结果
  const hit = findSection(sections, /复检|复查/);
  if (!hit) return { present: false, name: '', rows: [], missing: [] };
  const t = hit.table;
  const missing = [];
  if (!t.cols.some((c) => c.role === 'tankNo')) missing.push('水箱编号');
  if (!t.cols.some((c) => c.role === 'testItem')) missing.push('检测项目');
  const rows = (t.items || []).map((it) => ({
    line: it.line,
    tank_no: cell(it, 'tankNo'),
    item: cell(it, 'testItem'),
    date: normDate(it.recheckDate),
    date_raw: cell(it, 'recheckDate'),
    result: cell(it, 'recheckResult'),
    result_raw: cell(it, 'recheckResult'),
    raw: String(it.raw == null ? '' : it.raw).slice(0, 200),
  }));
  return { present: true, name: hit.name, rows, missing };
}

/** 按 key 建索引（同一 key 取第一条） */
function indexBy(rows, keyFn) {
  const m = new Map();
  for (const r of rows) {
    const k = keyFn(r);
    if (!k) continue;
    if (!m.has(k)) m.set(k, r);
  }
  return m;
}

/** 逐水箱算齐订阅版五项要用的所有聚合量（五项共用这一份取数） */
function buildTankAggregates(items, ctx) {
  const map = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'tankNo');
    if (!no) continue;
    if (!map.has(no)) {
      map.set(no, {
        tank_no: no,
        tank_name: cell(it, 'tankName'),
        community: cell(it, 'community') || '(未填小区)',
        first_line: it.line,
        rows: [],
        status: '',
        last_clean: null,
        next_clean: null,
        clean_company: '',
        clean_staff: '',
        health_expiry: null,
        test_dates: new Set(),
        items_seen: [],
        over_rows: [],
        under_rows: [],
      });
    }
    const a = map.get(no);
    a.rows.push(it);
    if (!a.tank_name) a.tank_name = cell(it, 'tankName');
    if (!a.community || a.community === '(未填小区)') a.community = cell(it, 'community') || a.community;
    if (!a.status) a.status = cell(it, 'supplyStatus');
    const lc = normDate(it.lastCleanDate);
    if (lc && !a.last_clean) a.last_clean = lc;
    const nc = normDate(it.nextCleanDate);
    if (nc && !a.next_clean) a.next_clean = nc;
    if (!a.clean_company) a.clean_company = cell(it, 'cleanCompany');
    if (!a.clean_staff) a.clean_staff = cell(it, 'cleanStaff');
    const he = normDate(it.healthCertExpiry);
    if (he && !a.health_expiry) a.health_expiry = he;
    const td = normDate(it.testDate);
    if (td) a.test_dates.add(td);
    const item = cell(it, 'testItem');
    if (item && a.items_seen.indexOf(item) < 0) a.items_seen.push(item);
    const j = judgeResult(cell(it, 'testResult'), cell(it, 'limitValue'));
    if (j.verdict === 'over') a.over_rows.push({ it, judge: j });
    if (j.verdict === 'under') a.under_rows.push({ it, judge: j });
  }

  const out = [];
  for (const a of map.values()) {
    const base = ctx.base;
    a.first = a.rows[0];
    a.clean_overdue_days = (a.last_clean && base)
      ? Math.max(0, daysBetween(a.last_clean, base) - CLEAN_CYCLE_DAYS) : 0;
    const dates = [...a.test_dates].sort();
    a.tested = dates.length > 0;
    a.last_test = a.tested ? dates[dates.length - 1] : null;
    a.test_overdue_days = (a.last_test && base)
      ? Math.max(0, daysBetween(a.last_test, base) - CLEAN_CYCLE_DAYS) : 0;
    a.missing_items = REQUIRED_TEST_ITEMS.filter((req) => !a.items_seen.some((t) => t.indexOf(req) >= 0));
    a.over_count = a.over_rows.length;
    a.under_count = a.under_rows.length;

    a.patrol_records = 0;
    a.patrol_lines = [];
    if (ctx.patrol.present) {
      const recs = ctx.patrolByTank.get(a.tank_no) || [];
      a.patrol_records = recs.length;
      a.patrol_lines = recs.map((r) => r.line);
    }

    a.disinfectant_gaps = [];
    if (ctx.disinfectant.present) {
      for (const d of dates) {
        const row = ctx.disinfectantByKey.get(a.tank_no + '|' + d);
        if (!row || (!row.has_chlorine && !row.has_dioxide)) {
          a.disinfectant_gaps.push({ date: d, line: row ? row.line : null });
        }
      }
    }
    a.disinfectant_gap_times = a.disinfectant_gaps.length;

    a.open_over_limit = 0;
    a.closed_over_limit = 0;
    if (ctx.recheck.present) {
      for (const o of a.over_rows) {
        const r = ctx.recheckByKey.get(a.tank_no + '|' + cell(o.it, 'testItem'));
        const closed = !!(r && r.date && r.result
          && judgeResult(r.result, cell(o.it, 'limitValue')).verdict === 'ok');
        if (closed) a.closed_over_limit += 1; else a.open_over_limit += 1;
      }
    }

    a.overdue_in_supply = a.status === '在供水'
      && (a.clean_overdue_days > 0 || !a.tested || a.test_overdue_days > 0);
    a.stale_in_patrol = (a.status === '停用' || a.status === '废弃') && a.patrol_records > 0;
    out.push(a);
  }
  return out;
}

function checkOverdueSupply(a, ctx) {
  // 订阅版 ⑦：超期未清洗或未检测，却仍然写着「在供水」（P0，附超期天数）
  if (!ctx.hasSupplyStatus) return [];
  if (a.status !== '在供水') return [];
  const parts = [];
  let diff = 0;
  if (a.clean_overdue_days > 0) {
    parts.push(`上次清洗日期 ${a.last_clean} 距核对基准日 ${ctx.base} 已经 `
      + `${daysBetween(a.last_clean, ctx.base)} 天，**清洗超期 ${a.clean_overdue_days} 天**`);
    diff = Math.max(diff, a.clean_overdue_days);
  }
  if (!a.tested) {
    parts.push('这本台账里找不到这个水箱任何一条有效「检测日期」（**未检测**）');
  } else if (a.test_overdue_days > 0) {
    parts.push(`最近一次水质检测 ${a.last_test} 距核对基准日 ${ctx.base} 已经 `
      + `${daysBetween(a.last_test, ctx.base)} 天，**检测超期 ${a.test_overdue_days} 天**`);
    diff = Math.max(diff, a.test_overdue_days);
  }
  if (!parts.length) return [];
  return [finding('P0', '超期未清洗或未检测仍在供水', a.first, diff || undefined,
    `${who(a.first)}：供水状态是「在供水」，但${parts.join('；')}。`
    + '这一条是卫生监督直接下整改 / 处罚项：水箱没按期清洗消毒、水质没按期检测，水却还在往住户家里送。',
    '当天处置：先安排清洗消毒与水质检测（必要时按当地要求临时停水或改由市政直供），'
    + '同步书面报物业负责人与卫生监督部门；检测合格后把新的清洗日期与检测日期填回台账，'
    + '并保留清洗消毒记录单与检测报告原件。')];
}

function checkStaleInPatrol(a, ctx) {
  // 订阅版 ⑧：停用 / 废弃水箱仍出现在巡检记录里（跨表交叉，点巡检记录原文行号）
  if (!ctx.patrol.present || !ctx.hasSupplyStatus) return [];
  if (a.status !== '停用' && a.status !== '废弃') return [];
  if (!a.patrol_records) return [];
  const show = a.patrol_lines.slice(0, 8).join('、');
  return [finding('P0', '停用废弃水箱仍在巡检记录', a.first, a.patrol_records,
    `${who(a.first)}：台账供水状态是「${a.status}」，但「${ctx.patrol.name}」段里还有 `
    + `${a.patrol_records} 条该水箱的记录（原文第 ${show} 行${a.patrol_lines.length > 8 ? ' 等' : ''}）。`,
    '停用 / 废弃的二次供水水箱应当办理停用手续、断开与管网的联系并挂牌：'
    + '巡检记录里还有它，要么现场仍在供水（水质事故风险），要么巡检是照抄的假记录。两种都要现场核实并留整改单。')];
}

function checkRecheckClosure(a, ctx) {
  // 订阅版 ⑨：检测结果超标未闭环（到「复检记录」段核对复检日期与复检结果）
  if (!ctx.recheck.present) return [];
  const out = [];
  for (const o of a.over_rows) {
    const it = o.it;
    const item = cell(it, 'testItem') || '(未填检测项目)';
    const raw = cell(it, 'testResult');
    const limRaw = cell(it, 'limitValue');
    const r = ctx.recheckByKey.get(a.tank_no + '|' + cell(it, 'testItem'));
    if (!r) {
      out.push(finding('P1', '检测结果超标未闭环', it, undefined,
        `${who(it)}：检测项目「${item}」的结果 ${raw} 已越过限值 ${limRaw}（${o.judge.why}），`
        + `但「${ctx.recheck.name}」段里没有这个水箱这一项的复检记录 —— **缺复检**。`,
        '超标必须有闭环：同一样点、同一项目复采复检，把复检日期与复检结果填进「复检记录」段；'
        + '复检合格前这份检测报告不能作为合格归档，也不能据此恢复供水。'));
      continue;
    }
    if (isBlank(r.date_raw)) {
      out.push(finding('P1', '检测结果超标未闭环', it, undefined,
        `${who(it)}：检测项目「${item}」的结果 ${raw} 已越过限值 ${limRaw}，`
        + `「${ctx.recheck.name}」段第 ${r.line} 行有这一项的复检记录，但**复检日期没填**。`,
        '复检日期是闭环的时间证据：把实际复采复检的日期补上（不是整改通知日期），再重跑。'));
      continue;
    }
    if (isBlank(r.result_raw)) {
      out.push(finding('P1', '检测结果超标未闭环', it, undefined,
        `${who(it)}：检测项目「${item}」的结果 ${raw} 已越过限值 ${limRaw}，`
        + `「${ctx.recheck.name}」段第 ${r.line} 行写了复检日期 ${r.date || r.date_raw}，但**复检结果没填**。`,
        '只填复检日期不算闭环：把复检报告的实测值填进复检结果，本工具会拿同一个限值再判一次。'));
      continue;
    }
    const rj = judgeResult(r.result_raw, limRaw);
    if (rj.verdict === 'ok') continue;              // 已闭环
    const verdictWord = rj.verdict === 'over' ? '仍然越过限值' : '仍然低于下限';
    out.push(finding('P0', '检测结果超标未闭环', it, rj.ratio,
      `${who(it)}：检测项目「${item}」的结果 ${raw} 越过限值 ${limRaw}；`
      + `「${ctx.recheck.name}」段第 ${r.line} 行（复检日期 ${r.date || r.date_raw}）的复检结果 `
      + `${r.result_raw} ${verdictWord}（${rj.why}）—— **复检未通过，闭环没完成**。`,
      '复检仍不合格说明消毒 / 清洗环节没整改到位：先停用或限制该水箱供水，重新清洗消毒、'
      + '排查投加设备与管网，整改后第三次采样检测；两次不合格的要按当地要求上报卫生监督部门。'));
  }
  return out;
}

function checkDisinfectantGaps(a, ctx) {
  // 订阅版 ⑩：消毒剂残留检测断档（按「水箱 × 检测日期」逐次比对，缺哪一次点哪一次）
  if (!ctx.disinfectant.present) return [];
  const out = [];
  for (const g of a.disinfectant_gaps) {
    const at = g.line
      ? `那一行（原文第 ${g.line} 行）既没有余氯也没有二氧化氯记录`
      : '**完全没有**对应的消毒剂残留记录行';
    out.push(finding('P1', '消毒剂残留检测断档', a.first, undefined,
      `${who(a.first)}：检测日期 ${g.date} 那一次在「${ctx.disinfectant.name}」段里 ${at} —— 缺 ${g.date} 这一次。`,
      '消毒剂残留要按次跟着水质检测走：哪一次缺就补哪一次（用次氯酸钠消毒就检余氯、'
      + '用二氧化氯就检二氧化氯，两者至少有一项）；断档的那几次拿检测报告或现场自检记录回填。'));
  }
  return out;
}

function groupActionFor(v) {
  // 订阅版 ⑪：每一组给一条可整改动作（先解决最要命的：超期了还在供水）
  if (v.overdue_in_supply_tanks > 0) {
    return `立即排查本组 ${v.overdue_in_supply_tanks} 个仍在供水的超期水箱：当天安排清洗消毒与水质检测，同步报物业与卫生监督`;
  }
  if (v.clean_overdue_tanks > 0) {
    return `把本组 ${v.clean_overdue_tanks} 个已超期水箱排进本月清洗消毒计划，清洗后补做水质检测并更新台账日期`;
  }
  if (v.over_limit_count > 0) {
    return `对本组 ${v.over_limit_count} 项超标结果先复采复检、再倒查消毒环节，整改后把复检结果填进复检记录`;
  }
  if (v.missing_items > 0) {
    return `补做本组缺的 ${v.missing_items} 个常规指标检测项目，补齐后再归档检测报告`;
  }
  if (v.stale_tanks > 0) {
    return `清理本组 ${v.stale_tanks} 个停用 / 废弃水箱的巡检记录，并补齐停用手续与管网隔离`;
  }
  if (v.disinfectant_gaps > 0) {
    return `补做本组 ${v.disinfectant_gaps} 次缺档的消毒剂残留检测，缺哪一次补哪一次`;
  }
  return '本组未发现清洗超期 / 检测缺项 / 超标未闭环 / 残留断档的问题，保持现有清洗与检测节奏即可';
}

function buildRollup(agg) {
  // 订阅版 ⑪：分小区 × 分水箱（设施）的汇总清单（按超期天数降序，每组附可整改动作）
  const blank = () => ({
    tanks: 0,
    clean_overdue_tanks: 0,
    overdue_in_supply_tanks: 0,
    clean_overdue_days_max: 0,
    clean_overdue_days_total: 0,
    test_overdue_tanks: 0,
    test_overdue_days_max: 0,
    overdue_days_max: 0,
    missing_items: 0,
    over_limit_count: 0,
    under_limit_count: 0,
    open_over_limit: 0,
    disinfectant_gaps: 0,
    stale_tanks: 0,
    patrol_records: 0,
    test_records: 0,
  });
  const add = (bk, a) => {
    bk.tanks += 1;
    if (a.clean_overdue_days > 0) {
      bk.clean_overdue_tanks += 1;
      bk.clean_overdue_days_total = round2(bk.clean_overdue_days_total + a.clean_overdue_days);
      bk.clean_overdue_days_max = Math.max(bk.clean_overdue_days_max, a.clean_overdue_days);
    }
    if (a.test_overdue_days > 0) {
      bk.test_overdue_tanks += 1;
      bk.test_overdue_days_max = Math.max(bk.test_overdue_days_max, a.test_overdue_days);
    }
    bk.overdue_days_max = Math.max(bk.clean_overdue_days_max, bk.test_overdue_days_max);
    if (a.overdue_in_supply) bk.overdue_in_supply_tanks += 1;
    bk.missing_items += a.missing_items.length;
    bk.over_limit_count += a.over_count;
    bk.under_limit_count += a.under_count;
    bk.open_over_limit += a.open_over_limit;
    bk.disinfectant_gaps += a.disinfectant_gap_times;
    if (a.stale_in_patrol) bk.stale_tanks += 1;
    bk.patrol_records += a.patrol_records;
    bk.test_records += a.rows.length;
    return bk;
  };

  const byComm = new Map();
  const byTank = new Map();
  const byCommTank = new Map();
  for (const a of agg) {
    const kc = a.community || '(未填小区)';
    const kt = a.tank_no + (a.tank_name ? ' ' + a.tank_name : '');
    const kct = kc + ' × ' + a.tank_no;
    if (!byComm.has(kc)) byComm.set(kc, blank());
    if (!byTank.has(kt)) byTank.set(kt, blank());
    if (!byCommTank.has(kct)) byCommTank.set(kct, blank());
    add(byComm.get(kc), a);
    add(byTank.get(kt), a);
    add(byCommTank.get(kct), a);
  }
  const toRows = (map, keyName) => [...map.entries()]
    .map(([k, v]) => Object.assign({ [keyName]: k, action: groupActionFor(v) }, v))
    .sort((x, y) => (y.overdue_days_max - x.overdue_days_max)
      || (y.overdue_in_supply_tanks - x.overdue_in_supply_tanks)
      || (y.over_limit_count - x.over_limit_count)
      || String(x[keyName]).localeCompare(String(y[keyName])));
  const total = agg.reduce((acc, a) => add(acc, a), blank());
  return {
    by_community: toRows(byComm, 'community'),
    by_tank: toRows(byTank, 'tank'),
    by_community_tank: toRows(byCommTank, 'community_tank'),
    total,
    basis: '按「小区 / 项目」「水箱（设施）」「小区 × 水箱」三档分组：每组给出水箱个数、清洗超期水箱数、'
      + '超期且仍在供水的水箱数、超期天数（最大 / 合计）、检测超期水箱数、缺少的常规指标项数、'
      + '超限值 / 低于限值项数、超标未闭环项数、消毒剂残留断档次数、停用废弃却在巡检的个数、'
      + '检测记录条数；排序按「超期天数最大 → 超期仍在供水个数 → 超标项数」降序，每组附一条可整改动作。',
  };
}

function buildConsolidatedActions(agg) {
  // 订阅版 ⑪：把每个水箱的问题合成一张整改清单（超期天数降序）
  const rows = [];
  for (const a of agg) {
    const issues = [];
    if (a.overdue_in_supply) {
      const bits = [];
      if (a.clean_overdue_days > 0) bits.push(`清洗超期 ${a.clean_overdue_days} 天`);
      if (!a.tested) bits.push('查不到有效检测日期（未检测）');
      else if (a.test_overdue_days > 0) bits.push(`检测超期 ${a.test_overdue_days} 天`);
      issues.push(`供水状态在供水但${bits.join('、')}`);
    } else if (a.clean_overdue_days > 0) {
      issues.push(`清洗超期 ${a.clean_overdue_days} 天`);
    }
    if (a.missing_items.length) issues.push(`常规指标缺 ${a.missing_items.join('、')}`);
    if (a.over_count > 0) issues.push(`检测结果超限值 ${a.over_count} 项`);
    if (a.under_count > 0) issues.push(`检测结果低于限值 ${a.under_count} 项`);
    if (a.open_over_limit > 0) issues.push(`超标未闭环 ${a.open_over_limit} 项`);
    if (a.disinfectant_gap_times > 0) issues.push(`消毒剂残留断档 ${a.disinfectant_gap_times} 次`);
    if (a.stale_in_patrol) issues.push(`台账已${a.status}但巡检记录有 ${a.patrol_records} 条`);
    if (!issues.length) continue;
    let action;
    if (a.overdue_in_supply) {
      action = '当天安排清洗消毒与水质检测 → 书面报物业负责人与卫生监督 → 检测合格后更新台账并留档';
    } else if (a.clean_overdue_days > 0) {
      action = '排进本月清洗消毒计划 → 清洗后补做水质检测 → 更新上次 / 下次清洗日期并归档记录单';
    } else if (a.stale_in_patrol) {
      action = '现场核实是否真的停用 / 废弃 → 断开与管网的联系并挂牌 → 补齐停用手续 → 清理巡检记录';
    } else if (a.open_over_limit > 0) {
      action = '同一样点同一项目复采复检 → 倒查消毒与投加设备 → 整改后把复检日期与结果填进复检记录';
    } else if (a.over_count > 0 || a.under_count > 0) {
      action = '复核该项检测报告与限值口径 → 必要时复采复检 → 整改后重新检测并留痕';
    } else if (a.missing_items.length) {
      action = '补采水样做齐缺的常规指标 → 补齐检测报告后再归档这本台账';
    } else if (a.disinfectant_gap_times > 0) {
      action = '按次补做消毒剂残留检测（缺哪一次补哪一次）→ 用检测报告或自检记录回填';
    } else {
      action = '核对本水箱的清洗与检测记录口径，确认是否属于台账笔误';
    }
    rows.push({
      tank_no: a.tank_no,
      tank_name: a.tank_name,
      community: a.community,
      line: a.first_line,
      status: a.status,
      level: (a.overdue_in_supply || a.stale_in_patrol || a.open_over_limit > 0) ? 'P0' : 'P1',
      clean_overdue_days: a.clean_overdue_days,
      test_overdue_days: a.test_overdue_days,
      issue: issues.join('；'),
      action,
    });
  }
  rows.sort((x, y) => (Math.max(y.clean_overdue_days, y.test_overdue_days) - Math.max(x.clean_overdue_days, x.test_overdue_days))
    || (y.clean_overdue_days - x.clean_overdue_days)
    || (x.line - y.line));
  return rows.map((r, i) => Object.assign({ seq: i + 1 }, r));
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的二次供水清洗消毒与水质检测台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的二次供水清洗消毒与水质检测台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的二次供水清洗消毒与水质检测台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行水箱检测明细（现在只有表头或只有合计行，没有可核对的水箱）']);
  }

  const paid = Boolean(payload && (payload.full || payload.credit || payload.token));
  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];
  const dataNotes = [];
  let rollup = null;
  let consolidated = null;

  for (const f of checkCleanCycle(t.items, base)) findings.push(f);
  for (const f of checkTestItemsAndLimits(t.items)) findings.push(f);
  for (const f of checkCleaningQualification(t.items, base)) findings.push(f);
  for (const f of checkDuplicateCleaning(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (paid) {
    const sections = parseSections(text);
    const disinfectant = readDisinfectant(sections);
    const patrol = readPatrol(sections);
    const recheck = readRecheck(sections);
    const ctx = {
      base,
      hasSupplyStatus: t.cols.some((c) => c.role === 'supplyStatus'),
      disinfectant,
      patrol,
      recheck,
      patrolByTank: new Map(),
      disinfectantByKey: new Map(),
      recheckByKey: new Map(),
    };
    for (const r of patrol.rows) {
      if (!r.tank_no) continue;
      if (!ctx.patrolByTank.has(r.tank_no)) ctx.patrolByTank.set(r.tank_no, []);
      ctx.patrolByTank.get(r.tank_no).push(r);
    }
    ctx.disinfectantByKey = indexBy(disinfectant.rows, (r) => (r.tank_no && r.date ? r.tank_no + '|' + r.date : ''));
    ctx.recheckByKey = indexBy(recheck.rows, (r) => (r.tank_no && r.item ? r.tank_no + '|' + r.item : ''));

    const agg = buildTankAggregates(t.items, ctx);
    for (const a of agg) {
      for (const f of checkOverdueSupply(a, ctx)) findings.push(f);
      for (const f of checkStaleInPatrol(a, ctx)) findings.push(f);
      for (const f of checkRecheckClosure(a, ctx)) findings.push(f);
      for (const f of checkDisinfectantGaps(a, ctx)) findings.push(f);
    }

    if (!ctx.hasSupplyStatus) {
      dataNotes.push('材料里没有「供水状态」列：第 7 项（超期未清洗或未检测仍在供水）与 '
        + '第 8 项（停用废弃水箱仍在巡检记录）本次**没有执行** —— 这不等于没问题。');
    }
    if (!patrol.present) {
      dataNotes.push('材料里没有「巡检记录」段：第 8 项跨表核对本次**没有执行** —— 这不等于没问题。');
    } else if (patrol.missing.length) {
      dataNotes.push('「' + patrol.name + '」段里认不出这些必需列：' + patrol.missing.join('、')
        + '；第 8 项本次**没有完整执行** —— 不等于没问题。');
    }
    if (!recheck.present) {
      dataNotes.push('材料里没有「复检记录」段：第 9 项（检测结果超标未闭环）本次**没有执行** —— 这不等于没问题。');
    } else if (recheck.missing.length) {
      dataNotes.push('「' + recheck.name + '」段里认不出这些必需列：' + recheck.missing.join('、')
        + '；第 9 项本次**没有完整执行** —— 不等于没问题。');
    }
    if (!disinfectant.present) {
      dataNotes.push('材料里没有「消毒剂残留检测记录」段：第 10 项（消毒剂残留检测断档）本次**没有执行** —— 这不等于没问题。');
    } else if (disinfectant.missing.length) {
      dataNotes.push('「' + disinfectant.name + '」段里认不出这些必需列：' + disinfectant.missing.join('、')
        + '；第 10 项本次**没有完整执行** —— 不等于没问题。');
    }

    rollup = buildRollup(agg);
    consolidated = buildConsolidatedActions(agg);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const overdueRows = findings.filter((f) => f.category === '清洗超期');
  const cleanOverdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);
  const communities = new Set(t.detail.map((it) => cell(it, 'community')).filter(Boolean));

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      communities: communities.size,
      water_tanks: t.totals.tankCount,
      test_records: t.totals.itemCount,
      clean_overdue_tanks: overdueRows.length,
      clean_overdue_days_max: cleanOverdueMax,
      check_date: base,
      basis: '核对基准日（表内「核对基准日」，逐行为准、缺行用表内第一个）− 上次清洗日期 ≤ 180 天，才算清洗周期被覆盖；'
        + '「下次清洗日期」必须等于「上次清洗日期 + 180 天」；'
        + '按水箱核对常规指标子集（色度 / 浑浊度 / pH / 游离余氯 / 菌落总数 / 总大肠菌群）是否齐全，'
        + '并逐项判定检测结果是否越过限值（单值按上限、区间按上下限、带比较符按对应边界、「不得检出」按定性）；'
        + '清洗单位 / 清洗人员不得空缺，健康证有效期要覆盖本次清洗作业日；'
        + '同一水箱编号 + 同一上次清洗日期下不得出现矛盾的清洗单位 / 清洗人员；'
        + '合计行的水箱数 = 不重复水箱编号个数、检测项数 = 明细行数；'
        + '供水状态只认 在供水 / 停用 / 废弃 三个值。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本台账按上面写明的口径算得对、'
      + '清洗周期与检测项目 / 限值都对得上**，不代表水箱现场真的已经清洗过、'
      + '不代表水样采集与实验室检测过程规范、也不代表清洗单位资质与健康证的真伪已经核验 —— 那些不在本工具范围内。'
      + (dataNotes.length ? '（注意：' + dataNotes.join('；') + '）' : '');
  }

  const scope = {
    checks: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    water_tanks: t.totals.tankCount,
    test_records: t.totals.itemCount,
    check_date: base,
  };
  result.scope = scope;
  if (dataNotes.length) result.data_notes = dataNotes;

  if (paid) {
    result.rollup = rollup;
    result.consolidated_actions = consolidated;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, addDays,
  judgeResult, parseLimit, tankGroups,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, REQUIRED_TEST_ITEMS,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
