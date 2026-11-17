#!/usr/bin/env node
/**
 * fire-safety-inspection-check.js —— 消防设施检查与维保记录核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：物业 / 工厂 / 商场 / 学校的消防管理员，**每月**都要把这张表核一遍才能交差：
 *   ① 灭火器、消火栓、喷淋、火灾自动报警、应急照明、疏散指示、防火门、防排烟 都要按规定频次**月度巡查**，
 *      少巡一次、漏一个点位，在消防监督检查里就是「未按规定开展防火巡查」；
 *   ② 灭火器要**年检 / 维修**、消防设施要**年度检测**，检查日期晚于「下次检定到期日」就是「灭火器超期未检」
 *      —— 这是直接处罚项；
 *   ③ 设施台账数量、巡查记录条数、合计行的数量类列要逐区域 / 逐设施类型对得上；
 *   ④ 故障从报修到整改完成要**闭环**，「记录有、隐患没整改」（状态=故障却一直不闭环）同样是处罚项；
 *   ⑤ 维保要按周期做、维保单位资质要在有效期内 —— 资质过期的维保记录等于没维保。
 * 这些都是台账上的字面算术与日期勾稽，却最容易在月底被漏掉。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现上面那六项**表内逐行算术、数量勾稽与字段合法性**；
 *    **完整档（付费）的实现不在这个包里** —— 故障整改闭环时长、故障未闭环清单、维保周期勾稽、
 *    维保单位资质有效期覆盖、分区域×分设施类型的汇总清单与整改动作清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *    本版本**只做**台账与记录的字面勾稽，**不做**消防设施是否合格、隐患是否真正消除的判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定消防设施是否合格、不判定隐患是否真正消除、不判定会不会被处罚、不读 .xlsx/.pdf/照片原件、
 *          不联网核验资质证书真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '巡查频次覆盖（逐项核对 本月巡查次数 ≥ 规定巡查频次，不足即报出缺口次数）',
  '检定有效期（检查日期 ≤ 下次检定到期日，超期即报出超期天数）',
  '数量勾稽（逐区域×逐设施类型：设施台账数量合计 = 明细登记条数，差额即报）',
  '同一设施同一日期重复登记检测（设施编号 + 检查日期 重复即点名在先的行号）',
  '合计行逐列复核（合计/小计行的数量类列与明细行之和逐列复算）',
  '空白/占位符/非法值检测（关键字段空白或占位符、日期格式非法、状态值不在 正常/故障/停用/已整改 之内、数量为负或无法解析）',
];

const CHECKS_WITHHELD = [
  '故障整改闭环时长（状态=已整改：报修日期 → 整改完成日期 ≤ 整改时限(天)，超时点名并给出超时天数）',
  '故障未闭环清单（状态=故障 但整改完成日期为空或超期未整改，按超期天数从大到小排队）',
  '维保周期勾稽（上次维保日期 + 维保周期(月) = 下次维保日期，逐行复算）',
  '维保单位资质有效期覆盖（上次/下次维保日期 ≤ 资质到期日）',
  '分区域×分设施类型的汇总清单（按故障数与超期数排序，给出逐组可整改动作）与合并后的整改动作清单',
];

const OUT_OF_SCOPE = [
  '判定消防设施是否「合格」、是否达到消防技术标准（那是消防技术服务机构与消防救援机构的认定权），本工具只核台账与记录的字面勾稽',
  '判定隐患整改是否真正消除了隐患（现场复查结论），本工具只核记录上的日期与时限',
  '判定灭火器压力表读数、消火栓压力、喷淋流量等现场参数是否达标',
  '判定维保单位是否真正具备消防技术服务资质（本工具只核「资质到期日」这个日期的覆盖关系）',
  '判定会不会被行政处罚、处罚多少（那是消防救援机构的裁量权）',
  '读取 .xlsx / .pdf / 现场照片原件、联网核验资质证书真伪、替代消防设施年度检测报告或消防备案',
];

// 样例：一张**干净**的消防设施月度巡查与维保记录表 —— 两个区域、六个「区域×设施类型」分组，
// 巡查次数都达到规定频次、检查日期都在检定有效期内、台账数量与登记条数逐组相符、
// 编号与检查日期无重复、字段齐整；唯一一条「已整改」的故障在 3 天时限内闭环、
// 维保周期满足 上次维保日期 + 周期 = 下次维保日期、维保资质到期日覆盖到两次维保日期。
const SAMPLE_TEXT = [
  '设施编号\t设施名称\t设施类型\t区域\t安装位置\t规定巡查频次\t本月巡查次数\t台账数量\t检查日期\t下次检定到期日\t状态\t故障描述\t报修日期\t整改完成日期\t整改时限(天)\t维保单位\t维保周期(月)\t上次维保日期\t下次维保日期\t资质到期日\t备注',
  'XF-A-001\t1号手提式干粉灭火器\t手提式干粉灭火器\tA栋\tA栋1层东侧走廊\t4\t4\t1\t2026-03-05\t2026-09-30\t正常\t\t\t\t3\t江苏安泰消防技术服务有限公司\t1\t2026-02-15\t2026-03-15\t2026-12-31\t压力表指针在绿区，铅封完好',
  'XF-A-002\t2号手提式干粉灭火器\t手提式干粉灭火器\tA栋\tA栋2层西侧楼梯口\t4\t4\t1\t2026-03-05\t2026-09-30\t正常\t\t\t\t3\t江苏安泰消防技术服务有限公司\t1\t2026-02-15\t2026-03-15\t2026-12-31\t灭火器箱无遮挡，挂钩牢固',
  'XF-A-003\t1层大厅南侧室内消火栓\t室内消火栓\tA栋\tA栋1层大厅南侧\t2\t2\t1\t2026-03-05\t2026-11-30\t正常\t\t\t\t3\t江苏安泰消防技术服务有限公司\t1\t2026-02-15\t2026-03-15\t2026-12-31\t水带接口密封圈完好，箱门开启灵活',
  'XF-B-001\t配电房门口灭火器\t手提式干粉灭火器\tB栋\tB栋1层配电房门口\t4\t4\t1\t2026-03-05\t2026-09-30\t正常\t\t\t\t3\t南京华安消防维保有限公司\t3\t2025-12-20\t2026-03-20\t2026-12-31\t压力表指针在绿区，已按规定月检',
  'XF-B-002\t1层安全出口应急照明及疏散指示\t应急照明及疏散指示\tB栋\tB栋1层安全出口上方\t2\t2\t1\t2026-03-05\t2026-11-30\t正常\t\t\t\t3\t南京华安消防维保有限公司\t3\t2025-12-20\t2026-03-20\t2026-12-31\t应急照明持续供电测试合格，指示方向正确',
  'XF-B-003\t2层东侧常闭式防火门\t防火门\tB栋\tB栋2层东侧楼梯间\t2\t2\t1\t2026-03-05\t2026-11-30\t正常\t\t\t\t3\t南京华安消防维保有限公司\t3\t2025-12-20\t2026-03-20\t2026-12-31\t闭门器与顺序器完好，门扇无变形',
  'XF-A-004\t消防控制室火灾报警控制器\t火灾自动报警系统\tA栋\tA栋1层消防控制室\t2\t2\t1\t2026-03-05\t2026-11-30\t已整改\t1#感烟探测器故障报警，已更换探头\t2026-03-02\t2026-03-04\t3\t江苏安泰消防技术服务有限公司\t1\t2026-02-15\t2026-03-15\t2026-12-31\t已闭环，复查合格',
].join('\n');

// 状态只认这四种（列里给的枚举口径）
const STATUS_SET = ['正常', '故障', '停用', '已整改'];

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'assetNo', 'assetName', 'assetType', 'zone', 'location', 'reqFreq', 'monthCount', 'ledgerQty',
  'checkDate', 'nextDueDate', 'status', 'faultDesc', 'reportDate', 'fixDate', 'maintUnit', 'maintCycle',
];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）。
// 故障描述 / 报修日期 / 整改完成日期 是**有条件**的：状态为「正常」时本来就该空着，所以不在这里强制。
const REQUIRED_FIELDS = [
  ['assetNo', '设施编号'],
  ['assetName', '设施名称'],
  ['assetType', '设施类型'],
  ['zone', '区域'],
  ['location', '安装位置'],
  ['reqFreq', '规定巡查频次'],
  ['monthCount', '本月巡查次数'],
  ['ledgerQty', '台账数量'],
  ['checkDate', '检查日期'],
  ['nextDueDate', '下次检定到期日'],
  ['status', '状态'],
  ['maintUnit', '维保单位'],
  ['maintCycle', '维保周期(月)'],
];

// 数量类列（用于「为负 / 无法解析」判定）
const QTY_FIELDS = [
  ['reqFreq', '规定巡查频次'],
  ['monthCount', '本月巡查次数'],
  ['ledgerQty', '台账数量'],
];

// 日期列（空白留给必需字段判定；非空但看不懂 ⇒ 日期格式非法）
const DATE_FIELDS = [
  ['checkDate', '检查日期'],
  ['nextDueDate', '下次检定到期日'],
  ['reportDate', '报修日期'],
  ['fixDate', '整改完成日期'],
];

// 数量类列（合计行逐列复核 + 汇总口径都用它）
const SUM_ROLES = ['ledgerQty', 'monthCount'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过多次，见 tools/header_map_check.py）：
//    「下次维保日期」必须排在只认「维保」的兜底词前、「设施类型」必须排在只认「设施」的兜底词前。
const ROLES = {
  assetNo: ['设施编号', '设备编号', '点位编号', '器材编号', '设施代码', '编号'],
  assetName: ['设施名称', '设备名称', '点位名称', '器材名称', '名称'],
  assetType: ['设施类型', '设备类型', '设施类别', '器材类型', '设备类别', '类型'],
  zone: ['区域名称', '所属区域', '区域', '分区', '楼栋', '片区'],
  location: ['安装位置', '设置位置', '安装地点', '具体位置', '位置'],
  reqFreq: ['规定巡查频次', '要求巡查频次', '巡查频次要求', '规定频次', '巡查频次', '频次'],
  monthCount: ['本月巡查次数', '本月巡查频次', '实际巡查次数', '巡查次数', '本月次数'],
  ledgerQty: ['设施台账数量', '台账数量', '设施数量', '台账数', '数量'],
  checkDate: ['本次检查日期', '本次巡查日期', '检查日期', '巡检日期', '巡查日期', '检查时间'],
  nextDueDate: ['下次检定到期日', '下次检定日期', '检定到期日', '下次检测到期日', '年检到期日', '检定到期'],
  status: ['设施状态', '运行状态', '巡查状态', '状态'],
  faultDesc: ['故障描述', '故障情况', '故障现象', '异常描述', '问题描述', '故障'],
  reportDate: ['故障报修日期', '报修日期', '报修时间', '发现日期', '报修'],
  fixDate: ['整改完成日期', '完成整改日期', '整改完成时间', '整改日期', '闭环日期', '整改完成'],
  fixLimit: ['整改时限', '规定时限', '整改期限', '整改天数', '时限'],
  maintUnit: ['消防维保单位', '维保服务单位', '维保单位', '保养单位', '服务单位'],
  maintCycle: ['维保周期', '保养周期', '维保间隔'],
  lastMaintDate: ['上次维保日期', '上次保养日期', '最近维保日期', '上次维保', '上次保养'],
  nextMaintDate: ['下次维保日期', '下次保养日期', '计划维保日期', '下次维保', '下次保养'],
  qualExpiry: ['维保资质到期日', '资质到期日', '资质有效期至', '资质有效期'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  assetNo: '设施编号',
  assetName: '设施名称',
  assetType: '设施类型',
  zone: '区域',
  location: '安装位置',
  reqFreq: '规定巡查频次',
  monthCount: '本月巡查次数',
  ledgerQty: '台账数量',
  checkDate: '检查日期',
  nextDueDate: '下次检定到期日',
  status: '状态',
  faultDesc: '故障描述',
  reportDate: '报修日期',
  fixDate: '整改完成日期',
  fixLimit: '整改时限(天)',
  maintUnit: '维保单位',
  maintCycle: '维保周期(月)',
  lastMaintDate: '上次维保日期',
  nextMaintDate: '下次维保日期',
  qualExpiry: '资质到期日',
  note: '备注',
};

// 合计行 / 小计行的编号或名称（这些行不参与逐行核对，只做合计复核）
const TOTAL_WORDS = ['合计', '总计', '全表合计', '汇总'];
const SUBTOTAL_WORDS = ['小计', '本区小计', '区域小计'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「都合规」，也不说「有问题」。',
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

const str = (v) => String(v == null ? '' : v).trim();

const fmtNum = (n) => String(round2(n));

/** 数量类单元格 → 数字：纯数字直接取；「4次/月」这类写法取其中的数字；认不出来返回 null */
function countOf(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const n = normNumber(s);
  if (n !== null) return n;
  const m = /(-?\d+(?:\.\d+)?)/.exec(s.replace(/[¥￥,，\s]/g, ''));
  if (!m) return null;
  const v = Number(m[1]);
  return Number.isFinite(v) ? v : null;
}

const pad2 = (n) => (n < 10 ? '0' + n : String(n));

/** 日期 → 'YYYY-MM-DD'；认不出来返回 null（不猜、不补默认值） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (!s) return null;
  let m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return `${y}-${pad2(mo)}-${pad2(d)}`;
}

/** b − a 的天数（两个入参都必须是 normDate 的产物） */
function dayDiff(a, b) {
  return Math.round((Date.parse(b + 'T00:00:00Z') - Date.parse(a + 'T00:00:00Z')) / 86400000);
}

/** 小计行：不参与逐行核对，只参与「合计行逐列复核」 */
function isSubtotalRow(it) {
  const no = str(it.assetNo).replace(/\s/g, '');
  const name = str(it.assetName).replace(/\s/g, '');
  return SUBTOTAL_WORDS.some((w) => no === w || name === w);
}

function isTotalRow(it) {
  const no = str(it.assetNo).replace(/\s/g, '');
  const name = str(it.assetName).replace(/\s/g, '');
  return TOTAL_WORDS.some((w) => no === w || name === w) || isSubtotalRow(it);
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
  const detailItems = items.filter((it) => !isTotalRow(it));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detailItems.reduce((acc, it) => {
      const n = countOf(it[role]);
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

function who(it) {
  const name = str(it.assetName);
  const no = str(it.assetNo);
  return `第 ${it.line} 行「${name || no || '未命名设施'}${no && name ? '（' + no + '）' : ''}」`;
}

/** 结论的「紧迫度」＝超期天数与差额绝对值里更大的那个（排序用；两个档都要有） */
const urgencyOf = (f) => Math.max(
  typeof f.days === 'number' ? Math.abs(f.days) : 0,
  typeof f.diff === 'number' ? Math.abs(f.diff) : 0);

/** 每条结论都带**原文依据**：行号 + 该行原文（evidence），消息里再引具体数字/日期 */
function finding(level, category, it, metrics, message, advice) {
  const f = {
    level, category, line: it.line, message,
    evidence: String(it.raw == null ? '' : it.raw),
  };
  if (metrics && typeof metrics === 'object') {
    if (typeof metrics.diff === 'number' && Number.isFinite(metrics.diff)) f.diff = round2(metrics.diff);
    if (typeof metrics.days === 'number' && Number.isFinite(metrics.days)) f.days = metrics.days;
  }
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 巡查频次覆盖：本月巡查次数 ≥ 规定巡查频次 */
function checkFrequency(items) {
  const out = [];
  for (const it of items) {
    const need = countOf(it.reqFreq);
    const done = countOf(it.monthCount);
    if (need === null || done === null || need < 0 || done < 0) continue;   // 非法值交给「空白/非法值」那一项
    if (done >= need) continue;
    out.push(finding('P1', '巡查频次未达规定', it, { diff: need - done },
      `${who(it)}：规定巡查频次 ${fmtNum(need)} 次/月，本月巡查次数只有 ${fmtNum(done)} 次，缺 ${fmtNum(need - done)} 次。`,
      '按月度防火巡查计划把漏掉的次数补上并留痕（记录要能点到日期与巡查人）；确实无法补巡的写清原因与替代措施。'
      + '本工具只核次数够不够，不判定巡查内容是否到位。'));
  }
  return out;
}

/** 2. 检定有效期：检查日期 ≤ 下次检定到期日（灭火器年检/维修、设施年度检测） */
function checkValidity(items) {
  const out = [];
  for (const it of items) {
    const check = normDate(it.checkDate);
    const due = normDate(it.nextDueDate);
    if (!check || !due) continue;          // 空白/格式非法交给「空白/非法值」那一项
    const late = dayDiff(due, check);
    if (late <= 0) continue;
    out.push(finding('P0', '检定有效期超期', it, { days: late },
      `${who(it)}：检查日期 ${check} 已晚于「下次检定到期日」${due}，超期 ${late} 天 —— 台账上属于「超期未检」。`,
      '灭火器的年检/维修、消防设施的年度检测都要在到期日前完成；先确认是否已送检只是日期没登记，'
      + '确属超期的应立即送检或停用并留凭证。本工具只核日期关系，不判定是否真的没检。'));
  }
  return out;
}

/** 3. 数量勾稽：逐区域×逐设施类型，台账数量合计 = 明细登记条数 */
function checkQuantityMatch(items) {
  const out = [];
  const groups = new Map();
  for (const it of items) {
    const zone = str(it.zone) || '(未填区域)';
    const type = str(it.assetType) || '(未填类型)';
    const key = `${zone}|${type}`;
    if (!groups.has(key)) groups.set(key, { zone, type, lines: [], ledger: 0, bad: false });
    const g = groups.get(key);
    g.lines.push(it.line);
    const q = countOf(it.ledgerQty);
    if (q === null || q < 0) g.bad = true; else g.ledger = round2(g.ledger + q);
  }
  for (const g of groups.values()) {
    if (g.bad) continue;                   // 组里有非法数量 ⇒ 交给「空白/非法值」那一项，这里不硬算
    const rows = g.lines.length;
    const diff = round2(g.ledger - rows);
    if (Math.abs(diff) < 0.005) continue;
    const first = items.find((it) => it.line === g.lines[0]);
    out.push(finding(diff > 0 ? 'P0' : 'P1', '数量勾稽不平', first, { diff },
      `${g.zone} × ${g.type}：台账数量合计 ${fmtNum(g.ledger)} 台，明细登记 ${rows} 条（第 ${g.lines.join('、')} 行），`
      + `差 ${fmtNum(diff)} 台（${diff > 0 ? '台账多于记录，疑有漏登/漏巡' : '记录多于台账，疑有重复登记或漏登台账'}）。`,
      '逐区域、逐设施类型把台账与记录对齐：台账上有的每一台都应有登记，登记多了要查是否重复。'
      + '本工具只报数量差，不判定哪一边是对的。'));
  }
  return out;
}

/** 4. 同一设施同一日期重复登记 */
function checkDuplicateRegistration(items) {
  const out = [];
  const seen = new Map();
  const reported = new Set();
  for (const it of items) {
    const no = str(it.assetNo);
    const day = str(it.checkDate);
    if (!no || !day) continue;
    const key = `${no}|${day}`;
    if (seen.has(key) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P1', '同一设施同一日期重复登记', it, null,
        `${who(it)}：设施编号「${no}」在检查日期 ${day} 已于第 ${seen.get(key)} 行登记过一次 —— 同一天同一设施重复登记，`
        + '巡查次数与数量勾稽都会被重复计算。',
        '同一天同一设施只登记一条；一天内多次巡查的写在「本月巡查次数」里，或按时段分行并保留原始巡查记录。'));
    }
    if (!seen.has(key)) seen.set(key, it.line);
  }
  return out;
}

/** 5. 合计行逐列复核（数量类列：台账数量 / 本月巡查次数） */
function checkTotalRows(items) {
  const out = [];
  const totalRows = items.filter((it) => isTotalRow(it));
  if (!totalRows.length) return out;
  const details = items.filter((it) => !isTotalRow(it));
  for (const tr of totalRows) {
    let scope = details;
    let scopeText = '全表明细行';
    if (isSubtotalRow(tr)) {
      const zone = str(tr.zone);
      if (!zone) {
        out.push(finding('P1', '合计行数量不平', tr, null,
          `第 ${tr.line} 行是「小计」行，但没有填「区域」，无法确定它汇总的是哪一段 —— 不给结论。`,
          '在小计行上写明「区域」（必要时再写「设施类型」），或者改用一行「合计」做全表合计。'));
        continue;
      }
      scope = details.filter((it) => str(it.zone) === zone);
      scopeText = `${zone} 的明细行`;
      const type = str(tr.assetType);
      if (type) {
        scope = scope.filter((it) => str(it.assetType) === type);
        scopeText = `${zone} × ${type} 的明细行`;
      }
    }
    for (const role of SUM_ROLES) {
      const declared = countOf(tr[role]);
      const computed = round2(scope.reduce((acc, it) => acc + (countOf(it[role]) || 0), 0));
      const label = LABELS[role];
      if (declared === null) {
        out.push(finding('P1', '合计行数量不平', tr, null,
          `第 ${tr.line} 行是合计/小计行，「${label}」的值「${str(tr[role])}」${isBlank(tr[role]) ? '是空的' : '不是可识别的数量'}，`
          + `无法与${scopeText}之和 ${fmtNum(computed)} 复核。`,
          '合计行的数量类列必须是数字；空着或写成文字都不行，改完重跑。'));
        continue;
      }
      const diff = round2(declared - computed);
      if (Math.abs(diff) < 0.005) continue;
      out.push(finding('P1', '合计行数量不平', tr, { diff },
        `第 ${tr.line} 行合计行的「${label}」写 ${fmtNum(declared)}，而${scopeText}逐行相加是 ${fmtNum(computed)}，`
        + `合计行${diff > 0 ? '多写' : '少写'}了 ${fmtNum(Math.abs(diff))}。`,
        '合计行的每一列都必须等于它汇总范围内明细行之和；先确认汇总范围（是否漏行、是否重复），再改合计。'));
    }
  }
  return out;
}

/** 6. 空白/占位符/日期格式/状态值/数量非法 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, null,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of QTY_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = countOf(raw);
      if (n === null) {
        out.push(finding('P1', '数量无法解析', it, null,
          `${who(it)}：「${label}」的值「${str(raw)}」不是可识别的数量（只认数字，或 4次/月 这类含数字的写法）。`,
          '把数量改成纯数字（如 4）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数量为负', it, { diff: n },
          `${who(it)}：「${label}」是负数（${fmtNum(n)}）—— 巡查次数、台账数量都不可能是负数。`,
          '核对是否填错了列或写成了红字冲销；确属冲销的请写在「备注」里，别直接改成别的数字。'));
      }
    }
    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, null,
          `${who(it)}：「${label}」的值「${str(raw)}」不是可识别的日期（只认 2026-03-05 / 2026/3/5 / 2026.3.5 / 2026年3月5日 / 20260305）。`,
          '统一成 2026-03-05 这种写法再跑；日期认不出来时，涉及它的核对（检定有效期、闭环时长、维保周期）都不会硬算。'));
      }
    }
    const st = str(it.status);
    if (st && STATUS_SET.indexOf(st) < 0) {
      out.push(finding('P1', '状态值非法', it, null,
        `${who(it)}：「状态」的值「${st}」不在口径枚举内 —— 只认 ${STATUS_SET.join(' / ')}。`,
        '状态值写歪了，故障闭环与超期统计都会漏掉这一行；按 正常 / 故障 / 停用 / 已整改 四选一填写。'));
    }
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的消防设施月度巡查与维保记录表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的消防设施月度巡查与维保记录表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的消防设施月度巡查与维保记录表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行设施明细（现在只有表头，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];
  const details = t.items.filter((it) => !isTotalRow(it));
  if (!details.length) {
    return insufficient(['至少一行设施明细（现在只有合计/小计行，没有可逐项核对的明细行）']);
  }

  for (const f of checkFrequency(details)) findings.push(f);
  for (const f of checkValidity(details)) findings.push(f);
  for (const f of checkQuantityMatch(details)) findings.push(f);
  for (const f of checkDuplicateRegistration(details)) findings.push(f);
  for (const f of checkTotalRows(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(details)) findings.push(f);

  // 免费档：完整档那五类检查一项都不执行，这里如实记下来（只记「没做」，不会伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (urgencyOf(y) - urgencyOf(x)));

  const ledgerTotal = t.totals.ledgerQty;
  const monthTotal = t.totals.monthCount;

  const result = {
    findings,
    summary: {
      rows: details.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      ledger_qty_total: ledgerTotal,
      month_checks_total: monthTotal,
      basis: '巡查频次按「本月巡查次数 ≥ 规定巡查频次」逐项核对；检查日期不得晚于「下次检定到期日」（灭火器年检/维修、'
        + '设施年度检测）；数量按「区域 × 设施类型」勾稽（台账数量合计 = 明细登记条数）；同一设施同一检查日期只应登记一次；'
        + '合计/小计行的数量类列必须等于其汇总范围内明细行之和；字段空白、日期格式与状态值按目录枚举核对。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对、数量与日期勾稽得上**，'
      + '不代表消防设施本身合格、隐患已经真正消除、也不会被行政处罚 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: details.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    ledger_qty_total: ledgerTotal,
    month_checks_total: monthTotal,
    groups: new Set(details.map((it) => `${str(it.zone) || '(未填区域)'}|${str(it.assetType) || '(未填类型)'}`)).size,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
