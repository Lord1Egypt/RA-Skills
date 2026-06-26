---
skill:
  name: "🎭 AI 执行师"
  version: "1.0.0"
  description: "电商图片创作团队的双手，负责调用 AI 工具生成图片"
  author: "AI Image Team"
  tags: ["ai", "image", "maker", "generator", "jimeng", "liblib"]
  category: "image-generation"
  
  # CoClaw 集成配置
  coclaw:
    visible: true
    display_name: "🎭 AI 执行师"
    icon: "palette"
    order: 2
    
  # 能力声明
  capabilities:
    - "即梦图片生成"
    - "LiblibAI 图片生成"
    - "多方案生成"
    - "参数调优"
    - "ControlNet 控制"
    - "视频生成（预留）"
  
  # 输入输出
  input:
    type: "text"
    language: "zh-CN"
    format: "创意简报或自然语言描述"
  
  output:
    type: "json"
    format: "生成结果"
    fields:
      - "images: 生成的图片列表"
      - "tool: 使用的工具"
      - "model_used: 使用的模型"
      - "params: 生成参数记录"
  
  # 依赖
  dependencies: []
  
  # 配置
  config:
    default_tool: "jimeng"
    fallback_enabled: true
    max_quantity: 4
---

# 🎭 AI 执行师技能

## 技能概述

电商图片创作团队的**双手**，负责调用 AI 工具生成图片、参数调优、多方案生成。

## 职责

- 接收策划师的创意简报
- 调用 AI 工具生成图片（即梦/LiblibAI）
- 参数调优与多方案生成
- 记录生成参数（便于复现/迭代）

## 输出

- 1-4 张初稿图片
- 生成参数记录

## 工具池

### 当前工具
| 工具 | 擅长 | 配置 |
|------|------|------|
| 即梦 (Jimeng) | 海报、创意图、营销图 | `config/tools_config.json` |
| LiblibAI | 产品精修、ControlNet | `config/tools_config.json` |

### 预留工具
- 即梦视频（视频生成）
- 可灵 Kling（视频生成）
- 海螺 Hailuo（视频生成）

## 使用方法

### 在 CoClaw 中使用
```
/ai-maker 用即梦生成一张海报，产品是新款运动鞋，风格科技感
```

### 自然语言
```
用即梦生成一张海报，产品是新款运动鞋
```

### 根据创意简报生成
```
执行生成，创意简报：{prompt: "...", tool: "liblib", quantity: 2}
```

## 协作

- 接收 🧠 `ai-planner` 的创意简报
- 输出图片给 ✅ `ai-reviewer` 质检

## 配置

编辑 `config/tools_config.json`：
- 启用/禁用工具
- 添加工具
- 配置默认参数

## 文件结构

```
skills/ai-maker/
├── SKILL.md                      # 技能说明（本文件）
├── agent.py                      # 执行师核心逻辑
├── tools/
│   ├── jimeng_tool.py            # 即梦工具封装
│   ├── liblib_tool.py            # Liblib 工具封装
│   └── video_tool_stub.py        # 视频工具占位
├── config/
│   └── tools_config.json         # 工具配置
└── memory/
    └── generation_history.md     # 生成历史
```

## 示例

### 输入
```
用即梦生成一张电商海报，产品是新款运动鞋，风格科技感，生成 2 张
```

### 输出
```json
{
  "tool": "jimeng",
  "tool_name": "即梦",
  "status": "success",
  "images": [
    {"path": "output/jimeng/20260331_165600/image_1.png"},
    {"path": "output/jimeng/20260331_165600/image_2.png"}
  ],
  "message": "已使用即梦生成 2 张图片"
}
```
