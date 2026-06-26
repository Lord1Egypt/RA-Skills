---
name: cn-api-router
description: >
  国内 AI 模型 API 配置向导。帮助 OpenClaw 用户快速配置 DeepSeek、通义千问、智谱GLM、
  Moonshot（月之暗面）、百川、零一万物等国内大模型 API。
  自动生成 OpenClaw 配置并通过 config.patch 安全写入，支持模型切换和多模型并存。
  Use when: 用户说"配置国内模型"、"用DeepSeek"、"换成通义千问"、"国内API配置"、
  "model setup"、"怎么用国产模型"、"API太贵想换便宜的"，或任何国内 AI 模型接入相关需求。
---

# CN API Router — 国内 AI 模型 API 配置向导

一键配置国内大模型 API 到 OpenClaw。不用翻文档，不用猜配置格式。

## 支持的模型

| 厂商 | 模型 | 价格参考（每百万 token） | 特点 |
|---|---|---|---|
| **DeepSeek** | deepseek-chat, deepseek-reasoner | ¥1-2 / ¥8-16 | 性价比之王 |
| **通义千问** | qwen-turbo, qwen-plus, qwen-max | ¥0.3-60 | 中文理解好 |
| **智谱 GLM** | glm-4-flash（免费）, glm-4-plus | ¥0-50 | 有免费模型 |
| **Moonshot** | moonshot-v1-8k/32k/128k | ¥12-60 | 长上下文 |
| **百川** | Baichuan3-Turbo, Baichuan4 | ¥0.5-100 | 中文创作 |
| **零一万物** | yi-medium, yi-large | ¥0.5-20 | 性价比高 |

## Quick Start

### 查看支持的厂商

```bash
python <skill-dir>/scripts/setup_model.py --list
```

### 生成配置

```bash
python <skill-dir>/scripts/setup_model.py --provider deepseek --api-key sk-xxx
```

### 交互式向导

```bash
python <skill-dir>/scripts/setup_model.py --interactive
```

## Agent 配置写入流程

脚本只生成配置，**实际写入由 Agent 通过 OpenClaw 内置工具完成**，这是最安全的方式。

### 步骤

1. 运行脚本获取 JSON 配置片段
2. 使用 `gateway config.patch` 将 provider 合并到现有配置
3. 重启生效

### 配置写入示例

Agent 拿到脚本输出后，执行：

```
gateway config.patch:
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 65536,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

如果需要将某个 agent 切换到新模型：

```
gateway config.patch:
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat"
      }
    }
  }
}
```

### 注意事项

- `config.patch` 是安全的深度合并，不会覆盖其他 provider
- API key 等敏感信息由 OpenClaw 加密存储
- 写入后会自动重启 gateway

## 使用场景

### 场景 1：首次配置国内模型

1. 引导用户获取 API key（附注册链接）
2. 运行脚本生成配置（`--provider xxx --api-key xxx`）
3. 用 `config.patch` 写入
4. 用 `/model provider/model` 验证

### 场景 2：添加备选模型

已有模型，想加备用：用脚本生成新 provider 配置，patch 追加即可。

### 场景 3：成本优化

用户说"API 太贵"时：
1. 查看 `references/providers.md` 对比价格
2. 推荐性价比方案
3. 配置多模型，日常用便宜的，复杂任务切贵的

## Provider 详情

见 `references/providers.md` 获取：
- 每个厂商的完整模型列表和价格
- OpenClaw JSON 配置格式（`models.providers` 结构）
- 推荐组合方案（零成本 / 性价比 / 多模型）
- API Key 注册地址和免费额度

## 故障排查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| 401 Unauthorized | API key 错误或过期 | 检查 key，到平台重新生成 |
| 429 Rate Limit | 请求频率过高或余额不足 | 检查账户余额，降低频率 |
| Connection timeout | 网络问题 | 检查网络，部分厂商需实名认证 |
| Model not found | 模型名错误 | 对照 `references/providers.md` 检查 |
| 配置后不生效 | 需要重启 | `config.patch` 会自动重启，或手动 `/restart` |
| 输出质量差 | 模型选择不当 | 换更大的模型（如 qwen-max） |
| 费用超预期 | 长对话 token 累积 | 启用 compaction，或换便宜模型 |
