---
name: Financial Industry Intelligent Customer Service
slug: bank-customer-service
description: AI-powered intelligent customer service for banking and securities — covers FAQ answering, account inquiry, transaction guidance, complaint handling, and 7x24 automated support. Built for China financial institution call centers and digital customer service teams. Keywords: intelligent customer service, chatbot, FAQ, complaint handling, banking service, securities service, 智能客服, 客服机器人, FAQ, 投诉处理, 银行服务, 证券客服, 呼入客服, 智能问答, 24小时客服.
version: "3.0.0"
---

# Financial Industry Intelligent Customer Service / 金融智能客服

> **English:** AI-powered intelligent customer service for banking and securities — covers FAQ, account services, transaction guidance, and complaint handling with compliance focus.
>
> **中文:** 金融智能客服——覆盖FAQ解答、账户服务、交易指导、投诉处理，7x24自动化支持。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **重复问题多** | 人工客服效率低 | 智能FAQ自动解答 |
| **响应慢** | 客户等待时间长 | 秒级AI响应 |
| **服务时间受限** | 非工作时间无法服务 | 24小时在线 |
| **情绪化投诉** | 处理不当升级 | 标准投诉处理SOP |
| **合规风险** | 服务话术不合规 | 实时合规检查 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** intelligent customer service, chatbot, FAQ, complaint handling, banking service, securities service, account inquiry, transaction guidance

**中文触发词（优先）：** 智能客服 / 客服机器人 / FAQ / 投诉处理 / 银行服务 / 账户查询 / 交易指导 / 开户咨询 / 密码重置 / 银行卡 / 信用卡 / 理财产品 / 基金 / 证券账户 / 转账 / 汇款 / 挂失 / 解冻 / 销户

---

## Core Capabilities / 核心能力

### 1. FAQ Knowledge Base / FAQ知识库

```python
FAQ_DATABASE = {
    "银行卡类": {
        "密码忘了怎么办": {
            "answer": """
            您可以通过以下方式重置密码：
            
            1. **手机银行重置**（推荐）
               登录手机银行 → 我的 → 安全中心 → 密码管理 → 重置密码
            
            2. **网上银行重置**
               登录网上银行 → 安全中心 → 密码管理
            
            3. **网点办理**
               携带有效身份证件前往任意网点办理
            
            ⚠️ 温馨提示：重置密码需要验证您的身份信息。
            """,
            "category": "账户服务",
            "satisfaction_score": 4.5
        },
        "卡片被盗刷怎么办": {
            "answer": """
            发现卡片被盗刷，请按以下步骤处理：
            
            🚨 **紧急处理**
            1. 立即拨打客服热线 955XX 冻结卡片
            2. 附近ATM做一笔查询交易（证明卡片在你手中）
            
            📝 **报案处理**
            3. 就近派出所报案，取得报案回执
            
            🏦 **银行处理**
            4. 携带报案材料前往网点
            5. 填写赔付申请表
            6. 银行将在3-5个工作日内审核
            
            💡 **预防建议**
            • 开通交易通知短信
            • 设置合理的单笔/日累计限额
            • 避免在不明商户刷卡
            """,
            "category": "紧急处理",
            "urgency": "high"
        }
    },
    
    "理财产品类": {
        "理财赎回多久到账": {
            "answer": """
            不同产品赎回到账时间不同：
            
            | 产品类型 | 工作日提交 | 非工作日提交 |
            |---------|-----------|-------------|
            | 货币基金 | T+1日 | 下个工作日 |
            | 债券基金 | T+2日 | 下个工作日 |
            | 混合基金 | T+3日 | 下个工作日 |
            | 股票基金 | T+3日 | 下个工作日 |
            | 银行理财 | T+1~3日 | 下个工作日 |
            
            ⏰ 到账时间：一般为工作日15:00前提交当日处理
            💰 资金将返回至您的绑定账户
            """,
            "category": "资金服务"
        }
    }
}
```

### 2. Complaint Handling SOP / 投诉处理SOP

```python
COMPLAINT_HANDLING_SOP = {
    "阶段一：情绪安抚（0-30秒）": {
        "目标": "让客户感受到被重视",
        "话术": """
        "您好，我是{姓名}，很高兴为您服务。
        
        我完全理解您现在的心情，{表示理解}确实会让人感到{情绪词}。
        
        请您放心，我会认真听取您的情况，
        尽全力帮您解决这个问题。"
        """,
        "关键点": [
            "使用尊称",
            "表达共情",
            "不打断客户",
            "记录关键信息"
        ]
    },
    
    "阶段二：问题收集（30秒-2分钟）": {
        "目标": "全面了解问题",
        "收集要素": [
            "客户姓名",
            "账户/卡号后四位",
            "问题类型",
            "发生时间",
            "涉及金额",
            "客户诉求"
        ],
        "话术": """
        "为了更好地帮您处理，
        请允许我确认几个信息：
        
        1. 您的姓名是...？
        2. 涉及的账户尾号是...？
        3. 这个问题是什么时候发生的？
        4. 涉及的具体金额是...？
        5. 您希望我们怎么帮您解决？"
        """
    },
    
    "阶段三：方案提供（2-5分钟）": {
        "方案类型": {
            "即时解决": "能当场处理的，立即解决",
            "升级处理": "复杂问题，承诺时限升级",
            "补偿方案": "服务失误时，适度补偿"
        },
        "话术": """
        "非常感谢您的耐心等待。
        
        针对您的问题，我有以下解决方案：
        
        【方案A】{方案描述}
        优点：{优点}
        预计时间：{时间}
        
        【方案B】{方案描述}
        优点：{优点}
        预计时间：{时间}
        
        您更倾向于哪个方案？
        或者您有其他想法也可以告诉我。"
        """
    },
    
    "阶段四：确认闭环（5-6分钟）": {
        "话术": """
        "好的，我已经记录了您的诉求。
        
        【问题确认】
        {复述问题}
        
        【解决方案】
        {解决方案}
        
        【预计时间】
        {时间承诺}
        
        【跟进人员】
        {跟进人姓名} {联系方式}
        
        我将这个问题记录为工单编号{工单号}，
        处理过程中如有进展会第一时间通知您。
        
        请问还有其他需要帮助的吗？"
        """
    }
}
```

### 3. Intent Classification / 意图分类

```python
class IntentClassifier:
    """客户意图分类"""
    
    INTENT_PATTERNS = {
        "查询类": {
            "keywords": ["查询", "看看", "多少", "有没有", "怎么"],
            "entities": ["余额", "账单", "记录", "流水", "积分"]
        },
        "办理类": {
            "keywords": ["办理", "开通", "申请", "设置", "修改"],
            "entities": ["转账", "分期", "还款", "挂失", "密码"]
        },
        "投诉类": {
            "keywords": ["投诉", "不满", "问题", "没用", "太差"],
            "entities": ["服务", "处理", "速度", "态度"]
        },
        "咨询类": {
            "keywords": ["问问", "了解一下", "怎么用", "是什么"],
            "entities": ["产品", "功能", "规则", "费用"]
        }
    }
    
    def classify(self, query: str) -> dict:
        """意图分类"""
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0
            for kw in patterns["keywords"]:
                if kw in query:
                    score += 1
            for entity in patterns["entities"]:
                if entity in query:
                    score += 2
            
            if score >= 2:
                return {
                    "intent": intent,
                    "confidence": min(score / 5, 1.0),
                    "suggested_response_type": self._get_response_type(intent)
                }
        
        return {"intent": "unknown", "confidence": 0}
```

---

## Disclaimer

This skill provides customer service tools for educational purposes. All responses must comply with applicable regulations and accuracy requirements.
