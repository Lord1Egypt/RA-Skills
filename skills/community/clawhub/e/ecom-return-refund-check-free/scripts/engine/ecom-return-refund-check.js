/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * ecom-return-refund-check.js —— 电商退货退款与库存回冲核对（完整档 / 买断版引擎）
 *
 * 这张表在真实业务里长这样（从 Excel 复制出来，Tab 分隔）：
 *   退货单号  退款单号  店铺  商品编码  退货日期  退货数量  回冲数量
 *   实收金额  运费扣除  包装扣除  折旧扣除  退款金额  退款状态  到账金额  备注
 *
 * 核对的是**表内勾稽**，全是确定性的算术与对应关系：
 *   · 退款金额 = 实收金额 − 运费扣除 − 包装扣除 − 折旧扣除（逐行复算，差 1 分钱也报）；
 *   · 退货单号 / 退款单号必须一一对应（一个单号只能对应一笔）；
 *   · 库存回冲数量 ≤ 退货数量（回冲超量是硬错，回冲不足提示）；
 *   · 退款状态与到账金额必须自洽（"已到账"却没有到账金额、未完成却已有到账金额、到账与退款金额不符）；
 *   · 关键字段空缺（单号 / 日期 / 数量 / 金额为空或写占位符）。
 *
 * 完整档（买断版）在此之上多一种能力：**跨店铺 / 跨期间的汇总台账**、
 * **按金额排序的追损清单**、以及把退款金额差异**归因**到扣款规则 / 运费承担 / 折旧三类。
 * 免费档只做上面 5 类逐行核对，未执行项由 `CHECKS_WITHHELD` 如实列出。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库 —— 不 require 本技能包以外的任何文件；
 *   · **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）；
 *   · **不写盘、不读环境变量**：纯函数，同样的输入永远给同样的输出；
 *   · 每条结论都引用**原文行号与原文**，第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做表内勾稽，**不做业务判断**（该不该退、折旧率怎么定是业务的事）。
 */

const CHECKS_GIVEN = [
  '退款金额逐行复算（退款金额 = 实收金额 − 运费扣除 − 包装扣除 − 折旧扣除）',
  '退款单号与退货单号一一对应（同一单号出现两次以上即报）',
  '库存回冲数量与退货数量勾稽（回冲超量为硬错、回冲不足提示）',
  '退款状态与到账金额自洽（状态说已完成却没有到账金额、未完成却已有到账金额、到账与退款不符）',
  '关键字段空缺（退货单号 / 退款单号 / 退货日期 / 退货数量 / 退款金额 为空或写占位符）',
];

const CHECKS_WITHHELD = [
  '跨店铺/跨期间汇总台账（按店铺与月份汇总笔数、退款金额合计与回冲数量）',
  '按退款金额排序的追损清单（把应追回/应补退的差额降序排列，≥2 条才出清单）',
  '差异归因（把退款金额差异归到扣款规则、运费承担、折旧计提三类）',
];

const SAMPLE_TEXT = [
  '退货单号\t退款单号\t店铺\t商品编码\t退货日期\t退货数量\t回冲数量\t实收金额\t运费扣除\t包装扣除\t折旧扣除\t退款金额\t退款状态\t到账金额\t备注',
  'TH20260501\tRF20260501\t旗舰店\tSKU-A100\t2026-05-06\t2\t2\t398.00\t10.00\t0.00\t0.00\t388.00\t已到账\t388.00\t七天无理由',
  'TH20260502\tRF20260502\t旗舰店\tSKU-B220\t2026-05-09\t1\t1\t129.00\t0.00\t5.00\t0.00\t124.00\t已到账\t124.00\t外包装破损',
  'TH20260503\tRF20260503\t旗舰店\tSKU-C310\t2026-05-14\t3\t3\t897.00\t12.00\t0.00\t60.00\t825.00\t已到账\t825.00\t质量问题计提折旧',
  'TH20260504\tRF20260504\t旗舰店\tSKU-A100\t2026-05-21\t1\t1\t199.00\t10.00\t0.00\t0.00\t189.00\t已到账\t189.00\t尺码不合适',
].join('\n');

/* ------------------------------------------------------------ 角色与标签 */

const LABELS = {
  returnNo: '退货单号',
  refundNo: '退款单号',
  shop: '店铺',
  sku: '商品编码',
  date: '退货日期',
  returnQty: '退货数量',
  restockQty: '回冲数量',
  receivedAmt: '实收金额',
  freightDeduct: '运费扣除',
  packDeduct: '包装扣除',
  deprecDeduct: '折旧扣除',
  refundAmt: '退款金额',
  refundStatus: '退款状态',
  arrivedAmt: '到账金额',
  memo: '备注',
};

const TEXT_ROLES = ['returnNo', 'refundNo', 'shop', 'sku', 'date', 'refundStatus', 'memo'];
const NUM_ROLES = ['returnQty', 'restockQty', 'receivedAmt', 'freightDeduct', 'packDeduct',
  'deprecDeduct', 'refundAmt', 'arrivedAmt'];

// 一个表至少要认出这些角色才给结论；缺哪一列都会让某条检查失去前提
const REQUIRED_ROLES = ['returnNo', 'refundNo', 'shop', 'date', 'returnQty', 'restockQty',
  'receivedAmt', 'freightDeduct', 'packDeduct', 'deprecDeduct', 'refundAmt', 'refundStatus', 'arrivedAmt'];

/** 能求和的金额/数量列（导出给外部核对口径用） */
const SUM_ROLES = ['returnQty', 'restockQty', 'receivedAmt', 'freightDeduct', 'packDeduct',
  'deprecDeduct', 'refundAmt', 'arrivedAmt'];

/* —— 表头关键词表：**更具体的别名必须排在更宽泛的别名前面**，
      否则宽泛词会抢走具体列（本仓库 header_map_check 专门钉这个坑）。
      顺序：单号 → 数量 → 各类扣除 → 状态 → 金额 → 日期 → 店铺/商品 → 备注 —— */
const HEADER_KEYS = [
  ['returnNo', ['退货单号', '退货编号', '退货流水']],
  ['refundNo', ['退款单号', '退款编号', '退款流水']],
  ['restockQty', ['回冲数量', '回冲件数', '入库数量']],
  ['returnQty', ['退货数量', '退货件数']],
  ['freightDeduct', ['运费扣除', '退货运费', '运费']],
  ['packDeduct', ['包装扣除', '包装费', '包装']],
  ['deprecDeduct', ['折旧扣除', '折旧费', '折旧']],
  ['refundStatus', ['退款状态', '退款进度', '状态']],
  ['refundAmt', ['退款金额', '应退金额', '退款额']],
  ['receivedAmt', ['实收金额', '实收', '订单金额']],
  ['arrivedAmt', ['到账金额', '实退金额', '已到账']],
  ['date', ['退货日期', '退货时间', '申请日期', '日期']],
  ['shop', ['店铺名称', '店铺', '门店']],
  ['sku', ['商品编码', '商品编号', 'sku', '商家编码']],
  ['memo', ['备注', '说明', '原因']],
];

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).trim().toLowerCase();
  if (!h) return null;
  for (const pair of HEADER_KEYS) {
    for (const key of pair[1]) {
      if (h.indexOf(key.toLowerCase()) >= 0) return pair[0];
    }
  }
  return null;
}

/* ---------------------------------------------------------------- 工具 */

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

const shortRaw = (s) => String(s === undefined || s === null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, 80);

const fmt = (n) => (n === null || n === undefined || !Number.isFinite(Number(n)))
  ? '(空)' : Number(n).toFixed(2);

const fmtQty = (n) => {
  if (n === null || n === undefined || !Number.isFinite(Number(n))) return '(空)';
  return Math.abs(Number(n) - Math.round(Number(n))) < 1e-9
    ? String(Math.round(Number(n))) : Number(n).toFixed(2);
};

const ev = (list) => list
  .filter((x) => x !== null && x !== undefined && String(x).trim() !== '')
  .map(shortRaw).join(' ‖ ');

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 检查函数一律返回数组；万一被改成返回 null 之类的非数组，也只当"没报"，
    不让整条流水线抛异常（真正被短路时，对照测试必须因此失败）。 */
const asList = (x) => (Array.isArray(x) ? x : []);

/** 只有明细行才需要报"行"；所有结论的 line 都是**原文行号**（1 起算） */
function parseTable(text) {
  const src = (text === undefined || text === null) ? '' : String(text);
  const lines = src.split(/\r?\n/);
  const rows = [];
  lines.forEach((l, i) => { if (String(l).trim() !== '') rows.push({ text: String(l), line: i + 1 }); });
  const missingAll = REQUIRED_ROLES.map((r) => LABELS[r]);
  if (rows.length === 0) {
    return { error: 'empty', items: [], totals: {}, header: [], roles: [], headerLine: 0, missingColumns: missingAll };
  }
  // 表头行 = 前 6 个非空行里"认出的角色数"最多的一行（容忍标题行/说明行）
  let best = null;
  for (let i = 0; i < Math.min(6, rows.length); i++) {
    const cells = splitRow(rows[i].text);
    const roles = cells.map((c) => roleOf(c));
    const n = roles.filter(Boolean).length;
    if (!best || n > best.n) best = { n, i, cells, roles };
  }
  if (!best || best.n < 2) {
    return { error: 'no_header', items: [], totals: {}, header: [], roles: [], headerLine: 0, missingColumns: missingAll };
  }
  const header = best.cells;
  const roles = best.roles;
  const missingColumns = REQUIRED_ROLES.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = { line: 0, raw: '' };
  for (let k = best.i + 1; k < rows.length; k++) {
    const cells = splitRow(rows[k].text);
    const first = String(cells[0] === undefined ? '' : cells[0]).trim();
    const row = { line: rows[k].line, raw: rows[k].text };
    TEXT_ROLES.forEach((r) => { row[r] = ''; });
    NUM_ROLES.forEach((r) => { row[r] = null; });
    header.forEach((_h, ci) => {
      const role = roles[ci];
      if (!role) return;
      const cell = cells[ci] === undefined ? '' : cells[ci];
      row[role] = NUM_ROLES.indexOf(role) >= 0 ? normNumber(cell) : String(cell).trim();
    });
    if (!totals.line && /^(合计|小计|总计|总合计)/.test(first)) {
      totals.line = row.line;
      totals.raw = row.raw;
      NUM_ROLES.forEach((r) => { totals[r] = row[r]; });
      continue;
    }
    items.push(row);
  }
  return { error: null, items, totals, header, roles, headerLine: rows[best.i].line, missingColumns };
}

/* ------------------------------------------------------------ 免费档检查 */

/** 1. 退款金额 = 实收 − 运费 − 包装 − 折旧（逐行复算） */
function checkRefundFormula(it) {
  const out = [];
  it.items.forEach((r) => {
    const need = [r.receivedAmt, r.freightDeduct, r.packDeduct, r.deprecDeduct, r.refundAmt];
    if (need.some((v) => v === null || v === undefined)) return;   // 列空缺由「关键字段空缺」负责
    const expect = round2(r.receivedAmt - r.freightDeduct - r.packDeduct - r.deprecDeduct);
    const diff = round2(r.refundAmt - expect);
    if (Math.abs(diff) < 0.005) return;
    out.push(finding('P0', '退款金额复算不符', r.line,
      `第 ${r.line} 行「${r.returnNo}／${r.refundNo}」退款金额 ${fmt(r.refundAmt)} ≠ 实收 ${fmt(r.receivedAmt)}`
      + ` − 运费 ${fmt(r.freightDeduct)} − 包装 ${fmt(r.packDeduct)} − 折旧 ${fmt(r.deprecDeduct)}`
      + ` = ${fmt(expect)}，相差 ${fmt(diff)}。`,
      '按表内口径重算这一行的退款金额，或把差额落到对应的扣除列（运费/包装/折旧）—— 差额挂空会让退款合计与库存回冲对不上。',
      ev([r.raw])));
  });
  return out;
}

/** 2. 退货单号 / 退款单号必须一一对应 */
function checkDocPairs(it) {
  const out = [];
  const scan = (role, label) => {
    const seen = new Map();
    it.items.forEach((r) => {
      const key = String(r[role] === undefined || r[role] === null ? '' : r[role]).trim();
      if (!key) return;                                            // 空单号由「关键字段空缺」负责
      if (!seen.has(key)) seen.set(key, []);
      seen.get(key).push(r);
    });
    seen.forEach((list, key) => {
      if (list.length < 2) return;
      out.push(finding('P1', '单号重复', list[0].line,
        `${label}「${key}」在表里出现 ${list.length} 次（第 ${list.map((x) => x.line).join('、')} 行）：`
        + '退款与退货必须一一对应，一个单号只能对应一笔。',
        '核对是重复录入，还是把同一笔退款拆成了两行；同一单号多行会让退款合计被重复统计、库存回冲被算两次。',
        ev(list.map((x) => x.raw).slice(0, 3))));
    });
  };
  scan('returnNo', '退货单号');
  scan('refundNo', '退款单号');
  return out;
}

/** 3. 库存回冲数量 ≤ 退货数量 */
function checkRestockQty(it) {
  const out = [];
  it.items.forEach((r) => {
    if (r.returnQty === null || r.restockQty === null) return;
    if (r.restockQty > r.returnQty + 0.005) {
      out.push(finding('P0', '库存回冲超量', r.line,
        `第 ${r.line} 行「${r.returnNo}」退货 ${fmtQty(r.returnQty)} 件，却回冲入库 ${fmtQty(r.restockQty)} 件，`
        + `多出 ${fmtQty(round2(r.restockQty - r.returnQty))} 件。`,
        '回冲数量不可能大于退货数量：核对是不是把别的退货单的回冲记到了这一行，或者退货数量本身填少了。',
        ev([r.raw])));
    } else if (r.restockQty < r.returnQty - 0.005) {
      out.push(finding('P2', '库存回冲不足', r.line,
        `第 ${r.line} 行「${r.returnNo}」退货 ${fmtQty(r.returnQty)} 件，只回冲入库 ${fmtQty(r.restockQty)} 件，`
        + `还差 ${fmtQty(round2(r.returnQty - r.restockQty))} 件。`,
        '若确实是部分入库（残次、缺件）属正常，请把原因写进备注；若是漏回冲，库存会被系统性少计。',
        ev([r.raw])));
    }
  });
  return out;
}

const DONE_STATUS = /^(已到账|已退款|退款成功|已打款|已完成|到账成功|已退|已完结)$/;
const PENDING_STATUS = /(处理中|退款中|待退款|未到账|审核中|待处理|申请中|失败|已关闭|已拒绝|已取消)/;

/** 4. 退款状态与到账金额自洽 */
function checkStatusVsArrived(it) {
  const out = [];
  it.items.forEach((r) => {
    const st = String(r.refundStatus === undefined || r.refundStatus === null ? '' : r.refundStatus).trim();
    if (!st) return;                                               // 空状态由「关键字段空缺」负责
    if (PENDING_STATUS.test(st)) {
      if (r.arrivedAmt !== null && r.arrivedAmt > 0.005) {
        out.push(finding('P1', '退款状态与到账金额不一致', r.line,
          `第 ${r.line} 行退款状态是「${st}」（按表内写法属于**未完成**），但到账金额已经填了 ${fmt(r.arrivedAmt)}。`,
          '要么状态没更新（款已到账就改成已完成），要么到账金额填错了行 —— 两者都会让"已到账合计"虚高。',
          ev([r.raw])));
      }
      return;
    }
    if (!DONE_STATUS.test(st)) return;                              // 认不出的状态命名不在本工具范围内
    if (r.arrivedAmt === null || r.arrivedAmt <= 0.005) {
      out.push(finding('P1', '退款状态与到账金额不一致', r.line,
        `第 ${r.line} 行退款状态是「${st}」（按表内写法属于**已完成**），但到账金额是 ${fmt(r.arrivedAmt)}。`,
        '已完成却没有到账金额：确认是银行/平台还没回单（那就先别标已完成），还是漏填了到账金额。',
        ev([r.raw])));
      return;
    }
    if (r.refundAmt !== null && Math.abs(round2(r.arrivedAmt - r.refundAmt)) >= 0.005) {
      out.push(finding('P1', '退款状态与到账金额不一致', r.line,
        `第 ${r.line} 行退款状态是「${st}」，但到账金额 ${fmt(r.arrivedAmt)} ≠ 退款金额 ${fmt(r.refundAmt)}，`
        + `相差 ${fmt(round2(r.arrivedAmt - r.refundAmt))}。`,
        '已到账的金额必须等于退款金额；差额常见于手续费、凑整或分次打款 —— 分次打款请拆成两行，别挤在一行里。',
        ev([r.raw])));
    }
  });
  return out;
}

const ROW_REQUIRED = ['returnNo', 'refundNo', 'date', 'returnQty', 'refundAmt'];

/** 5. 关键字段空缺 */
function checkMissingFields(it) {
  const out = [];
  it.items.forEach((r) => {
    const miss = ROW_REQUIRED.filter((k) => isBlank(r[k]));
    if (!miss.length) return;
    out.push(finding('P1', '关键字段空缺', r.line,
      `第 ${r.line} 行的必需字段为空或写了占位符：${miss.map((k) => LABELS[k]).join('、')}`
      + `（原文：${shortRaw(r.raw) || '(空行)'}）。`,
      '这些字段是逐行复算与单号对应的前提，补齐后再跑；本工具不会替它套默认值，也不会跳过这一行。',
      ev([r.raw])));
  });
  return out;
}

/* ------------------------------------------------ 对外边界与"缺什么"提示 */

const OUT_OF_SCOPE = [
  '判断该不该退、该退多少（退款政策与平台规则本身对不对，不在本工具范围内）',
  '核对退回的商品是否真的收到、质检结论是否成立（本工具只看表里的数量与金额）',
  '判断折旧率 / 包装费 / 运费标准定得对不对（表里填多少就以多少为准）',
  '识别退款状态的命名是否合规（只按已认得的「已完成 / 未完成」两类写法核对自洽性）',
  '连接电商后台、ERP 或库存系统自动取数（本工具只处理你贴进来的文本）',
  '给出税务、审计或法律意见',
];

const ADVICE = '请把「退货退款与库存回冲明细表」连同**表头行**一起贴进来（从 Excel 直接复制、Tab 分隔最稳）。'
  + '必需列：' + REQUIRED_ROLES.map((r) => LABELS[r]).join('、') + '。'
  + '每行一笔退货/退款，形如「TH20260501\tRF20260501\t旗舰店\tSKU-A100\t2026-05-06\t2\t2\t398.00\t10.00\t0.00\t0.00\t388.00\t已到账\t388.00\t七天无理由」。';

function run(payload) {
  const p = (payload && typeof payload === 'object' && !Array.isArray(payload)) ? payload : {};
  let text = '';
  if (typeof p.text === 'string') text = p.text;
  else if (Array.isArray(p.text)) text = p.text.join('\n');
  else if (Array.isArray(p.rows)) text = p.rows.map((r) => (Array.isArray(r) ? r.join('\t') : String(r))).join('\n');

  const it = parseTable(text);
  const missing = [];
  if (it.error === 'empty') {
    missing.push('没有收到任何材料（text 是空的）');
  } else if (it.error === 'no_header') {
    missing.push('认不出表头：没有任何一行能认出至少 2 个列名（如 '
      + REQUIRED_ROLES.slice(0, 4).map((r) => LABELS[r]).join('、') + '）');
  }
  if (!it.error && (it.missingColumns || []).length) {
    missing.push('缺少必需列：' + it.missingColumns.join('、'));
  }
  if (!it.error && !(it.missingColumns || []).length && it.items.length === 0) {
    missing.push('只有表头，没有任何明细行（合计行不算明细）');
  }
  if (missing.length) {
    return { status: 'insufficient_input', missing, advice: ADVICE };
  }

  const findings = [].concat(
    asList(checkRefundFormula(it)),
    asList(checkDocPairs(it)),
    asList(checkRestockQty(it)),
    asList(checkStatusVsArrived(it)),
    asList(checkMissingFields(it)),
  );

  const scope = {
    given: CHECKS_GIVEN.slice(),
    checks: CHECKS_GIVEN.slice(),
    checks_not_run: CHECKS_WITHHELD.slice(),
    withheld: CHECKS_WITHHELD.slice(),
    executed_locally: true,
    network_used: false,
  };



  const summary = { rows: it.items.length, p0: 0, p1: 0, p2: 0, total: 0, omitted: 0, by_category: {} };
  findings.forEach((f) => {
    const lv = String(f.level || 'P1');
    if (lv === 'P0') summary.p0 += 1;
    else if (lv === 'P2') summary.p2 += 1;
    else summary.p1 += 1;
    summary.by_category[f.category] = (summary.by_category[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.verdict = summary.p0 > 0 ? 'ERROR_FOUND'
    : (summary.total > 0 ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND');

  const sums = {};
  SUM_ROLES.forEach((r) => {
    sums[r] = round2(it.items.reduce((n, x) => n + (x[r] === null || x[r] === undefined ? 0 : x[r]), 0));
  });

  const result = {
    findings,
    summary,
    sums,
    rows: it.items.length,
    header: it.header.slice(),
    scope,
    checks_given: scope.given.slice(),
    checks_withheld: scope.checks_not_run.slice(),
    checks_executed: scope.checks.slice(),
    checks_out_of_scope: OUT_OF_SCOPE.slice(),
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
