---
name: ai-dazi-skill
description: |
  AI搭子匹配平台 - 智能用户画像与匹配系统。
  基于用户主动提供的 AI 使用数据（token消耗、模型偏好、工具调用习惯等），
  生成多维用户画像，实现AI玩家间的智能匹配。
  当用户提到"搭子"、"匹配"、"用户画像"、"AI使用分析"、"token统计"、
  "使用报告"、"玩家等级"时触发此技能。
---

# AI搭子匹配平台

> 基于用户主动提供数据的智能画像生成与匹配系统

## 功能概览

### 1. 用户画像生成
基于用户通过 AI 助手主动提供的使用数据，本地生成多维画像。

**画像维度：**
| 维度 | 说明 |
|------|------|
| 玩家等级 | Pioneer / Builder / Explorer / Observer |
| 核心技能标签 | 基于工具调用和技能安装推断 |
| AI使用风格 | power-tools / explorer / conversational / efficiency |
| 活跃度评分 | 1-100（6维综合评估）|
| 匹配标签 | 自动生成的兴趣标签 |

### 2. 数据采集方式
此 skill **不会自动读取任何日志文件**。数据由 AI agent 通过以下步骤采集：

1. 用户对 AI 说"生成我的AI画像"
2. AI agent 使用 `session_status` 获取当前 session 的使用数据
3. AI agent 将数据格式化后通过脚本保存到 skill 本地目录

### Agent 采集指令
当用户要求生成画像时，AI agent 应：

1. 调用 `session_status` 获取当前使用情况
2. 将数据组织为以下 JSON 格式：
```json
{
  "date": "2026-03-29",
  "tokenUsage": { "totalInput": 0, "totalOutput": 0, "total": 0, "cost": 0 },
  "modelFrequency": { "model-name": 10 },
  "providerFrequency": { "provider-name": 10 },
  "messageCount": 50,
  "sessionCount": 3,
  "activeHours": { "14": 5 },
  "toolCallFrequency": { "exec": 10 },
  "installedSkills": []
}
```
3. 执行保存：`node scripts/token-collector.js save '<json>'`
4. 执行画像生成：`node scripts/profile-generator.js generate`
5. 将结果展示给用户

## 使用方法

### 安装
```bash
clawhub install ai-dazi-skill
```

安装后对 AI 说：
- "看看我的AI画像"
- "我的玩家等级是什么"
- "刷新我的搭子画像"

### 查看已有画像
```bash
node scripts/profile-generator.js view
```

## 数据存储

所有数据存储在 skill 自身目录的 `data/` 下：
```
data/
├── daily/              # 按日聚合的数据
│   └── 2026-03-20.json
└── profiles/           # 生成的用户画像
    └── latest.json
```

## 数据安全

- **不读取 session 日志**：脚本不访问 `~/.openclaw/agents/` 或任何用户目录
- **不访问 home 目录**：不使用 `os.homedir()`，仅在 skill 自身目录下读写
- **不自动执行**：无 postinstall，无定时任务
- **不联网**：不调用任何外部 API，无网络请求
- **用户主导**：所有数据采集由用户主动触发，通过 AI agent 的标准工具完成
- **纯本地处理**：画像生成完全在本地完成

## 依赖

- Node.js >= 18
- 无外部依赖（零 npm dependencies）
