---
name: Financial Industry Intelligent Marketing Assistant
slug: bank-marketing-campaign
description: AI-powered intelligent marketing assistant for banking and securities — covers customer segmentation, marketing campaign design, content generation, A/B testing, and ROI analysis. Built for bank and securities marketing teams. Keywords: intelligent marketing, customer segmentation, campaign design, content marketing, marketing automation, 智能营销, 客户分群, 营销活动, 内容营销, 精准营销, 营销自动化, 银行营销, 券商营销, 营销转化, 获客, 促活.
version: "3.0.0"
---

# Financial Industry Intelligent Marketing Assistant / 金融智能营销助手

> **English:** AI-powered intelligent marketing assistant — covers customer segmentation, campaign design, content generation, and ROI analysis.
>
> **中文:** 金融智能营销助手——覆盖客户分群、营销活动设计、内容生成、A/B测试、ROI分析。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **客户画像粗** | 营销不精准，转化率低 | 多维度客户分层 |
| **内容生产慢** | 营销物料制作周期长 | AI批量生成 |
| **渠道选择难** | 不知道哪个渠道最有效 | ROI分析+最优渠道推荐 |
| **活动效果差** | 投入大但转化少 | 数据驱动优化 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** intelligent marketing, customer segmentation, campaign design, content marketing, marketing automation, bank marketing, securities marketing

**中文触发词（优先）：** 智能营销 / 客户分群 / 精准营销 / 营销活动 / 内容营销 / 营销自动化 / 银行营销 / 券商营销 / 活动策划 / 用户增长 / 私域运营 / 转化率 / 营销ROI / 触达率 / 打开率 / 点击率

---

## Core Capabilities / 核心能力

### 1. Customer Segmentation / 客户分层

```python
class CustomerSegmentation:
    """客户分层引擎"""
    
    def segment_customers(self, customer_data: list) -> dict:
        """
        客户分层模型
        基于RFM+生命周期+风险偏好
        """
        segments = {
            "高净值保守型": [],
            "高净值进取型": [],
            "中产稳健型": [],
            "年轻成长型": [],
            "老年保守型": [],
            "潜力待激活型": []
        }
        
        for customer in customer_data:
            segment = self._classify_segment(customer)
            segments[segment].append(customer)
        
        return segments
    
    def _classify_segment(self, customer: dict) -> str:
        """分层逻辑"""
        assets = customer.get("total_assets", 0)
        risk = customer.get("risk_preference", "稳健型")
        age = customer.get("age", 30)
        activity = customer.get("transaction_frequency", 0)
        
        if assets > 1000000:
            if risk in ["保守型", "稳健型"]:
                return "高净值保守型"
            else:
                return "高净值进取型"
        elif assets > 100000:
            return "中产稳健型"
        elif age < 35:
            return "年轻成长型"
        elif age > 55:
            return "老年保守型"
        else:
            return "潜力待激活型"
```

### 2. Campaign Design / 营销活动设计

```python
CAMPAIGN_TEMPLATES = {
    "产品拉新": {
        "目标": "获取新客户",
        "适用产品": ["存款", "理财", "基金"],
        "活动设计": """
        【活动名称】：{产品名}新手礼
        
        【活动时间】：{开始}-{结束}
        
        【参与条件】：
        - 首次购买{产品类型}产品
        - 新客户注册并完成实名
        
        【活动奖励】：
        - 首投满{X}元 → 奖励{金额}
        - 首投满{X}元 → 额外奖励{金额}
        
        【获客渠道】：
        1. 朋友圈广告投放
        2. 银行APP弹窗
        3. 员工朋友圈转发
        """,
        "ROI预估": "目标ROI≥3"
    },
    
    "存量激活": {
        "目标": "激活沉睡客户",
        "适用场景": "6个月无交易客户",
        "活动设计": """
        【活动名称】：唤醒礼包
        
        【触达策略】：
        - 首触：短信关怀
        - 二触：电话回访
        - 三触：专属优惠
        
        【激励方案】：
        - 沉睡客户专属加息券
        - 专属理财经理服务
        - 限时体验金{金额}
        """,
        "KPI": "激活率≥15%"
    }
}
```

### 3. Content Generation / 内容生成

```python
def generate_marketing_content(content_type: str, params: dict) -> dict:
    """营销内容生成"""
    
    if content_type == "朋友圈文案":
        templates = [
            "【{产品名}限时福利】\n\n{利益点}\n\n⏰仅限{时间}\n💰年化收益最高{收益率}\n\n戳我了解详情👇",
            
            "好消息！{产品名}正在热售中~\n\n✨{亮点1}\n✨{亮点2}\n✨{亮点3}\n\n私信我可享专属优惠哦🎁"
        ]
        
    elif content_type == "短信文案":
        templates = [
            "尊敬的{客户姓名}，{产品名}新品首发！年化收益率{收益率}%，{开始日期}至{结束日期}限时发售。回复Y办理，回复T退订。",
            
            "{客户姓名}，您的好友向您推荐{产品名}！首投满{金额}元即返{奖励金额}元，最高返{上限}元！戳{链接}参与。"
        ]
        
    elif content_type == "海报文案":
        return {
            "主标题": "{产品名} 限时抢购",
            "副标题": "{核心卖点}",
            "数据展示": [
                f"年化收益 {收益率}%",
                f"起投金额 {金额}元",
                f"剩余份额 {份额}份"
            ],
            "CTA按钮": "立即抢购",
            "紧迫感": "名额有限，先到先得"
        }
    
    return {
        "type": content_type,
        "templates": templates,
        "filled_examples": [
            fill_template(t, params) for t in templates
        ]
    }
```

### 4. A/B Testing Framework / A/B测试框架

```python
class ABTestAnalyzer:
    """A/B测试分析"""
    
    def analyze_ab_test(self, variant_a: dict, 
                       variant_b: dict) -> dict:
        """
        A/B测试结果分析
        """
        # 计算转化率
        cvr_a = variant_a["conversions"] / max(variant_a["visitors"], 1)
        cvr_b = variant_b["conversions"] / max(variant_b["visitors"], 1)
        
        # 提升幅度
        lift = (cvr_b - cvr_a) / max(cvr_a, 0.001) * 100
        
        # 统计显著性检验
        significant = self._chi_square_test(
            variant_a["visitors"] - variant_a["conversions"],
            variant_a["conversions"],
            variant_b["visitors"] - variant_b["conversions"],
            variant_b["conversions"]
        )
        
        return {
            "variant_a": {
                "visitors": variant_a["visitors"],
                "conversions": variant_a["conversions"],
                "cvr": round(cvr_a * 100, 2)
            },
            "variant_b": {
                "visitors": variant_b["visitors"],
                "conversions": variant_b["conversions"],
                "cvr": round(cvr_b * 100, 2)
            },
            "lift": round(lift, 2),
            "statistically_significant": significant,
            "recommendation": "选择B" if lift > 5 and significant else "继续测试"
        }
```

---

## Disclaimer

This skill provides marketing planning tools for educational purposes. All marketing activities must comply with applicable advertising and financial regulations.
