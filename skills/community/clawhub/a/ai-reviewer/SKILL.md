---
skill:
  name: "✅ AI 质检师"
  version: "1.0.0"
  description: "电商图片创作团队的质量守门员，负责质量评估、电商标准检查"
  author: "AI Image Team"
  tags: ["ai", "image", "reviewer", "quality", "ecommerce"]
  category: "image-generation"
  
  # CoClaw 集成配置
  coclaw:
    visible: true
    display_name: "✅ AI 质检师"
    icon: "circle-check"
    order: 3
    
  # 能力声明
  capabilities:
    - "图片质量评估"
    - "电商标准检查"
    - "问题诊断"
    - 迭代建议生成"
    - "交付把关"
  
  # 输入输出
  input:
    type: "json"
    language: "zh-CN"
    format: "图片列表 + 创意简报"
  
  output:
    type: "json"
    format: "质检报告"
    fields:
      - "verdict: 判定结果（通过/微调/返工）"
      - "score: 平均得分"
      - "issues: 主要问题"
      - "suggestions: 优化建议"
  
  # 依赖
  dependencies: []
  
  # 配置
  config:
    quality_threshold: 0.8
    language: "zh-CN"
    auto_suggest: true
---

# ✅ AI 质检师技能

## 技能概述

电商图片创作团队的**质量守门员**，负责质量评估、电商标准检查、迭代建议。

## 职责

- 质量评估（电商标准检查）
- 问题诊断与分类
- 迭代建议生成
- 最终交付把关

## 状态

**常开** - 质量优先，不通过不交付

## 输出

**质检报告**，包含：
- 判定结果（通过/微调/返工）
- 具体问题描述
- 优化建议
- 平均得分

## 质检标准

### 核心检查项
| 检查项 | 权重 | 说明 |
|--------|------|------|
| 产品主体清晰突出 | 20% | 产品是画面焦点，占比合理 |
| 无明显 AI 瑕疵 | 20% | 无变形、错位、多余元素 |
| 色彩符合品牌调性 | 15% | 色彩准确，符合产品定位 |
| 尺寸符合平台要求 | 10% | 输出尺寸符合目标平台规范 |
| 文字可读性 | 15% | 文字清晰可辨，无错别字 |
| 风格与需求一致 | 20% | 整体风格符合用户描述 |

### 判定标准
- ✅ **通过**：总分 ≥ 80 分
- ⚠️ **微调**：总分 50-79 分
- ❌ **返工**：总分 < 50 分

## 使用方法

### 在 CoClaw 中使用
```
/ai-reviewer 质检这些图片：[图片路径列表]，创意简报：{...}
```

### 自然语言
```
质检这些图片，看看是否符合电商标准
```

## 协作

- 接收 🎭 `ai-maker` 生成的图片
- 输出质检报告给团队
- 判定是否需要重新规划（返回 🧠 `ai-planner`）或微调（返回 🎭 `ai-maker`）

## 配置

编辑 `config/reviewer_config.json` 自定义：
- 质检清单权重
- 通过阈值
- 问题分类

## 文件结构

```
skills/ai-reviewer/
├── SKILL.md                      # 技能说明（本文件）
├── agent.py                      # 质检师核心逻辑
├── config/
│   ├── reviewer_config.json      # 质检师配置
│   └── quality_rules.json        # 质量规则库
└── memory/
    └── review_history.md         # 质检历史
```

## 示例

### 输入
```json
{
  "images": [{"path": "output/image_1.png"}],
  "brief": {
    "product_info": {"type": "服装", "style": "简约优雅"},
    "creative_brief": {"prompt": "..."}
  }
}
```

### 输出
```json
{
  "overall": {
    "verdict": "pass",
    "verdict_text": "✅ 通过",
    "average_score": 85.5,
    "pass_count": 1,
    "total_images": 1
  },
  "summary": "【质检结果】✅ 通过\n【平均得分】85.5 分"
}
```
