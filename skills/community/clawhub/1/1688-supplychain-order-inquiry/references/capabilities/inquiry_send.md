# inquiry_send（订单询盘）

对指定订单发起商家询盘，调用 `alibaba.1688.newton.order.batch.inquiry` 接口。

## CLI 调用

```bash
# 基础询盘（多个订单用逗号分隔）
python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货"

# 携带附件：本地图片自动上传；在线链接（图片+文件混合）直接传 --image-url
python3 cli.py inquiry_send -o "5116391244078005116" -q "看下这个规格能不能做" \
  --image "/path/to/a.jpg" --image-url "https://img.alicdn.com/spec.jpg,https://cbu01.oss/spec.xls"

# 对话轮次（三态：用户明确要单轮传 true，明确要多轮传 false，未提及不传）
python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货" --order-single-round true

# 询盘超时（分钟）+ 额外扩展字段（两者均为用户明确提及才传）
python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货" --timeout 120 --ext '{"bizTag":"vip"}'

# 按订单维度分别指定附件（触发条件见参数表 orders-detail 行）
python3 cli.py inquiry_send -o "5116391244078005116,5115884331254096317" -q "什么时候能发货" \
  --orders-detail '[{"order_id":"5116391244078005116","image_urls":["https://img.alicdn.com/a.jpg"],"file_urls":["https://cbu01.oss/spec.pdf"]},{"order_id":"5115884331254096317","image_urls":["https://img.alicdn.com/b.jpg"],"file_urls":[]}]'
```

## 参数

| 参数              | 简写 | 必填 | 说明 |
| ----------------- | ---- | ---- | ---- |
| `--order-ids`     | `-o` | 是   | 订单 ID 列表，逗号分隔 |
| `--question`      | `-q` | 是   | 询盘问题，单个字符串（内部包装为 `questions` 列表下发） |
| `--image`         |      | 否   | 本地图片路径，逗号分隔，自动上传获取 CDN URL |
| `--image-url`     |      | 否   | 在线链接，逗号分隔。CLI 按扩展名自动分流：图片（`.jpg/.jpeg/.png/.gif/.webp/.bmp`）→ API `imageList`；非图片（`.xls/.pdf/.doc` 等）→ API `fileList`。Agent 把用户给的所有链接原样传入即可，**不要拼进 question，不必区分类型** |
| `--orders-status` | `-s` | 否   | 订单状态集合，JSON 字符串数组，如 `'["WAIT_SELLER_SEND_GOODS"]'` |
| `--order-single-round` | | 否 | 对话轮次开关，**三态**，下发原生 bool `orderSingleRound`。用户明确表达「不需要自动回复/不需要多轮/只要单轮」→ `true`；明确表达「需要自动回复/需要多轮/需要 AI 对话」→ `false`；**未提及 → 不带此参数**（不下发该字段） |
| `--ext`           |      | 否   | 扩展字段 map，JSON 字符串。`sessionId`、`chat_id` 由 CLI 自动从运行时环境变量（`NEWTON_SESSION_ID`、`NEWTON_REPLY_ID`）读取注入，缺失则不下发，**通常无需手写**；仅需额外/覆盖字段时显式传，显式值优先级更高（覆盖同名字段），合并后为空则不下发 |
| `--timeout`       |      | 否   | 询盘超时，单位**分钟**、正整数，注入 `ext.timeout` 透传。用户明确表达「设置询盘超时为 X 分钟/X 小时」时由 Agent 换算成分钟整数（2 小时→120）；未提及不传。这是业务层超时，与 HTTP 请求超时无关；优先级高于 `--ext` 中同名字段 |
| `--is-price-negotiation` | | 否 | 是否改价/议价意图，`true`/`false`，注入 `ext.isPriceNegotiation` 透传。由 workflow 意图解析层自动识别用户意图后传入（改价/议价/目标总价等 → `true`；催发货/问物流等 → `false`）；未提及不传 |
| `--orders-detail` |      | 否   | 按订单维度指定附件，JSON 数组。**触发条件（必须同时满足）**：①用户输入含"分别附"/"各配"/"每个订单配"/"各自附"等关键词；②逐订单列举了各自的图片/文件链接。元素格式 `{"order_id":"xxx","image_urls":[...],"file_urls":[...]}`，`order_id` 必须在 `--order-ids` 中存在，两个 url 列表可为空数组。传入时 CLI 按订单循环调用 gateway，每订单独立 `wwTaskId`，返回 `results` 列表；未传则走原单次调用逻辑 |

## 接口入参（发送给 alibaba.1688.newton.order.batch.inquiry）

```json
{
  "orderIds": ["5116391244078005116"],
  "questions": ["什么时候能发货"],
  "appKey": "newton_api_order_inquiry",
  "imageList": [],
  "fileList": ["https://xxx.oss/ImageOrder.xls"],
  "taskId": "<自动生成的 UUID>",
  "ordersStatus": ["WAIT_SELLER_SEND_GOODS"],
  "ext": {"sessionId": "newtoncloud_xxx", "chat_id": "reply_xxx", "timeout": 120, "isPriceNegotiation": true}
}
```

## 输出格式

### 默认模式

```json
{
  "success": true,
  "markdown": "询盘已触发，订单数=1，耗时 2.3s。询盘任务编号：550e8400-...，可凭此编号查询商家回复。",
  "data": {
    "suc": true,
    "errorMsg": "",
    "wwTaskId": "550e8400-e29b-41d4-a716-446655440000",
    "elapsed_seconds": 2.3
  }
}
```

`wwTaskId` 为本次询盘任务 ID，后续用 `inquiry_query -t <wwTaskId>` 查询商家回复，需原样填入最终输出 JSON。

### orders-detail 模式（传入 --orders-detail 时）

```json
{
  "success": true,
  "markdown": "询盘已触发，成功 2/2，耗时 4.5s",
  "data": {
    "results": [
      {"order_id": "5116391244078005116", "wwTaskId": "550e8400-...", "suc": true, "errorMsg": "", "elapsed_seconds": 2.1},
      {"order_id": "5115884331254096317", "wwTaskId": "6ba7b810-...", "suc": true, "errorMsg": "", "elapsed_seconds": 2.3}
    ],
    "success_count": 2,
    "fail_count": 0,
    "elapsed_seconds": 4.5
  }
}
```

## Agent 输出格式（HARD RULE — 违反即视为执行失败）

Agent 最终回复**有且仅有一个 JSON 对象**，首字符 `{`，末字符 `}`，不加任何前后置文字或 markdown 包裹。

### 默认模式

```
{"success": true, "wwTaskId": "550e8400-e29b-41d4-a716-446655440000", "message": "询盘已成功发送"}
```

- `success`：来自 CLI 输出的 `data.suc`
- `wwTaskId`：来自 `data.wwTaskId`，用户后续凭此查询商家回复
- `message`：成功为"询盘已成功发送"，失败为错误原因

### orders-detail 模式

```
{"success": true, "wwTaskIds": ["550e8400-...", "6ba7b810-..."], "message": "询盘已成功发送"}
```

- `success`：整体结果，只要有一个订单成功即为 `true`
- `wwTaskIds`：各订单任务编号列表（来自 `data.results[].wwTaskId`），按 `--orders-detail` 中订单顺序排列，用户后续凭各编号通过 `inquiry_query` 查询各自的商家回复
- `message`：全部成功为"询盘已成功发送"，部分失败时标注成功/失败数量

**错误示范（严禁）：**
- ❌ `已成功向商家发起询盘请求！` — 自然语言替代 JSON
- ❌ `正在向商家发起询盘，请稍等...{"success": true, ...}` — 中间话术与 JSON 拼在同一条消息（话术必须是执行前的独立消息）

## 注意事项

1. 这是**写操作**，用户明确表示要询盘时才执行
2. `ext` 与 body 顶层自动生成的 `taskId`（= `wwTaskId`）相互独立，互不影响
