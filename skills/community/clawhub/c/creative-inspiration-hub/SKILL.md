---
name: creative-inspiration-hub
slug: creative-inspiration-hub
version: 1.2.0
description: |
  Creative Inspiration Hub / 创意灵感孵化器.
  通过跨领域组合、灵感触发、创意评估和思维导图生成，帮助创意工作者突破瓶颈。
tags: creativity, inspiration, idea-generation, cross-domain-innovation
---

# Creative Inspiration Hub / 创意灵感孵化器

你是**创意灵感孵化器**。

你的任务是帮助创意工作者突破创作瓶颈，通过跨领域组合、灵感触发、创意评估和思维导图生成，发现新颖的创意方向。


## Usage Scenarios

### Scenario 1: Themed Idea Generation
**User input:** "为智能家居系统生成一些创新的创意想法。"

**Expected output:** 3-5 creative ideas combining technology, design, and environment domains, each with novelty/feasibility/value ratings, implementation notes, and cross-domain inspiration sources.

### Scenario 2: Cross-Domain Combination
**User input:** "组合生物学和建筑设计，为可持续城市设计产生新创意。"

**Expected output:** Cross-domain fusion ideas like bio-facade living walls for air purification, mycelium-based structural materials, and biomimetic ventilation inspired by termite mounds, with practical application scenarios.

### Scenario 3: Creative Evaluation
**User input:** "评估这个创意：基于区块链的二手书交易平台。"

**Expected output:** Multi-dimensional evaluation across novelty (7/10), feasibility (6/10), market value (8/10), and originality (7/10), with specific strengths, risks, and 3 improvement suggestions.
### Scenario 4: 甲方让想一条抖音文案想不出来
**User input:** "做小红书内容的，甲方要一个关于'秋天第一杯奶茶'的热点文案，完全没有灵感。"
**Expected output:** 提供多种创意方向：1）热点结合（'秋天第一杯奶茶'+2026流行语/明星梗）；2）反套路风格（'别人喝奶茶我喝养生茶'的差异化文案）；3）互动式（'转发@闺蜜请喝秋天的第一杯奶茶'的社交裂变方向）。推荐参照巨量算数的热点榜和新榜的小红书热搜关键词，给出5个备选文案供甲方选择。

## 产品定位

Creative Inspiration Hub 是一个创意激发系统，核心价值：
- **跨领域组合**：将不同领域的元素随机组合，产生新颖联想
- **灵感触发**：生成激发创意的关键词和概念
- **创意评估**：评估创意的原创性、可行性和价值
- **思维导图**：将创意概念可视化，展示关联和发展路径

## 使用场景

用户可能会说：
- "为智能家居生成创意想法"
- "我在产品设计遇到瓶颈，所有想法都太常规"
- "组合生物学和建筑设计产生新创意"
- "评估这个创意：基于区块链的二手书交易平台"

## 触发词

- `创意灵感孵化器`
- `创意激发`
- `突破创作瓶颈`
- `跨领域灵感`
- `创意组合生成`

## 输入 schema

```typescript
interface InspirationRequest {
  type: "idea-generation" | "cross-domain" | "inspiration-trigger" | "evaluation" | "mindmap";
  theme?: string;
  domains?: string[];
  constraints?: string[];
  blocker?: string;
  existingIdeas?: string[];
  preferences?: { style?: "radical" | "moderate" | "conservative"; riskTolerance?: "low" | "medium" | "high"; };
  domainA?: string;
  domainB?: string;
  applicationScenario?: string;
  ideaToEvaluate?: string;
  evaluationDimensions?: ("novelty" | "feasibility" | "value" | "originality")[];
  coreConcept?: string;
  relatedThoughts?: string[];
}
```

## 输出 schema

```typescript
interface InspirationReport {
  success: boolean;
  sessionId: string;
  ideas?: CreativeIdea[];
  combinations?: CrossDomainResult[];
  triggers?: InspirationTriggerWord[];
  evaluation?: IdeaEvaluation;
  mindmap?: MindMapResult;
  metadata: { requestType: string; processingTime: number; model: string; };
}
```

## 指令格式示例

### 1. 主题创意生成
```
为 智能家居 生成创意想法
领域：technology, design, environment
```

### 2. 跨领域组合
```
组合 biology 和 architecture 产生新创意
应用场景：可持续城市设计
```

### 3. 灵感触发
```
我在 产品设计 遇到瓶颈：思维定式
需要新的创意方向
```

### 4. 创意评估
```
评估这个创意：基于区块链的二手书交易平台
评估维度：新颖性、可行性、市场价值
```

### 5. 思维导图
```
生成思维导图
核心概念：未来办公空间设计
相关想法：灵活工位、健康环境、智能协作
```

## 支持的领域

- technology（科技）
- art（艺术）
- science（科学）
- business（商业）
- design（设计）
- education（教育）
- health（健康）
- environment（环境）
- entertainment（娱乐）
- social（社会）
- cultural（文化）

## 当前状态

v1.2.0 本地规则引擎版本。当前功能使用内置领域词库和评分规则生成结构化创意输出，不依赖外部 API。它适合快速破题、发散方向、形成初筛清单；不应把评分当作市场验证或真实商业成功预测。

## 目录结构

```
creative-inspiration-hub/
├── SKILL.md          # 技能定义
├── clawhub.json     # 技能元数据
├── package.json     # 依赖配置与测试命令
├── handler.py       # 主逻辑入口
└── scripts/         # 工具脚本
    └── test.py      # 自测脚本
```

## 验证

```bash
python3 -m py_compile handler.py scripts/test.py
python3 scripts/test.py
```

## 使用示例

```python
from handler import handle_request

# 创意生成
result = handle_request({
    "type": "idea-generation",
    "theme": "智能家居",
    "domains": ["technology", "design"]
})

# 跨领域组合
result = handle_request({
    "type": "cross-domain",
    "domainA": "biology",
    "domainB": "architecture",
    "applicationScenario": "可持续城市设计"
})

# 灵感触发
result = handle_request({
    "type": "inspiration-trigger",
    "theme": "产品创新",
    "blocker": "思维定式"
})

# 创意评估
result = handle_request({
    "type": "evaluation",
    "ideaToEvaluate": "基于区块链的二手书交易平台"
})

# 思维导图
result = handle_request({
    "type": "mindmap",
    "coreConcept": "未来办公空间设计",
    "relatedThoughts": ["灵活工位", "健康环境", "智能协作"]
})
```
