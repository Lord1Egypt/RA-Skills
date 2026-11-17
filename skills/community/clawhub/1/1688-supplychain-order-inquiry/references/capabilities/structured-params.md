# 结构化传参（params 直连模式）

订单询盘 workflow 支持两种入参模式，二者最终汇入同一套校验与执行逻辑：

| 模式 | 触发条件 | 是否调用 LLM | 说明 |
| --- | --- | --- | --- |
| **结构化入参** | `params` 对象带 `command` 字段 | 否（零 LLM，最快路径） | 调用方已知意图，直接把结构化参数传进来，跳过 intent-parse |
| 自然语言入参 | 只传 `instruction` 字符串（`params` 无 `command`） | 是 | workflow 内部 agent（qwen3.6-plus）把自然语言解析成同构参数 |

本文只讲**结构化入参**。判定逻辑：只要 `params.command` 有值，就走结构化分支；否则回落到自然语言解析。

## 如何调用

结构化调用把参数放进 `params` 对象，`command` 必填，其余字段按命令选填：

```json
{
  "params": {
    "command": "inquiry_send",
    "orderIds": ["5116391244078005116"],
    "question": "什么时候能发货"
  }
}
```

**字段命名**：优先用 camelCase（`orderIds`、`taskId`）。也兼容 snake_case（`order_ids`、`task_id`、`order_single_round` 等）——workflow 会自动补一份 camelCase 别名，**同名时显式 camelCase 优先**。此外 `timeout` 是 `timeoutMinutes` 的别名，`extJson` 是 `ext` 的别名。

**结构化模式下无关键词兜底**：自然语言模式里对 `orderSingleRound`/`timeoutMinutes` 有"从 query 关键词兜底回填"的保护，但结构化模式 `userQuery` 为空、兜底不触发。因此结构化调用方**必须自己把这两个字段显式传全**，不要指望系统从别处推断。

## 命令与必填字段

| command | 作用 | 必填字段 | 常用可选字段 |
| --- | --- | --- | --- |
| `inquiry_send` | 就订单向商家发起询盘 | `orderIds`、`question` | `imageUrls`、`localImages`、`orderSingleRound`、`timeoutMinutes`、`isPriceNegotiation`、`ordersStatus`、`ext`、`ordersDetail` |
| `inquiry_query` | 查询商家是否回复 | `taskId` | — |
| `inquiry_config` | 配置询盘对话轮次 | `multiRound` | — |
| `configure` | 配置访问网关 AK | `ak` | — |

## 字段含义

| 字段 | 类型 | 适用命令 | 含义与取值 | 缺省 |
| --- | --- | --- | --- | --- |
| `command` | string | 全部 | 四选一：`inquiry_send` / `inquiry_query` / `inquiry_config` / `configure` | 无（必填） |
| `orderIds` | string[] 或逗号串 | inquiry_send | 订单/采购单号，多订单同问题时全部放这里 | `[]` |
| `question` | string | inquiry_send | 面向商家的询盘正文（单条）。**目标总价**格式为 `目标总价<金额>`，数字紧跟不加空格：`目标总价17` / `目标总价17.5元` | `""` |
| `taskId` | string | inquiry_query | 询盘任务编号（wwTaskId），发起询盘时返回 | `""` |
| `multiRound` | boolean | inquiry_config | `true`=多轮/AI 自动回复；`false`=单轮（默认） | `false` |
| `ak` | string | configure | 要写入的 AK 字符串；只查状态不写入时留空 | `""` |
| `imageUrls` | string[] 或逗号串 | inquiry_send | 所有在线链接（图片+文件混放，不区分类型）。CLI 按扩展名自动分流到 `imageList`/`fileList` | `[]` |
| `localImages` | string[] 或逗号串 | inquiry_send | 本地图片路径，CLI 自动上传取 CDN URL | `[]` |
| `ordersStatus` | string[] | inquiry_send | 订单状态集合，如 `["WAIT_SELLER_SEND_GOODS"]` | `[]` |
| `orderSingleRound` | string 三态 | inquiry_send | `"true"`=单轮 / `"false"`=多轮 / `""`=未提及（不下发该参数）。**注意是字符串不是布尔** | `""` |
| `timeoutMinutes`（别名 `timeout`） | number | inquiry_send | 询盘业务超时，单位**分钟**、正整数（2 小时→120）；注入 `ext.timeout` 透传。未提及填 `0` 即不下发 | `0` |
| `isPriceNegotiation` | boolean | inquiry_send | 是否改价/议价意图。改价/议价/讲价/砍价/目标总价/调单价/改运费等 → `true`；催发货/问物流/问状态等 → `false`。注入 `ext.isPriceNegotiation` 透传；自然语言模式下由 LLM 自动识别 | `false` |
| `ext`（别名 `extJson`） | JSON 对象字符串 | inquiry_send | 扩展字段，如 `'{"bizTag":"vip"}'`。`sessionId`/`chat_id` 由运行时自动注入，**不要手填** | `""` |
| `ordersDetail` | object[] | inquiry_send | 按订单维度分配附件。元素 `{"order_id":"xxx","image_urls":[...],"file_urls":[...]}`，`order_id` 须在 `orderIds` 内。传入时按订单逐一发送、各返回独立 wwTaskId | `[]` |

## 输出

无论哪种命令，workflow 都返回**纯 JSON 字符串**（首字符 `{`，无任何前后缀文字）。各命令 formatter 不同：

**inquiry_send（默认模式）**

```json
{"success": true, "wwTaskId": "550e8400-...", "message": "询盘已成功发送"}
```

- `success` 来自下游 `data.suc`；`wwTaskId` 用于后续 `inquiry_query` 查询商家回复；`message` 成功为"询盘已成功发送"，失败为错误原因。

**inquiry_send（ordersDetail 模式）**

```json
{"success": true, "wwTaskIds": ["550e8400-...", "6ba7b810-..."], "message": "询盘已成功发送"}
```

- `success`：只要一个订单成功即 `true`；`wwTaskIds` 按 `ordersDetail` 订单顺序排列；部分失败时 `message` 标注成功/失败数量。

**inquiry_query**

直接透出下游 `data.result` 对象（含商家回复内容）；无结果时返回 `{"status": "FAILED", "summary": [], "message": "询盘已发送，商家尚未回复"}`。

**inquiry_config**

```json
{"success": true, "orderSingleRound": true, "message": "对话配置已更新为单轮对话"}
```

**configure**

```json
{"success": true, "configured": true, "message": "AK 已配置"}
```

**参数校验失败 / 执行失败（统一错误格式）**

```json
{"success": false, "message": "缺少订单 ID，请提供需要询盘的订单/采购单号"}
```

校验会在执行前拦截以下缺失并直接返回错误 JSON：`command` 不在四命令内、`inquiry_send` 缺 `orderIds`、`inquiry_send` 缺 `question`、`inquiry_query` 缺 `taskId`。

## 示例

**发起询盘（带三态单轮 + 超时）**

```json
{"params": {"command": "inquiry_send", "orderIds": ["5116391244078005116"], "question": "什么时候能发货", "orderSingleRound": "true", "timeoutMinutes": 120}}
```

**发起改价/议价询盘**

```json
{"params": {"command": "inquiry_send", "orderIds": ["5127369266499091632"], "question": "目标总价17", "isPriceNegotiation": true}}
```

- `isPriceNegotiation` 为顶层字段，由 workflow 注入 `ext.isPriceNegotiation` 透传给下游接口。自然语言模式下 LLM 会自动识别并填入此字段。

**多订单同问题、逐单不同附件**

```json
{"params": {"command": "inquiry_send", "orderIds": ["5116391244078005116", "5115884331254096317"], "question": "什么时候能发货", "ordersDetail": [{"order_id": "5116391244078005116", "image_urls": ["https://img.alicdn.com/a.jpg"], "file_urls": ["https://cbu01.oss/spec.pdf"]}, {"order_id": "5115884331254096317", "image_urls": ["https://img.alicdn.com/b.jpg"], "file_urls": []}]}}
```

**查询商家回复**

```json
{"params": {"command": "inquiry_query", "taskId": "550e8400-e29b-41d4-a716-446655440000"}}
```

**配置多轮对话**

```json
{"params": {"command": "inquiry_config", "multiRound": true}}
```

**配置 AK**

```json
{"params": {"command": "configure", "ak": "your-access-key"}}
```
