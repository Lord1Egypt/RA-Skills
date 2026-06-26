const DIVINATION_SYSTEMS = [
  {
    id: "zhouyi-benjing",
    name: "周易本经占筮",
    family: "易",
    grade: "S",
    status: "已启用",
    basis: "《周易》本经卦辞、爻辞、用九、用六",
    bestFor: ["当下决策", "时机判断", "关系与事业抉择", "自我复盘"],
    inputs: ["一个明确问题", "起卦方式"],
    capability: "可起卦、取辞、引用本经原文并给出现代解释。",
    guardrail: "只作解释性参考，不替代专业判断。"
  },
  {
    id: "yijing-library",
    name: "六十四卦本经库",
    family: "易",
    grade: "S",
    status: "已启用",
    basis: "本地 Gutenberg《易經》整理文本",
    bestFor: ["查卦辞", "查爻辞", "校验卦序", "学习原文"],
    inputs: ["卦名、卦序或关键词"],
    capability: "可检索六十四卦卦辞和六爻原文。",
    guardrail: "当前只含本经，不混入彖象传和后世注解。"
  },
  {
    id: "meihua",
    name: "梅花易数",
    family: "易象",
    grade: "B",
    status: "知识库",
    basis: "以卦象、体用、生克、动爻为主的后世易占体系",
    bestFor: ["快速起象", "当下气机", "小事趋势"],
    inputs: ["数、时间、物象或随机触发"],
    capability: "当前只提供体系说明和路由建议，暂不自动断梅花盘。",
    guardrail: "避免把数字取卦与《周易》本经取辞混为一谈。"
  },
  {
    id: "liuyao",
    name: "六爻纳甲",
    family: "易占",
    grade: "B",
    status: "待校验",
    basis: "纳甲、六亲、世应、月建日辰、动变生克",
    bestFor: ["具体事项成败", "失物", "官司", "短期应期"],
    inputs: ["六爻结果", "起卦时间", "明确用神"],
    capability: "暂不开放自动断卦，只保留未来高精度实现入口。",
    guardrail: "必须先校验纳甲、世应、六亲、月日旺衰，否则不输出结论。"
  },
  {
    id: "xiaoliuren",
    name: "小六壬",
    family: "民间时占",
    grade: "C",
    status: "知识库",
    basis: "大安、留连、速喜、赤口、小吉、空亡六神课",
    bestFor: ["轻量日常问事", "出门前判断", "粗略吉凶"],
    inputs: ["月、日、时或指定数字"],
    capability: "当前只解释体系差异，不作为周易本经断语依据。",
    guardrail: "小六壬不是《周易》原文体系，不能冒充易经本经。"
  },
  {
    id: "qimen",
    name: "奇门遁甲",
    family: "三式",
    grade: "B",
    status: "待校验",
    basis: "节气、阴阳遁、局数、九星八门八神、三奇六仪",
    bestFor: ["择时", "方位", "项目推进窗口", "行动策略"],
    inputs: ["精确时间", "地点/时区", "问事类别"],
    capability: "只纳入百科与路由，不使用未校验日柱和定局算法。",
    guardrail: "四柱、节气、值符值使必须通过基准盘测试后才能开放排盘。"
  },
  {
    id: "bazi",
    name: "八字四柱",
    family: "命理",
    grade: "B",
    status: "待校验",
    basis: "年、月、日、时四柱与十神、旺衰、大运",
    bestFor: ["长期人格底色", "阶段节奏", "职业倾向"],
    inputs: ["出生年月日时", "出生地", "性别/历法说明"],
    capability: "当前只记录资料要求和解释边界。",
    guardrail: "必须使用可靠历法库和流派说明，不能用简化干支表替代。"
  },
  {
    id: "ziwei",
    name: "紫微斗数",
    family: "命理",
    grade: "B",
    status: "待校验",
    basis: "农历生日、时辰、命宫身宫、十四主星、辅煞、四化",
    bestFor: ["人生阶段", "十二宫主题", "关系与事业结构"],
    inputs: ["农历/公历生日", "时辰", "性别", "历法转换规则"],
    capability: "当前不自动排盘，避免命宫、五行局、安星错误。",
    guardrail: "必须通过成熟排盘库交叉验证后才输出命盘解释。"
  },
  {
    id: "fengshui",
    name: "风水与九宫飞星",
    family: "环境",
    grade: "C",
    status: "知识库",
    basis: "空间方位、流年飞星、住宅格局与现实动线",
    bestFor: ["居住调整", "办公布局", "空间复盘"],
    inputs: ["户型图", "朝向", "入住时间", "实际使用方式"],
    capability: "只提供知识框架，不用缺资料的脚本给方位断语。",
    guardrail: "没有户型和朝向时，只能做一般环境建议。"
  },
  {
    id: "tarot",
    name: "塔罗",
    family: "西方象征",
    grade: "C",
    status: "知识库",
    basis: "牌阵、牌义、关系与短期趋势象征",
    bestFor: ["心理镜像", "关系觉察", "短期选择题"],
    inputs: ["牌阵", "抽牌结果", "问题"],
    capability: "作为百科补充，不参与周易本经结论。",
    guardrail: "塔罗不是周易体系，不能与本经原文互相冒充依据。"
  },
  {
    id: "astrology",
    name: "西方星盘",
    family: "西方占星",
    grade: "C",
    status: "知识库",
    basis: "出生星图、行运、合盘",
    bestFor: ["人格模式", "关系合盘", "阶段性主题"],
    inputs: ["出生年月日时", "出生地"],
    capability: "当前只作为百科条目和未来扩展方向。",
    guardrail: "需要精确天文计算库，不使用泛星座替代星盘。"
  },
  {
    id: "routing",
    name: "综合问事路由",
    family: "产品层",
    grade: "S",
    status: "已启用",
    basis: "问题类型、资料完整度、体系可信度",
    bestFor: ["选择体系", "明确资料缺口", "避免误用"],
    inputs: ["用户问题", "已有资料"],
    capability: "帮助判断该用本经占筮、查卦库，还是等待更完整资料。",
    guardrail: "宁可降级说明，也不冒充高精度。"
  }
];

if (typeof window !== "undefined") window.DIVINATION_SYSTEMS = DIVINATION_SYSTEMS;
if (typeof module !== "undefined") module.exports = DIVINATION_SYSTEMS;
