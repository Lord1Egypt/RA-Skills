#!/usr/bin/env node
/**
 * subcontractor-qualification-check-full.js —— 分包商资质与安全许可核对引擎（**订阅版 / 买断版**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：总包/发包方对分包商资质负**连带责任**，商务与安全部**每月**必须把这张台账核一遍 ——
 *   ① 营业执照 / 资质证书 / 安全生产许可证 / 特种作业人员证件 的有效期必须**覆盖整个作业期**
 *      （进场到退场之间任一天证件失效，出了事故总包一起担责，招投标与检查也直接判不合格）
 *   ② 分包工程类别**要求的资质等级**与分包商**实际持证等级**要对得上（按等级序比较）
 *   ③ 在册特种作业人员清单要与证件清单对得上（缺证、多证、姓名对不上）
 *   ④ 同一分包商同一证件号重复登记（改了一个字段没改另一个，检查时被判资料不实）
 *   ⑤ 合同金额在同一个分包商的各证件行之间要一致；出现「合计」行时合计列要能对上
 *   ⑥ 空白/占位符/日期写成看不懂的形态/证件状态不在允许取值内
 *
 * 本文件是**订阅版（买断）**：在本包六项之上多出 5 项 ——
 *   社保/工伤保险缴纳覆盖（缺月点名）、分包再分包（转包）线索、证件类型齐全性、
 *   退场日期与证件注销/变更记录一致性、以及 分包商×证件汇总清单 与 consolidated_actions。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定分包商是否具备承接资格/能否中标、不核验证件真伪、不解释招标门槛口径、
 *          不读 .xlsx/.pdf/图片原件；材料不足**一律不给结论**。
 *
 * ⚠️ 免费包由 `tools/strip_free_engine.py` 从本文件摘出（形态 B）：
 *    · 开关常量在入口 `run` 里**只声明一次**，付费检查全部包在 `if (开关) { … }` 块里；
 *    · 付费专用实现写成顶层函数，摘除时按「删完付费分支后没人再引用」整块删掉
 *      ⇒ 付费函数**绝不能**被顶层的常量/数组/映射表引用（那样免费包会 ReferenceError）；
 *    · 注释里不要复述开关那一行的源码（残渣断言是**纯字符串包含**判断）；
 *    · 不要留「订阅版才执行的检查」那类 MARKER（两个形态同时存在会走形态 A 把免费检查也删掉）。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '证件有效期覆盖（逐行逐证：进场日期与退场日期都不得晚于 营业执照/资质证书/安全生产许可证/特种作业操作证 的到期日，否则点名该证、日期与缺口天数）',
  '资质等级匹配（按等级序比较「要求资质等级」与「持证资质等级」，持证等级低于要求即报出）',
  '人员-证件一致性（「在册特种作业人员清单」与特种作业/操作证类证件清单对账：缺证、多证、姓名对不上）',
  '同一分包商+同一证件号重复登记（同一分包商同一证件号出现两次及以上即报出，并指出首次出现行号）',
  '合同金额勾稽（同一分包商各证件行的合同金额必须一致；有「合计/小计/总计」行时，该行合同金额须等于按分包商去重后的合同金额合计）',
  '空白/占位符/日期格式/状态非法检测（关键字段空白或写成占位符、日期无法解析、证件状态不在允许取值内，逐处点名）',
];

const CHECKS_WITHHELD = [
  '社保/工伤保险缴纳覆盖（应缴月份 vs 已缴月份，缺哪个月点名到月）',
  '分包再分包（转包）线索（同一工程出现第二层分包商，或再分包金额合计超过合同金额）',
  '证件类型齐全性（按分包工程类别应有的证件清单逐项检查缺失）',
  '退场日期与证件注销/变更记录一致性（退场早于进场、注销/变更无日期、注销变更日期晚于退场日期）',
  '分包商×证件汇总清单与 consolidated_actions（按风险等级排序、给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定分包商是否**具备承接资格**、能不能中标（那是招标人与主管部门的认定权），本工具只核台账字段的字面一致性',
  '核验证件本身**真伪**（是否伪造、是否已被撤销/暂扣）—— 不联网查全国建筑市场监管公共服务平台等外部库',
  '解释招标文件/合同里具体的资质门槛口径（只按「等级序」做字面比较，不做政策解释与例外判断）',
  '读取 .xlsx/.pdf/图片原件、替代安全审查、法律意见或监管备案',
];

// 样例：一张**干净**的分包商资质与安全许可台账（一个证件一行，分包商与合同字段逐行重复）——
// 三个分包商共 12 行：证件类型齐全、有效期全部覆盖进场到退场、等级满足要求、
// 在册特种作业人员与证件一一对应、无重复证件号、合同金额各行一致、社保月份缴齐。
// ⚠️ 统一社会信用代码/证件编号一律**掩码形态**（如 91320100MA1********X），企业与人名均为编造。
const SAMPLE_TEXT = [
  '分包商名称\t统一社会信用代码\t分包工程类别\t要求资质等级\t持证资质等级\t营业执照到期日\t资质证书到期日\t安全生产许可证到期日\t进场日期\t退场日期\t合同金额\t证件名称\t证件编号\t持证人\t证件到期日\t上级分包商\t再分包金额\t在册特种作业人员清单\t证件状态\t注销变更日期\t社保应缴月份\t社保已缴月份\t工程名称\t备注',
  '江苏宏建机电安装工程有限公司\t91320100MA1********X\t建筑机电安装工程\t建筑机电安装工程专业承包二级\t建筑机电安装工程专业承包二级\t2028-06-30\t2027-12-31\t2027-03-31\t2026-03-01\t2026-12-31\t1860000.00\t营业执照\t91320100MA1********X\t王建国\t2028-06-30\t华宇建设集团有限公司\t0.00\t李明;张伟\t有效\t\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t江宁智造园机电安装工程\t资质与安全许可台账按月复核',
  '江苏宏建机电安装工程有限公司\t91320100MA1********X\t建筑机电安装工程\t建筑机电安装工程专业承包二级\t建筑机电安装工程专业承包二级\t2028-06-30\t2027-12-31\t2027-03-31\t2026-03-01\t2026-12-31\t1860000.00\t建筑业企业资质证书\tD2340512****\t王建国\t2027-12-31\t华宇建设集团有限公司\t0.00\t李明;张伟\t有效\t\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t江宁智造园机电安装工程\t资质证书在有效期内',
  '江苏宏建机电安装工程有限公司\t91320100MA1********X\t建筑机电安装工程\t建筑机电安装工程专业承包二级\t建筑机电安装工程专业承包二级\t2028-06-30\t2027-12-31\t2027-03-31\t2026-03-01\t2026-12-31\t1860000.00\t安全生产许可证\t(苏)JZ安许证字〔2024〕05****\t王建国\t2027-03-31\t华宇建设集团有限公司\t0.00\t李明;张伟\t有效\t\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t江宁智造园机电安装工程\t安许证在有效期内',
  '江苏宏建机电安装工程有限公司\t91320100MA1********X\t建筑机电安装工程\t建筑机电安装工程专业承包二级\t建筑机电安装工程专业承包二级\t2028-06-30\t2027-12-31\t2027-03-31\t2026-03-01\t2026-12-31\t1860000.00\t特种作业操作证（低压电工）\tT32010****0027\t李明\t2027-06-30\t华宇建设集团有限公司\t0.00\t李明;张伟\t有效\t\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t江宁智造园机电安装工程\t李明在册，证件在有效期内',
  '江苏宏建机电安装工程有限公司\t91320100MA1********X\t建筑机电安装工程\t建筑机电安装工程专业承包二级\t建筑机电安装工程专业承包二级\t2028-06-30\t2027-12-31\t2027-03-31\t2026-03-01\t2026-12-31\t1860000.00\t特种作业操作证（高处作业）\tT32010****0043\t张伟\t2027-05-31\t华宇建设集团有限公司\t0.00\t李明;张伟\t有效\t\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t2026-03;2026-04;2026-05;2026-06;2026-07;2026-08\t江宁智造园机电安装工程\t张伟在册，证件在有效期内',
  '苏州恒固建筑劳务有限公司\t91320500MA2********X\t房屋建筑工程\t施工劳务不分等级\t施工劳务不分等级\t2027-08-31\t2027-02-28\t2026-12-31\t2026-02-01\t2026-11-30\t2400000.00\t营业执照\t91320500MA2********X\t陈立\t2027-08-31\t华宇建设集团有限公司\t0.00\t赵强;孙丽\t有效\t\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t苏州园区人才公寓主体结构劳务\t资质与安全许可台账按月复核',
  '苏州恒固建筑劳务有限公司\t91320500MA2********X\t房屋建筑工程\t施工劳务不分等级\t施工劳务不分等级\t2027-08-31\t2027-02-28\t2026-12-31\t2026-02-01\t2026-11-30\t2400000.00\t建筑业企业资质证书\tD3320567****\t陈立\t2027-02-28\t华宇建设集团有限公司\t0.00\t赵强;孙丽\t有效\t\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t苏州园区人才公寓主体结构劳务\t资质证书在有效期内',
  '苏州恒固建筑劳务有限公司\t91320500MA2********X\t房屋建筑工程\t施工劳务不分等级\t施工劳务不分等级\t2027-08-31\t2027-02-28\t2026-12-31\t2026-02-01\t2026-11-30\t2400000.00\t安全生产许可证\t(苏)JZ安许证字〔2024〕11****\t陈立\t2026-12-31\t华宇建设集团有限公司\t0.00\t赵强;孙丽\t有效\t\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t苏州园区人才公寓主体结构劳务\t安许证在有效期内',
  '苏州恒固建筑劳务有限公司\t91320500MA2********X\t房屋建筑工程\t施工劳务不分等级\t施工劳务不分等级\t2027-08-31\t2027-02-28\t2026-12-31\t2026-02-01\t2026-11-30\t2400000.00\t特种作业操作证（建筑电工）\tT32050****0118\t赵强\t2027-04-30\t华宇建设集团有限公司\t0.00\t赵强;孙丽\t有效\t\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t苏州园区人才公寓主体结构劳务\t赵强在册，证件在有效期内',
  '苏州恒固建筑劳务有限公司\t91320500MA2********X\t房屋建筑工程\t施工劳务不分等级\t施工劳务不分等级\t2027-08-31\t2027-02-28\t2026-12-31\t2026-02-01\t2026-11-30\t2400000.00\t特种作业操作证（架子工）\tT32050****0126\t孙丽\t2027-01-31\t华宇建设集团有限公司\t0.00\t赵强;孙丽\t有效\t\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t2026-02;2026-03;2026-04;2026-05;2026-06;2026-07\t苏州园区人才公寓主体结构劳务\t孙丽在册，证件在有效期内',
  '无锡安泰物业服务有限公司\t91320200MA3********X\t物业服务\t物业服务企业资质二级\t物业服务企业资质二级\t2028-12-31\t2027-09-30\t\t2026-01-05\t2026-12-31\t960000.00\t营业执照\t91320200MA3********X\t周敏\t2028-12-31\t华宇建设集团有限公司\t0.00\t\t有效\t\t2026-01;2026-02;2026-03;2026-04;2026-05;2026-06\t2026-01;2026-02;2026-03;2026-04;2026-05;2026-06\t无锡新吴区产业园物业管理服务\t物业服务，不涉及安全生产许可证',
  '无锡安泰物业服务有限公司\t91320200MA3********X\t物业服务\t物业服务企业资质二级\t物业服务企业资质二级\t2028-12-31\t2027-09-30\t\t2026-01-05\t2026-12-31\t960000.00\t物业服务企业资质证书\tWXPM-2023-****\t周敏\t2027-09-30\t华宇建设集团有限公司\t0.00\t\t有效\t\t2026-01;2026-02;2026-03;2026-04;2026-05;2026-06\t2026-01;2026-02;2026-03;2026-04;2026-05;2026-06\t无锡新吴区产业园物业管理服务\t资质证书在有效期内',
].join('\n');

const TOL = 0.01;
const DAY = 86400000;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = ['subName', 'creditCode', 'workType', 'requiredLevel', 'heldLevel',
  'licenseExpiry', 'qualExpiry', 'safetyExpiry', 'entryDate', 'exitDate', 'contractAmount',
  'docName', 'docNo', 'holder', 'docExpiry'];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）。
// ⚠️ 营业执照/资质证书/安全生产许可证 三个到期日**不在**这里：不是每个分包商都持有每一类证件
//    （物业没有安全生产许可证是正常的），空着只表示不适用，由有效期覆盖那一项自行跳过。
const REQUIRED_CELL_FIELDS = [
  ['subName', '分包商名称'],
  ['creditCode', '统一社会信用代码'],
  ['workType', '分包工程类别'],
  ['requiredLevel', '要求资质等级'],
  ['heldLevel', '持证资质等级'],
  ['contractAmount', '合同金额'],
  ['docName', '证件名称'],
  ['docNo', '证件编号'],
  ['holder', '持证人'],
  ['entryDate', '进场日期'],
  ['docExpiry', '证件到期日'],
];

// 有效期覆盖要逐证核对的四类到期日
const EXPIRY_FIELDS = [
  ['licenseExpiry', '营业执照到期日'],
  ['qualExpiry', '资质证书到期日'],
  ['safetyExpiry', '安全生产许可证到期日'],
  ['docExpiry', '证件到期日'],
];

// 日期列（格式非法逐处点名）
const DATE_FIELDS = [
  ['licenseExpiry', '营业执照到期日'],
  ['qualExpiry', '资质证书到期日'],
  ['safetyExpiry', '安全生产许可证到期日'],
  ['entryDate', '进场日期'],
  ['exitDate', '退场日期'],
  ['docExpiry', '证件到期日'],
];

// 人员证件关键词（在册特种作业人员清单要能在这几类证件里找到对应的人）
const PERSON_DOC_KEYS = ['特种作业', '特种设备', '操作证', '上岗证', '作业人员证'];

// 证件状态允许取值（写别的值一律按「状态非法」逐处点名）
const ALLOWED_STATUS = ['有效', '换证中', '待换证', '已变更', '已注销', '已过期'];

// 等级序：数字越大等级越高。**顺序就是匹配顺序**，必须具体/高等级在前。
const LEVEL_TOKENS = [
  ['特级', 6], ['一级', 5], ['甲级', 5], ['二级', 4], ['乙级', 4],
  ['三级', 3], ['丙级', 3], ['四级', 2], ['丁级', 2], ['暂定级', 1], ['不分等级', 1],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过 6 次，见 tools/header_map_check.py）。
//    本表的顺序要点：上级分包商→分包商名称；分包工程类别→工程名称；
//    要求/持证资质等级→资质证书到期日；合同金额→再分包金额；
//    证件编号→证件到期日→证件状态→证件名称；在册人员清单→持证人（holder 有「姓名」这种宽泛词）。
const ROLES = {
  parentSub: ['上级分包商', '上游分包商', '上级单位', '总包单位', '发包方'],
  subName: ['分包商名称', '分包单位名称', '分包商', '分包单位', '供应商名称', '单位名称'],
  workType: ['分包工程类别', '分包工程类型', '工程类别', '分包类别', '专业类别', '工程类型'],
  projectName: ['工程名称', '项目名称', '工程项目', '工程', '项目'],
  creditCode: ['统一社会信用代码', '社会信用代码', '信用代码'],
  requiredLevel: ['要求资质等级', '要求等级', '所需资质等级', '资质要求等级', '资质要求'],
  heldLevel: ['持证资质等级', '持证等级', '持有资质等级', '持证资质'],
  licenseExpiry: ['营业执照到期日', '营业执照有效期', '营业执照失效日期', '营业执照'],
  qualExpiry: ['资质证书到期日', '资质证书有效期', '资质到期日', '资质证书'],
  safetyExpiry: ['安全生产许可证到期日', '安全生产许可证有效期', '安全许可证到期日', '安全生产许可证', '安全许可证'],
  entryDate: ['进场日期', '入场日期', '开工日期', '进场时间'],
  exitDate: ['退场日期', '离场日期', '退场时间', '完工日期'],
  contractAmount: ['合同金额', '分包合同金额', '合同价款', '合同总额', '签约金额'],
  subAmount: ['再分包金额', '转包金额', '分包合计', '分包金额'],
  docNo: ['证件编号', '证书编号', '证件号码', '证件号'],
  docExpiry: ['证件到期日', '证件有效期', '证书到期日', '证件失效日期'],
  docStatus: ['证件状态', '证书状态', '资质状态', '证件情况', '状态'],
  docName: ['证件名称', '证书名称', '证件种类', '证件'],
  roster: ['在册特种作业人员清单', '在册人员清单', '在册人员', '特种作业人员清单', '人员清单'],
  holder: ['持证人', '持证人姓名', '姓名'],
  changeDate: ['注销变更日期', '状态变更日期', '变更日期', '注销日期'],
  shouldMonths: ['社保应缴月份', '工伤保险应缴月份', '应缴社保月份', '应缴月份'],
  paidMonths: ['社保已缴月份', '工伤保险已缴月份', '实缴月份', '已缴月份'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  parentSub: '上级分包商',
  subName: '分包商名称',
  workType: '分包工程类别',
  projectName: '工程名称',
  creditCode: '统一社会信用代码',
  requiredLevel: '要求资质等级',
  heldLevel: '持证资质等级',
  licenseExpiry: '营业执照到期日',
  qualExpiry: '资质证书到期日',
  safetyExpiry: '安全生产许可证到期日',
  entryDate: '进场日期',
  exitDate: '退场日期',
  contractAmount: '合同金额',
  subAmount: '再分包金额',
  docNo: '证件编号',
  docExpiry: '证件到期日',
  docStatus: '证件状态',
  docName: '证件名称',
  roster: '在册特种作业人员清单',
  holder: '持证人',
  changeDate: '注销变更日期',
  shouldMonths: '社保应缴月份',
  paidMonths: '社保已缴月份',
  note: '备注',
};

const SUM_ROLES = ['contractAmount', 'subAmount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳，一个证件一行）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「资质齐全」，也不说「不合格」。',
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

/** 只认 YYYY-MM-DD / YYYY/M/D / YYYY.M.D / YYYY年M月D日，且必须是真实存在的日历日 */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/[日号]/g, '').replace(/[./]/g, '-').replace(/\s+/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const ts = Date.UTC(y, mo - 1, d);
  const dt = new Date(ts);
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return { y, mo, d, ts, key: `${m[1]}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}` };
}

/** 等级序：返回 {rank, token}；认不出（或空白）返回 null，交给字段完整性那一项去报 */
function levelRank(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw);
  for (const [tok, rank] of LEVEL_TOKENS) {
    if (s.indexOf(tok) >= 0) return { rank, token: tok };
  }
  const m = /([1-4])\s*级/.exec(s);
  if (m) {
    const d = Number(m[1]);
    return { rank: 5 - (d - 1), token: `${d}级` };
  }
  return null;
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

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

const textOf = (it, role) => String(it[role] == null ? '' : it[role]).trim();
const subName = (it) => textOf(it, 'subName');
const docNameOf = (it) => textOf(it, 'docName');
const projectOf = (it) => textOf(it, 'projectName');
const holderOf = (it) => textOf(it, 'holder');

/** 「合计/小计/总计/汇总」行：不是真实分包商，勾稽时单独处理 */
function isTotalRow(it) {
  return /合计|小计|总计|汇总/.test(subName(it));
}

function who(it) {
  const name = subName(it);
  const doc = docNameOf(it);
  const tag = [name, doc].filter(Boolean).join(' · ');
  return `第 ${it.line} 行「${tag || '未命名分包商'}」`;
}

function nameList(v) {
  return String(v == null ? '' : v).split(/[;；,，、/|\s]+/).map((s) => s.trim()).filter((s) => s !== '');
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 给结论打上「哪个分包商 / 哪类证件」的归属，供订阅版的汇总清单归集 */
function tagged(f, sub, doc) {
  if (sub) f.sub = sub;
  if (doc) f.doc = doc;
  return f;
}

function dayGap(from, to) {
  return Math.round((to.ts - from.ts) / DAY);
}

/* ============================ 本包检查（六项） ============================ */

/** 1. 证件有效期覆盖：进场日期与退场日期都不得晚于四类到期日（逐行逐证） */
function checkExpiryCoverage(items) {
  const out = [];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const entry = normDate(it.entryDate);
    const exit = normDate(it.exitDate);
    for (const [role, label] of EXPIRY_FIELDS) {
      const exp = normDate(it[role]);
      if (!exp) continue;                       // 空白/格式非法交给「字段完整性」那一项
      if (entry && entry.ts > exp.ts) {
        const gap = dayGap(exp, entry);
        out.push(finding('P0', '证件有效期未覆盖', it, -gap,
          `${who(it)}：「${label}」${exp.key} 在进场日期 ${entry.key} 之前就已到期（早 ${gap} 天）—— 进场当天该证已失效。`,
          '这一项直接决定能不能进场作业：先换证或换人，再补一份换证受理单；在换证下来之前不要安排进场。'));
        continue;
      }
      if (exit && exit.ts > exp.ts) {
        const gap = dayGap(exp, exit);
        out.push(finding('P0', '证件有效期未覆盖', it, -gap,
          `${who(it)}：退场日期 ${exit.key} 晚于「${label}」${exp.key}（合同期内有 ${gap} 天该证已失效）—— 作业期没有被证件有效期覆盖。`,
          '要么把证件续到覆盖退场日期，要么把退场日期改到证件到期日之前并留痕；'
          + '合同期内证件空档出事，总包与分包连带担责。'));
      }
    }
  }
  return out;
}

/** 2. 资质等级匹配：按等级序比较「要求资质等级」与「持证资质等级」 */
function checkLevelMatch(items) {
  const out = [];
  const seen = new Set();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    if (!sub) continue;
    const reqRaw = textOf(it, 'requiredLevel');
    const heldRaw = textOf(it, 'heldLevel');
    const key = `${sub}|${reqRaw}|${heldRaw}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const req = levelRank(reqRaw);
    const held = levelRank(heldRaw);
    if (!req || !held) continue;                // 空白/认不出等级交给「字段完整性」那一项
    if (held.rank >= req.rank) continue;
    out.push(finding('P0', '资质等级不满足要求', it, held.rank - req.rank,
      `${who(it)}：工程类别「${textOf(it, 'workType') || '(未填)'}」要求资质等级「${reqRaw}」（等级序 ${req.rank}），`
      + `分包商持证等级「${heldRaw}」（等级序 ${held.rank}）—— 持证等级低于要求 ${req.rank - held.rank} 档。`,
      '资质等级不够就是承接范围不匹配：要么换有对应等级的分包商，要么把工程范围拆到其持证等级允许的范围内'
      + '（本工具只按等级序做字面比较，不解释招标文件的具体门槛口径）。'));
  }
  return out;
}

/** 3. 人员-证件一致性：在册特种作业人员清单 vs 人员证件清单（缺证、多证、姓名对不上） */
function checkPeopleDocs(items) {
  const out = [];
  const subs = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    if (!sub) continue;
    if (!subs.has(sub)) subs.set(sub, { rows: [], roster: [], personRows: [] });
    const rec = subs.get(sub);
    rec.rows.push(it);
    for (const n of nameList(it.roster)) if (rec.roster.indexOf(n) < 0) rec.roster.push(n);
    const doc = docNameOf(it);
    if (PERSON_DOC_KEYS.some((k) => doc.indexOf(k) >= 0)) rec.personRows.push(it);
  }
  for (const [sub, rec] of subs) {
    const first = rec.rows[0];
    const holders = [];
    for (const r of rec.personRows) {
      const h = holderOf(r);
      if (h && holders.indexOf(h) < 0) holders.push(h);
    }
    if (!rec.personRows.length && !rec.roster.length) continue;   // 两边都没有 ⇒ 没什么可对，不给结论
    if (rec.personRows.length && !rec.roster.length) {
      out.push(finding('P1', '在册人员清单缺失', first, undefined,
        `「${sub}」有 ${rec.personRows.length} 张特种作业类证件（持证人：${holders.join('、') || '(未填)'}），`
        + '但「在册特种作业人员清单」是空的 —— 人员与证件没法对。',
        '把该项目在册的特种作业人员名单按分号填进「在册特种作业人员清单」（如 李明;张伟）后重跑；本工具不会替你推断名单。'));
      continue;   // 清单整列空 ⇒ 没有比对基准，只报「清单缺失」，不再顺带把每个人都报成"多证"
    }
    const noCert = rec.roster.filter((n) => holders.indexOf(n) < 0);
    const notOnRoster = holders.filter((n) => rec.roster.indexOf(n) < 0);
    if (noCert.length) {
      out.push(finding('P0', '人员与证件不一致', first, undefined,
        `「${sub}」在册人员 ${noCert.join('、')} 在证件清单里找不到对应的特种作业证件（缺证）—— `
        + `在册 ${rec.roster.length} 人，人员证件持证人只有 ${holders.length} 人（${holders.join('、') || '无'}）。`,
        '缺证的人不能上岗：补齐操作证并把证件编号与到期日登记进台账；对不上姓名的（同音字/别名）要统一成身份证姓名。'));
    }
    if (notOnRoster.length) {
      out.push(finding('P0', '人员与证件不一致', first, undefined,
        `「${sub}」证件上的持证人 ${notOnRoster.join('、')} 不在在册特种作业人员清单里（多证或姓名对不上）—— `
        + `清单：${rec.roster.join('、') || '无'}。`,
        '多出来的证件可能是人员已离场（应从在册清单与台账同时下架），也可能是姓名写错；先与身份证/花名册核对。'));
    }
  }
  return out;
}

/** 4. 同一分包商 + 同一证件号重复登记 */
function checkDuplicateCert(items) {
  const out = [];
  const first = new Map();
  const reported = new Set();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    const no = textOf(it, 'docNo');
    if (!sub || !no) continue;
    const key = `${sub}|${no}`;
    if (first.has(key)) {
      if (reported.has(it.line)) continue;
      reported.add(it.line);
      out.push(finding('P0', '证件重复登记', it, undefined,
        `${who(it)}：证件编号「${no}」在同一个分包商「${sub}」下第 ${first.get(key)} 行已经登记过 —— 同一证件重复登记。`,
        '一个证件只应有一行台账；分次换证请新增行并注明旧证失效日期，不要重复登记同一个证号。'
        + '重复登记会让「在册证件数」虚高，检查时会被判资料不实。'));
      continue;
    }
    first.set(key, it.line);
  }
  return out;
}

/** 5. 合同金额勾稽：同一分包商各行金额一致；「合计」行须等于按分包商去重后的合计 */
function checkContractAmount(items) {
  const out = [];
  const bySub = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    if (!sub) continue;
    if (!bySub.has(sub)) bySub.set(sub, []);
    bySub.get(sub).push(it);
  }
  let expected = 0;
  let counted = 0;
  for (const [sub, rows] of bySub) {
    const vals = [];
    for (const r of rows) {
      const v = normNumber(r.contractAmount);
      if (v === null) continue;
      if (!vals.some((x) => Math.abs(x.v - v) < TOL)) vals.push({ v, line: r.line });
    }
    if (vals.length > 1) {
      out.push(finding('P1', '合同金额勾稽不符', rows[rows.length - 1], round2(vals[vals.length - 1].v - vals[0].v),
        `「${sub}」的合同金额在各证件行上不一致：第 ${vals[0].line} 行 ${money(vals[0].v)}，`
        + vals.slice(1).map((x) => `第 ${x.line} 行 ${money(x.v)}`).join('，')
        + '（同一份分包合同只有一个金额，改过合同只改了一行、或串了行都会这样）。',
        '以合同原件为准统一各行金额；同一分包商的多行证件应共享同一个合同金额，不要按证件拆金额。'));
    }
    if (vals.length) {
      expected = round2(expected + vals[0].v);
      counted += 1;
    }
  }
  for (const it of items) {
    if (!isTotalRow(it)) continue;
    const v = normNumber(it.contractAmount);
    if (v === null) continue;
    const diff = round2(v - expected);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding('P1', '合同金额勾稽不符', it, diff,
      `${who(it)}：合计行合同金额 ${money(v)}，按 ${counted} 个分包商去重后的合同金额合计 ${money(expected)}，差 ${money(diff)}。`,
      '合计行必须等于各分包商合同金额之和（同一分包商多行只算一次）；差在哪个分包商，就回去核那一份合同与补充协议。'));
  }
  return out;
}

/** 6. 空白/占位符 + 日期格式 + 证件状态非法 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_CELL_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段空白或占位符', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw)) continue;
      out.push(finding('P1', '日期格式非法', it, undefined,
        `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期（只认 2026-03-01 / 2026/3/1 / 2026.3.1 / 2026年3月1日）。`,
        '把日期改成 YYYY-MM-DD 再跑；写成「2026.3」「3月」这类形态本工具不会当成某一天，也不会当成有效。'));
    }
    const status = textOf(it, 'docStatus');
    if (status && !ALLOWED_STATUS.some((s) => status.indexOf(s) >= 0)) {
      out.push(finding('P1', '状态非法', it, undefined,
        `${who(it)}：「证件状态」的值「${status}」不在允许取值内（允许：${ALLOWED_STATUS.join('/')}）。`,
        '状态是后续判断（退场与注销/变更是否对得上）的输入，先按台账口径改成允许的取值；'
        + '实在是别的状态的，请在备注里说明而不是随手填一个词。'));
    }
  }
  return out;
}

/* ===== 追加检查（仅订阅版执行；免费包里这些函数整块不在了） ===== */

/** 订阅版①：社保/工伤保险缴纳覆盖（应缴月份 vs 已缴月份；缺哪个月点名到月） */
function checkSocialInsurance(it, seen) {
  const out = [];
  if (isTotalRow(it)) return out;
  const sub = subName(it);
  if (!sub || seen.has(sub)) return out;
  seen.add(sub);
  return socialInsuranceFindings(it, sub);
}

/** 订阅版①的判定体：月份清单优先（点名到月），退而用月数，只有一边可读就如实报「没法核」 */
function socialInsuranceFindings(it, sub) {
  const out = [];
  const doc = docNameOf(it);
  const shouldRaw = it.shouldMonths;
  const paidRaw = it.paidMonths;
  if (isBlank(shouldRaw) && isBlank(paidRaw)) return out;
  const should = parseMonths(shouldRaw);
  const actual = parseMonths(paidRaw);
  if (should && actual) {
    const missing = should.filter((m) => actual.indexOf(m) < 0);
    const extra = actual.filter((m) => should.indexOf(m) < 0);
    if (missing.length) {
      out.push(tagged(finding('P0', '社保缴纳未覆盖', it, -missing.length,
        `「${sub}」应缴 ${should.length} 个月（${should[0]} ~ ${should[should.length - 1]}），`
        + `已缴清单里缺 ${missing.length} 个月 —— ${missing.join('、')}。`,
        '按缺的月份让分包商补缴，并把补缴凭证按月份钉进台账；缺月期间发生工伤，总包要连带。'
        + '本工具只按台账列出的月份比对，不代替社保经办机构的缴费记录。'), sub, doc));
    }
    if (extra.length) {
      out.push(tagged(finding('P2', '社保缴纳未覆盖', it, extra.length,
        `「${sub}」已缴清单里多出 ${extra.length} 个月（${extra.join('、')}），不在应缴范围内 —— 核对是否串到了别的分包商或别的项目。`,
        '多缴月份通常是台账串行或把别的项目的人算进来了；按分包商单独建缴费台账，不要混在一张表里。'), sub, doc));
    }
    return out;
  }
  const nShould = normNumber(shouldRaw);
  const nPaid = normNumber(paidRaw);
  if (nShould !== null && nPaid !== null) {
    if (nPaid < nShould - TOL) {
      out.push(tagged(finding('P0', '社保缴纳未覆盖', it, round2(nPaid - nShould),
        `「${sub}」应缴 ${nShould} 个月，已缴 ${nPaid} 个月，缺 ${round2(nShould - nPaid)} 个月（台账只给了月数，没给月份）。`,
        '补上「应缴月份 / 已缴月份」两列的**具体月份**（如 2026-03;2026-04），本工具才能点名缺哪个月。'), sub, doc));
    }
    return out;
  }
  out.push(tagged(finding('P1', '社保缴纳未覆盖', it, undefined,
    `「${sub}」的社保缴纳情况只有一边能读出来（应缴月份「${textOf(it, 'shouldMonths') || '(空)'}」／`
    + `已缴月份「${textOf(it, 'paidMonths') || '(空)'}」），这一项没法核。`,
    '应缴与已缴两列都给全（月份用分号分隔）；只给月数就点名不到具体缺哪个月，只给一边则没有比对基准。'), sub, doc));
  return out;
}

/** 月份清单解析：只认 4 位年在前的月份形态（2026-03 / 2026年3月 / 2026/3），否则返回 null */
function parseMonths(raw) {
  if (isBlank(raw)) return null;
  const toks = String(raw).split(/[;；,，、/|\s]+/).map((s) => s.trim()).filter(Boolean);
  if (!toks.length) return null;
  const set = [];
  for (const t of toks) {
    const m = /^(\d{4})\D*(\d{1,2})(?:\D+\d{1,2})?\D*$/.exec(t);
    if (!m) return null;
    const mo = Number(m[2]);
    if (mo < 1 || mo > 12) return null;
    const key = `${m[1]}-${String(mo).padStart(2, '0')}`;
    if (set.indexOf(key) < 0) set.push(key);
  }
  return set.sort();
}

/** 订阅版②：分包再分包（转包）线索 —— 第二层分包商，或再分包金额合计 > 合同金额 */
function checkSubcontracting(it, ctx) {
  const out = [];
  if (isTotalRow(it)) return out;
  const sub = subName(it);
  if (!sub) return out;
  const doc = docNameOf(it);
  const parent = textOf(it, 'parentSub');
  if (parent && parent !== sub && ctx.names.has(parent)) {
    out.push(tagged(finding('P0', '疑似转包或再分包', it, undefined,
      `${who(it)}：上级分包商「${parent}」本身也是本表里的分包商 —— 同一工程出现**第二层分包**（转包线索）。`,
      '主体结构不得分包、分包不得再分包：先核发包方是否书面同意，再查是否属于违法转包；'
      + '确属专业分包的要有分包合同备案，本工具只报线索、不认定违法。'), sub, doc));
  }
  const key = `${projectOf(it) || '(未填工程)'}|${sub}`;
  if (ctx.amountSeen.has(key)) return out;
  ctx.amountSeen.add(key);
  const agg = ctx.amountIndex.get(key);
  if (agg && agg.contract !== null && agg.sum > agg.contract + TOL) {
    const diff = round2(agg.sum - agg.contract);
    out.push(tagged(finding('P0', '疑似转包或再分包', it, diff,
      `「${sub}」在工程「${projectOf(it) || '(未填工程)'}」上的再分包金额合计 ${money(agg.sum)}`
      + ` 超过其分包合同金额 ${money(agg.contract)}（超出 ${money(diff)}，涉及第 ${agg.lines.join('、')} 行）——`
      + '分包合计大于合同金额，通常意味着把活整包转出去了（或重复记了再分包）。',
      '把再分包合同与结算单按工程归集，逐笔核到发包方书面同意与备案；金额对不上先查是不是重复登记。'), sub, doc));
  }
  return out;
}

/** 订阅版②的上下文：本表出现过的分包商名 + 按（工程×分包商）归集的再分包金额 */
function buildSubContractCtx(items) {
  const names = new Set();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const s = subName(it);
    if (s) names.add(s);
  }
  const amountIndex = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    if (!sub) continue;
    const key = `${projectOf(it) || '(未填工程)'}|${sub}`;
    if (!amountIndex.has(key)) amountIndex.set(key, { sum: 0, contract: null, lines: [] });
    const agg = amountIndex.get(key);
    const a = normNumber(it.subAmount);
    if (a !== null) agg.sum = round2(agg.sum + a);
    if (agg.contract === null) agg.contract = normNumber(it.contractAmount);
    if (agg.lines.indexOf(it.line) < 0) agg.lines.push(it.line);
  }
  return { names, amountIndex, amountSeen: new Set() };
}

/** 订阅版③：按分包工程类别应有的证件清单，逐类检查缺失 */
function checkDocTypeCompleteness(it, subIndex) {
  const out = [];
  if (isTotalRow(it)) return out;
  const sub = subName(it);
  const rec = subIndex.get(sub);
  if (!rec || rec.done) return out;
  rec.done = true;
  const need = requiredDocTypes(rec.workType);
  const have = rec.docs;
  const missing = need.filter((n) => !have.some((d) => d.indexOf(n) >= 0));
  if (!missing.length) return out;
  out.push(tagged(finding('P1', '证件类型缺失', it, undefined,
    `「${sub}」分包工程类别「${rec.workType || '(未填)'}」按口径应备 ${need.length} 类证件（${need.join('、')}），`
    + `现在缺 ${missing.length} 类 —— ${missing.join('、')}（现有证件：${have.join('、') || '无'}；涉及第 ${rec.lines.join('、')} 行）。`,
    '按工程类别把缺的证件类型补进台账并附原件扫描件；本工具只核**证件类型字面是否点到**，不判断证件内容是否合格。'), sub));
  return out;
}

/** 按分包工程类别给应有证件清单（口径写在代码里，可被第三方复算） */
function requiredDocTypes(workType) {
  const t = String(workType == null ? '' : workType);
  if (/建筑|施工|安装|市政|装饰|机电|工程|建设|劳务/.test(t)) {
    return ['营业执照', '资质证书', '安全生产许可证', '特种作业操作证'];
  }
  if (/制造|生产|加工|设备|维修|修理/.test(t)) {
    return ['营业执照', '安全生产许可证', '特种作业操作证'];
  }
  if (/物业|保洁|绿化|服务|餐饮|安保/.test(t)) {
    return ['营业执照', '资质证书'];
  }
  return ['营业执照', '资质证书'];
}

/** 订阅版③的上下文：分包商 → 工程类别 + 现有证件名称集合 */
function buildDocIndex(items) {
  const index = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const sub = subName(it);
    if (!sub) continue;
    if (!index.has(sub)) index.set(sub, { workType: '', docs: [], lines: [], done: false });
    const rec = index.get(sub);
    if (!rec.workType) rec.workType = textOf(it, 'workType');
    const doc = docNameOf(it);
    if (doc && rec.docs.indexOf(doc) < 0) rec.docs.push(doc);
    if (rec.lines.indexOf(it.line) < 0) rec.lines.push(it.line);
  }
  return index;
}

/** 订阅版④：退场日期与证件注销/变更记录一致性 */
function checkExitConsistency(it) {
  const out = [];
  if (isTotalRow(it)) return out;
  const sub = subName(it);
  const doc = docNameOf(it);
  const entry = normDate(it.entryDate);
  const exit = normDate(it.exitDate);
  const chg = normDate(it.changeDate);
  const status = textOf(it, 'docStatus');
  const cancelled = status.indexOf('已注销') >= 0 || status.indexOf('已变更') >= 0;
  if (entry && exit && exit.ts < entry.ts) {
    out.push(tagged(finding('P1', '退场与注销/变更记录不一致', it, -dayGap(exit, entry),
      `${who(it)}：退场日期 ${exit.key} 早于进场日期 ${entry.key}（早 ${dayGap(exit, entry)} 天）—— 作业期本身不成立。`,
      '先确认是进场日期抄错还是退场日期抄错；退场早于进场的记录会让"合同期内是否持续有效"完全没法核。'), sub, doc));
  }
  if (cancelled && !chg) {
    out.push(tagged(finding('P1', '退场与注销/变更记录不一致', it, undefined,
      `${who(it)}：证件状态是「${status}」，但没有「注销/变更日期」—— 无法与退场日期核对。`,
      '注销/变更必须留日期：把受理单或变更记录上的日期填进「注销变更日期」，并确认它落在作业期内。'), sub, doc));
  }
  if (chg && exit && chg.ts > exit.ts) {
    out.push(tagged(finding('P1', '退场与注销/变更记录不一致', it, dayGap(exit, chg),
      `${who(it)}：「注销变更日期」${chg.key} 晚于退场日期 ${exit.key}（晚 ${dayGap(exit, chg)} 天）—— 人和证都退场了才注销/变更。`,
      '退场当天就应同步办注销/变更并在台账留痕；日期对不上说明台账是事后补的，检查时会被追问。'), sub, doc));
  }
  if (chg && entry && chg.ts < entry.ts) {
    out.push(tagged(finding('P1', '退场与注销/变更记录不一致', it, -dayGap(chg, entry),
      `${who(it)}：「注销变更日期」${chg.key} 早于进场日期 ${entry.key}（早 ${dayGap(chg, entry)} 天）—— 进场时该证已经注销/变更过。`,
      '先核进场时用的到底是哪一张证：若是换证后的新证，请把新证的编号与到期日登记为独立一行。'), sub, doc));
  }
  return out;
}

/** 订阅版⑤：分包商 × 证件 的汇总清单（按风险等级排序，每个证件给出可整改动作） */
function buildRollup(items, findings) {
  const RISK = ['高风险', '中风险', '低风险', '无问题'];
  const subs = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const s = subName(it) || '(未填分包商)';
    const d = docNameOf(it) || '(未填证件)';
    if (!subs.has(s)) subs.set(s, { sub: s, rows: 0, lines: [], docs: new Map(), findings: [] });
    const rec = subs.get(s);
    rec.rows += 1;
    if (rec.lines.indexOf(it.line) < 0) rec.lines.push(it.line);
    if (!rec.docs.has(d)) rec.docs.set(d, { doc: d, rows: 0, findings: [] });
    rec.docs.get(d).rows += 1;
  }
  for (const f of findings) {
    if (!f.sub || !subs.has(f.sub)) continue;
    const rec = subs.get(f.sub);
    rec.findings.push(f);
    if (f.doc && rec.docs.has(f.doc)) rec.docs.get(f.doc).findings.push(f);
  }
  const rankOf = (p0, p1, p2) => (p0 > 0 ? 0 : (p1 > 0 ? 1 : (p2 > 0 ? 2 : 3)));
  const counts = (list) => ({
    p0: list.filter((f) => f.level === 'P0').length,
    p1: list.filter((f) => f.level === 'P1').length,
    p2: list.filter((f) => f.level === 'P2').length,
  });
  const bySub = [];
  let docCount = 0;
  for (const rec of subs.values()) {
    const c = counts(rec.findings);
    const riskRank = rankOf(c.p0, c.p1, c.p2);
    const docs = [];
    for (const d of rec.docs.values()) {
      const dc = counts(d.findings);
      const dRank = rankOf(dc.p0, dc.p1, dc.p2);
      docCount += 1;
      const ordered = d.findings.slice().sort((a, b) => String(a.level).localeCompare(String(b.level))
        || (a.line - b.line));
      docs.push({
        doc: d.doc,
        rows: d.rows,
        findings: d.findings.length,
        p0: dc.p0,
        p1: dc.p1,
        p2: dc.p2,
        risk: RISK[dRank],
        risk_rank: dRank,
        action: ordered.length ? (ordered[0].advice || '按原文行号逐条核对证件原件与台账登记。')
          : '证件字段与台账一致，按月份继续复核。',
      });
    }
    docs.sort((a, b) => (a.risk_rank - b.risk_rank) || String(a.doc).localeCompare(String(b.doc)));
    bySub.push({
      subcontractor: rec.sub,
      rows: rec.rows,
      lines: rec.lines,
      findings: rec.findings.length,
      p0: c.p0,
      p1: c.p1,
      p2: c.p2,
      risk: RISK[riskRank],
      risk_rank: riskRank,
      docs,
    });
  }
  bySub.sort((a, b) => (a.risk_rank - b.risk_rank) || String(a.subcontractor).localeCompare(String(b.subcontractor)));
  const all = counts(findings);
  return {
    by_subcontractor: bySub,
    total: {
      subcontractors: bySub.length,
      docs: docCount,
      findings: findings.length,
      p0: all.p0,
      p1: all.p1,
      p2: all.p2,
      high_risk_subcontractors: bySub.filter((r) => r.risk_rank === 0).length,
      risk_order: RISK,
    },
  };
}

/** 订阅版⑤：可整改动作清单（P0 在前，再按行号） */
function buildConsolidatedActions(findings) {
  const rank = { P0: 0, P1: 1, P2: 2 };
  return findings.slice()
    .sort((a, b) => (rank[a.level] - rank[b.level])
      || (a.line - b.line) || String(a.category).localeCompare(String(b.category)))
    .map((f, i) => ({
      seq: i + 1,
      level: f.level,
      line: f.line,
      subcontractor: f.sub || '',
      doc: f.doc || '',
      category: f.category,
      action: f.advice || '按原文行号逐条核对证件原件与台账登记。',
    }));
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的分包商资质与安全许可台账（营业执照/资质证书/安全生产许可证/特种作业证 逐证一行）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的分包商资质与安全许可台账（营业执照/资质证书/安全生产许可证/特种作业证 逐证一行）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的分包商资质与安全许可台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳，一个证件一行）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行证件明细（现在只有表头，没有可核对的明细行）']);
  }

  const paid = Boolean(p && (p.full || p.credit || p.token));
  const findings = [];
  const notRun = [];

  for (const f of checkExpiryCoverage(t.items)) findings.push(f);
  for (const f of checkLevelMatch(t.items)) findings.push(f);
  for (const f of checkPeopleDocs(t.items)) findings.push(f);
  for (const f of checkDuplicateCert(t.items)) findings.push(f);
  for (const f of checkContractAmount(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  let rollup = null;
  if (paid) {
    const socialSeen = new Set();
    const subCtx = buildSubContractCtx(t.items);
    const docIndex = buildDocIndex(t.items);
    for (const it of t.items) {
      for (const f of checkSocialInsurance(it, socialSeen)) findings.push(f);
      for (const f of checkSubcontracting(it, subCtx)) findings.push(f);
      for (const f of checkDocTypeCompleteness(it, docIndex)) findings.push(f);
      for (const f of checkExitConsistency(it)) findings.push(f);
    }
    rollup = buildRollup(t.items, findings);
  } else {
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  }

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const contractTotal = t.totals.contractAmount;
  const subNames = [];
  for (const it of t.items) {
    const s = subName(it);
    if (s && !isTotalRow(it) && subNames.indexOf(s) < 0) subNames.push(s);
  }

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      subcontractors: subNames.length,
      contract_total: contractTotal,
      basis: '证件有效期必须覆盖进场日期到退场日期（逐行逐证比较四类到期日）；持证资质等级按等级序不得低于要求等级；'
        + '在册特种作业人员清单与特种作业/操作证类证件清单逐人比对；同一分包商同一证件号只能登记一次；'
        + '同一分包商的合同金额各行必须一致、合计行须等于按分包商去重后的合计；关键字段不得空白或用占位符、'
        + '日期必须可解析、证件状态必须在允许取值内。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: paid ? CHECKS_GIVEN.concat(CHECKS_WITHHELD) : CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、证件字段字面一致、清单点到的证件与人员都在**，'
      + '不代表分包商真的具备承接资格、证件是真的、也不代表安全检查已经通过 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    subcontractors: subNames.length,
    contract_total: contractTotal,
  };
  if (paid) {
    scope.checks = CHECKS_GIVEN.concat(CHECKS_WITHHELD);
    scope.sub_amount_total = t.totals.subAmount;
    scope.qualification_rollup_total = rollup ? rollup.total : null;
  }
  result.scope = scope;

  if (paid) {
    result.qualification_rollup = rollup;
    result.consolidated_actions = buildConsolidatedActions(findings);
    result.summary.high_risk_subcontractors = rollup ? rollup.total.high_risk_subcontractors : 0;
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
