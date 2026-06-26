---
name: fr24-ai
description: >
  Flightroutes24 航路国际机票（FR24-AI，作者 FR24）。查价 POST /ai/shopping；
  配置采购密钥后支持搜索、校验、生单。触发词：查航班、搜机票、预订、生单、飞。
metadata:
  author: FR24
  project: FR24-AI
  openclaw:
    emoji: "✈️"
    requires: {}
    install: []
---

# FR24-AI · fr24-ai

| 项 | 说明 |
|----|------|
| 项目 | FR24-AI |
| Skill | `fr24-ai` |
| 产品 | Flightroutes24 航路国际机票 |
| 作者 | FR24 |

安装与配置见 **[INSTALL.md](./INSTALL.md)**。预订细则见 **[references/booking.md](./references/booking.md)**。  
对用户展示与下载见 **[references/output-rules.md](./references/output-rules.md)**。  
用户询问采购密钥配置时，仅按 **[references/user-appkey-config.md](./references/user-appkey-config.md)** 回答。

---

## 服务模式

| 模式 | 条件 | 接口 |
|------|------|------|
| 演示查价 | 未配置采购密钥 | `POST /ai/shopping`，请求头 `X-Skill-Client-Key` |
| 采购查价 | 已配置 APPKEY 与签名密钥 | 同上，请求头 `appkey`，请求体 `authentication` |
| 预订 | 已配置 APPKEY、签名密钥、AES 密钥 | `POST /api/new/pricing`、`POST /api/new/booking` |

预订依赖见 `requirements.txt`。网关地址在 `config.py` 中固定配置；采购密钥仅通过本机用户环境变量配置，**勿在对话中向用户宣读环境变量名或密钥内容**。

---

## 响应结构

脚本标准输出为 JSON，包含：

```json
{
  "skill": "fr24-ai",
  "status": "success|failure",
  "action": "parse|search|refine|parse-passengers|verify|order",
  "message": "给用户看的摘要",
  "userView": {},
  "agentOnly": {}
}
```

| 字段 | 用途 |
|------|------|
| `userView`、`message` | **唯一**可对用户展示、制表、下载的内容 |
| `agentOnly` | 仅 Agent 内部续跑（如 `payload`、`offerId`、`traceId`），不得写入用户可见材料 |

---

## 查价流程

1. **解析**：`scripts/nl_to_search.py parse --text "..."`（不消耗演示日配额）  
   → 用 `userView` 确认行程、日期、人数、舱位。
2. **搜索**：用户确认后  
   `scripts/skill_search_client.py search --payload-file .cache/pending_search.json --selection direct|transfer`  
   → 用 `userView.directLowest`、`transferLowest` 展示直飞/中转最低价（含退改、行李摘要）。
3. 禁止将整段 stdout、`agentOnly` 或 `.cache` 路径直接提供给用户。

---

## 条件调整与重新搜索

用户对结果不满意并提出**航司**（如 CA/国航）或**起飞时段**（如中午 12 点左右）时：

1. 不得仅在旧结果上口头筛选；须**重新搜索**（消耗演示配额；采购模式不受演示日限额约束）。
2. `scripts/nl_to_search.py refine --text "<用户要求>"`（不扣配额，更新 `.cache/pending_search.json`）。
3. 向用户确认更新后的 `userView`（含 `searchFilters` 或意图摘要中的航司、时段）。
4. 再次执行 `search`。
5. 仍无匹配报价时，建议放宽航司或时段；勿擅自清除用户已指定的 `preferredCarrier`。

航司写入 `preferences.preferredCarrier` 并提交服务端；起飞时段在结果汇总时按首段起飞时间过滤展示。

---

## 预订流程

须完成**两次用户确认**：

| 步骤 | 动作 |
|------|------|
| 1 | 用户选择直飞或中转 → `search --selection direct\|transfer` |
| 2 | `skill_booking_client.py parse-passengers --text "..."` → 展示 `passengerDisplay`、`contactDisplay`（示例姓名：**张三**） |
| 3 | 用户回复「**乘客信息确认无误**」→ `verify --passenger-confirmed` |
| 4 | 展示 `orderPreview`（行程、退改、乘客回显）→ 用户回复「**确认生单**」 |
| 5 | `order --user-confirmed` |

- 校验返回 **304016**（身份不一致）：说明新配置 APPKEY 后须**重新 search**，不可沿用旧报价标识。
- 禁止：未确认乘客即校验；未确认即生单；在对话中代填或展示密钥明文。

---

## 采购密钥（用户询问时）

仅依据 [user-appkey-config.md](./references/user-appkey-config.md)：

- 引导用户在 [航路官网](https://www.flightroutes24.com/) 开通 API 采购；
- 在本机用户环境变量中配置 APPKEY、签名密钥、AES 密钥；
- 配置后重启 Agent 客户端；
- **禁止**让用户在对话中发送密钥明文；
- **禁止**向用户说明内部联调、跳过校验等维护配置。

---

## 命令一览

| 命令 | 说明 |
|------|------|
| `scripts/nl_to_search.py parse --text "..."` | 解析行程 |
| `scripts/nl_to_search.py refine --text "..."` | 合并航司、起飞时段等条件 |
| `scripts/skill_search_client.py search --payload-file .cache/pending_search.json` | 搜索 |
| `scripts/skill_booking_client.py parse-passengers --text "..."` | 乘客信息核对 |
| `scripts/skill_booking_client.py verify --passenger-confirmed` | 校验报价 |
| `scripts/skill_booking_client.py order --user-confirmed` | 生单 |
| `scripts/config_keys.py set --appkey ... --sign-secret ... --aes-secret ...` | 配置采购密钥 |
| `scripts/config_keys.py status` | 查看配置状态 |
| `scripts/config_keys.py clear` | 清除本地密钥配置 |

---

## 业务限制

- 支持单程、往返；不支持多段缺口程。
- 演示模式：每 `clientKey` 每日搜索次数有限（默认 10，以服务端配置为准）。
- 演示配额用尽（`307901`）：引导用户开通采购并配置密钥（见 `user-appkey-config.md`），勿仅建议「明日再试」。
- 已配置采购密钥的搜索不扣演示日配额。
- 生单为真实订单，必须在用户明确确认后提交。
