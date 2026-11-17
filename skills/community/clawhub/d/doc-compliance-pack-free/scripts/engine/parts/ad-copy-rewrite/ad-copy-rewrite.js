'use strict';
/**
 * ad-copy-rewrite.js —— 广告文案违规体检（免费档）本地引擎
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 * 技能包是从注册表单独下载安装的，跨包引用一定会断，所以刻意不与仓库其他技能共享代码。
 *
 * 这个能力**不吃表格**：输入就是一段广告文案（标题、正文、口播稿、商品标签都可以拼进来）。
 * 因此引擎里没有 parseTable / roleOf / normNumber —— 它们是为"表头 + 多行数据"那类产品准备的，
 * 本能力用不上。全仓守卫（`tools/header_map_check.py`）读不到 `roleOf` 会**显式跳过**这类引擎，
 * 不会误判；所以这里不补空实现。真正被跨包守卫读到的导出只有：
 *   `CHECKS_GIVEN`（免费档执行）/ `CHECKS_WITHHELD`（免费档如实声明"未执行"）/
 *   `OUT_OF_SCOPE`（本能力根本不做的事）/ `SAMPLE_TEXT`（样例）。
 *   —— `tools/add_paid_funnel.py`、`tools/funnel_withheld_check.py` 读 WITHHELD，
 *      `tools/fix_sample_json.py`、`tools/build_mcp_server.py` 读 SAMPLE_TEXT。
 *      为兼容 `build_mcp_server.py` 里的 `CHECKS_OUT_OF_SCOPE` 字段名，额外导出一个**同值别名**
 *      （不是空实现，是同一份数据）。
 *
 * 免费档执行 6 项**机械可判定**的表述检查（每一项都给出原文行号与一句依据）：
 *   ① 绝对化用语（含《广告绝对化用语执法指南》的豁免情形判定）
 *   ② 医疗／药品／医美类违禁表述（疗效、根治、无副作用等）
 *   ③ 教育培训保证性承诺（保过、包就业、提分 X 分等）
 *   ④ 投资理财／房地产承诺（保本、稳赚、升值回报）
 *   ⑤ 虚假广告类保证性承诺（100% 有效、3 天见效）
 *   ⑥ 缺失必要提示（保健食品未标「本品不能代替药物」等）
 *
 * 刻意不实现（属完整档／服务端订阅能力，见 CHECKS_WITHHELD）：
 *   给出改写后的整段可发布文案、违禁词替换建议库、批量文案体检。
 *
 * 精准度优先：**宁可漏报，不可误报**。
 *   · 绝对化用语命中后先过豁免判定（《执法指南》第二条、第五条、第六条），可豁免的**不报**，
 *     但会登记进 `exempted` 并写明豁免依据 —— 用户能看见"我们故意没报什么、为什么"；
 *   · 「100% 羊毛」这类**客观成分含量标示**不算"最高级"声称，明确不报（误报会让人不再信任工具）；
 *   · 「最后」「最近」「最新」等时间／顺序类常用词不报（字典式极限词工具在这里翻车最多）。
 *
 * 材料不足时**绝不输出"没问题"**：run() 返回 status='insufficient_input'（**没有 result 字段**），
 * 由 run.mjs 打印缺什么并以退出码 3 结束。
 *
 * 确定性：同一输入两次调用，findings / exempted / summary 完全一致（只有 checked_at 是时间戳）。
 */

/* ---------------------------------------------------------------- 常量 */

const RULES_VERSION = '2026-09-17';

const CHECKS_GIVEN = [
  '①绝对化用语（含《广告绝对化用语执法指南》豁免情形判定）',
  '②医疗／药品／医美类违禁表述（疗效、根治、无副作用等）',
  '③教育培训保证性承诺（保过、包就业、提分 X 分等）',
  '④投资理财／房地产承诺（保本、稳赚、升值回报等）',
  '⑤虚假广告类保证性承诺（100% 有效、3 天见效等）',
  '⑥缺失必要提示（保健食品未标「本品不能代替药物」等）',
];

/* 完整档（服务端订阅）能力 —— 免费档**如实声明未执行**，绝不用默认值假装给出。
 * ⚠️ 这里的字符串**不能含半角逗号**：`tools/add_paid_funnel.py` 用 `,` 切分这个数组。 */
const CHECKS_WITHHELD = [
  '给出改写后的整段可发布文案（免费档只标问题、不改写）',
  '违禁词替换建议库（持续更新）',
  '批量文案体检（一次几十条并给出合并整改清单）',
  '按发布平台（抖音／小红书／天猫等）差异化的口径',
  '违规风险分级与整改优先级建议',
];

const OUT_OF_SCOPE = [
  '不判断广告整体是否违法：只做机械可判定的表述检查，是否违法由市场监管部门结合语境、事实依据与社会危害程度认定',
  '不替代法务、监管口径与平台审核规则；本工具不是法律意见，也不能用来对抗处罚',
  '不核查文案里的事实是否真实（例如「销量第一」是否真有第三方数据支撑），只提示举证责任在广告主一方',
  '不判断画面、视频、音频、代言人资质、商标授权、价格标示、赠品规则等其他合规维度',
  '不做跨句语境推断（反讽、引用法规原文、竞品评测的正当引用等），因此每个命中项都需要人工复核',
  '不覆盖特殊行业的专门审批口径（药品／医疗器械／农药／兽药／酒类／烟草／持牌金融产品等）',
  '不覆盖境外投放地法律（美国 FTC、欧盟 UCPD 等），只对齐中国大陆《广告法》体系',
  '不做语义级改写与创意评估（那是完整档与服务端订阅能力）',
];

const GUIDE = '《广告绝对化用语执法指南》（市场监管总局 2023-02-25 公告）';
const BASIS_ABSOLUTE = '《广告法》第九条第三项（广告不得使用“国家级”“最高级”“最佳”等用语）';
const BASIS_MEDICAL = '《广告法》第十六条（医疗、药品、医疗器械广告不得含有表示功效、安全性的断言或者保证，不得说明治愈率或者有效率）、第十七条（除医疗、药品、医疗器械广告外，禁止其他任何广告涉及疾病治疗功能）';
const BASIS_EDU = '《广告法》第二十四条第一项（教育、培训广告不得对升学、通过考试、获得学位学历或者合格证书，或者对教育、培训的效果作出明示或者暗示的保证性承诺）';
const BASIS_INVEST = '《广告法》第二十五条第一项（投资理财类广告不得对未来效果、收益或者与其相关的情况作出保证性承诺，不得明示或者暗示保本、无风险或者保收益）、第二十六条第一项（房地产广告不得含有升值或者投资回报的承诺）';
const BASIS_FALSE = '《广告法》第四条（广告不得含有虚假或者引人误解的内容）、第二十八条第二款（对商品的性能、功能、质量、销售状况等作虚假或者引人误解的宣传）';
const BASIS_NOTICE_FOOD = '《广告法》第十八条第二款（保健食品广告应当显著标明“本品不能代替药物”）';
const BASIS_NOTICE_DRUG = '《广告法》第十六条第一款（药品广告应当显著标明“请按药品说明书或者在药师指导下购买和使用”并显著标明禁忌、不良反应）';

/* ------------------------------------------------------ 绝对化用语的豁免 */

/**
 * 豁免情形（依据《广告绝对化用语执法指南》第二条、第五条、第六条）。
 * 单列出来是为了把"我们故意没报的东西"和理由**给用户看** —— 这既是精准度，也是可审计性。
 */
const EXEMPT = {
  ATTITUDE: {
    code: 'ATTITUDE',
    label: '服务态度／经营理念／主观愿望',
    basis: `${GUIDE}第五条`,
    detail: '仅表明服务态度、经营理念、企业文化或主观愿望、目标追求，未指向所推销商品的性能质量',
  },
  USAGE: {
    code: 'USAGE',
    label: '使用方法／保存期限等消费提示',
    basis: `${GUIDE}第六条第（二）项`,
    detail: '仅用于宣传商品的使用方法、使用时间、保存期限等消费提示',
  },
  SELF_COMPARE: {
    code: 'SELF_COMPARE',
    label: '同一品牌自我比较',
    basis: `${GUIDE}第六条第（一）项`,
    detail: '仅用于对同一品牌或同一企业的商品进行自我比较（需出现「相比／上一代／迭代前」这类比较标记）',
  },
  STANDARD: {
    code: 'STANDARD',
    label: '依据标准的商品分级用语',
    basis: `${GUIDE}第六条第（三）项`,
    detail: '依据国家标准、行业标准、地方标准等认定的商品分级用语，且能够说明依据',
  },
  NAME_MODEL: {
    code: 'NAME_MODEL',
    label: '商品名称／型号／商标／专利',
    basis: `${GUIDE}第六条第（四）项`,
    detail: '商品名称、规格型号、注册商标或专利中含有绝对化用语，用于指代商品以区别于其他商品',
  },
  AWARD: {
    code: 'AWARD',
    label: '依规评定的奖项、称号',
    basis: `${GUIDE}第六条第（五）项`,
    detail: '依据国家有关规定评定的奖项、称号中含有绝对化用语',
  },
  TIME_FACT: {
    code: 'TIME_FACT',
    label: '限定具体时间、地域的时空顺序或事实信息',
    basis: `${GUIDE}第六条第（六）项`,
    detail: '在限定具体时间、地域等条件的情况下表述时空顺序客观情况，或宣传销量、销售额、市场占有率等事实信息；**时间限定与事实信息两者缺一不可**',
  },
  TEMPORAL: {
    code: 'TEMPORAL',
    label: '时间／顺序类常用词',
    basis: `${GUIDE}第二条（绝对化用语指含义为“最高级”的用语）`,
    detail: '「最后」「最近」「最新」等是表示时间或顺序的常用词，并未声称商品最优，不属于绝对化用语',
  },
  FIXED_PHRASE: {
    code: 'FIXED_PHRASE',
    label: '日常固定搭配',
    basis: `${GUIDE}第二条`,
    detail: '「一站式」「一体化」「第一时间」等固定搭配中的「一」不构成“第一”的排他性声称',
  },
  COMPOSITION: {
    code: 'COMPOSITION',
    label: '客观成分／含量标示',
    basis: `${GUIDE}第二条`,
    detail: '「100% 羊毛」「100% 纯棉」是客观成分含量标示，不是“最高级”声称，不属绝对化用语',
  },
};

/** 时间／顺序类常用词：**不报**，但登记进 exempted 让用户看得见（字典式工具误报的重灾区）。 */
const SAFE_TEMPORAL = ['最后', '最近', '最终', '最初', '最新', '最快', '最多', '最少', '最晚', '最早'];
/** 日常固定搭配：**不报**，同样登记。 */
const SAFE_FIXED = ['一站式', '一体化', '一条龙', '一系列', '第一时间', '一揽子', '一次性', '一键'];

/** 客观成分／含量词：跟在「100%／百分百」后面时按含量标示处理，不报。 */
const COMPOSITION_WORDS = /^\s*(?:纯)?(?:羊毛|棉|真丝|桑蚕丝|山羊绒|羊绒|羽绒|亚麻|麻|果汁|原浆|大豆|牛奶|生牛乳|可可|乳胶|实木|含量|澳洲|进口)/;

/* ------------------------------------------------------- 检查规则（6 项） */

/**
 * 每条规则 = { check, category, level, basis, advice, terms?, res?, notice? }。
 *   · `terms` 是字面量（命中位置就是它本身）；
 *   · `res` 是正则（用于「提分 X 分」「N 天见效」这类带变量的写法）；
 *   · `notice` 表示"检查是否**缺失**某句必要提示"，不是文字命中；
 *   · 同一处表述在**跨规则**层面只报一次：严重级别高的优先（P0 > P1 > P2），
 *     同级再按"具体规则优先于泛化规则"（例如「100% 有效」按虚假承诺报，而不是按绝对化用语报）。
 */
const RULES = [
  /* --- ② 医疗／药品／医美（法律明文禁止的表述，最具体，优先级最高） --- */
  {
    check: 'MEDICAL_CLAIM',
    category: '医疗·药品·医美违禁表述',
    level: 'P0',
    basis: BASIS_MEDICAL,
    advice: '删除功效断言与治愈承诺，改为可核验的客观描述；医疗、药品、医疗器械广告须先经审查，非医疗类商品一律不得涉及疾病治疗功能。',
    terms: ['根治', '治愈', '治愈率', '有效率', '疗效', '药到病除', '包治', '包治百病', '无副作用',
      '没有任何副作用', '无任何副作用', '特效药', '祖传秘方', '抗癌', '降血糖', '降血压', '降血脂',
      '降尿酸', '治疗', '痊愈', '根除', '断根'],
  },
  {
    check: 'MEDICAL_HINT',
    category: '医疗·保健功效断言（需按产品资质复核）',
    level: 'P1',
    basis: BASIS_MEDICAL,
    advice: '这类功效宣称只有取得相应资质（保健食品注册／备案、特殊化妆品注册、医疗器械注册）并在批准范围内才能说；无资质时删掉，有资质时补上批准文号。',
    terms: ['增强免疫力', '提高免疫力', '排毒', '抗炎', '修复细胞', '减肥', '丰胸', '壮阳',
      '改善睡眠', '缓解疲劳', '助眠', '祛斑', '美白', '生发', '护肝', '养胃', '抗氧化', '补充胶原蛋白'],
  },

  /* --- ⑤ 虚假广告类保证性承诺（带变量的"见效"写法，比 ① 更具体） --- */
  {
    check: 'FALSE_PROMISE',
    category: '虚假广告类保证性承诺',
    level: 'P0',
    basis: BASIS_FALSE,
    advice: '效果承诺需要证据支撑且不得绝对化；改成可举证的实测结论（标明样本量、检测机构与报告编号），或直接删掉时间承诺。',
    terms: ['100%有效', '百分百有效', '绝对有效', '当天见效', '立刻见效', '马上见效', '即刻见效',
      '一次见效', '一针见效', '立竿见影', '永久有效', '永久见效'],
    res: [/(?:\d+|[一二三四五六七八九十]+)\s*天\s*见效/],
  },
  {
    check: 'FALSE_HINT',
    category: '效果担保类承诺（需复核）',
    level: 'P1',
    basis: BASIS_FALSE,
    advice: '「无效退款」这类写法把效果与退款绑定，等于对效果作出保证；平台审核常按保证性承诺处理，建议改为服务承诺（如「7 天无理由退换」）。',
    terms: ['无效退款', '保证有效', '保证见效', '效果保证'],
  },

  /* --- ③ 教育培训保证性承诺 --- */
  {
    check: 'EDU_GUARANTEE',
    category: '教育培训保证性承诺',
    level: 'P0',
    basis: BASIS_EDU,
    advice: '删掉"保过／包就业／保录取"和对提分分数的承诺；可改为如实描述师资、课时、往期学员的真实数据（附统计口径）。',
    terms: ['保过', '包过', '保过关', '包过关', '保就业', '包就业', '包分配', '保录取', '保上岸',
      '包拿证', '保拿证', '一次通过', '确保通过', '保证录取', '保进', '包进', '保底一本', '保底本科'],
    res: [/(?:保证|承诺|确保)[^，。！？；\s]{0,8}(?:通过|上岸|录取|就业|拿证|考(?:上|过))/,
      /(?:提|涨)\s*\d+\s*分/, /保底\s*\d+\s*分/],
  },
  {
    check: 'EDU_HINT',
    category: '教育培训效果暗示（需复核）',
    level: 'P1',
    basis: BASIS_EDU,
    advice: '「提分」「保分」这类写法容易被认定为对培训效果的暗示保证；建议改为「按课程大纲完成 XX 课时」这类过程描述。',
    terms: ['提分', '涨分', '保分', '冲分', '提成绩', '不过退款'],
  },

  /* --- ④ 投资理财／房地产承诺 --- */
  {
    check: 'INVEST_PROMISE',
    category: '投资理财·房地产承诺',
    level: 'P0',
    basis: BASIS_INVEST,
    advice: '删掉保本、保收益、无风险、升值／投资回报的承诺；持牌产品也必须在显著位置同时提示风险，且不得对未来收益作保证。',
    terms: ['保本保息', '保本', '保息', '稳赚不赔', '稳赚不亏', '稳赚', '包赚', '零风险', '无风险', '保收益',
      '保底收益', '高回报', '高收益', '只赚不赔', '旱涝保收', '刚性兑付', '本金保障', '升值',
      '投资回报', '回报率', '躺赚', '翻倍', '一夜暴富'],
    res: [/增值(?!税)/, /年化(?:收益|利率|回报)[^，。；\s]{0,6}\d/],
  },
  {
    check: 'INVEST_HINT',
    category: '投资收益暗示（需复核）',
    level: 'P1',
    basis: BASIS_INVEST,
    advice: '「只涨不跌」「必涨」属于对未来效果的暗示性保证；改为客观陈述历史数据并显著提示「市场有风险」。',
    terms: ['只涨不跌', '稳涨', '必涨', '稳中有升', '买到就是赚到'],
  },

  /* --- ① 绝对化用语（泛化规则放最后：同一处表述优先按前面的具体规则报） --- */
  {
    check: 'ABSOLUTE_TERM',
    category: '绝对化用语',
    level: 'P0',
    basis: `${BASIS_ABSOLUTE}；${GUIDE}`,
    advice: '删掉或改成可举证的具体描述（具体参数、检测结论、可核验的排名来源）；确有依据的，请保留证明材料 —— 依《执法指南》第七条，无法证明真实性的仍会被查处。',
    terms: [
      // 最-family
      '最好', '最佳', '最优', '最强', '最先进', '最便宜', '最低价', '最优质', '最专业', '最权威',
      '最领先', '最火爆', '最热销', '最受欢迎', '最值得', '最有效', '最安全', '最齐全', '最全面',
      '最顶级', '最高级', '最高端', '最豪华', '最划算', '最省钱', '最全', '最高品质', '最好用',
      '最新科技', '最牛', '最棒',
      // 一-family（排他性声称）
      '第一品牌', '排名第一', '销量第一', '全国第一', '全球第一', '世界第一', '行业第一', '第一名',
      '唯一', '独家', '独一无二', '首屈一指', '仅此一家', '绝无仅有', '独家首发', '全网独家',
      '唯一选择', '一劳永逸',
      // 级／极 family
      '国家级', '世界级', '国际级', '顶级', '极品', '极佳', '极致', '终极', '顶级品质',
      // 绝对／无上限 family
      '绝对', '100%', '百分百', '全网最低', '史上最', '前所未有', '空前绝后', '无人能及',
    ],
  },

  /* --- ⑥ 缺失必要提示（检查的是"漏了"而不是"写了"，单独判定） --- */
  {
    check: 'MISSING_NOTICE',
    category: '缺失必要提示',
    level: 'P2',
    basis: BASIS_NOTICE_FOOD,
    advice: '保健食品广告必须显著标明「本品不能代替药物」；补上这行提示再发布。',
    notice: {
      signals: ['保健食品', '保健品', '蓝帽子', '国食健字', '保健功能'],
      required: [['本品不能代替药物'], ['不能代替药物'], ['不能替代药物']],
    },
  },
  {
    check: 'MISSING_NOTICE',
    category: '缺失必要提示',
    level: 'P2',
    basis: BASIS_NOTICE_DRUG,
    advice: '药品广告必须显著标明「请按药品说明书或者在药师指导下购买和使用」，并显著标明禁忌、不良反应；补上再发布。',
    notice: {
      signals: ['处方药', '非处方药', 'OTC', '国药准字', '中成药', '药品广告'],
      required: [['按药品说明书'], ['药师指导'], ['禁忌'], ['不良反应']],
    },
  },
];

/** 同级冲突时的"具体优先"次序（数字越小越先报）。 */
const RULE_RANK = {
  MEDICAL_CLAIM: 1, FALSE_PROMISE: 2, EDU_GUARANTEE: 3, INVEST_PROMISE: 4, ABSOLUTE_TERM: 5,
  MEDICAL_HINT: 6, FALSE_HINT: 7, EDU_HINT: 8, INVEST_HINT: 9, MISSING_NOTICE: 10,
};
const LEVEL_RANK = { P0: 0, P1: 1, P2: 2 };

/* ---------------------------------------------------------------- 工具 */

function normalize(v) {
  return String(v == null ? '' : v);
}

/** 命中词前后各截 14 字，便于人工复核（去掉换行，避免输出被撑开）。 */
function excerpt(line, index, term) {
  const start = Math.max(0, index - 14);
  const end = Math.min(line.length, index + term.length + 14);
  return (start > 0 ? '…' : '') + line.slice(start, end).replace(/\s+/g, ' ') + (end < line.length ? '…' : '');
}

function spansOverlap(a, b) {
  const aEnd = a.index + String(a.term).length;
  const bEnd = b.index + String(b.term).length;
  return a.index < bEnd && b.index < aEnd;
}

function matchTerm(line, term) {
  const out = [];
  let from = 0;
  for (;;) {
    const i = line.indexOf(term, from);
    if (i < 0) break;
    out.push({ index: i, term });
    from = i + Math.max(1, term.length);
  }
  return out;
}

function matchRe(line, re) {
  const out = [];
  const r = new RegExp(re.source, re.flags.includes('g') ? re.flags : `${re.flags}g`);
  let m;
  while ((m = r.exec(line)) !== null) {
    if (m[0]) out.push({ index: m.index, term: m[0] });
    if (m.index === r.lastIndex) r.lastIndex += 1;   // 零宽匹配兜底，防死循环
  }
  return out;
}

/* ------------------------------------------------------------ 豁免判定 */

const RE_ATTITUDE = /(努力|宗旨|理念|追求|致力于|竭诚|全力|尽可能|尽量|欢迎|期待|决心|愿望|使命|态度|初心)/;
const RE_USAGE = /(食用|饮用|服用|冲泡|保存|储存|存放|冷藏|冷冻|保质|保鲜|赏味|期限|使用(?:方法|时间|温度|期限|说明)|服用方法|建议用量|开袋|开封|加热|洗涤|手洗|阴干|晾干|保养)/;
const RE_SELF = /(相比|相较|对比|较上|比上|上一代|前代|旧款|历代|前作|老款|上一版|上一款|迭代前|升级前)/;
const RE_STANDARD = /(国家标准|行业标准|地方标准|团体标准|企业标准|GB\s*\/?\s*T?\s*\d*|特级|一级品|优级|执行标准|标准认定|分级)/;
const RE_NAME = /(商标|注册商标|专利|注册号|型号|规格型号|品牌名|品名|系列名)/;
const RE_AWARD = /(荣获|获评|评定|评选|称号|奖项|金奖|银奖|授予|认证)/;
const RE_TIME_LIMIT = /(20\d{2}\s*年|第[一二三四]季度|\d{1,2}\s*月|上半年|下半年|年度|本季度|上季度|去年同期)/;
const RE_FACT = /(销量|销售额|营收|市场占有率|份额|排名|出货量|复购率|好评率|回购率)/;

/**
 * 判断一个绝对化用语命中是否可依《执法指南》豁免。
 * @returns {Object|null} 命中豁免则返回豁免定义，否则 null
 */
function evaluateExemption(line, index, term) {
  // 客观成分／含量标示：「100% 羊毛」「百分百纯棉」
  if (term === '100%' || term === '百分百') {
    if (COMPOSITION_WORDS.test(line.slice(index + term.length))) return EXEMPT.COMPOSITION;
  }
  // 第五条：只表明服务态度、经营理念、主观愿望或目标追求（如「尽最大努力」）
  if (RE_ATTITUDE.test(line)) return EXEMPT.ATTITUDE;
  if (RE_USAGE.test(line)) return EXEMPT.USAGE;
  if (RE_SELF.test(line)) return EXEMPT.SELF_COMPARE;
  if (RE_STANDARD.test(line)) return EXEMPT.STANDARD;
  if (RE_NAME.test(line)) return EXEMPT.NAME_MODEL;
  if (RE_AWARD.test(line)) return EXEMPT.AWARD;
  // 第六条第（六）项：限定具体时间 + 事实信息，两者缺一不可
  if (RE_TIME_LIMIT.test(line) && RE_FACT.test(line)) return EXEMPT.TIME_FACT;
  return null;
}

/* ---------------------------------------------------------------- 判定 */

function verdictOf(counts) {
  if (counts.p0 || counts.p1) return 'ERROR_FOUND';
  if (counts.p2) return 'NEEDS_REVIEW';
  return 'NO_ISSUE_FOUND';
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * 广告文案违规体检（免费档）。
 *
 * @param {Object} input
 * @param {string} input.text 待检文案，一行一句最清晰（标题／正文／口播稿／标签都可拼接后传入）
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(input) {
  // 契约是 {text}；顺手兼容"直接传一段字符串"，但**任何非字符串都按材料不足处理**
  const payload = (input && typeof input === 'object' && !Array.isArray(input))
    ? input
    : (typeof input === 'string' ? { text: input } : {});

  if (payload.text !== undefined && payload.text !== null && typeof payload.text !== 'string') {
    return insufficient(
      [`text 不是字符串（收到的是 ${Array.isArray(payload.text) ? 'array' : typeof payload.text}）`],
      '把待检文案作为字符串传给 text，例如 {"text":"本店全场包邮，7 天无理由退换。"}。',
    );
  }

  const text = normalize(payload.text);
  if (!text.trim()) {
    return insufficient(
      ['没有收到待检文案：text 缺失或只有空白'],
      '把标题、正文、口播稿、商品标签拼接后传给 text（一行一句最清晰），例如 {"text":"…"}。',
    );
  }
  if (text.trim().length < 2) {
    return insufficient(
      [`text 只有 1 个字符（「${text.trim()}」）`, '一个字符不构成一条可判定的广告文案'],
      '把完整的一句广告文案传给 text，至少 2 个字符。',
    );
  }

  const rawLines = text.split(/\r?\n/);
  // 行号必须对应**原文**的行：空行也占号，否则报出来的行号会与用户看到的原文错位
  const lines = rawLines.map((l, i) => ({ no: i + 1, raw: l }));

  const candidates = [];
  const exempted = [];
  const pushExempted = (line, index, term, ex) => {
    if (exempted.some((x) => x.line === line && x.index === index && x.term === term)) return;
    exempted.push({
      line,
      index,
      term,
      exemption: ex.code,
      exemption_label: ex.label,
      basis: ex.basis,
      note: ex.detail,
      context: excerpt(rawLines[line - 1] || '', index, term),
    });
  };

  for (const doc of lines) {
    const line = doc.raw;
    if (!line.trim()) continue;

    for (const rule of RULES) {
      if (rule.notice) continue;                     // ⑥ 是"是否缺失"，单独判定
      const hits = [];
      for (const t of rule.terms || []) hits.push(...matchTerm(line, t));
      for (const re of rule.res || []) hits.push(...matchRe(line, re));
      if (!hits.length) continue;

      // 规则内去重：同一处只留一个（长的优先 —— 「保本保息」留「保本」这一条依据即可）
      hits.sort((a, b) => (a.index - b.index) || (b.term.length - a.term.length));
      const kept = [];
      for (const h of hits) {
        if (kept.some((k) => spansOverlap(k, h))) continue;
        kept.push(h);
      }

      for (const h of kept) {
        if (rule.check === 'ABSOLUTE_TERM') {
          const ex = evaluateExemption(line, h.index, h.term);
          if (ex) { pushExempted(doc.no, h.index, h.term, ex); continue; }
        }
        candidates.push({ ...h, rule, line: doc.no });
      }
    }

    // 故意没报的词也登记出来，让用户看得见（并且不与已报问题重复）
    for (const [list, ex] of [[SAFE_TEMPORAL, EXEMPT.TEMPORAL], [SAFE_FIXED, EXEMPT.FIXED_PHRASE]]) {
      for (const t of list) {
        const i = line.indexOf(t);
        if (i < 0) continue;
        const overlapsReported = candidates.some((c) => c.line === doc.no && spansOverlap(c, { index: i, term: t }));
        if (overlapsReported) continue;
        pushExempted(doc.no, i, t, ex);
      }
    }

    // ⑥ 缺失必要提示：命中"商品类别信号"但没有必需的提示语 ⇒ P2
    for (const rule of RULES) {
      if (!rule.notice) continue;
      const signal = rule.notice.signals.find((s) => line.includes(s));
      if (!signal) continue;
      const hasNotice = rule.notice.required.some((alts) => alts.some((x) => text.includes(x)));
      if (hasNotice) continue;
      candidates.push({ index: line.indexOf(signal), term: signal, rule, line: doc.no, isNotice: true });
    }
  }

  // 跨规则去重：同一处表述只报一次 —— 级别高的优先，同级按"具体规则优先"
  candidates.sort((a, b) => (a.line - b.line)
    || (LEVEL_RANK[a.rule.level] - LEVEL_RANK[b.rule.level])
    || (RULE_RANK[a.rule.check] - RULE_RANK[b.rule.check])
    || (a.index - b.index));

  const accepted = [];
  for (const c of candidates) {
    if (accepted.some((a) => a.line === c.line && spansOverlap(a, c))) continue;
    accepted.push(c);
  }
  accepted.sort((a, b) => (a.line - b.line)
    || (LEVEL_RANK[a.rule.level] - LEVEL_RANK[b.rule.level])
    || (RULE_RANK[a.rule.check] - RULE_RANK[b.rule.check])
    || (a.index - b.index));

  const findings = accepted.map((c) => {
    const line = rawLines[c.line - 1] || '';
    const message = `${c.rule.category}：第 ${c.line} 行命中「${c.term}」｜依据：${c.rule.basis}`;
    return {
      check: c.rule.check,
      category: c.rule.category,
      level: c.rule.level,
      line: c.line,
      col: c.index + 1,
      term: c.term,
      evidence: line.trim().slice(0, 200),
      context: excerpt(line, c.index, c.term),
      basis: c.rule.basis,
      advice: c.rule.advice,
      is_missing_notice: c.isNotice === true,
      message,                       // 页面渲染 f.detail || f.message，两个都给，避免正文空白
      detail: message,
    };
  });

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'AD_COPY_COMPLIANCE_CHECK_FREE',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: CHECKS_WITHHELD,
      checks_out_of_scope: OUT_OF_SCOPE,
      lines: lines.length,
      chars: text.length,
      rules_version: RULES_VERSION,
      guide: GUIDE,
      executed_locally: true,
      network_used: false,
    },
    summary: {
      total: findings.length,
      p0,
      p1,
      p2,
      lines_scanned: lines.filter((l) => l.raw.trim()).length,
      exempted: exempted.length,
      verdict: verdictOf({ p0, p1, p2 }),
    },
    findings,
    exempted,
    note: '本次只执行上面 6 项免费检查，全部在本机完成（不联网、不外发文案）；'
      + '「改写后的整段可发布文案」「违禁词替换建议库」「批量文案体检」属完整档（服务端订阅）能力，'
      + '本次**未执行**，也不会用默认值编造。exempted 里是**按《执法指南》判定可豁免、因此故意没报成问题**的表述。',
    disclaimer: '本报告只做机械可判定的表述比对与法条对照，不构成法律意见，也不判断广告整体是否违法；'
      + '最终是否违法由市场监督管理部门结合广告整体语境、事实依据与社会危害程度依法认定。',
    checked_at: new Date().toISOString(),
  };

  return { status: 'success', result };
}

/* ---------------------------------------------------- 样例（必须干净） */

/**
 * 样例是**一份合规的广告文案**：跑出来 0 命中。
 * 里面刻意放了两个"字典式极限词工具会误报"的写法 —— 「最新款」「100% 羊毛」——
 * 它们会被判为可豁免并登记进 exempted（时间／顺序类常用词、客观成分标示），**不报成问题**。
 */
const SAMPLE_TEXT = [
  '秋季最新款女士针织开衫，100% 羊毛，柔软亲肤。',
  'S 至 XL 四个尺码，通勤、约会都合适。',
  '洗涤建议：30℃ 以下手洗，平铺阴干，避免暴晒。',
  '下单后 48 小时内发出，支持 7 天无理由退换。',
].join('\n');

module.exports = {
  run,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  OUT_OF_SCOPE,
  CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,   // build_mcp_server.py 读的字段名（同值别名，不是空实现）
  SAMPLE_TEXT,
  // 供第三方复算的口径（对照测试与人工复核都用得上）
  evaluateExemption,
  RULES,
  EXEMPT,
  RULES_VERSION,
};
