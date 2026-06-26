# AIsa 供应商中文指南

## 简介

AIsa 提供与 OpenAI 风格兼容的模型网关，可用于 OpenClaw 及其他兼容运行时。

本指南只聚焦三件事：

- 如何提供 `AISA_API_KEY`
- 如何把运行时指向 `https://api.aisa.one/v1`
- 如何验证模型 ID、价格、可用性与数据边界

所有价格、模型目录、区域、合作关系、保留策略与隐私条款都属于时间敏感信息。发生产业、合规或高敏感数据场景前，请先以 AIsa 官方文档和当前控制台信息为准。

## 快速配置

### 方法一：环境变量

```bash
export AISA_API_KEY="你的密钥"
```

### 方法二：交互式引导

```bash
openclaw onboard --auth-choice aisa-api-key
```

### 方法三：手动配置

如果你的运行时不支持自动发现，可在配置中显式声明 AIsa provider：

```json
{
  "models": {
    "providers": {
      "aisa": {
        "baseUrl": "https://api.aisa.one/v1",
        "apiKey": "${AISA_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "aisa/qwen3-max",
            "name": "Qwen3 Max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false
          }
        ]
      }
    }
  }
}
```

## 使用前先确认的数据边界

- 你的运行时会把请求发送到 `https://api.aisa.one/v1`
- `AISA_API_KEY` 是敏感凭据，应通过环境变量、交互式引导或安全配置存储提供
- 对价格、模型可用性、保留策略、路由策略、合作关系等外部信息，请在发送敏感数据前重新核实

## 常用模型示例

下表只给出示例模型，实际可用列表请以当前模型目录为准。

| 模型 | 示例 ID | 适用场景 |
|------|---------|----------|
| Qwen3 Max | `aisa/qwen3-max` | 复杂推理、旗舰任务 |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | 主力生产模型 |
| Qwen MT Flash | `aisa/qwen-mt-flash` | 高频、轻量任务 |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | 成本敏感的推理任务 |
| Kimi K2.5 | `aisa/kimi-k2.5` | 中文推理，需注意温度限制 |

### Kimi K2.5 说明

- 若 AIsa 当前仍暴露 `aisa/kimi-k2.5`，请先确认模型目录中确实存在该 ID
- 该模型曾出现只接受 `temperature=1.0` 的情况；如果请求报错，请回退到模型默认值或做模型级覆盖
- 隐私、保留、价格和路由条款请始终以 AIsa 与对应模型供应商的最新公开说明为准

## 模型 ID 说明

AIsa 的部分模型会使用版本化 ID。若出现 `503 - No available channels` 或 `model not found`，优先检查 ID 是否过期。

| 常见名称 | 当前常见 ID | 备注 |
|---------|-------------|------|
| Qwen3 Max | `aisa/qwen3-max` | 直接可用 |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | 需要带版本后缀 |
| Qwen Flash | `aisa/qwen-mt-flash` | 不要误写成 `qwen3-flash` |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | 直接可用 |
| Kimi K2.5 | `aisa/kimi-k2.5` | 视当前目录与路由而定 |

## 获取 API Key

1. 访问 https://marketplace.aisa.one/
2. 注册并创建 API key
3. 通过环境变量或引导流程提供给运行时

## 故障排查

### `503 - No available channels`

- 先检查模型 ID 是否仍然有效
- 再确认账号权限、余额或当前路由状态

### 模型找不到

- 确认模型 ID 带有 `aisa/` 前缀
- 重新对照最新模型目录，不要假设旧 ID 仍可用

### API key 未生效

不要直接打印真实密钥。可以只检查变量是否存在：

```bash
if [ -n "${AISA_API_KEY:-}" ]; then
  echo "AISA_API_KEY is set"
else
  echo "AISA_API_KEY is missing"
fi
```

如果变量已设置但仍无法调用：

- 检查运行时是否读取当前 shell 的环境变量
- 检查 provider 配置是否引用了 `${AISA_API_KEY}`
- 重新运行引导：`openclaw onboard --auth-choice aisa-api-key`

### Kimi K2.5 温度错误

若出现 `invalid temperature`，请移除该模型的自定义温度，或显式设置为 `1.0`。

## 进一步核实

- AIsa 官网：https://aisa.one
- API 参考：https://aisa.one/docs/api-reference
- 定价页：https://marketplace.aisa.one/pricing
