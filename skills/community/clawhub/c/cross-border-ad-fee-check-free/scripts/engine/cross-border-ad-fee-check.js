#!/usr/bin/env node
/**
 * cross-border-ad-fee-check.js —— 跨境电商平台佣金与广告费核对引擎（完整档 / 买断版）。
 *
 * 真实痛点：做跨境电商的人每月都要把**平台结算单**和**广告费账单**对一遍。钱就是三条串行算式：
 *   ① 平台佣金 = 销售额 × 佣金率
 *   ② 结算净额 = 销售额 − 佣金 − 广告费 − 其它费用
 *   ③ 结算单上列示的广告费 = 广告费账单金额（两张表勾稽）
 * 佣金率用错档（15% 的店被按 20% 扣）、广告费在两处列成不同金额、其它费用（仓储 / 退款 /
 * 支付手续费）把净额吃成负数 —— 每一处都是每月少收几百到几万块；而几十上百行靠人眼核不动，
 * 这三条却**纯算术、可复算**。
 *
 * 与仓库里已有能力的区别（同一仓库内别买重）：
 *   · `platform-settlement-aging-check` 核的是结算款的**账龄**（什么时候到账）；
 *   · `cross-border-ad-fee-check`（本能力）核的是结算单与广告费账单的**金额与算术**；
 *   · `ad-agency-rebate-check` 核的是给广告代理的**返点**；
 *   · `ecommerce-refund-settlement-check` 核的是**退款**结算。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查平台费率合同与广告投放后台、不调用大模型；
 *   材料不足不给结论；不代你向平台申诉。
 *
 * ⚠️ 本文件是免费档与完整档的**共用源码**：完整档（买断版）在此基础上追加
 *   「按店铺 / 平台 / 站点汇总台账 + 按费用额排序的申诉清单 + 佣金率与广告费异常归因」那一段；
 *   免费包由 tools/strip_free_engine.py 把那段实现摘掉，只留免费检查项。
 */
'use strict';

const CHECKS_GIVEN = [
  '平台佣金逐行复算（佣金 = 销售额 × 佣金率）',
  '广告费勾稽（结算单列示的广告费 = 广告费账单金额）',
  '结算净额逐行复算（净额 = 销售额 − 佣金 − 广告费 − 其它费用）',
  '合计行逐列复核（每一列的合计是否等于各明细行之和）',
  '重复结算检测（同一店铺 + 平台 + 站点 + 期间出现多行）',
  '关键字段缺失与占位符检测（缺失时不复算、不套默认值）',
];

const CHECKS_WITHHELD = [
  '跨店铺 / 跨平台 / 跨站点汇总台账（按维度合计销售额、佣金、广告费与净额）',
  '按费用额从大到小排序的申诉清单（带行号、归因与应补 / 应退金额）',
  '佣金率异常归因（超出 0~30% 合理区间 / 同一店铺同期间佣金率不一致 / 与整表口径系统性偏离）',
  '广告费异常归因（广告费占销售额比例过高）',
  '结算净额为负检测（扣项吃掉全部销售额）',
  '费用项为负检测（佣金 / 广告费 / 其它费用出现负数）',
];

const OUT_OF_SCOPE = [
  '判断平台佣金率档位与广告费单价是否符合你与平台签的合同或商务条款'
  + '（那是商务条款的事；本工具只按账单自己列示的数字复算）',
  '把广告费账单里的逐条投放明细（广告活动 / 关键词 / 素材）与结算单勾稽'
  + '（本表是账单汇总口径；逐条核对请先把投放明细汇总成同结构）',
  '核广告的曝光 / 点击 / 转化等投放效果指标，也不判断广告花得值不值',
  '处理汇率折算、退款与取消单、跨期结算、佣金返还等特殊口径',
  '读取 .xlsx / CSV 文件，也不联网抓取平台后台的结算单或广告费账单（需要你先导出成文本贴进来）',
  '代你向平台申诉、发工单或与招商经理沟通（本工具只给出可复算的依据、金额与话术文本）',
];

const TOL = 0.01;          // 金额容差（分）

/**
 * 表头 → 角色。
 * ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库反复踩过的坑，见 tools/header_map_check.py）：
 *   「佣金率」必须排在「佣金」之前，否则佣金率那一列会被佣金抢走，整列算错却不会报缺列；
 *   「广告费平台账单 / 广告费账单」必须排在「广告费」之前（否则账单那一列被结算单的广告费抢走，
 *     广告费勾稽就变成"自己减自己"，永远通过）；
 *   「销售额」用「销售额 / 结算基数 / 成交金额 / gmv」这些**唯一**写法，不用「结算金额」——
 *     否则它会和「结算净额」抢同一列。
 */
const ROLES = {
  ad_bill: ['广告费平台账单', '广告费账单', '广告账单', '平台广告账单', '广告费对账单', '广告账单金额'],
  rate: ['佣金率', '抽佣率', '费率', '佣金比例'],
  commission: ['佣金', '平台佣金', '技术服务费', '平台服务费'],
  ad_fee: ['广告费', '推广费', '广告支出'],
  other_fee: ['其它费用', '其他费用', '其它扣款', '其他扣款', '杂项费用'],
  net: ['结算净额', '净额', '到账金额', '实际结算', '打款金额'],
  base: ['销售额', '结算基数', '商品销售额', '计佣基数', '成交金额', 'gmv'],
  period: ['结算期间', '期间', '账期', '月份', '结算周期'],
  site: ['站点', '国家', '市场'],
  shop: ['店铺名称', '店铺', '门店', '商户'],
  platform: ['平台名称', '平台', '渠道'],
};

const LABELS = {
  shop: '店铺', platform: '平台', site: '站点', period: '期间', base: '销售额', rate: '佣金率',
  commission: '佣金', ad_bill: '广告费账单', ad_fee: '广告费', other_fee: '其它费用', net: '结算净额',
};

/** 必备列：缺了任何一列 ⇒ 材料不足，不给任何结论（不含糊地用默认值替代）。 */
const REQUIRED = ['base', 'rate', 'commission', 'ad_bill', 'ad_fee', 'other_fee', 'net'];
/** 参与「合计 = 各明细行之和」逐列复核的列。 */
const SUM_ROLES = ['base', 'commission', 'ad_bill', 'ad_fee', 'other_fee', 'net'];

/**
 * 干净样例：一张平台结算单（含合计行）。
 * 每列的数值都刻意互不相同（避免对照测试的变异锚点互相撞车）：
 *   行 2：120000 × 15% = 18000；120000 − 18000 − 19000 − 2600 = 80400；广告费账单 19000 ✓
 *   行 3： 80000 × 11.5% = 9200；80000 − 9200 − 10800 − 1800 = 58200；广告费账单 10800 ✓
 *   合计行逐列都等于两行之和 ⇒ 0 条发现（干净样例绝不误报）。
 */
const SAMPLE_TEXT = [
  '店铺\t平台\t站点\t期间\t销售额\t佣金率\t佣金\t广告费平台账单\t广告费\t其它费用\t结算净额',
  'US-OUTDOOR\tAmazon\tUS\t2026-03\t120000.00\t15%\t18000.00\t19000.00\t19000.00\t2600.00\t80400.00',
  'EU-HOME\tAmazon\tDE\t2026-03\t80000.00\t11.5%\t9200.00\t10800.00\t10800.00\t1800.00\t58200.00',
  '合计\t\t\t\t200000.00\t\t27200.00\t29800.00\t29800.00\t4400.00\t138600.00',
].join('\n');

/** 一个"可核对要点"的行定位说明（有店铺/平台/站点时点名，否则退回行号）。 */
function who(it) {
  const parts = [];
  for (const role of ['shop', 'platform', 'site', 'period']) {
    const s = cell(it, role);
    if (s) parts.push(`${LABELS[role]}「${s}」`);
  }
  return parts.length ? parts.join('·') : `第 ${it.line} 行`;
}

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

/** 表格切分：Tab 优先（Excel 复制最稳），否则按两个以上空格切。 */
function splitRow(line) {
  if (String(line).indexOf('\t') >= 0) return String(line).split('\t').map((s) => s.trim());
  return String(line).split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

/** 表头 → 全部**可能**的角色（按具体优先的顺序；第一个就是优先采纳的角色）。 */
function rolesOf(header) {
  const h = String(header === undefined || header === null ? '' : header)
    .toLowerCase().replace(/[\s（）()【】\[\]]/g, '');
  if (!h) return [];
  const out = [];
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) out.push(role);
  }
  return out;
}

/** 表头认角色：返回最具体的一个（认不出返回 null）。 */
function roleOf(header) {
  const all = rolesOf(header);
  return all.length ? all[0] : null;
}

/**
 * 逐列认角色 + **冲突消解**：一列被别的列抢走就顺位让给下一个候选角色。
 * 反例（实测踩到）：`广告费平台账单` 里的「平台」会把整列抢成 platform，
 * 于是「广告费账单」这一列静默消失、广告费勾稽变成"自己减自己"，永远通过；
 * 「平台服务费」同理会被 platform 抢走。按顺序优先 + 冲突顺位即可两全。
 */
function resolveRoles(headers) {
  const claimed = new Set();
  const chosen = [];
  for (const h of headers) {
    const cands = rolesOf(h);
    let role = null;
    for (const c of cands) {
      if (!claimed.has(c)) { role = c; break; }
    }
    if (role) claimed.add(role);
    chosen.push({ header: h, role, candidates: cands });
  }
  return chosen;
}

/** 数字口径：允许千分位、货币符号、百分号与会计负数写法 (1,234.00)。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim().replace(/[¥￥$,，\s]/g, '');
  const neg = /^\(.*\)$/.test(s);
  s = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

const cell = (it, role) => {
  const v = it.byRole[role];
  return v === undefined || v === null ? '' : String(v).trim();
};
const num = (it, role) => normNumber(it.byRole[role]);

function parseTable(text) {
  const lines = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!lines.length) return { error: 'empty', items: [], totals: [], cols: [], missingColumns: [] };
  const headerCells = splitRow(lines[0]);
  const cols = resolveRoles(headerCells);
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingColumns = REQUIRED.filter((r) => !have.has(r)).map((r) => LABELS[r]);
  if (missingColumns.length) {
    return { error: 'no_header', missingColumns, missingRoles: missingColumns, cols, items: [], totals: [] };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = splitRow(lines[i]);
    const row = { line: i + 1, raw: lines[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const lead = `${cell(row, 'shop')}${cell(row, 'platform')}${String(cells[0] || '').trim()}`
      + `${cell(row, 'site')}`;
    if (/^(合计|总计|小计|汇总|total)/i.test(lead)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals, missingColumns: [] };
}

/** 表里实际出现了哪些角色（用于决定"广告费账单"这类可选列要不要逐格查空）。 */
function presentRoles(t) {
  const have = new Map();
  for (const c of (t && t.cols) || []) {
    if (c.role && !have.has(c.role)) have.set(c.role, c.header);
  }
  return have;
}

function distinct(items, role) {
  const s = new Set();
  for (const it of items) {
    const v = cell(it, role);
    if (v) s.add(v);
  }
  return [...s];
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

/* ===== 免费档（完整可用的核心产出）执行的检查 ===== */

/** 检查 1：佣金 = 销售额 × 佣金率（按账单自己列示的数字逐行复算）。 */
function checkCommission(it) {
  const base = num(it, 'base');
  const rate = num(it, 'rate');
  const stated = num(it, 'commission');
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate / 100);
  const diff = round2(stated - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '佣金与复算不符', line: it.line,
    message: `${who(it)}的佣金列的是 ${stated.toFixed(2)}；按账单自己列示的 销售额 ${base.toFixed(2)}`
      + ` × 佣金率 ${rate}% 应为 ${expect.toFixed(2)}，`
      + `${diff > 0 ? `多扣 ${diff.toFixed(2)}` : `少扣 ${Math.abs(diff).toFixed(2)}`}。`,
    advice: `先核佣金率档位：这张结算单这一行写的佣金率是 ${rate}%；若实际适用档位不是它，`
      + '结算单的「佣金率」列也要一起改 —— 只改佣金不改佣金率，下个月还会错。',
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

/** 检查 2：广告费勾稽（结算单列示的广告费 = 广告费账单金额）。 */
function checkAdFee(it) {
  const stated = num(it, 'ad_fee');
  const bill = num(it, 'ad_bill');
  if (stated === null || bill === null) return null;
  const diff = round2(stated - bill);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '广告费与账单不符', line: it.line,
    message: `${who(it)}结算单上列示的广告费是 ${stated.toFixed(2)}，广告费账单金额是 ${bill.toFixed(2)}，`
      + `相差 ${Math.abs(diff).toFixed(2)}（${diff > 0 ? '结算单多列' : '结算单少列'}）。`,
    advice: '两张表口径要一致：先确认是不是账单期间与结算期间错开（跨期广告费最常在这里差），'
      + '再看账单里有没有返还 / 赠款没冲减。差额部分在查清前不要认。',
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

/** 检查 3：结算净额 = 销售额 − 佣金 − 广告费 − 其它费用。 */
function checkNet(it) {
  const base = num(it, 'base');
  const commission = num(it, 'commission');
  const adFee = num(it, 'ad_fee');
  const otherFee = num(it, 'other_fee');
  const stated = num(it, 'net');
  if (base === null || commission === null || adFee === null || otherFee === null || stated === null) return null;
  const expect = round2(base - commission - adFee - otherFee);
  const diff = round2(stated - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '结算净额与复算不符', line: it.line,
    message: `${who(it)}的结算净额列的是 ${stated.toFixed(2)}；按 销售额 ${base.toFixed(2)}`
      + ` − 佣金 ${commission.toFixed(2)} − 广告费 ${adFee.toFixed(2)} − 其它费用 ${otherFee.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，`
      + `${diff < 0 ? `账单少结 ${Math.abs(diff).toFixed(2)}` : `账单多结 ${diff.toFixed(2)}`}。`,
    advice: '把这条差额和同一行里的三个扣项比一比（佣金 / 广告费 / 其它费用）：差额与哪一项相等，'
      + '问题就在哪一项 —— 完整档会把差额直接归到这三类并给出带行号的申诉口径。',
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

/**
 * 检查 4：合计行逐列复核（合计 ≠ 各明细行相加 ⇒ 行数没对齐，先别再往下核）。
 * 一行合计只出一条结论（把这一行里所有对不上的列一起列出来），
 * 否则 6 个金额列会变出 6 条内容几乎相同的发现，把申诉清单冲淡。
 */
function checkTotals(totals, items) {
  const out = [];
  for (const t of totals) {
    const bad = [];
    for (const role of SUM_ROLES) {
      const raw = t.byRole[role];
      if (raw === undefined || String(raw).trim() === '') continue;
      if (isBlank(raw)) continue;                   // 合计行该列本来就留空 ⇒ 不是问题
      const stated = normNumber(raw);
      if (stated === null) continue;                // 不是数字（占位符由缺失检查负责）
      const sum = round2(items.reduce((s, it) => {
        const n = num(it, role);
        return s + (n === null ? 0 : n);
      }, 0));
      if (Math.abs(sum - stated) > TOL) {
        bad.push(`「${LABELS[role]}」合计 ${stated.toFixed(2)} vs 明细相加 ${sum.toFixed(2)}`
          + `（差 ${round2(stated - sum).toFixed(2)}）`);
      }
    }
    if (!bad.length) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line,
      message: `第 ${t.line} 行合计行有 ${bad.length} 列对不上：${bad.join('；')}。`,
      advice: '要么明细行漏了某个店铺 / 平台 / 站点，要么合计行没跟着更新；'
        + '合计对不上时先别拿这张单去核佣金率，先把行数对齐。',
      basis: `原文第 ${t.line} 行：${t.raw}`,
    });
  }
  return out;
}

/** 检查 5：重复结算（同一店铺 + 平台 + 站点 + 期间正常只有一行汇总）。 */
function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = ['shop', 'platform', 'site', 'period'].map((r) => cell(it, r)).join('|');
    if (key === '|||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复结算（同一维度出现多行）', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次。`,
        advice: '同一店铺 + 平台 + 站点 + 期间正常只有一行汇总；重复行会让佣金、广告费和净额一起翻倍，'
          + '先确认是不是"结算明细行 + 汇总行"混在同一张表里了。',
        basis: `原文第 ${it.line} 行：${it.raw}`,
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 检查 6：关键字段缺失或占位符（缺这一格就算不出来，绝不用 0 或默认值替你填）。 */
function checkBlanks(items, roles) {
  const out = [];
  for (const it of items) {
    for (const role of roles) {
      const s = cell(it, role);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔钱就算不出来；补齐前本工具不会用 0 或默认值替你填，也不会替你下结论。',
          basis: `原文第 ${it.line} 行：${it.raw}`,
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  const text = p.text || p.content || '';
  if (!String(text).trim()) {
    return insufficient(['原文（text）'], '请把平台结算单与广告费账单（含表头）贴进来：'
      + '可用 {"text": "…"}，或先用 --sample 看看需要什么格式。');
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）'], '入参里没有任何可读的行；请把结算单与广告费账单（含表头）贴进来。');
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的平台结算单与广告费账单汇总（要能认出「销售额」「佣金率」「佣金」'
      + '「广告费平台账单」「广告费」「其它费用」「结算净额」）',
      `本次没认出来的列：${t.missingColumns.join('、')}`,
      '从平台后台把结算单与广告费账单导出后，连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一个结算明细行（店铺 / 平台 / 站点 / 期间的汇总行）'],
      '只认到表头，没有明细行；请把结算单的数据行一起贴进来。');
  }

  const have = presentRoles(t);
  // 只在表头认出来时才逐格查空：缺列本身已由 no_header 拦下，可选列没出现就不该报缺失。
  const blankRoles = [];
  for (const role of ['shop', 'platform', 'site', 'period', 'base', 'rate', 'commission',
    'ad_bill', 'ad_fee', 'other_fee', 'net']) {
    if (have.has(role)) blankRoles.push(role);
  }

  const findings = [];
  let executed = CHECKS_GIVEN.slice();

  for (const it of t.items) {
    const a = checkCommission(it); if (a) findings.push(a);
    const b = checkAdFee(it); if (b) findings.push(b);
    const c = checkNet(it); if (c) findings.push(c);
  }
  for (const f of checkTotals(t.totals, t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items, blankRoles)) findings.push(f);

  let appeals = [];


  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    basis: '佣金 = 销售额 × 佣金率；结算净额 = 销售额 − 佣金 − 广告费 − 其它费用；'
      + '结算单列示的广告费 = 广告费账单金额；合计行 = 各明细行之和（逐列复核）。',
    summary: {
      rows: t.items.length,
      shops: distinct(t.items, 'shop').length,
      platforms: distinct(t.items, 'platform').length,
      sites: distinct(t.items, 'site').length,
      periods: distinct(t.items, 'period').length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      base_total: sumOf('base'),
      commission_total: sumOf('commission'),
      ad_bill_total: sumOf('ad_bill'),
      ad_fee_total: sumOf('ad_fee'),
      other_fee_total: sumOf('other_fee'),
      net_total: sumOf('net'),
    },
    scope: {
      executed,
      checks_not_run: CHECKS_WITHHELD.slice(),
      out_of_scope: OUT_OF_SCOPE,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: executed,
    checks_out_of_scope: OUT_OF_SCOPE,
  };

    result.checks_not_run = CHECKS_WITHHELD.slice();
  

  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张结算单与广告费账单按上面写明的口径算得对**：'
      + '佣金 = 销售额 × 佣金率、结算净额 = 销售额 − 佣金 − 广告费 − 其它费用、'
      + '结算单列示的广告费 = 广告费账单金额、合计行逐列相符。'
      + '它**不代表**平台的佣金率档位与你的合同一致，也不代表广告投放明细逐条无差 —— 那些不在本工具范围内。';
  }

  return { status: 'success', result };
}

// ⛔ 骨架原来只导出 4 个名字 ⇒ 新包从一开始就不满足引擎契约
//    （各守卫都要 parseTable/roleOf/OUT_OF_SCOPE），这里一次给全。
module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
