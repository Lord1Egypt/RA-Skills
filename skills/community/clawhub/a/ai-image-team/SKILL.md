---
skill:
  name: "🎨 AI 电商图片创作团队"
  version: "1.0.0"
  description: "3 人 Agent 团队协作，完成电商图片创作全流程（策划 + 执行 + 质检）"
  author: "AI Image Team"
  tags: ["ai", "image", "team", "ecommerce", "design", "jimeng", "liblib"]
  category: "image-generation"
  
  # CoClaw 集成配置
  coclaw:
    visible: true
    display_name: "🎨 AI 电商图片创作团队"
    icon: "users"
    order: 0
    featured: true
  
  # 能力声明
  capabilities:
    - "需求深度分析"
    - "创意简报生成"
    - "AI 图片生成（即梦/Liblib）"
    - "质量评估把关"
    - "迭代优化"
    - "电商场景适配"
    - "视频生成（预留）"
  
  # 输入输出
  input:
    type: "text"
    language: "zh-CN"
    format: "自然语言需求描述"
  
  output:
    type: "json"
    format: "交付结果"
    fields:
      - "status: 状态（delivered/need_revision/error）"
      - "images: 生成的图片列表"
      - "brief: 创意简报"
      - "review: 质检报告"
  
  # 团队成员
  team:
    members:
      - skill: "ai-planner"
        role: "🧠 策划师"
        description: "需求分析、创意简报"
      - skill: "ai-maker"
        role: "🎭 执行师"
        description: "图片生成"
      - skill: "ai-reviewer"
        role: "✅ 质检师"
        description: "质量把关"
  
  # 依赖
  dependencies:
    - "ai-planner"
    - "ai-maker"
    - "ai-reviewer"
  
  # 配置
  config:
    language: "zh-CN"
    quality_threshold: 0.8
    max_iterations: 3
    auto_mode: true
---

# 🎨 AI 电商图片创作团队

## 技能概述

协调 🧠 策划师、🎭 执行师、✅ 质检师 三个独立技能，形成完整的电商图片创作工作流。

## 团队架构

```
┌─────────────────────────────────────────────────────────────┐
│              🎨 AI 电商图片创作团队                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户输入                                                    │
│    ↓                                                        │
│  ┌───────────────┐                                          │
│  │ 🧠 策划师      │ skills/ai-planner/                       │
│  │ (需求分析)     │                                          │
│  └───────┬───────┘                                          │
│          │ 创意简报                                          │
│          ↓                                                  │
│  ┌───────────────┐                                          │
│  │ 🎭 执行师      │ skills/ai-maker/                         │
│  │ (图片生成)     │                                          │
│  └───────┬───────┘                                          │
│          │ 初稿图片                                          │
│          ↓                                                  │
│  ┌───────────────┐                                          │
│  │ ✅ 质检师      │ skills/ai-reviewer/                      │
│  │ (质量把关)     │                                          │
│  └───────┬───────┘                                          │
│          │                                                  │
│          ↓                                                  │
│  ┌───────────────┐                                          │
│  │ 📤 交付        │                                          │
│  └───────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 成员技能

| Agent | 技能路径 | 职责 |
|-------|----------|------|
| 🧠 策划师 | `skills/ai-planner/` | 需求分析、创意简报、Prompt 优化 |
| 🎭 执行师 | `skills/ai-maker/` | 调用工具生成图片 |
| ✅ 质检师 | `skills/ai-reviewer/` | 质量评估、迭代建议 |

## 工作流

### 标准流程
1. 用户输入中文需求
2. 策划师分析 → 创意简报
3. 执行师生成 → 1-4 张初稿
4. 质检师把关 → 质检报告
5. 判定：
   - ✅ 通过 → 交付
   - ⚠️ 微调 → 执行师调整后交付
   - ❌ 返工 → 策划师重新规划

### 迭代流程
```
质检不通过
    ↓
┌───────────────┐
│ 小问题？       │
└───────┬───────┘
    ├─ 是 → 执行师微调 → 再次质检
    └─ 否 → 策划师重新规划 → 重新生成
```

## 使用方法

### 在 CoClaw 中使用
```
/ai-image-team 帮我生成一张电商海报，产品是新款运动鞋，风格科技感
```

### 自然语言（推荐）
```
帮我生成一张电商海报，产品是新款运动鞋，风格科技感
```

### 指定工具
```
用即梦生成一张食品海报，要突出食欲感
```

### 详细需求
```
我需要一张淘宝主图，产品是女士连衣裙，白色雪纺材质，
风格简约优雅，目标人群是 25-35 岁职场女性
```

## 配置

### 启用/禁用成员
编辑 `config/team_config.json`：
```json
{
  "members": {
    "planner": {"enabled": true, "skill": "ai-planner"},
    "maker": {"enabled": true, "skill": "ai-maker"},
    "reviewer": {"enabled": true, "skill": "ai-reviewer"}
  }
}
```

### 质量阈值
```json
{
  "quality_threshold": 0.8,
  "max_iterations": 3
}
```

## 扩展

### 添加新成员
1. 创建新技能目录
2. 在 `config/team_config.json` 注册
3. 在 `agent.py` 中集成

### 添加新工具
在执行师技能中添加：
- `skills/ai-maker/tools/新工具.py`
- 在 `config/tools_config.json` 注册

## 文件结构

```
skills/ai-image-team/
├── SKILL.md                      # 技能说明（本文件）
├── README.md                     # 使用说明
├── agent.py                      # 团队协调器
├── config/
│   └── team_config.json          # 团队配置
└── memory/
    └── project_history.md        # 项目历史
```

## 独立技能

每个成员都是独立技能，可单独使用：

- 🧠 `openclaw skills run ai-planner --input "分析需求：..."`
- 🎭 `openclaw skills run ai-maker --input "生成图片：..."`
- ✅ `openclaw skills run ai-reviewer --input "质检图片：..."`

## 协作模式

### 全自动模式（默认）
用户输入 → 团队自动完成全流程 → 交付

### 手动确认模式
每步完成后等待用户确认再继续

### 单成员模式
单独调用某个成员技能

## 使用示例

| 场景 | 输入示例 |
|------|----------|
| 淘宝主图 | `帮我生成一张淘宝主图，产品是白色运动鞋，背景干净` |
| 食品海报 | `用即梦生成一张巧克力海报，要突出食欲感和高级感` |
| 服装详情页 | `需要一套连衣裙详情页配图，展示面料细节和上身效果` |
| 数码产品 | `生成一张蓝牙耳机主图，科技感，用于京东店铺` |
