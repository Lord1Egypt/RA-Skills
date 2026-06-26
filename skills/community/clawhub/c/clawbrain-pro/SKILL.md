---
name: ClawBrain Pro
description: ClawBrain v1.6 — 更准、更稳、越用越懂你的大模型。记忆系统 + 数据保真 + 自动容错 + 输出验证。21 场景评测第一。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "homepage": "https://github.com/michaelfeng/clawbrain", "requires": {}}}
---

# ClawBrain Pro

给你的 OpenClaw 装上更准、更稳、越用越懂你的大脑。

## 它能帮你做什么

- **复杂任务自动规划**：你说一句话，它拆成步骤按顺序执行
- **智能适配**：自动判断任务类型，调整推理深度，给出最优回答
- **出错自动修复**：文件找不到自己去翻，命令出错换方法试，失败自动切换策略
- **做事做到底**：多步任务每一步都盯着，不半途而废
- **听得懂模糊的话**：说"帮我准备下"，它知道先查什么再做什么
- **结果自动验证**：独立四维评分（准确/完整/逻辑/格式），不合格就重来
- **记忆系统**：跨会话记住你的偏好、项目、决策，越用越懂你
- **数据保真**：你的数字/日期/人名不会被篡改，生成后逐一校验
- **记忆有来源**：清晰区分"你说过的原话"和"AI 归纳的摘要"
- **身份实时更新**：告诉 AI "我换工作了"，它马上更新
- **长对话不崩溃**：超长对话自动智能压缩而非报错
- **兼容 Claude Code**：支持 Anthropic Messages API（/v1/messages）

## 评测数据（21 场景实测）

| 能力 | ClawBrain Auto | ClawBrain Pro | 最好的通用模型 |
|------|:---:|:---:|:---:|
| 综合得分 | **90%** | 86% | 83% |
| 错误恢复 | **100%** | 100% | 80% |
| 模糊指令 | **100%** | 100% | 65% |
| 多步任务 | 80% | 80% | 80% |

## 接入方法

```json
{
  "models": {
    "providers": {
      "clawbrain": {
        "baseUrl": "https://api.factorhub.cn/v1",
        "apiKey": "你的 API Key",
        "api": "openai-completions",
        "models": [
          {"id": "clawbrain-auto", "name": "ClawBrain Auto", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536},
          {"id": "clawbrain-pro", "name": "ClawBrain Pro", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536},
          {"id": "clawbrain-max", "name": "ClawBrain Max", "input": ["text", "image"], "contextWindow": 262144, "maxTokens": 65536},
          {"id": "clawbrain-flash", "name": "ClawBrain Flash", "contextWindow": 262144, "maxTokens": 65536}
        ]
      }
    }
  },
  "agents": {"defaults": {"model": {"primary": "clawbrain/clawbrain-auto"}}}
}
```

然后 `openclaw gateway restart`。

## 其他工具

```bash
clawhub install clawbrain-boost            # 一键优化配置 + 记忆 + SOUL
```

获取 API Key：https://clawbrain.dev/dashboard
