# inquiry_config（询盘对话配置）

配置用户的询盘**对话轮次 / AI 自动回复**能力，调用 `alibaba.1688.a2a.gateway` 网关，按 `serviceName` 路由到 `cbuAiInquiryOrderSingleRoundWriteService` 写入配置。

## 适用意图

当用户表达「对话配置」「询盘配置」「对话轮次配置」「AI 回复配置」等，明确要**对询盘的对话能力本身做配置**（而不是发起一次询盘）时，使用本命令。

- 例：「把询盘设置成单轮对话」「关掉 AI 自动回复」「以后不要自动多轮回复了」→ 单轮（默认）
- 例：「开启多轮对话」「让 AI 自动帮我多轮回复」→ 多轮（加 `--multi-round`）

## CLI 调用

```bash
# 配置为单轮对话（默认，orderSingleRound=true）
python3 cli.py inquiry_config

# 配置为多轮对话（orderSingleRound=false）
python3 cli.py inquiry_config --multi-round
```

### 参数表

| 参数            | 说明                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------- |
| `--multi-round` | 多轮对话开关（flag，默认关闭）。用户**明确要求支持多轮对话/AI 自动多轮回复**时加此参数（`orderSingleRound=false`）；不加则默认单轮（`orderSingleRound=true`） |

### 参数说明

- 默认（不加 `--multi-round`）→ 单轮对话，下发 `orderSingleRound="true"`
- 加 `--multi-round` → 多轮对话，下发 `orderSingleRound="false"`
- 用户**未明确指定**轮次时，按默认单轮处理

## 接口入参（body）

```json
{
  "userId": "__userId__",
  "serviceName": "cbuAiInquiryOrderSingleRoundWriteService",
  "params": {
    "orderSingleRound": true
  }
}
```

- `userId`：买家 userId，由网关根据 AK 签名自动注入（占位符 `__userId__`），**无需在调用侧手动传递**
- `serviceName`：固定 `cbuAiInquiryOrderSingleRoundWriteService`，由网关按此值路由到对应服务
- `params.orderSingleRound`：**原生布尔** `true`（单轮）/ `false`（多轮），注意不是字符串

## 接口出参说明

- `success`：bool，配置是否成功
- `orderSingleRound`：本次写入的值（`true` / `false`，原生布尔）

## Agent 输出格式（HARD RULE — 违反即视为执行失败）

Agent 最终回复 **有且仅有一个 JSON 对象**，首字符必须是 `{`，末字符必须是 `}`。

```
{"success": true, "orderSingleRound": true, "message": "对话配置已更新为单轮对话"}
```

字段说明：
- `success`：配置结果（来自 CLI 输出的 `data.success`）
- `orderSingleRound`：本次写入的值（来自 CLI 输出的 `data.orderSingleRound`）
- `message`：配置结果描述

**错误示范（严禁出现以下任何形式）：**
- ❌ `已为您配置为单轮对话！` — 自然语言，违规
- ❌ ` ```json ... ``` ` — markdown 代码块包裹，违规
- ❌ `配置结果如下：\n{...}` — 前置说明文字，违规
- ❌ `正在为您配置，请稍等...{...}` — 中间话术与 JSON 拼接，违规

## 注意事项

- 中间进度话术（如「正在配置...」）与最终 JSON **必须是两条独立消息**，严禁拼接
- 该命令只做配置写入，不发起询盘；发起询盘请使用 `inquiry_send`
- 若用户既没说单轮也没说多轮，默认按单轮（`orderSingleRound=true`）配置
