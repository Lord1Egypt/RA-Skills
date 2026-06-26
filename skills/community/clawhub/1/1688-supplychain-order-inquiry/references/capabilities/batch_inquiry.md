# batch_inquiry - 批量订单询盘（并行）

## 说明

并行执行多个独立的订单询盘任务，内部使用进程池同时调用多次 `inquiry_send`，一次性返回全部询盘结果。

**适用场景**：
- 用户需要对多组独立订单发起询盘，各组订单的询盘问题不同（如"对订单A问发货时间，对订单B问退款"）
- **用户提供多个订单各自有不同的目标总价**（最典型场景）：每个订单需单独议价，问题各不相同，必须拆分为多个 task 并行执行

**不适用场景**：
- 只有一组订单需要询盘，或多个订单的问题完全相同 → 直接用 `inquiry_send`

## 参数

| 参数 | 短写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--tasks` | `-t` | string | 与-f二选一 | JSON 字符串：任务数组 |
| `--tasks-file` | `-f` | string | 与-t二选一 | JSON 文件路径（内容同 --tasks 格式） |

### Task 对象字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `order_ids` | string \| list[str] | 是 | 订单 ID 列表，逗号分隔字符串或数组，最多 10 个 |
| `question` | string | 是 | 询盘问题，单个字符串 |
| `local_images` | list[str] | 否 | 本地图片路径列表，采购商品图片说明（自动上传获取URL） |
| `image_urls` | list[str] | 否 | 图片URL列表，采购商品图片说明（已有在线链接） |
| `orders_status` | list[str] | 否 | 订单状态集合 |

## 示例

```bash
# 典型场景：多个订单各有不同目标总价（每个订单单独一个 task）
# 用户输入：
#   订单ID：5116391244078005116  目标总价：17
#   订单ID：5115884331254096317  目标总价：18
python3 cli.py batch_inquiry -t '[
  {"order_ids":["5116391244078005116"],"question":"目标总价17"},
  {"order_ids":["5115884331254096317"],"question":"目标总价18"}
]'

# 并行询盘两组订单（不同问题）
python3 cli.py batch_inquiry -t '[
  {"order_ids":["5116391244078005116"],"question":"什么时候能发货"},
  {"order_ids":["5116391244078005117","5116391244078005118"],"question":"能退款吗"}
]'

# 使用文件传入任务
python3 cli.py batch_inquiry -f /path/to/inquiry_tasks.json
```

## 输出格式

```json
{
  "success": true,
  "markdown": "批量询盘完成：2/2 成功，共 3 个订单（耗时 4.5s）",
  "data": {
    "total_tasks": 2,
    "success_count": 2,
    "fail_count": 0,
    "total_orders_inquired": 3,
    "elapsed_seconds": 4.5,
    "results": [
      {
        "index": 0,
        "success": true,
        "order_count": 1,
        "suc": true,
        "errorMsg": "",
        "elapsed_seconds": 2.1
      },
      {
        "index": 1,
        "success": true,
        "order_count": 2,
        "suc": true,
        "errorMsg": "",
        "elapsed_seconds": 3.2
      }
    ]
  }
}
```

### 部分失败时

整体 `success` 为 `true`（只要至少一个任务成功），失败任务的 result 包含 `errorMsg` 字段：

```json
{
  "index": 1,
  "success": false,
  "order_count": 2,
  "suc": false,
  "errorMsg": "询盘触发失败: ..."
}
```

## Agent 执行流程

1. **解析用户输入**：
   - 提取每个订单 ID 和对应的目标总价（或其他询盘问题）
   - 若每个订单的问题/目标总价不同 → 每个订单单独构造一个 task
   - 若所有订单问题相同 → 合并为一个 task 直接调用 `inquiry_send`
2. **构造任务数组**：每个 task 包含该订单的 `order_ids` 和对应的 `question`
3. **执行 batch_inquiry**：传入任务数组，一次并行调用
4. **告知结果**：告知用户哪些询盘成功，哪些失败，失败的可建议单独用 `inquiry_send` 重试

### 目标总价场景的问题拼装规则

用户输入「目标总价 17」时，`question` 字段直接传 `"目标总价17"`（数字紧跟单位，不加空格）。

| 用户输入 | question 字段值 |
|---|---|
| 目标总价：17 | `"目标总价17"` |
| 目标总价：17元 | `"目标总价17元"` |
| 目标总价 17.5 | `"目标总价17.5"` |

## 限制

- 单次最多 10 个任务
- 并行进程上限 5，由系统自动管理
- 每个任务内的订单 ID 最多 10 个
- 每个任务内部的超时规则与 `inquiry_send` 一致
