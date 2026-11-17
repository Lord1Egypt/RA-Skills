/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * consignment-settlement-check —— 寄售代销结算核对引擎（免费层 + 收费层，同一份源码）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 真实痛点：**零售 / 制造 / 品牌方每月都要和代销方（商场专柜、电商代运营）对一次账**，
 * 台账上跑的是这几条串行算式：
 *   ① 寄售结存 = 上期结存 + 本期发货 − 本期已销 − 退货数量
 *   ② 应结金额 = 代销方已销金额 − 代销手续费
 *   ③ 代销手续费 = 代销方已销金额 × 手续费率
 * 每月真正漏钱的地方往往不在算式本身，而在算式**之外**：
 * 已销未结（货卖了钱没结）、手续费率高于合同约定（多扣）、退货未冲减（多结给代销方）、
 * 寄售库存与总账勾稽不上、代销方结存与实盘有差。
 *
 * 与已有能力的区别：仓库里已有的是"寄售货物库存数量"类的核对；
 * 本能力核的是**结算口径**（结存数量 → 应结金额 → 手续费 → 已结/未结），
 * 并且收费层直接给"按差额金额排序的追收处理清单"，而不是多报几个数。
 *
 * 刻意不做：不联网、不查合同库、不调用大模型；材料不足不给结论；不给法律意见。
 */

/*
 * 口径契约：run(payload) 返回 {status:'success',result} 或
 *           {status:'insufficient_input',missing,advice}（材料不足时绝不给结论）。
 *
 * ⚠️ 本引擎的档位开关：一个由 paid（Boolean(payload 里的 full / credit / token 任一为真)）控制的顶层分支，
 *    付费检查全部包在里面；**不要**把它改写成别的写法，
 *    也不要在注释里写出它对应的代码形态 —— `strip_free_engine.py` 会把残留当泄漏并整块回滚
 *    （修改后必须执行 `cp 完整档引擎 → 免费包` 再跑 `python3 tools/strip_free_engine.py --apply`）。
 */

const CHECKS_GIVEN = [
  '寄售结存数量复算（上期结存 + 本期发货 − 本期已销 − 退货数量）',
  '应结金额复算（代销方已销金额 − 代销手续费）',
  '代销手续费复算（代销方已销金额 × 手续费率）',
  '发货数量复算（代销方已销 + 退货 + 寄售结存 − 上期结存）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复清单号检测',
  '空白与占位符检测（含负值、日期倒挂）',
];

/**
 * 收费层（完整档）多做的那一件事 —— 口径与类别的**唯一来源**：
 *   label    = 写进 CHECKS_WITHHELD / scope.checks_not_run 的说明文字（免费档如实列出未执行的检查项）
 *   category = 该检查真正报出的 findings[].category
 * 两者放在同一张表里，完整档里多做的那一件事与免费档"未执行项"清单一一对应 —— 不许含糊、不许虚报。
 */
const PAID_CHECKS = [
  { label: '已销未结检测（含挂账月数）', category: '已销未结' },
  { label: '手续费率高于合同约定检测（算多扣差额）', category: '手续费率高于合同约定' },
  { label: '退货未冲减检测（算多结金额）', category: '退货未冲减' },
  { label: '寄售库存与总账不符检测', category: '寄售库存与总账不符' },
  { label: '代销方结存与实盘差异检测', category: '代销方结存与实盘差' },
];

const PAID_CATEGORIES = PAID_CHECKS.map((c) => c.category);
const CHECKS_WITHHELD = PAID_CHECKS.map((c) => c.label);
// ⚠️ 免费包里这张表**必须保留**（它正是免费档如实列出的未执行检查项）；
//    被摘掉的是上面那 5 个 check 函数本身 —— 说明文本不是实现，实现不在免费包里。

const OUT_OF_SCOPE = [
  '判断代销合同条款本身是否有效（那是法务与合同审查的事）',
  '处理含税/不含税口径转换与发票税额勾稽（请把同一口径的金额贴进来）',
  '处理跨币种折算与汇率差异',
  '给出税务意见或催收法律意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

// ⚠️ 样例必须是**干净稿**（跑出来 0 命中）：买家第一次用看到的就是它。
//    第二、三行刻意带上「退货数量 / 退货冲减 / 合同手续费率 / 总账寄售库存 / 实盘结存 / 未结账月数」，
//    否则收费层的检查在这张样例上根本没有材料可核（那不是"没问题"，是"没得核"）。
const SAMPLE_TEXT = [
  '清单号\t代销方\t商品编码\t商品名称\t期初结存\t本期发货\t本期已销数量\t退货数量\t含税单价\t代销方已销金额\t合同手续费率\t代销手续费率\t代销手续费\t应结金额\t已结金额\t结算日期\t结账日期\t单据日期\t总账寄售库存\t代销方实盘结存\t未结账月数\t备注',
  'JX-202603-01\t星河百货专柜\tSP-1001\t甲款风衣\t120\t300\t260\t10\t399.00\t103740.00\t20%\t20%\t20748.00\t82992.00\t82992.00\t2026-04-05\t2026-03-31\t2026-03-12\t150\t150\t0\t月度对账',
  'JX-202603-02\t星河百货专柜\tSP-1002\t乙款衬衫\t80\t200\t180\t10\t199.00\t35820.00\t10%\t10%\t3582.00\t32238.00\t32238.00\t2026-04-05\t2026-03-31\t2026-03-13\t90\t90\t0\t月度对账',
  'JX-202603-03\t优品电商代运营\tSP-1003\t丙款童装\t150\t420\t330\t0\t159.00\t52470.00\t15%\t15%\t7870.50\t44599.50\t44599.50\t2026-04-08\t2026-03-31\t2026-03-14\t240\t240\t0\t代运营结算',
  '合计\t\t\t\t350\t920\t770\t20\t\t192030.00\t\t\t32200.50\t159829.50\t159829.50\t\t\t\t480\t480\t\t',
].join('\n');

const TOL = 0.01;
const PCT_TOL = 0.02;   // 手续费率保留两位小数，容差 0.02 个百分点

/** 与写入端一致的容差：金额/数量相符的判据（与复算用同一个 round2 口径） */
function near(a, b, tol) {
  return Math.abs(round2(a - b)) <= (tol === undefined ? TOL : tol);
}

// ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过两次的坑，见 tools/header_map_check.py）：
//    ·「含税单价」必须在「单价」前，否则被抢走；
//    ·「退货数量」必须排在「本期已销数量 / 已销数量」之前；
//    ·「代销方已销金额」要排在「已销金额」前；「代销手续费率」要排在「代销手续费」前；
//    ·「代销方实盘结存」与「总账寄售库存」都要排在宽泛别名之前，且**不能**含「结存」以外的共同词。
const ROLES = {
  docNo: ['清单号', '结算单号', '对账单号', '单据号'],
  // ⚠️「代销方已销金额」（soldAmt）与「代销方实盘结存」（countQty）都必须排在宽泛的
  //    「代销方」（agent）**之前**：agent 抢走这两列时**不会报缺列**，
  //    只会让"应结金额 / 手续费 / 实盘差异"整列算错（header_map_check 的判据就是这个）。
  soldAmt: ['代销方已销金额', '已销金额', '销售金额', '销售额'],
  countQty: ['代销方实盘结存', '实盘结存', '实盘数量'],
  agent: ['代销方', '受托方', '代销商', '经销商', '专柜'],
  sku: ['商品编码', '商品编号', '货号', '编码'],
  item: ['商品名称', '品名', '商品'],
  openQty: ['期初结存', '上期结存', '期初数量', '上期结余'],
  shipQty: ['本期发货', '发货数量', '本期发出', '发货'],
  soldQty: ['本期已销数量', '已销数量', '本期销售数量', '销售数量'],
  returnQty: ['退货数量', '退货数量小计', '退回数量'],
  price: ['含税单价', '单价', '结算单价'],
  rateContract: ['合同手续费率', '约定手续费率', '合同费率'],
  rateFee: ['代销手续费率', '手续费率', '扣点', '佣金率'],
  fee: ['代销手续费', '手续费', '佣金', '代销费用'],
  payable: ['应结金额', '应结货款', '应付代销方'],
  settled: ['已结金额', '已结货款', '已结算金额', '实收金额'],
  settleDate: ['结算日期', '付款日期', '结款日期'],
  ledgerDate: ['结账日期', '记账日期', '账期截止'],
  docDate: ['单据日期', '发货日期', '发生日期', '日期'],
  bookQty: ['总账寄售库存', '账面寄售库存', '总账库存'],
  aging: ['未结账月数', '挂账月数', '未结月数'],
  // 备注/说明/行号这类列**不参与任何检查**，但要显式认成一个角色：
  //   否则它们会以"没有被识别成任何角色"的形式静默穿过表头映射守卫
  //   （守卫的本意就是"不许有列悄悄不参与检查"，所以要么核它、要么明确标注为不核）。
  note: ['备注', '说明', '附注', '摘要', '行号', '序号'],
};

const LABELS = {
  docNo: '清单号', agent: '代销方', sku: '商品编码', item: '商品名称',
  openQty: '期初结存', shipQty: '本期发货', soldQty: '本期已销数量', returnQty: '退货数量',
  price: '含税单价', soldAmt: '代销方已销金额', rateContract: '合同手续费率',
  rateFee: '代销手续费率', fee: '代销手续费', payable: '应结金额', settled: '已结金额',
  settleDate: '结算日期', ledgerDate: '结账日期', docDate: '单据日期',
  bookQty: '总账寄售库存', countQty: '代销方实盘结存', aging: '未结账月数',
};

const REQUIRED = ['docNo', 'agent', 'sku', 'item', 'openQty', 'shipQty', 'soldQty',
  'returnQty', 'price', 'soldAmt', 'rateFee', 'fee', 'payable', 'settled', 'bookQty'];

// 逐列复核合计行的列（都是"每月必对"的金额与数量列）
const SUM_ROLES = ['openQty', 'shipQty', 'soldQty', 'returnQty', 'soldAmt', 'fee',
  'payable', 'settled', 'bookQty', 'countQty'];

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
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[./]/g, '-').replace(/年|月/g, '-').replace(/日/g, '');
  const m = s.match(/^(\d{4})-(\d{1,2})(?:-(\d{1,2}))?/);
  if (!m) return null;
  const mo = Number(m[2]);
  const d = m[3] === undefined ? 1 : Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return { y: Number(m[1]), m: mo, d, key: Number(m[1]) * 10000 + mo * 100 + d };
}

const round2 = (n) => Math.round(n * 100) / 100;
const money = (n) => (Number.isFinite(n) ? n : 0).toFixed(2);

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `清单「${it.byRole.docNo || '(未填清单号)'}」`
  + `（代销方 ${it.byRole.agent || '(未填)'} / 商品 ${it.byRole.item || '(未填)'}）`;

/* ===== 免费层：逐行复算 + 合计勾稽 + 台账体检 ===== */

function checkBalanceQty(it) {
  const open = num(it, 'openQty');
  const ship = num(it, 'shipQty');
  const sold = num(it, 'soldQty');
  const back = num(it, 'returnQty');
  const stated = num(it, 'bookQty');
  if (open === null || ship === null || sold === null || back === null || stated === null) return null;
  const expect = round2(open + ship - sold - back);
  if (near(expect, stated)) return null;
  return {
    level: 'P0', category: '寄售结存与复算不符', line: it.line,
    message: `${who(it)}的总账寄售库存是 ${money(stated)}，按 期初结存 ${money(open)} + 本期发货 ${money(ship)}`
      + ` − 本期已销 ${money(sold)} − 退货 ${money(back)} = ${money(expect)}。`,
    advice: '寄售结存是下期对账的起点：这里差了，下个月期初结存就会跟着差。',
  };
}

function checkPayable(it) {
  const amt = num(it, 'soldAmt');
  const fee = num(it, 'fee');
  const stated = num(it, 'payable');
  if (amt === null || fee === null || stated === null) return null;
  const expect = round2(amt - fee);
  if (near(expect, stated)) return null;
  return {
    level: 'P0', category: '应结金额与复算不符', line: it.line,
    message: `${who(it)}的应结金额是 ${money(stated)}，按 代销方已销金额 ${money(amt)} − 代销手续费 ${money(fee)}`
      + ` = ${money(expect)}。`,
    advice: '应结金额是本月真正要跟代销方收的钱；这一格错了，收款单就跟着错。',
  };
}

function checkFee(it) {
  const amt = num(it, 'soldAmt');
  const rate = num(it, 'rateFee');
  const stated = num(it, 'fee');
  if (amt === null || rate === null || stated === null) return null;
  const expect = round2(amt * rate / 100);
  if (near(expect, stated)) return null;
  return {
    level: 'P0', category: '代销手续费与复算不符', line: it.line,
    message: `${who(it)}的代销手续费是 ${money(stated)}，按 代销方已销金额 ${money(amt)} × ${rate}% 应为 ${money(expect)}。`,
    advice: '手续费多算一块钱，就是本月少收一块钱；费率与金额至少有一个要改。',
  };
}

function checkShipQty(it) {
  const open = num(it, 'openQty');
  const sold = num(it, 'soldQty');
  const back = num(it, 'returnQty');
  const stated = num(it, 'bookQty');
  const ship = num(it, 'shipQty');
  if (open === null || sold === null || back === null || stated === null || ship === null) return null;
  const expect = round2(stated - open + sold + back);
  if (near(expect, ship)) return null;
  return {
    level: 'P1', category: '发货数量与复算不符', line: it.line,
    message: `${who(it)}的本期发货是 ${money(ship)}，按 寄售结存 ${money(stated)} − 期初结存 ${money(open)}`
      + ` + 本期已销 ${money(sold)} + 退货 ${money(back)} 应为 ${money(expect)}。`,
    advice: '发货数与发货单核对：少了是把货记到别处，多了是仓库漏发却被对成已发。',
  };
}

function checkTotalRows(totals, items) {
  const out = [];
  for (const t of totals) {
    for (const role of SUM_ROLES) {
      const stated = num(t, role);
      if (stated === null) continue;
      const sum = round2(items.reduce((s, it) => {
        const n = num(it, role);
        return s + (n === null ? 0 : n);
      }, 0));
      if (near(sum, stated)) continue;
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，`
          + `相差 ${money(stated - sum)}。`,
        advice: '要么明细行漏了一条清单，要么合计行没跟着更新；先找漏的那一行。',
      });
    }
  }
  return out;
}

function checkDuplicateDocNo(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.docNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一清单号出现多行', line: it.line,
        message: `清单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一清单号重复出现会把已销数量与应结金额重复计算；确认是否同一张对账单被贴了两遍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这条清单的结算就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

const NONNEG_ROLES = ['openQty', 'shipQty', 'soldQty', 'returnQty', 'price', 'soldAmt',
  'fee', 'payable', 'settled', 'bookQty', 'countQty'];

function checkNegative(it) {
  const out = [];
  for (const role of NONNEG_ROLES) {
    const v = num(it, role);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '出现负值', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${money(v)}。`,
        advice: '寄售台账这几列按口径都不该为负：退货与红字请单独列一行并用正数填写，'
          + '否则勾稽会朝错误方向抵消。',
      });
    }
  }
  return out;
}

function checkDateOrder(it) {
  const out = [];
  const doc = normDate(it.byRole.docDate);
  const ledger = normDate(it.byRole.ledgerDate);
  const settle = normDate(it.byRole.settleDate);
  if (ledger && doc && doc.key > ledger.key) {
    out.push({
      level: 'P1', category: '日期倒挂', line: it.line,
      message: `${who(it)}的单据日期（${it.byRole.docDate}）晚于结账日期（${it.byRole.ledgerDate}）。`,
      advice: '结账日之后的发货不该算进本期已销与本期退货；确认是日期填错还是期间归属错了。',
    });
  }
  if (ledger && settle && settle.key < ledger.key) {
    out.push({
      level: 'P1', category: '日期倒挂', line: it.line,
      message: `${who(it)}的结算日期（${it.byRole.settleDate}）早于结账日期（${it.byRole.ledgerDate}）。`,
      advice: '结算日期早于结账日期，说明这笔"已结"其实是上期结的；本期仍应算未结。',
    });
  }
  return out;
}

/* ===== 付费档专属：下面这几个检查函数只在完整档里被调用 ===== */

const UNPAID_TOL = 0.5;         // 已结金额小于应结金额的容差（到分位）
const DAYS_PER_MONTH = 365.25 / 12;

/** 从起始月数到结账月的整月数（首尾不足一月按 0 计，跨月才计 1） */
/** 收费层专属产出：把 5 类判定结果收成一张"按差额金额排序"的追收处理清单 */
function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的寄售/代销结算台账（要能认出「清单号」「代销方」「商品编码」「商品名称」'
      + '「期初结存」「本期发货」「本期已销数量」「退货数量」「含税单价」「代销方已销金额」'
      + '「代销手续费率」「代销手续费」「应结金额」「已结金额」「总账寄售库存」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从台账或对账单导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一条清单明细行']);

  const findings = [];
  const notRun = [];
  const scope = {};

  for (const it of t.items) {
    const a = checkBalanceQty(it); if (a) findings.push(a);
    const b = checkPayable(it); if (b) findings.push(b);
    const c = checkFee(it); if (c) findings.push(c);
    const d = checkShipQty(it); if (d) findings.push(d);
    for (const f of checkNegative(it)) findings.push(f);
    for (const f of checkDateOrder(it)) findings.push(f);
  }
  for (const f of checkTotalRows(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicateDocNo(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
    scope.checks_not_run = CHECKS_WITHHELD;
    scope.why_not_run = '这些检查项的实现在完整档里，本档位没有执行 —— 不代表这些事没问题。';
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const soldAmt = sumOf('soldAmt');
  const feeTotal = sumOf('fee');
  const payableTotal = sumOf('payable');
  const settledTotal = sumOf('settled');

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      // P2 是"值得看一眼"的提示级；本能力的判定只有 P0/P1 两档，但这一格必须存在 ——
      // 批量入口 scripts/batch.mjs 会累加 p2，缺了它汇总会印出 NaN（已踩过一次）。
      p2: findings.filter((f) => f.level === 'P2').length,
      sold_amt_total: soldAmt,
      fee_total: feeTotal,
      payable_total: payableTotal,
      settled_total: settledTotal,
      outstanding_total: round2(payableTotal - settledTotal),
      fee_rate_pct: soldAmt > 0 ? round2(feeTotal / soldAmt * 100) : null,
      basis: '寄售结存 = 上期结存 + 本期发货 − 本期已销 − 退货数量；'
        + '应结金额 = 代销方已销金额 − 代销手续费；代销手续费 = 代销方已销金额 × 手续费率；'
        + '发货数量 = 寄售结存 − 期初结存 + 本期已销 + 退货；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    scope,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };

  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表代销合同条款有效、也不代表含税口径与发票勾稽一致 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, REQUIRED,
};
