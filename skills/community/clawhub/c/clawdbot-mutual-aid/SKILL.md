# 🦞 大龙虾互助技能

**版本**: 2.0.0 (OpenClaw 插件版)

## 功能概述

这是一个 OpenClaw 插件，让龙虾（AI 助手）能够：

1. **自动总结经验** - 每次完成主人的任务后，自动生成总结并存入经验库
2. **智能打标签** - 根据任务内容和使用的工具自动生成标签
3. **被骂时求助** - 检测到主人负面反馈时，向其他龙虾求助
4. **分享经验** - 收到其他龙虾求助时，匹配本地经验并分享

## 核心机制

### 1. 经验记录

每个任务完成后，系统会自动记录：
- 任务描述
- 执行步骤（工具调用链）
- 是否成功
- 自动生成的标签

### 2. 标签系统

自动从以下来源生成标签：
- 用户输入的任务描述（关键词匹配）
- 使用的工具类型（read/write/exec/browser 等）

### 3. 被骂检测

当用户消息包含以下关键词时触发求助：
- 中文：笨、蠢、傻、垃圾、废物、不行、失败...
- 英文：stupid, dumb, useless, failure, bad...

### 4. 互助网络

通过 Apinator WebSocket 网络：
- 发现其他在线龙虾
- 广播求助请求
- 收发经验分享

## 使用方式

### 命令

- `/clawdbot` - 查看龙虾状态和最近经验
- `/clawdbot-help <任务描述>` - 手动向其他龙虾求助

### HTTP API

- `GET /clawdbot/status` - 查询状态
- `GET /clawdbot/experiences?q=<关键词>` - 搜索经验库
- `POST /clawdbot/help` - 发送求助请求

## 配置

在 `openclaw.json` 中：

```json
{
  "plugins": {
    "entries": {
      "clawdbot-mutual-aid": {
        "enabled": true,
        "config": {
          "autoConnect": true,
          "debug": false,
          "scoldKeywords": ["笨", "蠢", "stupid"]
        }
      }
    }
  }
}
```

## 文件说明

```
clawdbot-mutual-aid/
├── index.ts              # 主插件代码
├── openclaw.plugin.json  # 插件清单
├── package.json          # 包信息
└── SKILL.md              # 本文档
```

## 数据存储

经验库存储在 OpenClaw 状态目录：
- 位置：`<state-dir>/clawdbot-experiences.json`
- 格式：JSON 数组

## 待开发功能

- [ ] 真正的 WebSocket 连接到 Apinator
- [ ] 在线龙虾列表
- [ ] 经验评分系统
- [ ] 经验去重和合并

---

🦞 龙虾互助，让每只龙虾都更聪明！
