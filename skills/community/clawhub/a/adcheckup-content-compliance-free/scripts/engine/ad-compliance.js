'use strict';
/**
 * ad-compliance.js —— 广告文案合规预检（免费档）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以这里刻意不与仓库其他技能共享代码。
 *
 * 免费档只做两项检查，别无其他：
 *   1. 绝对化用语检测 —— 只报**真正带"最优 / 第一 / 唯一"声称**的写法，
 *      绝不因为出现单字「最」或「一」就报（那是"字典式极限词工具"误报的主要来源）；
 *   2. 豁免判定 —— 命中后先按《广告绝对化用语执法指南》第五条、第六条判断该不该报。
 *      可豁免的**不报**，但会单独列进 `exempted` 并写明豁免依据（条例原文层级可追溯）。
 *
 * 刻意不实现（那些属于本版本范围之外的检查项，见 CHECKS_WITHHELD）：
 *   医疗／药品／医美违禁表述、保健食品功效断言、教育培训保证性承诺、
 *   投资理财与招商承诺、房地产升值回报承诺、虚假广告类保证性承诺、批量文案检测。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'，
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 */

/* ---------------------------------------------------------------- 常量 */

const RULES_VERSION = '2026-09-14';

const CHECKS_GIVEN = ['绝对化用语检测（含《广告绝对化用语执法指南》豁免判定）'];

const CHECKS_WITHHELD = [
  '医疗／药品／医美违禁表述',
  '保健食品功效断言',
  '教育培训保证性承诺',
  '投资理财与招商承诺',
  '房地产升值回报承诺',
  '虚假广告类保证性承诺',
  '批量文案检测',
];

const BASIS_ABSOLUTE = '《广告法》第九条第三项（不得使用"国家级""最高级""最佳"等用语）';
const BASIS_GUIDE = '《广告绝对化用语执法指南》（市场监管总局 2023-02-25 公告）';

/**
 * 豁免依据（原文见《广告绝对化用语执法指南》第五条、第六条）。
 * 单列出来是为了让用户看得见"我们故意没报的东西"和理由 —— 这既是精准度，也是可审计性。
 */
const EXEMPTION = {
  NOT_TARGETING: {
    code: 'NOT_TARGETING',
    label: '未指向所推销商品',
    basis: `${BASIS_GUIDE}第五条`,
    detail: '仅表明服务态度、经营理念、企业文化或主观愿望／仅表达目标追求／与商品性能质量无直接关联且不误导',
  },
  SELF_COMPARE: {
    code: 'SELF_COMPARE',
    label: '同一品牌自我比较',
    basis: `${BASIS_GUIDE}第六条第（一）项`,
    detail: '仅用于对同一品牌或同一企业商品进行自我比较',
  },
  USAGE_HINT: {
    code: 'USAGE_HINT',
    label: '使用／保存等消费提示',
    basis: `${BASIS_GUIDE}第六条第（二）项`,
    detail: '仅用于宣传商品的使用方法、使用时间、保存期限等消费提示',
  },
  GRADE_STANDARD: {
    code: 'GRADE_STANDARD',
    label: '依据标准的商品分级用语',
    basis: `${BASIS_GUIDE}第六条第（三）项`,
    detail: '依据国家标准、行业标准、地方标准等认定的商品分级用语，且能够说明依据',
  },
  NAME_MODEL: {
    code: 'NAME_MODEL',
    label: '商品名称／型号／商标／专利',
    basis: `${BASIS_GUIDE}第六条第（四）项`,
    detail: '商品名称、规格型号、注册商标或专利中含有绝对化用语，用于指代商品以区分其他商品',
  },
  AWARD: {
    code: 'AWARD',
    label: '依规评定的奖项称号',
    basis: `${BASIS_GUIDE}第六条第（五）项`,
    detail: '依据国家有关规定评定的奖项、称号中含有绝对化用语',
  },
  TIME_FACT: {
    code: 'TIME_FACT',
    label: '限定条件下的时空顺序／事实信息',
    basis: `${BASIS_GUIDE}第六条第（六）项`,
    detail: '在限定具体时间、地域等条件的情况下，表述时空顺序客观情况，或宣传销量、销售额、市场占有率等事实信息',
  },
  TEMPORAL_WORD: {
    code: 'TEMPORAL_WORD',
    label: '时间／顺序类常用词，不构成"最高级"含义',
    basis: `${BASIS_GUIDE}第二条（绝对化用语指"最高级"含义的用语）`,
    detail: '「最后」「最近」等是表示时间或顺序的常用词，并未声称商品为最优，不属于绝对化用语',
  },
  COMMON_WORD: {
    code: 'COMMON_WORD',
    label: '日常固定搭配，不构成最高级声称',
    basis: `${BASIS_GUIDE}第二条`,
    detail: '如「一站式」「一体化」「第一时间」等固定搭配中的「一」，不构成"第一"的排他性声称',
  },
};

/* -------------------------------------------------------- 绝对化用语词表 */

/**
 * 绝对化用语（高置信）：只收录**明确带"最优 / 第一 / 唯一"声称**的写法。
 * 刻意不收单字「最」「一」「级」；也不做"见到「最」字就报"的字典式匹配。
 * 词条按前缀覆盖，例如「最低价」一条即可覆盖其后各种续写（最低价位等），无需逐字列出变体。
 */
const ABSOLUTE_TERMS = [
  // 最-family：直接的"最优 / 最好"声称
  '最好', '最佳', '最优', '最强', '最先进', '最便宜', '最低价', '最优质', '最专业',
  '最权威', '最领先', '最火爆', '最热销', '最受欢迎', '最值得', '最有效', '最安全',
  '最齐全', '最全面', '最顶级', '最高级', '最高端', '最豪华', '最新科技', '最大', '最全',
  '最高品质', '最佳选择', '最好用', '最划算', '最省钱',
  // 一-family：排他性声称
  '第一品牌', '排名第一', '销量第一', '全国第一', '全球第一', '世界第一', '行业第一',
  '同行业第一', '第一名', '唯一', '独家', '独一无二', '首屈一指', '一劳永逸', '唯一选择',
  '独家首发', '全网独家', '仅此一家', '绝无仅有',
  // 级／极-family
  '国家级', '世界级', '国际级', '顶级', '极品', '极佳', '极致', '终极',
  // 绝对／无上限 family
  '绝对', '100%', '百分百', '全网最低', '史上最', '前所未有', '空前绝后', '无人能及',
  '顶级品质', '史上最强', '秒杀一切', '碾压', '无敌',
];

/**
 * 时间／顺序类「最」字词：**不报**，并给出理由。
 * 这是误报控制的第一道闸 —— 字典式工具在这里翻车最多。
 */
const TEMPORAL_SAFE = [
  '最后', '最近', '最终', '最初', '最新', '最晚', '最早', '最先', '最末',
  '最快', '最多', '最少', '最低', '最高',
];

/** 日常固定搭配：**不报** */
const COMMON_SAFE = ['一站式', '一体化', '一条龙', '一系列', '第一时间', '一揽子', '一次性', '一键'];

/* ---------------------------------------------------------------- 工具 */

function normalize(text) {
  return String(text == null ? '' : text);
}

/** 取命中词前后的上下文，用于人工复核 */
function excerpt(text, index, term) {
  const start = Math.max(0, index - 14);
  const end = Math.min(text.length, index + term.length + 14);
  return (start > 0 ? '…' : '') + text.slice(start, end).replace(/\s+/g, ' ') + (end < text.length ? '…' : '');
}

/** 该命中位置附近是否匹配任一模式（默认前后 20 字窗口） */
function near(text, index, term, re, span = 20) {
  const start = Math.max(0, index - span);
  const end = Math.min(text.length, index + term.length + span);
  return re.test(text.slice(start, end));
}

/* ------------------------------------------------------------ 豁免判定 */

const RE_USAGE = /(食用|饮用|服用|冲泡|保存|储存|存放|冷藏|冷冻|保质|保鲜|赏味|期限|使用(方法|时间|温度|期限|说明)|服用方法|建议用量|开袋|开封|加热|施工温度)/;
/** 第五条：只表明服务态度、经营理念、企业文化、主观愿望或目标追求，未指向商品本身 */
const RE_ATTITUDE = /(努力|宗旨|理念|追求|致力于|竭诚|全力|尽可能|尽量|欢迎|期待|决心|愿望|使命|态度)/;
/** 自我比较必须是**真的在比**，出现「相比／上一代」这类比较标记词才算 */
const RE_SELF = /(相比|相较|对比|较上|比上|上一代|前代|旧款|历代|前作|老款|上一版|上一款|迭代前)/;
const RE_GRADE = /(国家标准|行业标准|地方标准|GB\s*\/?\s*T?\s*\d*|特级|一级品|优级|执行标准|标准认定|分级)/;
const RE_NAME = /(商标|注册商标|专利|注册号|型号|规格型号|品牌名|品名)/;
const RE_AWARD = /(荣获|评定|评选|称号|奖项|金奖|银奖|获评|授予)/;
/** 第六条第（六）项要求「限定具体时间」——只写"全国"不算限定，所以时间与事实信息都要有 */
const RE_TIME_LIMIT = /(20\d{2}\s*年|第[一二三四]季度|\d{1,2}\s*月|上半年|下半年|全年度|年度|本季度|上季度)/;
const RE_FACT = /(销量|销售额|营收|市场占有率|份额|排名|出货量|复购率)/;

/**
 * 判断一个绝对化用语命中是否可依《执法指南》豁免。
 * @returns {Object|null} 命中豁免则返回豁免定义，否则 null
 */
function evaluateExemption(text, index, term) {
  // 一整词就是"最低价 / 最高级"这类真声称时，不能被下面的时间词分支截胡，
  // 但它仍可能命中标准分级、消费提示等豁免
  const isRealClaim = /^最(低|高)(价|级|端|品质|档)/.test(term);
  if (!isRealClaim && TEMPORAL_SAFE.some((w) => term === w || term.startsWith(w))) {
    return EXEMPTION.TEMPORAL_WORD;
  }
  if (COMMON_SAFE.some((w) => term === w || term.startsWith(w) || term.endsWith(w))) {
    if (!/第一(名|品牌)/.test(term)) return EXEMPTION.COMMON_WORD;
  }
  // 第五条：只表明服务态度、经营理念、主观愿望或目标追求（如「尽最大努力」），未指向商品本身
  if (near(text, index, term, RE_ATTITUDE)) return EXEMPTION.NOT_TARGETING;
  if (near(text, index, term, RE_USAGE)) return EXEMPTION.USAGE_HINT;
  if (near(text, index, term, RE_SELF)) return EXEMPTION.SELF_COMPARE;
  if (near(text, index, term, RE_NAME)) return EXEMPTION.NAME_MODEL;
  if (near(text, index, term, RE_AWARD)) return EXEMPTION.AWARD;
  if (near(text, index, term, RE_GRADE)) return EXEMPTION.GRADE_STANDARD;
  // 第六条第（六）项：限定具体时间 + 事实信息，两者缺一不可
  if (near(text, index, term, RE_TIME_LIMIT, 26) && near(text, index, term, RE_FACT, 26)) {
    return EXEMPTION.TIME_FACT;
  }
  return null;
}

/* ---------------------------------------------------------------- 判定 */

function pushFinding(list, f) {
  // 同一位置同一词只报一次
  if (list.some((x) => x.term === f.term && x.index === f.index)) return;
  /* 结论必须有一句**能直接念给人听**的话。
   * 由来（第 168 轮，靠新加的守卫抓出来的真缺陷）：本引擎的结论用 `term` + `context`，
   * **没有 `message` / `detail`** —— 而 `/check` 页面渲染的是 `f.detail || f.message`，
   * 于是广告合规的每条结论在页面上**只有「P0 绝对化用语」这个标题、正文是空的**，
   * 用户根本不知道查到了什么词。这里统一补一句，所有调用方一起受益。 */
  if (!f.message) {
    const t = f.term ? `「${f.term}」` : '';
    f.message = `${f.category || '合规问题'}${t ? '：命中 ' + t : ''}`
      + (f.context ? `（原文：${String(f.context).slice(0, 60)}）` : '');
  }
  list.push(f);
}

/**
 * 广告文案绝对化用语预检（免费档）。
 *
 * @param {Object} input
 * @param {string} input.text        待检文案（标题、正文、口播稿、标签均可拼接后传入）
 * @param {string[]} [input.texts]   多条文案，逐条检测并汇总
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(input) {
  const payload = (input && typeof input === 'object' && !Array.isArray(input)) ? input
    : (typeof input === 'string' ? { text: input } : {});

  let docs = [];
  // 类型不对时如实报"材料不足"，绝不把 123 之类的东西当成文案去扫（那会得出"合规"的假结论）
  if (payload.texts !== undefined && payload.texts !== null && !Array.isArray(payload.texts)) {
    return {
      status: 'insufficient_input',
      missing: [`texts 不是数组（收到的是 ${typeof payload.texts}）`],
      advice: 'texts 需要是字符串数组，例如 {"texts":["文案一","文案二"]}；单条文案请用 {"text":"…"}。',
    };
  }
  if (Array.isArray(payload.texts) && payload.texts.some((t) => typeof t !== 'string')) {
    return {
      status: 'insufficient_input',
      missing: ['texts 里含非字符串元素（应为字符串数组）'],
      advice: '把每条文案作为字符串放进 texts，例如 {"texts":["文案一","文案二"]}。',
    };
  }
  if (payload.text !== undefined && payload.text !== null && typeof payload.text !== 'string') {
    return {
      status: 'insufficient_input',
      missing: [`text 不是字符串（收到的是 ${Array.isArray(payload.text) ? 'array' : typeof payload.text}）`],
      advice: '把待检文案作为字符串传给 text；多条文案请用 texts 字符串数组。',
    };
  }

  if (Array.isArray(payload.texts) && payload.texts.length) {
    docs = payload.texts.map((t, i) => ({ label: `文案${i + 1}`, text: normalize(t) }));
  } else if (Array.isArray(payload.texts) && !payload.texts.length && payload.text === undefined) {
    return {
      status: 'insufficient_input',
      missing: ['texts 是空数组，而且没有给 text —— 没有待检文案'],
      advice: '传 text（单条文案）或 texts（多条文案数组），每条至少 2 个字符。',
    };
  } else {
    docs = [{ label: '文案', text: normalize(payload.text) }];
  }

  const usable = docs.filter((d) => d.text.trim().length >= 2);
  if (!usable.length) {
    const tooShort = docs
      .map((d, i) => ({ d, i }))
      .filter(({ d }) => d.text.trim().length === 1)
      .map(({ d, i }) => `${docs.length > 1 ? `文案${i + 1}` : 'text'} 只有 1 个字符（「${d.text.trim()}」）`);
    const missing = [];
    if (tooShort.length) missing.push(...tooShort, '一个字符不构成一条可判定的广告文案');
    else missing.push('没有收到待检文案：text / texts 为空或只有空白');
    return {
      status: 'insufficient_input',
      missing,
      advice: '把标题、正文、口播稿、标签拼接后传给 text（或传给 texts 数组），每条至少 2 个字符；'
        + '文案为空时不套用默认值，也不会给出"合规"的结论。',
    };
  }

  const findings = [];
  const exempted = [];
  const skipped = docs.length - usable.length;

  for (const doc of usable) {
    const text = doc.text;
    const where = docs.length > 1 ? `${doc.label}：` : '';
    const findingsBeforeThisDoc = findings.length;   // 位置区间必须按本条文案算

    /* --- 1) 绝对化用语（先过豁免判定）--- */
    for (const term of ABSOLUTE_TERMS) {
      let from = 0;
      for (;;) {
        const idx = text.indexOf(term, from);
        if (idx < 0) break;
        from = idx + term.length;
        const ex = evaluateExemption(text, idx, term);
        if (ex) {
          exempted.push({
            term,
            index: idx,
            context: where + excerpt(text, idx, term),
            exemption: ex.code,
            exemption_label: ex.label,
            basis: ex.basis,
            note: ex.detail,
          });
          continue;
        }
        pushFinding(findings, {
          type: 'ABSOLUTE_TERM',
          category: '绝对化用语',
          level: 'P0',
          term,
          index: idx,
          context: where + excerpt(text, idx, term),
          basis: BASIS_ABSOLUTE,
          advice: '删除或改为可举证的具体描述（例如具体参数、检测结论、可核验的排名来源）。'
            + '若确有依据，请保留证明材料 —— 依《执法指南》第七条，无法证明真实性的仍会被查处。',
          // 销量／排名类用语有一条明确的合法化路径，直接告诉用户，免得他以为只能删掉
          exemption_hint: /(销量|销售额|市场占有率|份额|排名|出货量)/.test(term)
            ? `若能同时限定具体时间与范围且确有事实依据（例如「2024年上半年华东区销量第一」并附第三方数据来源），`
              + `可依${BASIS_GUIDE}第六条第（六）项主张不适用绝对化用语规定；但依第七条，无法证明真实性的仍会依《广告法》查处。`
            : undefined,
        });
      }
    }

    /* --- 2) 单独登记"故意没报"的词：时间／顺序类与日常固定搭配 ---
     * 与上面命中豁免的情形合并去重；若该词所在位置已经被报成问题（例如「最高品质」里的「最高」），
     * 就不再重复登记，免得出现"同一个位置既报问题又说豁免"的自相矛盾。
     * 注意：位置区间必须**按本条文案**算 —— 不同文案的 index 各自从 0 开始，混着比会张冠李戴。 */
    const reported = findings
      .slice(findingsBeforeThisDoc)
      .map((f) => [f.index, f.index + String(f.term).length]);
    const overlapsFinding = (idx, term) => reported.some(([s, e]) => idx < e && idx + term.length > s);

    for (const term of TEMPORAL_SAFE) {
      const idx = text.indexOf(term);
      if (idx < 0 || overlapsFinding(idx, term)) continue;
      exempted.push({
        term,
        index: idx,
        context: where + excerpt(text, idx, term),
        exemption: EXEMPTION.TEMPORAL_WORD.code,
        exemption_label: EXEMPTION.TEMPORAL_WORD.label,
        basis: EXEMPTION.TEMPORAL_WORD.basis,
        note: EXEMPTION.TEMPORAL_WORD.detail,
      });
    }
    for (const term of COMMON_SAFE) {
      const idx = text.indexOf(term);
      if (idx < 0 || overlapsFinding(idx, term)) continue;
      exempted.push({
        term,
        index: idx,
        context: where + excerpt(text, idx, term),
        exemption: EXEMPTION.COMMON_WORD.code,
        exemption_label: EXEMPTION.COMMON_WORD.label,
        basis: EXEMPTION.COMMON_WORD.basis,
        note: EXEMPTION.COMMON_WORD.detail,
      });
    }
  }

  const order = { P0: 0, P1: 1, P2: 2 };
  findings.sort((a, b) => (order[a.level] || 9) - (order[b.level] || 9));

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'AD_COMPLIANCE_CHECK_FREE',
    scope: {
      checks: CHECKS_GIVEN,
      documents: usable.length,
      documents_skipped_too_short: skipped,
      chars: usable.reduce((n, d) => n + d.text.length, 0),
      rules_version: RULES_VERSION,
      guide: BASIS_GUIDE,
      executed_locally: true,
      network_used: false,
    },
    summary: {
      total: findings.length,
      p0,
      p1,
      p2,
      returned: findings.length,
      omitted: 0,
      exempted: exempted.length,
      verdict: p0 ? 'HAS_ABSOLUTE_TERMS' : (p1 ? 'NEEDS_REVIEW' : 'NO_ABSOLUTE_TERM'),
    },
    findings,
    exempted,
    note: 'exempted 里的词是**按《执法指南》判定为可豁免、因此故意没有报成问题**的表述，'
      + '并附豁免依据供复核。本结果只覆盖绝对化用语一项；其余检查项见 checks_withheld，本次未执行。',
    disclaimer: '本报告只做AI比对与法条对照，不构成法律意见，也不替代市场监督管理部门的认定。'
      + '最终是否违法由监管部门结合广告整体语境、事实依据与社会危害程度依法判断。',
    checked_at: new Date().toISOString(),
  };

  return { status: 'success', result };
}

module.exports = {
  run,
  evaluateExemption,
  ABSOLUTE_TERMS,
  TEMPORAL_SAFE,
  COMMON_SAFE,
  EXEMPTION,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
