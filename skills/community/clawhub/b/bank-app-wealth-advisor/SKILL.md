---
name: "Bank APP Wealth Advisor Assistant"
slug: bank-app-wealth-advisor
description: "AI-powered wealth advisory assistant for bank mobile applications — provides product recommendations, investment consultation, and compliance-compliant customer interaction. Built for digital banking teams."
version: 3.0.1
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Bank APP Wealth Advisor Assistant / 银行APP财富顾问助手

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 合规与风险警告**
> - 本技能仅供教育培训参考，**不构成任何投资建议或销售推荐**
> - 资产配置方案和产品匹配为**方法论演示**，实际投资决策须由持牌金融机构及专业人员作出
> - 严禁使用本技能的输出作为"保本""稳赚"等承诺性表述的依据
> - 所有理财建议须遵守《商业银行理财业务监督管理办法》及相关监管规定
> - 用户应结合自身风险承受能力独立判断

## Identity

**⚠️ 精确触发规则**：仅当用户明确提到银行APP财富管理、智能投顾、产品推荐等相关需求时激活。日常对话提及"银行"、"APP"、"理财"等通用词汇时**不会自动触发**。

**用户确认规则**：匹配以下关键词时，需先向用户确认后再进入财富顾问模式：
- "您需要银行APP财富顾问服务吗？请注意：本技能仅供参考，不构成投资建议。"

> **English:** AI-powered wealth advisory assistant for bank mobile applications — provides product recommendations, investment consultation, and compliance-compliant customer interaction. Built for digital banking teams.
>
> **中文:** 银行APP财富顾问助手——为手机银行提供产品推荐、投资咨询、合规客户交互。适用：数字银行团队、财富管理师。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill参考方案 |
| :--- | :--- | :--- |
| **APP用户粘性低** | 用户用完即走，无深度服务 | AI投顾提升个性化体验 |
| **产品匹配效率低** | 人工推荐成本高 | 智能产品匹配引擎 |
| **合规要求严** | 监管禁止虚假宣传 | 合规话术自动检查 |
| **服务覆盖有限** | 人工客服无法7x24 | AI24小时在线解答 |
| **交叉销售难** | 客户画像不完整 | 多维度客户分析 |

---

## Trigger Keywords / 触发关键词

**精确匹配规则**：激活关键词需与银行APP财富管理场景直接相关。

**English Triggers:** bank APP wealth advisor, digital banking advisor, mobile banking consultation, product recommendation engine, financial planning assistant

**中文触发词：** 银行APP财富顾问 / 智能投顾建议 / 手机银行理财 / 产品推荐匹配 / 资产配置方案

**不适用场景**（若用户意图属于以下范畴，请引导至其他技能）：
- 个人股票投资建议（请使用投资分析技能）
- 保险产品购买（请使用保险相关技能）
- 具体基金/理财产品购买执行（应通过银行APP官方渠道）

---

## Core Capabilities / 核心能力

### 1. Product Matching Engine / 产品匹配引擎

> **⚠️ 以下代码为教学示例，展示产品匹配的方法论逻辑，不构成实际推荐。** 实际产品匹配须基于持牌金融机构的合规系统和适当性管理要求。

```python
class WealthAdvisor:
    """智能财富顾问（教学参考）"""

    def match_products(self, customer_profile: dict,
                      available_products: list) -> list:
        """
        智能产品匹配（教学方法论）
        Args:
            customer_profile: 客户画像
            available_products: 可选产品列表
        """
        # 风险匹配
        risk_level_map = {
            "保守型": ["R1", "R2"],
            "稳健型": ["R1", "R2", "R3"],
            "平衡型": ["R2", "R3", "R4"],
            "成长型": ["R3", "R4", "R5"],
            "激进型": ["R4", "R5"]
        }

        allowed_risk = risk_level_map.get(
            customer_profile.get("risk_preference", "稳健型"), ["R2", "R3"]
        )

        # 收益匹配
        expected_return = customer_profile.get("expected_return", 0.05)

        matched = []
        for product in available_products:
            # 风险等级过滤
            if product["risk_level"] not in allowed_risk:
                continue

            # 收益率匹配
            if product["expected_return"] >= expected_return - 0.02:
                score = self._calculate_match_score(
                    customer_profile, product
                )
                matched.append({
                    **product,
                    "match_score": score,
                    "recommendation_reason": self._generate_reason(
                        customer_profile, product
                    )
                })

        return sorted(matched, key=lambda x: x["match_score"], reverse=True)

    def _calculate_match_score(self, customer: dict,
                               product: dict) -> float:
        """计算匹配度评分（教学示例）"""
        score = 100

        # 期限匹配
        preferred_term = customer.get("preferred_term", 365)
        product_term = product.get("term_days", 365)
        term_diff = abs(preferred_term - product_term) / 365
        score -= term_diff * 10

        # 起购金额
        if product.get("min_amount", 0) > customer.get("available_fund", 0):
            score -= 30

        # 收益率
        expected = customer.get("expected_return", 0.05)
        actual = product.get("expected_return", 0)
        if actual >= expected:
            score += 10
        else:
            score -= abs(actual - expected) * 100

        return max(0, min(100, score))
```

### 2. Investment Consultation Scripts / 投资咨询话术参考

> **⚠️ 重要声明**：以下话术为**教学参考模板**，展示合规话术的结构和方法。实际使用须经持牌金融机构合规部门审核，并严格遵守《商业银行理财业务监督管理办法》及相关规定。

```python
INVESTMENT_SCRIPTS = {
    "基金购买引导": {
        "场景": "客户咨询基金",
        "话术模板": """
        "您好！根据您的风险测评结果【{risk_level}】，
        我们推荐您关注【{fund_name}】基金（仅供示例参考）。

        这只基金的特点：
        • 基金类型：{fund_type}
        • 风险等级：{risk_level}
        • 近一年收益：{return_1y}%
        • 基金经理：{manager}（从业{years}年）

        供您参考的理由：
        1. {reason_1}
        2. {reason_2}
        3. {reason_3}

        【风险提示】基金有风险，投资需谨慎。过往业绩不代表未来表现。
        本推荐不构成投资建议，请您根据自身情况谨慎决策。"
        """,
        "合规检查": [
            "不得承诺保本或最低收益",
            "必须说明基金有风险",
            "过往业绩仅供参考，不预示未来表现",
            "须匹配客户风险等级"
        ]
    },

    "资产配置建议参考": {
        "场景": "客户有大额资金需配置",
        "话术模板": """
        "张先生/女士，您好！

        以下是一个参考性的资产配置框架示例：

        【稳健型配置】40% → 银行存款+国债
        特点：风险较低，收益相对稳定

        【均衡型配置】30% → 银行理财+债券基金
        特点：收益稳健，波动较小

        【成长型配置】20% → 混合基金+股票基金
        特点：追求较高收益，承担一定风险

        【流动性管理】10% → 货币基金
        特点：随存随取，应急备用

        以上配置方案仅为方法论示例，不构成投资建议。
        实际配置方案须由持牌理财经理根据客户实际情况和合规要求制定。
        "
        """
    }
}
```

### 3. Compliance Check / 合规检查清单

```markdown
## APP投顾合规检查清单

### 必须包含的要素
| 检查项 | 要求 |
|-------|------|
| 风险提示 | 必须出现"投资有风险" |
| 收益说明 | 不得承诺保本保收益 |
| 历史业绩 | 必须注明"仅供参考，不预示未来表现" |
| 适当性 | 必须匹配客户风险等级 |
| 产品揭示 | 须包含产品说明书或风险揭示书 |

### 禁止用语
| 禁止 | 替代 |
|-----|------|
| "保本"/"保本保息" | "风险较低""相对稳健" |
| "稳赚不赔" | "追求稳健收益" |
| "最低收益X%" | "历史平均收益X%（仅供参考）" |
| "100%安全" | "风险可控" |
| "适合保本需求" | "风险偏好较低的投资者可关注" |
```

---

## Disclaimer / 免责声明

> ⚠️ **重要声明**
> - This skill provides wealth advisory tools for **educational reference only**
> - All recommendations must comply with applicable regulations and be reviewed by qualified financial advisors
> - 本技能提供财富顾问工具的**教学参考**，仅供教育用途
> - 所有推荐必须遵守适用的法规，并由合格财务顾问审核
> - **不得**基于本技能输出向客户作出任何保本或收益承诺
> - 实际理财产品销售须通过银行官方渠道完成，并遵循适当性管理要求
