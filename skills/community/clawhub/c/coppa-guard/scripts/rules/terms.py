#!/usr/bin/env python3
"""COPPA 美国儿童隐私护栏 - 规则包 (terms)。

覆盖美国《儿童在线隐私保护法》(Children's Online Privacy Protection Act,
15 U.S.C. § 6501 et seq.) 及 FTC 实施规则 (16 C.F.R. Part 312) 语境下，
面向美国市场（尤其中国出海企业的儿童向 App / 游戏 / 电商 / 教育产品）
在文案、隐私政策、应用商店描述中需警惕的儿童隐私合规触发点与违规表述。

纯数据定义，无副作用、无网络、无动态执行。

每条术语字段：
    term        触发/违规用语（子串匹配，大小写不敏感）
    category    类别
    severity    风险等级 high / medium / low
    suggestion  整改建议（可选，缺省时使用类别默认建议）

设计原则：
  - 只收录"红线清晰、可编码"的高频触发词与违规表述，降低误报。
  - COPPA 适用前提是"面向 13 岁以下儿童"或"明知收集 13 岁以下儿童信息"，
    因此第一要务是识别"是否进入 COPPA 适用范围"（directed_children 类）。
  - 一旦进入范围，核心合规义务是"可验证家长同意"(Verifiable Parental Consent, VPC)。
  - 规则可扩展：直接在 TERMS 中追加即可，内核无需改动。
"""

PROFILE = {
    "id": "coppa",
    "name": "COPPA 儿童隐私护栏规则",
    "version": "1.0.0",
    "basis": "美国《儿童在线隐私保护法》(Children's Online Privacy Protection Act, 15 U.S.C. § 6501 et seq.) 及 FTC 实施规则 (16 C.F.R. Part 312)",
}

# ============ 类别默认建议 ============
CATEGORY_DEFAULT = {
    "directed_children": "若服务'面向 13 岁以下儿童'(directed to children under 13)或为明知的收集对象，COPPA 全面适用：须取得可验证家长同意(VPC)、提供家长审查/撤回通道、最小化收集并告知目的与范围。",
    "collect_minor_pii": "向 13 岁以下儿童收集个人信息前，须取得可验证家长同意(VPC)并明确告知收集目的与范围；建议核对 COPPA 合规流程与隐私政策披露。",
    "behavioral_ads_kids": "向儿童投放行为定向广告须先取得可验证家长同意；COPPA 禁止在未获同意前利用儿童持久标识符做跨站追踪/定向。",
    "no_vpc": "COPPA 核心要求是'可验证家长同意'(Verifiable Parental Consent)；声称无需家长同意即收集儿童数据属明显违规，须立即补正并取得同意机制。",
    "third_party_kids": "向第三方披露儿童个人信息须取得家长同意，并披露接收方身份与用途；建议审查数据流转与第三方协议。",
    "persistent_id_kids": "收集儿童'持久标识符'(cookie、设备 ID 等)用于跨站追踪须获家长同意；仅用于支持的持久标识符(如会话维持)可豁免但须声明。",
}

CATEGORY_LABEL = {
    "directed_children": "面向儿童(触发适用)",
    "collect_minor_pii": "收集儿童个人信息",
    "behavioral_ads_kids": "儿童行为定向广告",
    "no_vpc": "缺少可验证家长同意",
    "third_party_kids": "第三方披露儿童数据",
    "persistent_id_kids": "儿童持久标识符追踪",
}

# ============ 术语表 ============
# (term, category, severity, suggestion?)
TERMS = [
    # —— 面向儿童(触发 COPPA 适用) medium ——
    ("for kids", "directed_children", "medium", None),
    ("for children", "directed_children", "medium", None),
    ("kids app", "directed_children", "medium", None),
    ("children's app", "directed_children", "medium", None),
    ("kids game", "directed_children", "medium", None),
    ("children's game", "directed_children", "medium", None),
    ("for toddlers", "directed_children", "medium", None),
    ("preschool", "directed_children", "medium", None),
    ("elementary school", "directed_children", "medium", None),
    ("ages 3", "directed_children", "medium", None),
    ("cartoon for kids", "directed_children", "medium", None),
    ("baby game", "directed_children", "medium", None),
    ("儿童", "directed_children", "medium", None),
    ("少儿", "directed_children", "medium", None),
    ("幼儿", "directed_children", "medium", None),
    ("宝宝", "directed_children", "medium", None),
    ("适龄儿童", "directed_children", "medium", None),
    ("益智游戏", "directed_children", "medium", None),
    ("儿童版", "directed_children", "medium", None),
    ("少儿版", "directed_children", "medium", None),

    # —— 收集儿童个人信息 high ——
    ("collect children's data", "collect_minor_pii", "high", None),
    ("collect from children", "collect_minor_pii", "high", None),
    ("child account", "collect_minor_pii", "high", None),
    ("children's information", "collect_minor_pii", "high", None),
    ("under 13 account", "collect_minor_pii", "high", None),
    ("kids' profiles", "collect_minor_pii", "high", None),
    ("收集儿童信息", "collect_minor_pii", "high", None),
    ("儿童账号", "collect_minor_pii", "high", None),
    ("未满13岁", "collect_minor_pii", "high", None),
    ("未满13", "collect_minor_pii", "high", None),
    ("儿童个人资料", "collect_minor_pii", "high", None),

    # —— 儿童行为定向广告 high ——
    ("personalized ads for kids", "behavioral_ads_kids", "high", None),
    ("targeted ads to children", "behavioral_ads_kids", "high", None),
    ("behavioral advertising to children", "behavioral_ads_kids", "high", None),
    ("kids ads", "behavioral_ads_kids", "high", None),
    ("向儿童推送广告", "behavioral_ads_kids", "high", None),
    ("儿童精准广告", "behavioral_ads_kids", "high", None),
    ("儿童定向广告", "behavioral_ads_kids", "high", None),

    # —— 缺少可验证家长同意 high ——
    ("no parental consent", "no_vpc", "high", None),
    ("without parental consent", "no_vpc", "high", None),
    ("parents not required", "no_vpc", "high", None),
    ("no parent approval", "no_vpc", "high", None),
    ("parental consent not needed", "no_vpc", "high", None),
    ("无需家长同意", "no_vpc", "high", None),
    ("不通知家长", "no_vpc", "high", None),
    ("家长无需同意", "no_vpc", "high", None),
    ("不征求家长同意", "no_vpc", "high", None),

    # —— 第三方披露儿童数据 medium ——
    ("share children's data", "third_party_kids", "medium", None),
    ("sell kids' information", "third_party_kids", "medium", None),
    ("disclose children's data", "third_party_kids", "medium", None),
    ("出售儿童数据", "third_party_kids", "medium", None),
    ("共享儿童信息", "third_party_kids", "medium", None),
    ("向第三方提供儿童数据", "third_party_kids", "medium", None),

    # —— 儿童持久标识符追踪 medium ——
    ("track kids across sites", "persistent_id_kids", "medium", None),
    ("children's device id", "persistent_id_kids", "medium", None),
    ("persistent identifier children", "persistent_id_kids", "medium", None),
    ("追踪儿童设备", "persistent_id_kids", "medium", None),
    ("儿童设备识别码", "persistent_id_kids", "medium", None),
    ("追踪儿童 cookies", "persistent_id_kids", "medium", None),
]
