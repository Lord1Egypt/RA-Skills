#!/usr/bin/env node
/**
 * food-label-compliance-check.js —— 食品标签与配料表合规核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：食品生产企业**每个新品上市**、**每次包材改版**，都得把标签与配料表核一遍：
 *   配料表必须按加入量递减排列（量大的在前，同量并列）；配料表要与**投料记录**一一对应
 *   （投料里有、配料表没有 = 漏标；配料表写了却没投 = 抄错或虚假标示）；
 *   投料里出现的致敏物质必须在标签上提示；营养成分表要能按「蛋白质×17 + 脂肪×37 + 碳水×17」
 *   复算出能量、NRV% 要和营养素参考值对上。标签错一项 = **下架 + 罚款 + 召回**，
 *   市场监管抽检直接拿标签与配料表对投料记录 —— 对不上就是虚假标示。
 *
 * ⚠️ 本文件是**免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *     ① 配料表顺序；② 配料与投料记录一致性；③ 致敏物质提示；
 *     ④ 营养成分表算术复算；⑤ 批次重复登记与同产品同日两个标签版本；⑥ 字段合法性。
 *    **完整档（付费）的实现不在这个包里** —— 生产日期/保质期与贮存条件矛盾检测、
 *    标签与包材版本对应关系（跨表比对）、净含量与规格/箱规复算、宣称与配料矛盾、
 *    分产品×分配料汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定配方本身是否合法、不判定标签版式与字符高度是否合规、不判定致敏原是否低于阈值、
 *          不读 .xlsx / .pdf / 实物标签图片、不联网核验检测报告真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '配料表顺序（按加入量递减，量大的在前，同量可并列；与投料记录逐位比对）',
  '配料与投料记录一致性（投料里有、配料表没有 / 配料表有、投料记录没有，双向点名）',
  '致敏物质提示（含麸质谷物 / 甲壳类 / 鱼 / 蛋 / 花生 / 大豆 / 乳 / 坚果 / 芝麻；投料里有则标签必须提示）',
  '营养成分表算术复算（每 100g 能量 = 蛋白质×17 + 脂肪×37 + 碳水化合物×17；NRV% 与营养素参考值一致）',
  '同一批次重复登记（同一产品 + 同一批次号只能有一行）与同产品同日两个标签版本',
  '字段合法性（净含量单位、日期格式、数值为负或为零、必需字段缺失）',
];

const CHECKS_WITHHELD = [
  '生产日期/保质期与贮存条件矛盾检测（常温保质期却要求冷藏 / 冷冻、已超出保质期，逐行给出到期日与超出天数）',
  '标签与包材版本对应关系（同一产品多版本标签未标注换版日期；与「包材版本台账」段跨表比对）',
  '净含量与规格/箱规复算（单件净含量 × 件数 = 箱规，单位换算后比对）',
  '宣称与配料矛盾（写"无糖"却含糖、写"不含防腐剂"却有防腐剂、写"不含麸质"却含小麦）',
  '分产品 × 分配料汇总清单（按问题数降序 + 每组可整改动作）+ result.rollup',
];

const OUT_OF_SCOPE = [
  '判定这款食品的配方本身是否合法、该用什么配料、配料能不能用（本工具只核标签与投料记录的字面一致性）',
  '判定标签版式、字体字号、字符高度、营养标签版面是否符合 GB 7718 / GB 28050 的版式要求（那要看实物标签与第三方判定）',
  '判定致敏物质是否真的低于阈值、是否属于可豁免情形（本工具只按投料记录里出现的致敏原关键词做提示核对）',
  '读取 .xlsx / .pdf / 实物标签图片原件、联网核验检测报告与供应商声明的真伪，替代企业食品安全管理员或监管部门的认定',
];

// 样例：一本**干净**的食品标签与配料表台账 —— 两个产品、三个批次（其中一个产品有两个标签版本），
// 配料表顺序与投料量一致、配料表与投料记录一一对应、致敏物质提示齐全、营养成分表算术与 NRV% 复算一致、
// 批次不重复、字段都合法；追加五项也全过：保质期与贮存条件不矛盾、包材版本台账能对上、箱规复算一致、
// 宣称与配料不矛盾。**全表零命中**。
const SAMPLE_TEXT = [
  '产品名称\t批次号\t配料表\t投料记录\t净含量\t规格\t箱规\t生产日期\t保质期\t贮存条件\t营养成分表\t致敏物质\t标签版本\t换版日期\t宣称\t核对基准日\t备注',
  '原味苏打饼干\tPC-2026-0301\t小麦粉、棕榈油、白砂糖、食用盐、碳酸氢钠、酵母\t小麦粉 45kg、棕榈油 12kg、白砂糖 6kg、食用盐 1kg、碳酸氢钠 0.4kg、酵母 0.3kg\t200g\t200g×24袋/箱\t4.8kg/箱\t2026-03-01\t12个月\t常温干燥处\t能量 1839kJ；蛋白质 7.0g；脂肪 18.0g；碳水化合物 62.0g；钠 320mg；NRV% 能量 22%，蛋白质 12%，脂肪 30%，碳水化合物 21%，钠 16%\t含麸质谷物（小麦）\tV2\t2026-02-10\t不添加防腐剂\t2026-03-31\t标签已备案',
  '芝麻苏打饼干\tSB-2026-0310\t小麦粉、棕榈油、白砂糖、芝麻、食用盐、碳酸氢钠\t小麦粉 42kg、棕榈油 11kg、白砂糖 5kg、芝麻 4kg、食用盐 0.9kg、碳酸氢钠 0.35kg\t180g\t180g×20袋/箱\t3.6kg/箱\t2026-03-10\t12个月\t常温干燥处\t能量 1816kJ；蛋白质 6.8g；脂肪 17.0g；碳水化合物 63.0g；钠 280mg；NRV% 能量 22%，蛋白质 11%，脂肪 28%，碳水化合物 21%，钠 14%\t含麸质谷物（小麦）、芝麻\tV1\t2025-11-20\t不添加防腐剂\t2026-03-31\t—',
  '芝麻苏打饼干\tSB-2026-0320\t小麦粉、棕榈油、白砂糖、芝麻、食用盐、碳酸氢钠\t小麦粉 40kg、棕榈油 10.5kg、白砂糖 4.8kg、芝麻 3.8kg、食用盐 0.85kg、碳酸氢钠 0.33kg\t180g\t180g×20袋/箱\t3.6kg/箱\t2026-03-20\t12个月\t常温干燥处\t能量 1816kJ；蛋白质 6.8g；脂肪 17.0g；碳水化合物 63.0g；钠 280mg；NRV% 能量 22%，蛋白质 11%，脂肪 28%，碳水化合物 21%，钠 14%\t含麸质谷物（小麦）、芝麻\tV3\t2026-03-15\t不添加防腐剂\t2026-03-31\t换版后启用新包材',
  '--- 包材版本台账 ---',
  '产品名称\t标签版本\t换版日期',
  '原味苏打饼干\tV2\t2026-02-10',
  '芝麻苏打饼干\tV1\t2025-11-20',
  '芝麻苏打饼干\tV3\t2026-03-15',
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'productName', 'ingredients', 'batching', 'netContent', 'spec',
  'productionDate', 'shelfLife', 'storage', 'nutrition', 'allergens',
  'labelVersion', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['productName', '产品名称'],
  ['ingredients', '配料表'],
  ['batching', '投料记录'],
  ['netContent', '净含量'],
  ['spec', '规格'],
  ['productionDate', '生产日期'],
  ['shelfLife', '保质期'],
  ['storage', '贮存条件'],
  ['nutrition', '营养成分表'],
  ['allergens', '致敏物质'],
  ['labelVersion', '标签版本'],
  ['checkDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['productionDate', '生产日期'],
  ['checkDate', '核对基准日'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位：「箱规」必须排在「规格」前面（否则「装箱规格」会被规格抢走）；
//    「换版日期」必须排在「标签版本」前面（否则带"版次"的表头会落到版本角色上）；
//    兜底的窄词（如「配料」「投料」）只能放在各自具体词之后。
const ROLES = {
  productName: ['产品名称', '品名', '产品'],
  batchNo: ['批次号', '生产批号', '批次编号', '批号', '批次'],
  cartonSpec: ['箱规', '装箱规格', '每箱规格', '外箱规格'],
  spec: ['规格', '包装规格', '单件规格'],
  netContent: ['净含量', '净重'],
  ingredients: ['配料表', '配料清单', '配料次序', '配料'],
  batching: ['投料记录', '投料清单', '投料明细', '投料表', '投料'],
  nutrition: ['营养成分表', '营养成分', '营养素含量'],
  allergens: ['致敏物质提示', '致敏物质', '致敏原', '过敏原'],
  labelVersionDate: ['换版日期', '包材换版日期', '标签换版日期', '版次日期', '启用日期'],
  labelVersion: ['标签版本', '标签版次', '标签版本号', '版本号', '版次'],
  claims: ['标签宣称', '宣称', '声称'],
  productionDate: ['生产日期', '制造日期', '生产日'],
  shelfLife: ['保质期', '保存期', '货架期'],
  storage: ['贮存条件', '储存条件', '贮藏条件', '保存条件', '贮存'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明'],
};

const LABELS = {};
for (const [role, label] of REQUIRED_FIELDS) LABELS[role] = label;
LABELS.batchNo = '批次号';
LABELS.cartonSpec = '箱规';
LABELS.labelVersionDate = '换版日期';
LABELS.claims = '宣称';
LABELS.note = '备注';

// 每种致敏物质类别的识别关键词（GB 7718 的八类 + 芝麻；只按关键词做提示核对，不判定阈值）
const ALLERGEN_GROUPS = [
  { group: '含麸质谷物', keys: ['麸质', '小麦', '大麦', '黑麦', '燕麦', '青稞', '面粉'] },
  { group: '甲壳类', keys: ['甲壳', '虾', '蟹', '龙虾', '螯虾', '虾皮'] },
  { group: '鱼类', keys: ['鱼'] },
  { group: '蛋类', keys: ['蛋'] },
  { group: '花生', keys: ['花生'] },
  { group: '大豆', keys: ['大豆', '黄豆', '豆粉', '豆浆', '豆蛋白', '腐竹', '酱油', '豆豉'] },
  { group: '乳', keys: ['乳粉', '乳清', '乳糖', '牛乳', '羊乳', '炼乳', '奶油', '乳酪', '奶酪', '乳蛋白', '牛奶', '奶粉', '酸奶', '黄油', '乳固体'] },
  { group: '坚果', keys: ['坚果', '杏仁', '核桃', '腰果', '榛子', '开心果', '碧根果', '夏威夷果', '松子'] },
  { group: '芝麻', keys: ['芝麻'] },
];

// 营养素参考值（GB 28050：能量 8400 kJ、蛋白质 60 g、脂肪 60 g、碳水化合物 300 g、钠 2000 mg）
const NRV_REFS = { energy: 8400, protein: 60, fat: 60, carb: 300, sodium: 2000 };

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「合规」，也不说「有问题」。',
  };
}

/** 全角数字 / 全角标点 / 全角空格归一化成半角（真实台账里全角很常见） */
function fw(raw) {
  return String(raw === undefined || raw === null ? '' : raw)
    .replace(/[\uFF10-\uFF19]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\uFF0E/g, '.')
    .replace(/\uFF0D/g, '-')
    .replace(/\uFF05/g, '%')
    .replace(/\u3000/g, ' ');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = fw(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 空白 / 占位符判定。⚠️ 「无」**不算**空白：致敏物质栏写「无」是有效值（表示不含致敏物质），
 *  把它当空白会漏掉"投料里有致敏原、标签却写无"这种最要命的错。日期用的空白判定见 isBlankDate。 */
function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = fw(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|不适用|待填|待补|待定|待核|暂无)$/i.test(s);
}

/** 日期字段的空白判定：「无」「/」这类等于没填 */
function isBlankDate(v) {
  if (isBlank(v)) return true;
  return /^(无|没有|暂无|\/)$/.test(fw(v).trim());
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = fw(raw).trim();
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
/** b − a（整天数，正数表示 b 在 a 之后） */
/** 日期 + 月数（按自然月加，目标月没有那一天就退到当月最后一天） */
const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line === undefined || line === null ? '' : line));
}

function roleOf(header) {
  const h = fw(header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/**
 * 解析成 {header, cols, items, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text === undefined || text === null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [],
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
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const cell = (it, role) => String(it[role] === undefined || it[role] === null ? '' : it[role]).trim();

function who(it) {
  const name = cell(it, 'productName');
  const batch = cell(it, 'batchNo');
  return `第 ${it.line} 行「${name || '未命名产品'}${batch ? ' / ' + batch : ''}」`;
}

/** 每条结论都带原文依据：行号 + 产品名称 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    product: cell(it, 'productName'),
    batch_no: cell(it, 'batchNo'),
    evidence: String(it.raw === undefined || it.raw === null ? '' : it.raw).slice(0, 200),
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

/* ============================ 单位与字段解析 ============================ */

/** 计量单位 → {kind:'mass'|'volume', factor:换算成 g / mL 的系数}；认不出来返回 null */
function unitKind(unit) {
  const u = fw(unit).trim();
  const l = u.toLowerCase();
  if (l === 'g' || u === '克') return { kind: 'mass', factor: 1 };
  if (l === 'kg' || u === '千克' || u === '公斤') return { kind: 'mass', factor: 1000 };
  if (l === 'mg' || u === '毫克') return { kind: 'mass', factor: 0.001 };
  if (u === '斤') return { kind: 'mass', factor: 500 };
  if (l === 'ml' || u === '毫升') return { kind: 'volume', factor: 1 };
  if (l === 'l' || u === '升') return { kind: 'volume', factor: 1000 };
  return null;
}

/** 配料表 → 有序的配料名数组（顿号 / 逗号 / 分号 / 竖线都当分隔符） */
function parseIngredientList(raw) {
  const s = fw(raw).replace(/[；;|]/g, '、').replace(/\n/g, '、');
  return s.split(/[、,，]/)
    .map((x) => x.trim().replace(/^[（(]?\d+[）).、]\s*/, '').trim())
    .filter(Boolean);
}

/** 配料名归一化：去掉括号里的补充说明（如「小麦粉（≥30%）」）与所有空格，用于两边比对 */
function cleanName(name) {
  return fw(name).replace(/[（(][^）)]*[）)]/g, '').replace(/\s+/g, '').trim();
}

/** 投料记录 → [{name, amount(换算到 g/mL), value(原始数值), unit, kind}]；读不出数量的条目 amount 为 null */
function parseMaterialAmounts(raw) {
  const s = fw(raw).replace(/[；;|]/g, '、').replace(/\n/g, '、');
  const out = [];
  for (const tokRaw of s.split(/[、,，]/)) {
    const tok = tokRaw.trim().replace(/[：:]/g, ' ');
    if (!tok) continue;
    const m = /^(.+?)\s*(\d+(?:\.\d+)?)\s*([A-Za-z\u4e00-\u9fa5]{0,3})$/.exec(tok);
    if (!m) {
      out.push({ name: cleanName(tok), amount: null, value: null, unit: '', kind: null });
      continue;
    }
    const k = m[3] ? unitKind(m[3]) : null;
    const n = normNumber(m[2]);
    if (n === null) {
      out.push({ name: cleanName(m[1]), amount: null, unit: m[3] || '', kind: null });
      continue;
    }
    out.push({
      name: cleanName(m[1]),
      unit: m[3] || '',
      value: n,
      kind: k ? k.kind : null,
      amount: k ? round2(n * k.factor) : n,
    });
  }
  return out;
}

/** 净含量 → {value, unit, kind, base, unitOk}；形态不对返回 null（example: 200g / 1.5L） */
function parseNetContent(raw) {
  const s = fw(raw).replace(/\s+/g, '').replace(/^净含量[:：]?/, '').replace(/^\+/, '');
  const m = /^(-?\d+(?:\.\d+)?)([A-Za-z\u4e00-\u9fa5]*)$/.exec(s);
  if (!m) return null;
  const k = m[2] ? unitKind(m[2]) : null;
  const value = normNumber(m[1]);
  if (value === null) return null;
  return {
    value,
    unit: m[2] || '',
    kind: k ? k.kind : null,
    base: k ? value * k.factor : value,
    unitOk: k !== null,
  };
}

/** 规格 → {value, unit, kind, base, count}（example: 200g×24袋/箱）；读不出返回 null */
/** 箱规 → {value, unit, kind, base}（example: 4.8kg/箱）；读不出返回 null */
/** 保质期 → {value, unit:'month'|'year'|'day'}；读不出返回 null（允许「常温 12个月」这种带前缀的写法） */
function parseShelfLife(raw) {
  const m = /(\d+(?:\.\d+)?)\s*(个月|月|天|日|年)/.exec(fw(raw));
  if (!m) return null;
  const v = Number(m[1]);
  if (!Number.isFinite(v)) return null;
  if (m[2] === '个月' || m[2] === '月') return { value: v, unit: 'month' };
  if (m[2] === '年') return { value: v, unit: 'year' };
  return { value: v, unit: 'day' };
}

/** 生产日期 + 保质期 = 到期日 */
/** 营养成分表 → {energyKj, protein, fat, carb, sodiumMg, nrv:{…}}；认不出来的项为 null */
function parseNutrition(raw) {
  const s = fw(raw);
  if (!s.trim()) return null;
  const idx = s.search(/NRV|营养素参考值|参考值/);
  const main = idx >= 0 ? s.slice(0, idx) : s;
  const nrvPart = idx >= 0 ? s.slice(idx) : s;
  const pick = (re, text) => {
    const m = re.exec(text);
    return m ? Number(m[1]) : null;
  };
  const protein = pick(/(?:蛋白质|蛋白)[^\d]{0,4}(\d+(?:\.\d+)?)\s*(?:g|克)/, main);
  const fat = pick(/(?:脂肪)[^\d]{0,4}(\d+(?:\.\d+)?)\s*(?:g|克)/, main);
  const carb = pick(/(?:碳水化合物|碳水)[^\d]{0,4}(\d+(?:\.\d+)?)\s*(?:g|克)/, main);
  const sod = /(?:钠)[^\d]{0,4}(\d+(?:\.\d+)?)\s*(mg|毫克|g|克)/.exec(main);
  const sodiumMg = sod ? (/^(mg|毫克)$/.test(sod[2]) ? Number(sod[1]) : Number(sod[1]) * 1000) : null;
  const en = /(?:能量)[^\d]{0,4}(\d+(?:\.\d+)?)\s*(kJ|kj|KJ|千焦|kcal|千卡|大卡)/.exec(main);
  const energyKj = en
    ? (/^(kcal|千卡|大卡)$/.test(en[2]) ? round2(Number(en[1]) * 4.184) : Number(en[1]))
    : null;
  return {
    energyKj,
    protein,
    fat,
    carb,
    sodiumMg,
    nrv: {
      energy: pick(/(?:能量)[^\d%]{0,10}(\d+)\s*%/, nrvPart),
      protein: pick(/(?:蛋白质)[^\d%]{0,10}(\d+)\s*%/, nrvPart),
      fat: pick(/(?:脂肪)[^\d%]{0,10}(\d+)\s*%/, nrvPart),
      carb: pick(/(?:碳水化合物|碳水)[^\d%]{0,10}(\d+)\s*%/, nrvPart),
      sodium: pick(/(?:钠)[^\d%]{0,10}(\d+)\s*%/, nrvPart),
    },
  };
}

/* ============================ 免费档检查（六项） ============================ */

function checkIngredientOrder(items) {
  // ① 配料表顺序：按加入量递减，量大的在前；同量可并列（投料记录是加入量的唯一来源）
  const out = [];
  for (const it of items) {
    const list = parseIngredientList(cell(it, 'ingredients')).map(cleanName).filter(Boolean);
    const feed = parseMaterialAmounts(cell(it, 'batching'));
    if (list.length < 2 || !feed.length) continue;
    const amt = new Map();
    for (const m of feed) if (m.name && m.amount !== null && !amt.has(m.name)) amt.set(m.name, m);
    for (let i = 0; i + 1 < list.length; i++) {
      const a = amt.get(list[i]);
      const b = amt.get(list[i + 1]);
      if (!a || !b || a.kind !== b.kind || a.amount === b.amount) continue;
      if (a.amount < b.amount - TOL) {
        out.push(finding('P1', '配料表顺序与投料量不符', it, round2(b.amount - a.amount),
          `${who(it)}：配料表第 ${i + 1} 位「${list[i]}」（投料 ${a.value}${a.unit}）的加入量`
          + `小于第 ${i + 2} 位「${list[i + 1]}」（投料 ${b.value}${b.unit}）`
          + `—— 配料表要按加入量递减排列，量大的排在前面（只有同量才可以并列）。`,
          '按投料记录把加入量大的物料往前排（或者核对是不是投料量抄错了）。'
          + '配料表顺序是标签抽检最容易直接判不合格的一条，改完记得同步包材文件与标签稿。'));
      }
    }
  }
  return out;
}

function checkIngredientConsistency(items) {
  // ② 配料与投料记录一致性：投料里有、配料表没有 / 配料表有、投料记录没有
  const out = [];
  for (const it of items) {
    const list = parseIngredientList(cell(it, 'ingredients')).map(cleanName).filter(Boolean);
    const feed = parseMaterialAmounts(cell(it, 'batching'));
    if (!list.length || !feed.length) continue;
    const feedNames = feed.map((m) => m.name).filter(Boolean);
    const labelSet = new Set(list);
    const feedSet = new Set(feedNames);
    const onlyFeed = feedNames.filter((n, i) => !labelSet.has(n) && feedNames.indexOf(n) === i);
    const onlyLabel = list.filter((n, i) => !feedSet.has(n) && list.indexOf(n) === i);
    if (!onlyFeed.length && !onlyLabel.length) continue;
    const parts = [];
    if (onlyFeed.length) parts.push(`投料记录里有、配料表上没有：${onlyFeed.join('、')}`);
    if (onlyLabel.length) parts.push(`配料表上有、投料记录里没有：${onlyLabel.join('、')}`);
    out.push(finding('P0', '配料与投料记录不一致', it, onlyFeed.length + onlyLabel.length,
      `${who(it)}：配料表与投料记录对不上 —— ${parts.join('；')}。`,
      '配料表必须与投料记录一一对应：投料里有的物料一定要在配料表里出现（并按加入量排序）；'
      + '配料表写了却没投的物料更要查清楚（是漏投、还是抄了别的配方）。'
      + '先按投料记录把两边对齐，再重跑一遍。'));
  }
  return out;
}

function checkAllergens(items) {
  // ③ 致敏物质提示：投料记录里出现的致敏原，标签的「致敏物质」栏必须提示（反向多余提示也点出来）
  const out = [];
  for (const it of items) {
    const feedRaw = cell(it, 'batching');
    if (!feedRaw) continue;
    // 「蛋白质」里的「蛋」不是蛋类致敏原，先剔掉再按关键词扫
    const feed = fw(feedRaw).replace(/蛋白质/g, '');
    const label = fw(cell(it, 'allergens'));
    const miss = [];
    const extra = [];
    for (const g of ALLERGEN_GROUPS) {
      const inFeed = g.keys.some((k) => feed.indexOf(k) >= 0);
      const inLabel = g.keys.some((k) => label.indexOf(k) >= 0);
      if (inFeed && !inLabel) miss.push(g.group);
      if (!inFeed && inLabel) extra.push(g.group);
    }
    if (miss.length) {
      out.push(finding('P0', '致敏物质提示缺失', it, undefined,
        `${who(it)}：投料记录里出现了 ${miss.join('、')} 这几类致敏物质，`
        + `但标签「致敏物质」栏写的是「${label || '(空)'}」—— 没有提示。`,
        '只要配料（含投料时加入的辅料、复配原料带入的）里含有致敏物质，标签就必须提示：'
        + '按实际投料补上致敏物质提示，并同步包材文件；复配原料要向下游供应商要致敏原声明再确认一遍。'));
    }
    if (extra.length) {
      out.push(finding('P2', '致敏物质与投料不符', it, undefined,
        `${who(it)}：标签「致敏物质」栏提示了 ${extra.join('、')}，`
        + `但投料记录里找不到对应的致敏原 —— 可能是多写、也可能是投料记录漏登了这类物料。`,
        '两种情况都要查清：确实是多余提示的删掉（多余提示会白白缩小客群）；'
        + '是投料记录漏登的补上记录（漏登会让致敏物质核对永远失真）。'));
    }
  }
  return out;
}

function checkNutrition(items) {
  // ④ 营养成分表算术复算：每 100g 能量 = 蛋白质×17 + 脂肪×37 + 碳水化合物×17；NRV% 与参考值一致
  const out = [];
  for (const it of items) {
    const raw = cell(it, 'nutrition');
    if (!raw) continue;
    const n = parseNutrition(raw);
    const hasAny = n && (n.energyKj !== null || n.protein !== null || n.fat !== null || n.carb !== null);
    if (!hasAny) {
      out.push(finding('P2', '营养成分表无法解析', it, undefined,
        `${who(it)}：营养成分表「${raw}」里读不出能量 / 蛋白质 / 脂肪 / 碳水化合物的数值`
        + '（请写成「能量 1839kJ；蛋白质 7.0g；脂肪 18.0g；碳水化合物 62.0g；钠 320mg」这种形态）。',
        '按标签上印的数值逐项写成「项目 + 数值 + 单位」，本工具才能复算；'
        + '解析不出来的项一律不给结论，不会替你猜。'));
      continue;
    }
    if (n.energyKj !== null && n.protein !== null && n.fat !== null && n.carb !== null) {
      const calc = round2(17 * n.protein + 37 * n.fat + 17 * n.carb);
      const diff = round2(n.energyKj - calc);
      if (Math.abs(diff) > 1) {
        out.push(finding('P1', '营养成分表算术不符', it, diff,
          `${who(it)}：能量按「蛋白质×17 + 脂肪×37 + 碳水化合物×17」复算是 ${calc} kJ`
          + `（${n.protein}×17 + ${n.fat}×37 + ${n.carb}×17），标签写的是 ${n.energyKj} kJ，差 ${diff} kJ。`,
          '营养标签的能量必须与三个产能营养素对得上：先核对是不是化验报告抄串了，'
          + '或者碳水里漏了膳食纤维 / 糖醇的折算系数（膳食纤维按 8 kJ/g、部分糖醇按 10 kJ/g）。'
          + '改完把配方与测算表一起归档。'));
      }
    }
    const pairs = [
      ['energy', n.energyKj, NRV_REFS.energy, '能量', 'kJ'],
      ['protein', n.protein, NRV_REFS.protein, '蛋白质', 'g'],
      ['fat', n.fat, NRV_REFS.fat, '脂肪', 'g'],
      ['carb', n.carb, NRV_REFS.carb, '碳水化合物', 'g'],
      ['sodium', n.sodiumMg, NRV_REFS.sodium, '钠', 'mg'],
    ];
    for (const [key, val, ref, label, unit] of pairs) {
      const declared = n.nrv[key];
      if (declared === null || val === null) continue;
      const calc = Math.round((val / ref) * 100);
      if (Math.abs(declared - calc) > 1) {
        out.push(finding('P2', '营养素参考值不一致', it, declared - calc,
          `${who(it)}：「${label}」的 NRV% 按 ${val}${unit} ÷ 参考值 ${ref}${unit} 复算是 ${calc}%，`
          + `标签写的是 ${declared}%，差 ${declared - calc} 个百分点。`,
          `NRV% 是强制标示项，按 GB 28050 的参考值（能量 8400kJ、蛋白质 60g、脂肪 60g、`
          + `碳水化合物 300g、钠 2000mg）重算并取整；改完连营养标签版面一起换版。`));
      }
    }
  }
  return out;
}

function checkDuplicates(items) {
  // ⑤ 同一批次重复登记（同一产品 + 同一批次号只能有一行）与同产品同日两个标签版本
  const out = [];
  const seenBatch = new Map();
  const seenFull = new Map();
  const byProdDate = new Map();
  for (const it of items) {
    const name = cleanName(cell(it, 'productName'));
    if (!name) continue;
    const batch = cell(it, 'batchNo');
    const prod = normDate(it.productionDate);
    const prodRaw = cell(it, 'productionDate');
    const dateKey = prod || prodRaw;
    const ver = cleanName(cell(it, 'labelVersion'));
    let dupBatch = false;

    if (batch) {
      const k = name + '|' + batch;
      if (seenBatch.has(k)) {
        dupBatch = true;
        out.push(finding('P0', '批次重复登记', it, undefined,
          `${who(it)}：批次号「${batch}」在第 ${seenBatch.get(k)} 行已经登记过 —— 同一批次重复登记。`,
          '一个批次在一本台账里只应有一行：重复登记会让配料表、投料记录、标签版本各算一套，'
          + '抽检时拿哪一行都能对不上。合并成一行，历史改动写进备注（别直接删行）。'));
      } else {
        seenBatch.set(k, it.line);
      }
    }

    if (dateKey && !dupBatch) {
      const k = name + '|' + dateKey + '|' + ver;
      if (seenFull.has(k)) {
        out.push(finding('P0', '批次重复登记', it, undefined,
          `${who(it)}：同一产品 + 同一生产日期 + 同一标签版本在第 ${seenFull.get(k)} 行已经登记过 —— 重复登记。`,
          '同一产品、同一生产日期、同一标签版本只应有一行：先确认是不是两个批次的批次号没分开填，'
          + '把批次号与投料记录拆清楚再合并重复行。'));
      } else {
        seenFull.set(k, it.line);
      }
      const g = name + '|' + dateKey;
      if (!byProdDate.has(g)) byProdDate.set(g, { it, date: dateKey, name, versions: new Set() });
      byProdDate.get(g).versions.add(ver || '(未填版本)');
    }
  }
  for (const g of byProdDate.values()) {
    if (g.versions.size < 2) continue;
    const list = [...g.versions].join('、');
    out.push(finding('P1', '同产品同日两个标签版本', g.it, g.versions.size,
      `${who(g.it)}：同一个产品（${g.name}）在同一天（${g.date}）上有 ${g.versions.size} 个标签版本`
      + `（${list}）—— 同一天不该同时存在两张不同版本的标签。`,
      '先确认是不是包材换版期的"新旧标签同时在使用"：如果是，按换版计划停用旧版标签；'
      + '如果只是台账登记串了，把生产日期与标签版本分别改对。标签版本混用是**换版管理**上最典型的漏项。'));
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 字段合法性：必需字段缺失 / 日期格式非法 / 净含量单位非法 / 数值为负或为零 / 保质期读不出
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些必需字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如投料记录空着就判不了配料表顺序与致敏物质提示）；'
        + '补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-03-31 / 2026/3/31 / 2026年3月31日 / 20260331 这几种形态）。',
          '把日期改成 2026-03-31 这种形态再跑；日期认不出来时本工具不会拿它去算保质期。'));
      }
    }

    const netRaw = cell(it, 'netContent');
    if (netRaw) {
      const n = parseNetContent(netRaw);
      if (n && n.value < 0) {
        out.push(finding('P0', '数值为负或为零', it, n.value,
          `${who(it)}：净含量是负数（${n.value}）—— 台账里出现负数通常是填反了或用了红字冲销。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n && n.value === 0) {
        out.push(finding('P1', '数值为负或为零', it, n.value,
          `${who(it)}：净含量是 0 —— 净含量为零的预包装食品在标签口径上不成立。`,
          '按实际灌装 / 包装量填真实净含量；还没定量的规格不要先登上标签台账。'));
      } else if (!n || !n.unitOk) {
        out.push(finding('P1', '净含量单位非法', it, undefined,
          `${who(it)}：净含量「${netRaw}」不是「数值 + 法定计量单位」的形态`
          + '（预包装食品只认 g / kg / mL / L 及其中文写法，例如 200g、1.5L；不能写"200"或"200袋"）。',
          '净含量必须与法定计量单位一起标示，而且要与规格、箱规能对得上；'
          + '改完记得同步包材文件（净含量字号还有最小高度要求，那不在本工具范围内）。'));
      }
    }

    const shelfRaw = cell(it, 'shelfLife');
    if (shelfRaw) {
      const s = parseShelfLife(shelfRaw);
      if (!s) {
        out.push(finding('P1', '保质期无法解析', it, undefined,
          `${who(it)}：保质期「${shelfRaw}」读不出「数值 + 单位」（要写成 12个月 / 18个月 / 365天 / 2年）。`,
          '保质期要写成"数字 + 月/天/年"，本工具才能算到期日；'
          + '写成"常温避光"这类只有条件没有期限的，等于没写保质期。'));
      } else if (s.value < 0) {
        out.push(finding('P0', '数值为负或为零', it, s.value,
          `${who(it)}：保质期是负数（${s.value}）—— 台账里出现负数通常是填反了。`,
          '确认是红字冲销还是填错方向；保质期必须是与贮存条件配套的正数。'));
      } else if (s.value === 0) {
        out.push(finding('P1', '数值为负或为零', it, s.value,
          `${who(it)}：保质期是 0 —— 保质期为零等于产品出厂即过期，标签口径上不成立。`,
          '按稳定性试验结论填真实保质期；还没做完试验的不要先印上标签。'));
      }
    }
  }
  return out;
}

/* ============================ 完整档追加检查（付费） ============================ */

/* ============================ 汇总（付费第五项） ============================ */

function countMaterials(items) {
  const set = new Set();
  for (const it of items) {
    for (const m of parseIngredientList(cell(it, 'ingredients'))) {
      const n = cleanName(m);
      if (n) set.add(n);
    }
  }
  return set.size;
}

function buildSummary(items, findings, base) {
  return {
    rows: items.length,
    total: findings.length,
    p0: findings.filter((f) => f.level === 'P0').length,
    p1: findings.filter((f) => f.level === 'P1').length,
    p2: findings.filter((f) => f.level === 'P2').length,
    products: new Set(items.map((it) => cleanName(cell(it, 'productName'))).filter(Boolean)).size,
    materials: countMaterials(items),
    check_date: base,
    basis: '配料表按投料记录的加入量递减排列（同量并列）；配料表与投料记录双向一一对应 —— 差一个物料就报；'
      + '投料记录里出现的每一类致敏物质都必须在「致敏物质」栏被提示；'
      + '营养标签按「蛋白质×17 + 脂肪×37 + 碳水化合物×17」复算能量（kJ/g），NRV% 按参考值'
      + '（能量 8400kJ、蛋白质 60g、脂肪 60g、碳水化合物 300g、钠 2000mg）复算并取整；'
      + '同一产品 + 同一批次号只能有一行；同一产品 + 同一生产日期上出现两个标签版本要报；'
      + '净含量只认 g / kg / mL / L，日期认不出来一律不给结论。',
  };
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text !== undefined && p.text !== null
    ? p.text
    : (p.content !== undefined && p.content !== null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的食品标签与配料表台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的食品标签与配料表台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的食品标签与配料表台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行产品明细（现在只有表头，没有可核对的产品）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];

  for (const f of checkIngredientOrder(t.items)) findings.push(f);
  for (const f of checkIngredientConsistency(t.items)) findings.push(f);
  for (const f of checkAllergens(t.items)) findings.push(f);
  for (const f of checkNutrition(t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  const result = {
    findings,
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
  };

  // 免费档：完整档追加的那五项检查一项都不执行，这里如实记下来（只记「没做」，绝不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);
  result.checks_executed = CHECKS_GIVEN;
  result.checks_not_run = notRun;

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  result.summary = buildSummary(t.items, findings, base);
  result.scope = {
    checks: result.checks_executed,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    check_date: base,
  };
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、'
      + '配料表与投料记录对得上、致敏物质与营养标签自洽**，不代表配方本身合法、'
      + '不代表标签版式与字符高度合规、也不代表致敏原低于阈值或检测报告为真 —— 那些不在本工具范围内。'
      + '（注意：完整档追加的 ' + CHECKS_WITHHELD.length + ' 项检查本次**没有执行** —— '
      + '上面这句"通过"只覆盖本次实际执行的 ' + CHECKS_GIVEN.length + ' 项。）';
  }

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
