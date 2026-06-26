---
name: article-taster
description: 文章品鉴师 - 多维度评估文章质量、检测AI味/大便味、识别原创内容
author: Article Taster Team
version: 1.0.0
tags:
  - 文章分析
  - AI检测
  - 质量评估
  - 原创识别
  - 阅读推荐
languages:
  - 中文
  - Python
platform:
  - claude
  - openclaw
  - agent
created: 2026-04-08
updated: 2026-04-08
---

# Article Taster - 文章品鉴师

> 帮助用户提前品尝文章可读性，过滤低质量内容，节省宝贵阅读时间

## 核心定位

**"文章含大质量检测"** —— 站在文章分析师的角度，多维度评估文章价值：
- 技术文章：衡量技术含量、学习价值
- AI生成检测：正确识别原创内容（古诗等不被误判）
- 情感散文：分析情感曲线、架构模式
- 小说：分析情节结构（但不剧透）

---

## 工作流程

```
输入文章文本/标题
       ↓
┌─────────────────────────────────────┐
│  M1: 文章类型识别                     │
│  技术文章 | 情感散文 | 小说 | 其他     │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  M2: 专业分析 (根据类型分发)           │
│  ├─ 技术文章 → TechAnalyzer          │
│  ├─ 情感/散文 → CreativeAnalyzer     │
│  ├─ 小说 → NovelAnalyzer (无剧透)   │
│  └─ 其他 → GenericAnalyzer           │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  M3: AI生成检测与原创识别              │
│  ├─ 文本统计特征                      │
│  ├─ 困惑度分析                        │
│  ├─ 风格一致性                        │
│  └─ 原创内容豁免 (古诗词/经典文学)     │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  M4: 综合评分与阅读建议                │
│  最终评分 + 等级 + 阅读价值建议        │
└─────────────────────────────────────┘
       ↓
输出: JSON报告 + Markdown摘要
```

---

## 评分体系

### 技术文章评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 技术深度 | 30% | 原理剖析、实战经验、解决方案复杂度 |
| 结构清晰度 | 25% | 逻辑组织、层次分明 |
| 实用性 | 20% | 可操作、可落地 |
| 原创性 | 15% | 独特观点、非AI生成 |
| 可读性 | 10% | 表达流畅、图文配合 |

### 情感散文/小说评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 情感表达 | 30% | 情感深度、感染力、曲线设计 |
| 文笔水平 | 25% | 修辞手法、句式变化、词汇丰富度 |
| 叙事结构 | 20% | 情节安排、节奏把控 |
| 创意性 | 15% | 独特视角、创新表达 |
| 共鸣度 | 10% | 读者情感连接 |

### AI生成检测维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 文本统计 | 10% | 句子长度方差、词汇密度、标点多样性 |
| 困惑度 | 15% | 语言模型困惑度（过低=疑似AI） |
| 词汇丰富度 | 10% | Type-Token Ratio、罕见词汇比例 |
| 风格一致性 | 10% | 开头词重复率、过渡词规律性 |
| 语义连贯 | 5% | 指代一致性、主题集中度 |
| 特殊模式 | 10% | 古诗词/经典文学豁免检测 |

### AI味/大便味检测维度 (新增)

| 维度 | 权重 | 说明 |
|------|------|------|
| 段落一致性 | 15% | AI文章段落长度高度一致，像模具铸出来的 |
| 废话率 | 10% | 每句都对但空洞，无实质信息密度 |
| 模板化程度 | 10% | 三段式、综上所述、首先其次最后等 |
| 人类标记 | 5% | 踩坑、血泪史、说实话等personal voice |

### AI味评分等级

| 评分 | 等级 | 说明 |
|------|------|------|
| <20 | 人类写作 | 几乎无AI味 |
| 20-40 | 轻度疑似AI | 可能有轻微AI辅助 |
| 40-60 | 中度疑似AI | 明显AI特征 |
| 60-80 | 高度疑似AI | 强烈AI味 |
| >80 | 大便味 | 极强AI味，内容空洞 |

### 综合评分公式

```
最终评分 = 加权得分 × 类型匹配度 × (1 - AI概率 × 0.3)
```

### 评分等级

| 等级 | 分数 | 阅读建议 |
|------|------|----------|
| A+ | 90-100 | 极力推荐！值得反复研读 |
| A | 80-89 | 强烈推荐！内容扎实 |
| B+ | 70-79 | 推荐阅读，有价值 |
| B | 60-69 | 可读，碎片时间可看 |
| C | 40-59 | 一般，可选择性阅读 |
| D | <40 | 不推荐，浪费时间 |

---

## AI生成检测豁免规则

为防止误判真正的原创内容，采用豁免机制：

| 类型 | 检测特征 | 豁免效果 |
|------|---------|---------|
| 古诗词 | 五言/七言、押韵、意象密度 | AI阈值提高50%+ |
| 经典文学 | 长句、复合句、修辞丰富 | 方差阈值放宽100% |

**古诗测试预期**: "床前明月光..." → 识别为 classical_poetry，得分>85，标注"高度可信原创"

---

## 输出报告格式

### JSON 完整报告

```json
{
  "report_id": "taster_20260408_001",
  "title": "文章标题",
  "type": "technical_article|essay|novel|other",
  "type_confidence": 0.92,
  "overall_score": 85,
  "grade": "A",
  "reading_advice": {
    "verdict": "强烈推荐！内容扎实，适合认真阅读",
    "target_audience": "初中级开发者",
    "time_estimation": "10分钟",
    "key_benefits": ["深入浅出的架构设计", "实操性强"],
    "suitable_moments": ["专注阅读", "深度学习"]
  },
  "dimension_scores": {
    "technical_depth": {"score": 88, "weight": 0.30},
    "structure": {"score": 85, "weight": 0.25},
    "practicality": {"score": 82, "weight": 0.20},
    "originality": {"score": 78, "weight": 0.15},
    "readability": {"score": 80, "weight": 0.10}
  },
  "ai_detection": {
    "ai_probability": 0.15,
    "is_ai_generated": false,
    "ai_flavor_score": 38,
    "ai_flavor_level": "轻度疑似AI",
    "confidence_label": "高度可信原创",
    "dimensions": {
      "text_statistics": {"score": 75},
      "perplexity": {"score": 80},
      "vocabulary_richness": {"score": 72},
      "style_consistency": {"score": 68},
      "semantic_coherence": {"score": 85},
      "special_patterns": {"score": 95, "exemption_type": "classical_poetry"},
      "paragraph_uniformity": {"score": 70},
      "bullshit_ratio": {"score": 85},
      "template_patterns": {"score": 90},
      "human_markers": {"score": 80}
    },
    "ai_flavor_warnings": [
      "段落长度高度一致，AI味特征明显",
      "缺少人类真实表达痕迹"
    ]
  },
  "detailed_analysis": {
    "spoiler_warnings": [],
    "genre_specific": {...}
  },
  "timestamp": "2026-04-08T10:00:00Z"
}
```

### Markdown 用户报告

```markdown
# 文章品鉴报告

## 基本信息
- **标题**: 技术架构设计原则
- **类型**: 技术文章 (置信度: 92%)
- **评分**: 85分 (A级)

## 综合评价
强烈推荐！内容扎实，适合认真阅读

**目标读者**: 初中级开发者
**预计阅读时间**: 10分钟

## 维度评分
| 维度 | 得分 | 权重 |
|------|------|------|
| 技术深度 | 88 | 30% |
| 结构清晰度 | 85 | 25% |
| 实用性 | 82 | 20% |
| 原创性 | 78 | 15% |
| 可读性 | 80 | 10% |

## AI检测结果
- **AI生成概率**: 15%
- **AI味评分**: 38 (轻度疑似AI)
- **结论**: 高度可信原创

### AI味警告
- 段落长度高度一致，AI味特征明显
- 缺少人类真实表达痕迹

## 阅读建议
- 适合专注阅读、深度学习
- 核心价值: 深入浅出的架构设计、实操性强
```

---

## Skill 结构

```
article-taster/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── __init__.py
│   ├── main.py                 # 主入口
│   ├── article_classifier.py   # M1: 类型识别
│   ├── tech_analyzer.py        # M2-T: 技术文章分析
│   ├── creative_analyzer.py    # M2-C: 情感/散文分析
│   ├── novel_analyzer.py       # M2-N: 小说分析 (无剧透)
│   ├── ai_detector.py          # M3: AI生成检测
│   ├── scorer.py               # M4: 综合评分
│   └── report_generator.py     # 报告生成
├── config/
│   ├── scoring_weights.json    # 评分权重
│   ├── type_keywords.json      # 类型关键词
│   ├── ai_patterns.json        # AI检测模式
│   └── exemption_rules.json    # 原创豁免规则
├── references/
│   ├── scoring_methodology.md  # 评分方法论
│   └── spoiler_free_principles.md # 无剧透分析原则
├── requirements.txt
└── README.md
```

---

## 使用方式

```bash
# 分析单篇文章
python -m article_taster analyze --text "文章内容..."
python -m article_taster analyze --file article.txt

# 批量分析
python -m article_taster batch --dir ./articles

# 仅获取快速评分
python -m article_taster quick --text "文章内容..."

# 指定文章类型
python -m article_taster analyze --text "..." --type technical_article
```

---

## 依赖项

- Python 3.10+
- jieba (中文分词)
- scikit-learn (文本相似度)
- openai / anthropic (可选，LLM辅助评分)
