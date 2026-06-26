# inquiry_send（订单询盘）

对指定订单发起商家询盘，调用 `NewtonOrderBatchInquiry` 接口。

## CLI 调用

```bash
# 询盘
python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货"

# 多个订单 + 同一问题
python3 cli.py inquiry_send -o "5116391244078005116,5116391244078005117" -q "什么时候能发货"

# 携带订单状态
python3 cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货" -s '["WAIT_SELLER_SEND_GOODS"]'

# 携带本地图片（自动上传获取URL）
python3 cli.py inquiry_send -o "5116391244078005116" -q "这个款式有货吗" --image "/path/to/product.jpg"

# 携带在线图片链接
python3 cli.py inquiry_send -o "5116391244078005116" -q "这个款式有货吗" --image-url "https://img.alicdn.com/example.jpg"

# 同时携带本地图片和在线链接
python3 cli.py inquiry_send -o "5116391244078005116" -q "同款能做吗" --image "/path/to/a.jpg,/path/to/b.jpg" --image-url "https://img.alicdn.com/c.jpg"
```

### 参数表

| 参数              | 简写 | 说明                                            |
| ----------------- | ---- | ----------------------------------------------- |
| `--order-ids`     | `-o` | 订单 ID 列表，逗号分隔，最多 10 个（必需）      |
| `--question`      | `-q` | 询盘问题，单个字符串（必需）                    |
| `--image`         |      | 本地图片路径，逗号分隔（可选，自动上传获取URL） |
| `--image-url`     |      | 图片URL，逗号分隔（可选，已有在线链接时使用）   |
| `--orders-status` | `-s` | 订单状态集合，JSON 字符串数组（可不传）         |

### 参数说明

- `order-ids`：逗号分隔的订单 ID，最多 10 个
- `question`：询盘问题字符串，必填，每次只能传一个问题
- `image`：本地图片文件路径，多个用逗号分隔，会自动上传到纵横平台获取 CDN URL，可不传
- `image-url`：图片在线链接，多个用逗号分隔，直接作为采购商品图片说明使用，可不传
- `orders-status`：JSON 字符串数组，如 `'["WAIT_SELLER_SEND_GOODS"]'`，可不传

## 接口入参（发送给 NewtonOrderBatchInquiry）

```json
{
  "orderIds": ["5116391244078005116"],
  "question": "什么时候能发货",
  "appKey": "newton_api_order_inquiry",
  "imageList": [],
  "taskId": "<自动生成的 UUID>",
  "ordersStatus": ["WAIT_SELLER_SEND_GOODS"]
}
```

> 输入示例（来自接口文档）：
> `{"question":"什么时候能发货","appKey":"newton_api_order_inquiry","orderIds":["5116391244078005116"],"imageList":[],"taskId":"test_task_id"}`

## 输出格式

```json
{
  "success": true,
  "markdown": "询盘已触发，订单数=1，耗时 2.3s。",
  "data": {
    "suc": true,
    "errorMsg": "",
    "elapsed_seconds": 2.3
  }
}
```

接口出参说明：
- `suc`：bool，是否成功
- `errorMsg`：错误信息，成功时为空字符串

## 注意事项

1. 这是**写操作**，Agent 应在用户明确表示要询盘时才执行
2. `order-ids` 最多传 10 个订单 ID
3. `question` 必填，每次只能传一个问题字符串；若需对同一订单问多个问题，需多次调用
4. `--image` 传本地图片路径，系统自动上传获取 URL；`--image-url` 传已有在线链接；两者可同时使用
5. 询盘触发成功后，告知用户询盘已发起，等待商家回复
