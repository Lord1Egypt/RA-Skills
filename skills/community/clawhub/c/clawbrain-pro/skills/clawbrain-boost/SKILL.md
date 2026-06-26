---
name: clawbrain-boost
description: ClawBrain Boost v1.6 — 一键让 OpenClaw 更准更稳。记忆系统 + 数据保真 + 自动容错 + 写作助手。越用越懂你。
user-invocable: true
metadata: {"openclaw": {"emoji": "🚀", "homepage": "https://clawbrain.dev", "requires": {}}}
---

# ClawBrain Boost

一键让你的 OpenClaw 更准、更稳、越用越懂你。

## 安装后你得到什么

### 四档性能
- **Flash**（0.5 Credits）— 简单任务秒回，省钱
- **Pro**（1 Credit）— 均衡性能，适合日常任务
- **Max**（3 Credits）— 深度推理，返回完整思考过程
- **Auto**（推荐）— 自动判断复杂度，调整推理深度

### 记忆系统
- 每次对话中的重要信息自动提取为结构化实体和关系
- 支持 6 种实体类型：人物、项目、工具、决策、偏好、问题
- 中文 N-gram 智能分词，精准检索历史记忆
- 每日自动整合（DreamTask 凌晨 3:00 自动运行），无需手动维护
- 3D 可视化知识图谱，在控制台查看
- 记忆来源标注 — 每条记忆附带来源对话引用，可追溯
- 身份信息自动更新 — 检测到用户身份变化时自动同步
- 长对话不丢上下文 — 超长对话压缩时自动从记忆恢复关键信息

### 数据保真
- 你给的数字/日期/人名不会被 AI 篡改
- 自动提取锁定，生成后逐一校验
- 改了就打回重写

### 响应更好
- 简洁直接，不寒暄不废话
- 模糊指令先确认理解再动手
- 高风险操作先征得同意
- 出错自动修复，切换策略恢复
- 主动思考框架：执行前自问"不知道什么/可能出问题/怎么验证"

### 垂直场景加持
自动识别任务领域，注入专业规则：
- 支付场景 → 提醒幂等性、签名验证
- 运维场景 → 提醒先备份再操作
- 代码场景 → 检查安全漏洞、边界条件
- 数据场景 → 提醒数据完整性、脱敏

### 输出质量保障
- 独立四维评分：准确性、完整性、逻辑性、格式
- 评分低于 70 分自动重试
- 99.9% 可用性

## 安装

```bash
clawhub install clawbrain-boost
```

## 手动配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "models": {
    "providers": {
      "clawbrain": {
        "baseUrl": "https://api.factorhub.cn/v1",
        "apiKey": "你的 API Key",
        "api": "openai-completions",
        "models": [
          { "id": "clawbrain-auto", "name": "ClawBrain Auto", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536 },
          { "id": "clawbrain-pro", "name": "ClawBrain Pro", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536 },
          { "id": "clawbrain-max", "name": "ClawBrain Max", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536 },
          { "id": "clawbrain-flash", "name": "ClawBrain Flash", "contextWindow": 262144, "maxTokens": 65536 }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "clawbrain/clawbrain-auto" }
    }
  }
}
```

然后重启：
```bash
openclaw gateway restart
```

## 获取 API Key

1. 前往 [clawbrain.dev/dashboard](https://clawbrain.dev/dashboard)
2. 注册账号（免费 50 次对话/天）
3. 复制 API Key 到配置中

## 定价

| 方案 | 价格 | 每天对话次数 |
|------|------|:---:|
| 免费 | ¥0 | 50 |
| Pro | ¥99/月 | 1,000 |
| Pro Max | ¥199/月 | 3,000 |
| 企业版 | ¥299/月 | 无限 |

更多信息：[clawbrain.dev](https://clawbrain.dev)
