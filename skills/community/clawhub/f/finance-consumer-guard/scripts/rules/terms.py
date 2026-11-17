#!/usr/bin/env python3
"""金融消保合规护栏 - 规则包 (terms)。

覆盖金融营销 / 销售场景中与"金融消费者权益保护"相关的高频危险表述，
主要依据（全文公开，监管机构官网可查）：
  - 《关于规范金融机构资产管理业务的指导意见》（银发〔2018〕106号，资管新规）：
    打破刚性兑付，金融机构不得承诺保本保收益。
  - 《商业银行理财业务监督管理办法》（银保监会2018年第6号）：
    理财业务不得宣传预期收益率，不得承诺保本保收益。
  - 《理财公司理财产品销售管理暂行办法》（银保监会2021年第4号）：
    不得误导销售，不得承诺保本保收益，应当充分揭示风险。
  - 《保险销售行为管理办法》（国家金融监督管理总局令，2024年施行）：
    不得夸大保险责任或保险产品收益，不得与存款混淆。
  - 《中华人民共和国广告法》第二十五条：
    招商等有投资回报预期的商品或服务广告，应当对风险及风险责任承担作出合理提示或警示，
    不得对未来效果、收益作出保证性承诺，不得利用学术机构、行业协会等作推荐证明。

本护栏聚焦"表述级红线"——即文本中明确写出、可能直接违反金融消保义务的
高频违规 / 高风险表述。它不评估金融机构是否真实持牌、是否真实履行
风险揭示与适当性义务（属 check / audit 形态），而是拦截文案里
"承诺保本保收益、夸大收益、弱化风险、无资质代销、使用极限词"等
可直接编码识别的危险表述，供发布前实时拦截。

纯数据定义，无副作用、无网络、无动态执行。

每条术语字段：
    term        违规表述（子串匹配，大小写不敏感）
    category    违规类别
    severity    风险等级 high / medium / low
    suggestion  整改建议（可选，缺省时使用类别默认建议）

设计原则：
  - 只收录"红线清晰、可编码"的高频表述，优先用短语降低误报。
  - 六类对应金融消保义务的不同侧面，便于溯源。
  - 规则可扩展：直接在 TERMS 中追加即可，内核无需改动。
"""

PROFILE = {
    "id": "finance_consumer",
    "name": "金融消保合规护栏规则",
    "version": "1.0.0",
    "basis": (
        "《关于规范金融机构资产管理业务的指导意见》（银发〔2018〕106号，资管新规）、"
        "《商业银行理财业务监督管理办法》（银保监会2018年第6号）、"
        "《理财公司理财产品销售管理暂行办法》（银保监会2021年第4号）、"
        "《保险销售行为管理办法》（2024年施行）、《中华人民共和国广告法》第二十五条。"
        "以上文件全文公开，国家金融监督管理总局 / 人民银行 / 证监会官网可查。"
    ),
}

# ============ 类别默认建议 ============
CATEGORY_DEFAULT = {
    "no_principal_guarantee": (
        "资管新规明确打破刚性兑付：金融机构开展资产管理业务时不得承诺保本保收益，"
        "不得保证本金安全或保证收益。不得对外宣称“保本理财 / 保本保收益 / 刚性兑付”。"
        "理财产品、基金、资管产品均不保证本金与收益，请以产品合同与风险揭示书为准。"
    ),
    "return_promise": (
        "金融营销不得对未来收益作出保证性承诺，不得明示或暗示“稳赚不赔 / 保证盈利 / "
        "保底收益 / 翻倍收益”。业绩比较基准、过往收益均非收益承诺，"
        "须在显著位置提示“市场有风险，投资需谨慎”。"
    ),
    "risk_weakness": (
        "金融营销须充分、显著揭示风险，不得弱化或隐瞒风险。"
        "“低风险高收益 / 高收益低风险 / 无风险高回报”等矛盾表述误导消费者，"
        "属典型违规；应当如实披露产品风险等级，不得宣称“几乎无风险”。"
    ),
    "past_performance_mislead": (
        "过往业绩不代表未来表现，不得使用“历史业绩保证 / 过往收益必然延续”等"
        "暗示未来收益的表述。引用历史业绩须同时醒目提示风险，不得作为收益承诺。"
    ),
    "unqualified_sales": (
        "金融产品的销售、代销须具备相应业务资质；任何机构 / 个人不得无证代销，"
        "不得以“代客理财 / 替您操盘 / 代你投资”等方式违规代客操作或承诺操盘收益。"
        "请核实销售机构与人员的金融业务资质。"
    ),
    "ad_superlative": (
        "《广告法》禁止在金融广告中使用“国家级 / 最高级 / 最佳 / 第一 / 顶级”等"
        "绝对化用语，不得使用“最安全理财”等误导性极限词。宣传应客观、有依据。"
    ),
}

CATEGORY_LABEL = {
    "no_principal_guarantee": "保本保收益/刚兑红线",
    "return_promise": "收益承诺/夸大",
    "risk_weakness": "风险弱化/误导",
    "past_performance_mislead": "过往业绩误导",
    "unqualified_sales": "无资质/代客理财",
    "ad_superlative": "广告极限词",
}

# ============ 违规表述表 ============
# (term, category, severity, suggestion?)
TERMS = [
    # —— 第一类：保本保收益 / 刚性兑付（high）——
    ("保本保收益", "no_principal_guarantee", "high", None),
    ("保证本金安全", "no_principal_guarantee", "high", None),
    ("保证收益", "no_principal_guarantee", "high", None),
    ("承诺保本", "no_principal_guarantee", "high", None),
    ("刚性兑付", "no_principal_guarantee", "high", None),
    ("保本理财", "no_principal_guarantee", "high", None),
    ("零风险理财", "no_principal_guarantee", "high", None),
    ("无风险理财", "no_principal_guarantee", "high", None),

    # —— 第二类：收益承诺 / 夸大（high）——
    ("稳赚不赔", "return_promise", "high", None),
    ("稳赚", "return_promise", "high", None),
    ("承诺收益", "return_promise", "high", None),
    ("保证盈利", "return_promise", "high", None),
    ("百分百盈利", "return_promise", "high", None),
    ("翻倍收益", "return_promise", "high", None),
    ("超高收益", "return_promise", "high", None),
    ("保底收益", "return_promise", "high", None),

    # —— 第三类：风险弱化 / 误导（high）——
    ("低风险高收益", "risk_weakness", "high", None),
    ("高收益低风险", "risk_weakness", "high", None),
    ("几乎无风险", "risk_weakness", "high", None),
    ("不提示风险", "risk_weakness", "high", None),
    ("无风险高回报", "risk_weakness", "high", None),
    ("风险极低且收益高", "risk_weakness", "high", None),

    # —— 第四类：过往业绩误导（medium）——
    ("历史业绩保证", "past_performance_mislead", "medium", None),
    ("过往收益保证未来", "past_performance_mislead", "medium", None),
    ("历史百分百盈利", "past_performance_mislead", "medium", None),
    ("过往收益必然延续", "past_performance_mislead", "medium", None),

    # —— 第五类：无资质 / 代客理财（high）——
    ("代客理财", "unqualified_sales", "high", None),
    ("无资质代销", "unqualified_sales", "high", None),
    ("替您操盘", "unqualified_sales", "high", None),
    ("保证操盘收益", "unqualified_sales", "high", None),
    ("代你投资", "unqualified_sales", "high", None),

    # —— 第六类：广告极限词 / 违规宣传（medium）——
    ("最佳理财", "ad_superlative", "medium", None),
    ("国家级理财", "ad_superlative", "medium", None),
    ("第一理财平台", "ad_superlative", "medium", None),
    ("顶级理财", "ad_superlative", "medium", None),
    ("最安全理财", "ad_superlative", "medium", None),
]
