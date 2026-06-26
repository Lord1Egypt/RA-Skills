---
skill:
  name: "🧠 AI 策划师"
  version: "1.0.0"
  description: "电商图片创作团队的大脑，负责需求分析、创意构思、Prompt 优化"
  author: "AI Image Team"
  tags: ["ai", "image", "planner", "ecommerce", "design"]
  category: "image-generation"
  
  # CoClaw 集成配置
  coclaw:
    visible: true
    display_name: "🧠 AI 策划师"
    icon: "brain"
    order: 1
    
  # 能力声明
  capabilities:
    - "需求深度分析"
    - "创意简报生成"
    - "Prompt 优化"
    - "工具推荐"
    - "电商场景识别"
  
  # 输入输出
  input:
    type: "text"
    language: "zh-CN"
    format: "自然语言需求描述"
  
  output:
    type: "json"
    format: "创意简报"
    fields:
      - "prompt: 精准中文 Prompt"
      - "negative_prompt: 负面提示词"
      - "recommended_tool: 推荐工具"
      - "quantity: 建议生成数量"
  
  # 依赖
  dependencies: []
  
  # 配置
  config:
    default_language: "zh-CN"
    auto_ask_clarification: true
    quality_threshold: 0.6
---

# 🧠 AI 策划师技能

## 技能概述

电商图片创作团队的**大脑**，负责需求深度分析、创意构思、风格定位、Prompt 优化。

## 职责

- 需求深度分析（产品类型、使用场景、目标人群、风格偏好）
- 创意构思与风格定位
- Prompt 优化（精准中文 Prompt + 负面提示词）
- 推荐工具选择（即梦/LiblibAI）
- 建议生成数量

## 输出

**创意简报**，包含：
- 精准中文 Prompt
- 负面提示词
- 推荐工具
- 建议生成数量
- 电商场景要点

## 电商能力

- 识别产品类型（服装/食品/数码/美妆/家居）
- 识别使用场景（主图/详情页/海报/社交媒体）
- 识别目标人群
- 匹配平台规范（淘宝/京东/抖音/微信）

## 使用方法

### 在 CoClaw 中使用
```
/ai-planner 帮我分析这个需求：我需要一张淘宝主图，产品是女士连衣裙，白色雪纺材质，风格简约优雅
```

### 自然语言
```
帮我分析这个需求：我需要一张淘宝主图，产品是女士连衣裙
```

## 协作

策划师输出的创意简报可传递给：
- 🎭 `ai-maker` - 执行图片生成
- ✅ `ai-reviewer` - 后续质量把关

## 配置

编辑 `config/planner_config.json` 自定义：
- 产品类型规则
- 平台规范
- Prompt 模板

## 文件结构

```
skills/ai-planner/
├── SKILL.md                      # 技能说明（本文件）
├── agent.py                      # 策划师核心逻辑
├── config/
│   ├── planner_config.json       # 策划师配置
│   └── ecommerce_rules.json      # 电商规则库
└── memory/
    └── brief_history.md          # 创意简报历史
```

## 示例

### 输入
```
我需要一张淘宝主图，产品是女士连衣裙，白色雪纺材质，风格简约优雅，目标人群是 25-35 岁职场女性
```

### 输出
```json
{
  "type": "brief",
  "product_info": {
    "type": "服装",
    "name": "女士连衣裙",
    "scenario": "主图",
    "platform": "淘宝"
  },
  "creative_brief": {
    "prompt": "女士连衣裙，白色雪纺材质，风格简约优雅，产品主体突出，背景干净简洁",
    "negative_prompt": "模糊，变形，低质量，背景杂乱",
    "recommended_tool": "liblib",
    "quantity": 2
  }
}
```
