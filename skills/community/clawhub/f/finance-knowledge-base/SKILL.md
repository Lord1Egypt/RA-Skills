---
name: Financial Industry Knowledge Base Manager
slug: finance-knowledge-base
description: AI-powered financial industry knowledge base manager — covers document organization, knowledge graph construction, semantic search, and intelligent Q&A. Built for financial institutions' internal knowledge management. Keywords: knowledge management, knowledge base, document management, semantic search, RAG, 知识库, 知识管理, 文档管理, 语义搜索, RAG, 知识图谱, 智能问答, 文档检索, 内部知识库, 企业知识管理.
version: "5.0.0"
---

# Financial Industry Knowledge Base Manager / 金融行业知识库

> **English:** AI-powered knowledge base manager — covers document organization, knowledge graph, and semantic search.
>
> **中文:** 知识库管理器——覆盖文档组织、知识图谱、语义搜索。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融行业知识库需覆盖最新监管政策 | 知识库需新增2026年Q1监管政策相关条目 |
| 金融监管 | 保险新规（车险/人身险/医疗险）、银行合规、证券信披等 | 知识库需新增2026年Q1监管政策相关条目 |
| 金融监管 | 反洗钱和合规管理知识条目需大幅扩充 | 知识库需新增2026年Q1监管政策相关条目 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **知识分散** | 文档散落各处，难找 | 统一知识库管理 |
| **知识孤岛** | 部门间知识不共享 | 跨部门知识共享 |
| **更新滞后** | 制度更新后知识未同步 | 知识版本管理 |
| **检索不准** | 关键词搜索效果差 | 语义搜索 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** knowledge management, knowledge base, document management, semantic search, RAG

**中文触发词（优先）：** 知识库 / 知识管理 / 文档管理 / 语义搜索 / 知识图谱 / RAG / 检索 / 查询

---

## Core Capabilities / 核心能力

### 1. Document Organization / 文档组织

```python
KNOWLEDGE_STRUCTURE = {
    "regulations": {
        "banking": ["监管法规", "合规要求", "检查清单"],
        "insurance": ["监管法规", "产品规则", "偿付能力"],
        "securities": ["证监会规则", "交易所规则", "自律规则"]
    },
    "products": {
        "banking": ["存款产品", "贷款产品", "理财", "信用卡"],
        "insurance": ["寿险", "财险", "健康险", "团险"],
        "securities": ["股票", "债券", "基金", "期权"]
    },
    "processes": {
        "操作规程": [...],
        "风险控制": [...],
        "客户服务": [...]
    }
}
```

### 2. RAG Search / RAG检索

```python
class KnowledgeBaseSearch:
    """知识库语义搜索"""
    
    def semantic_search(self, query: str, top_k: int = 5) -> list:
        """语义搜索"""
        # 1. Query embedding
        query_vector = embed_text(query)
        
        # 2. 向量相似度搜索
        results = vector_search(query_vector, top_k)
        
        # 3. Reranking
        reranked = rerank(query, results)
        
        # 4. 生成答案
        context = "\n".join([r["content"] for r in reranked])
        answer = generate_answer(query, context)
        
        return {
            "answer": answer,
            "sources": reranked
        }
```

---

## Disclaimer

This skill provides knowledge management tools for educational purposes.
## Appendix G. Alibaba Dianjin Fusion — finance-knowledge-base v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `investement-advisor` (AI投资顾问) & `researcher` (AI研究员)  
> **Essence**: 金融产品知识库、投资建议生成、客户画像分析、合规披露  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
用户请求 → 产品知识查询 → 客户画像匹配 → 投资建议生成 → 合规审查
   ↓
Knowledge Base:
  - 产品库（股票/基金/债券/衍生品）
  - 策略库（价值/成长/量化/对冲）
  - 案例库（历史成功/失败案例）
  - 合规库（监管规定/禁止行为）
   ↓
Advisory Process:
  1. 了解客户（风险偏好/投资期限/资金规模）
  2. 匹配产品（基于画像+市场状态）
  3. 生成建议（配置比例+买入时机+止损策略）
  4. 合规审查（风险提示+适当性匹配）
   ↓
Output:
  - 投资建议书（PDF/Markdown）
  - 产品对比表
  - 风险提示函
```

---

### G.2 Customer Profile & Risk Tolerance (Dianjin method)

**客户画像框架**：

| 维度 | 保守型 | 稳健型 | 激进型 |
|------|--------|--------|--------|
| 风险偏好 | 不能接受亏损 | 可接受<10%回撤 | 可接受>20%回撤 |
| 投资期限 | >3年 | 1-3年 | <1年 |
| 资金规模 | <50万 | 50-300万 | >300万 |
| 投资经验 | 无/少 | 3-5年 | >5年 |
| 推荐产品 | 债券/货币基金 | 混合基金/蓝筹股 | 成长股/衍生品 |

**适当性匹配规则（Dianjin风格）**：

```
客户风险等级 → 可推荐产品等级：

C1（保守型） → R1（低风险）产品
  - 国债、央行票据、政策性金融债
  - 货币市场基金、短期理财债券基金
  - 禁止推荐：股票、股票基金、衍生品

C2（稳健型） → R2（中低风险）产品
  - 高等级信用债、可转债
  - 混合基金（股票仓位<30%）
  - 禁止推荐：ST股票、杠杆产品

C3（平衡型） → R3（中风险）产品
  - 蓝筹股、ETF、混合基金
  - 禁止推荐：退市风险股、场外期权

C4（成长型） → R4（中高风险）产品
  - 成长股、行业主题基金
  - 禁止推荐：未上市公司股权

C5（激进型） → R5（高风险）产品
  - 衍生品、杠杆产品、ST股博弈
  - 必须签署《高风险警示函》
```

---

### G.3 Investment Advice Generation (Dianjin essence)

**投资建议书模板（Dianjin风格）**：

```
【投资建议书】

客户姓名：XXX
风险等级：C3（平衡型）
建议日期：2026-05-31

一、资产配置建议

| 资产类别 | 配置比例 | 产品示例 | 预期收益 | 风险等级 |
|----------|----------|----------|----------|----------|
| 现金管理 | 10% | 货币基金 | 2-3% | R1 |
| 固定收益 | 40% | 国债+高等级信用债 | 3-4% | R2 |
| 权益类 | 45% | 沪深300ETF+中证500ETF | 8-12% | R3 |
| 另类投资 | 5% | 黄金ETF | 5-8% | R3 |

二、具体产品推荐（TOP 5）

1. **华泰柏瑞沪深300ETF** (510300)
   - 推荐理由：估值低位（PE=11.2x），股息率3.2%
   - 买入时机：分批建仓，每月定投
   - 止损策略：跌破年线（-8%）止损

2. **易方达蓝筹精选混合** (005827)
   - 推荐理由：基金经理张坤，长期业绩优秀
   - 买入时机：回调5-8%时加仓
   - 止损策略：回撤>15%止损

...

三、风险提示

⚠️ 市场风险：股市波动可能导致本金亏损
⚠️ 流动性风险：开放式基金可能暂停赎回
⚠️ 信用风险：债券可能违约

四、合规声明

本人已充分了解客户风险承受能力，所推荐产品风险等级符合客户风险承受能力。本人承诺不以任何方式承诺收益或承担损失。

顾问签名：_________
日期：2026-05-31
```

---

### G.4 Compliance & Risk Constraints (Dianjin standards)

**合规要求（投资顾问精髓）**：

1. **适当性管理**：
   - 必须评估客户风险承受能力（问卷+面谈）
   - 禁止向C1客户推荐R3以上产品
   - 必须留存评估记录（至少5年）

2. **禁止行为**：
   - ❌ 不允许承诺收益（"年化10%", "保本"）
   - ❌ 不允许虚假宣传（"稳赚不赔"）
   - ❌ 不允许代客理财（全权委托）
   - ❌ 不允许利益冲突（未披露推荐产品的佣金）

3. **信息披露**：
   - 必须披露产品风险等级
   - 必须披露历史业绩（注明"过往业绩不代表未来"）
   - 必须披露费用（管理费+托管费+申购赎回费）

---

### G.5 Test Case (Dianjin quality)

**Test Case 1: 客户画像分析**

```
Input: "客户王先生，50岁，可投资资产200万，希望年化收益6-8%，不能接受超过10%的亏损"

Expected Output:
1. 风险等级评定：C3（平衡型）
2. 适当性匹配：可推荐R3及以下产品
3. 资产配置建议：固收40%+权益45%+现金15%
4. 具体产品推荐（TOP 3）

Quality Check:
- ✅ 风险评级准确
- ✅ 配置比例合理
- ✅ 产品风险匹配
- ✅ 合规披露完整
```

---

**End of Dianjin Fusion Content — finance-knowledge-base v5.0.0**
