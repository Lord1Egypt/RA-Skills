---
name: delivery-verifier
description: "虚拟商品发货结果验证器，确认网盘链接可访问+闲鱼消息已发送+订单状态已变更（来源: 05文档§4.5 P0-6）。 触发：EP-02发货后门下省事后验证/自动发货Review阶段 不触发：发货执行中/非发货任务"
version: 1.0.0
tools: [read, exec]
dependencies: [auto-delivery]
metadata:
  priority: P0
  category: xianyu-ops
  openclaw:
    emoji: "🛒"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["ALIST_BASE_URL", "ALIST_TOKEN", "SILICONFLOW_API_KEY"]
      config: ["mcp.servers.alist-mcp", "mcp.servers.xianyu-agent-mcp"]
---

# 虚拟商品发货结果验证器

确认网盘链接可访问+闲鱼消息已发送+订单状态已变更。

## 使用场景

1. EP-02虚拟商品自动发货流程的事后验证
2. 门下省Review阶段验证发货是否真的完成
3. auto-delivery执行后确认全链路结果
4. 订单投诉时回溯验证发货记录

## 工作流

1. 接收验证请求：`{task_id, order_id, link_url, buyer_id, order_created_at?, share_password?, share_expiry?}`
2. 验证existence：alist-mcp检查link_url返回HTTP 200
3. 验证completeness：xianyu-agent-mcp get_chat_history确认消息已发送
4. 验证correctness：get_order_status确认订单状态为"已发货"
5. 验证timeliness：比较发货完成时间与SLA时限(来源:01手册§五5.1，虚拟商品SLA=订单创建后30分钟内发货)，超时则status:warning
6. 验证safety：检查分享链接密码强度(≥6位且含字母+数字)和有效期(≤7天，来源:01手册§五5.1风控策略)，不达标则status:warning
7. 输出验证报告JSON

## 输入格式

```json
{
  "task_id": "JJC-20260511-002",
  "order_id": "XY20260511001",
  "link_url": "https://pan.example.com/s/abc123",
  "buyer_id": "user_12345",
  "order_created_at": "2026-05-11T14:00:00Z",
  "share_password": "ab1234",
  "share_expiry": "2026-05-18T14:00:00Z"
}
```

| 字段 | 别名 | 必填 | 说明 |
|:-----|:-----|:----:|:-----|
| task_id | - | 是 | 任务ID |
| order_id | - | 是 | 订单号 |
| link_url | share_link | 是 | 网盘分享链接(share_link) |
| buyer_id | - | 是 | 买家ID |
| order_created_at | - | 否 | 订单创建时间(ISO8601)，timeliness验证必需 |
| share_password | - | 否 | 分享链接密码，safety验证必需 |
| share_expiry | - | 否 | 分享链接有效期(ISO8601)，safety验证必需 |

## 输出格式

```json
{
  "success": true,
  "data": {
    "verification_id": "VR-20260511-EP02-001",
    "flow_id": "EP-02",
    "verification_type": "post_execution",
    "verifier": "menxia",
    "timestamp": "2026-05-11T14:35:00Z",
    "target": {
      "skill": "auto-delivery",
      "action": "deliver_virtual_goods",
      "input_summary": "发货AI代写文案服务"
    },
    "result": {
      "status": "pass",
      "checks": [
        {
          "check_id": "C001",
          "dimension": "existence",
          "description": "网盘链接可访问",
          "expected": "HTTP 200",
          "actual": "HTTP 200, 文件大小:2.3MB",
          "status": "pass"
        },
        {
          "check_id": "C002",
          "dimension": "completeness",
          "description": "闲鱼消息已发送",
          "expected": "消息记录中含网盘链接",
          "actual": "找到含链接的消息",
          "status": "pass"
        },
        {
          "check_id": "C003",
          "dimension": "correctness",
          "description": "订单状态为已发货",
          "expected": "shipped",
          "actual": "shipped",
          "status": "pass"
        },
        {
          "check_id": "C004",
          "dimension": "timeliness",
          "description": "发货在SLA时限内完成",
          "expected": "订单创建后30分钟内发货(来源:01手册§五5.1)",
          "actual": "耗时15分钟",
          "status": "pass"
        },
        {
          "check_id": "C005",
          "dimension": "safety",
          "description": "分享链接密码强度和有效期合规",
          "expected": "密码≥6位含字母+数字,有效期≤7天(来源:01手册§五5.1)",
          "actual": "密码6位含字母+数字,有效期7天",
          "status": "pass"
        }
      ],
      "pass_count": 5,
      "fail_count": 0,
      "warning_count": 0
    },
    "evidence": {
      "method": "alist-mcp + xianyu-agent-mcp get_chat_history + get_order_status",
      "raw_response": "{...}",
      "screenshot_path": null
    },
    "recommendation": null
  },
  "error": null,
  "code": null
}
```

## 验证维度

| 维度 | 检查项 | 通过标准 |
|:-----|:-------|:---------|
| existence | 网盘链接可访问 | alist-mcp返回HTTP 200 |
| completeness | 闲鱼消息已发送 | get_chat_history含链接消息 |
| correctness | 订单状态正确 | get_order_status返回shipped/completed |
| timeliness | 发货在SLA时限内 | 订单创建后30分钟内完成发货(来源:01手册§五5.1) |
| safety | 分享链接安全合规 | 密码≥6位含字母+数字且有效期≤7天(来源:01手册§五5.1) |

## 异常处理

| 异常场景 | 处理方式 |
|:---------|:---------|
| alist-mcp不可用 | 降级为人工访问链接确认 |
| alist-mcp超时(>30秒) | 重试1次，仍超时则降级为人工确认，记录超时日志 |
| xianyu-agent-mcp不可用 | 降级为人工检查闲鱼聊天记录 |
| xianyu-agent-mcp熔断(连续3次调用失败) | 标记circuit_breaker=open，暂停自动验证，转人工处理，记录熔断事件 |
| 网盘链接404 | status:fail + 建议重新生成链接 |
| 网盘链接403(权限变更) | status:fail + 建议检查分享权限设置 |
| 消息未找到 | status:fail + 建议重新发送 |
| 消息发送但买家未读 | status:warning + 记录未读状态，建议24小时后复查 |
| 订单状态异常 | status:fail + 记录实际状态 |
| 订单状态为退款中 | status:fail + 标记退款风险，建议暂停后续发货 |
| 发货超SLA时限(>30分钟) | status:warning + 记录超时时长，建议优化发货流程(来源:01手册§五5.1) |
| order_created_at缺失 | 跳过timeliness验证，checks中标注skipped:true+reason:"缺少order_created_at" |
| 分享链接无密码 | status:warning + 建议设置密码保护(来源:01手册§五5.1) |
| 分享密码强度不足(<6位或纯数字) | status:warning + 建议重设为≥6位含字母+数字的密码 |
| 分享链接有效期>7天 | status:warning + 建议缩短有效期至7天内(来源:01手册§五5.1) |
| share_password/share_expiry缺失 | 跳过safety验证，checks中标注skipped:true+reason:"缺少安全参数" |
| 验证请求参数缺失 | 返回error，提示缺少字段名，code=VERIFY_ERR_01 |
| 同一订单重复验证 | 返回上次验证结果缓存，标注is_cached=true |

## 降级验证方案

alist-mcp不可用→人工访问链接确认; xianyu-agent-mcp不可用→人工检查闲鱼聊天记录

## 示例

### 示例1: 正常发货验证（全通过）

```
输入: {task_id:"JJC-002", order_id:"XY001", link_url:"https://pan.example.com/s/abc", buyer_id:"user_123", order_created_at:"2026-05-11T14:00:00Z", share_password:"ab1234", share_expiry:"2026-05-18T14:00:00Z"}
执行: alist-mcp检查链接 → get_chat_history确认消息 → get_order_status确认状态 → 比较发货时间与SLA → 检查密码强度和有效期
输出: {success:true, data:{result:{status:"pass", pass_count:5, fail_count:0, warning_count:0}}}
```

### 示例2: 网盘链接404（验证失败）

```
输入: {task_id:"JJC-003", order_id:"XY002", link_url:"https://pan.example.com/s/expired", buyer_id:"user_456"}
执行: alist-mcp检查链接 → 返回HTTP 404
输出: {success:true, data:{result:{status:"fail", pass_count:0, fail_count:1, checks:[{dimension:"existence", status:"fail", actual:"HTTP 404"}]}, recommendation:"网盘链接已失效，建议重新生成分享链接并补发"}}
```

### 示例3: xianyu-agent-mcp熔断（降级处理）

```
输入: {task_id:"JJC-004", order_id:"XY003", link_url:"https://pan.example.com/s/ok", buyer_id:"user_789"}
执行: alist-mcp检查链接→pass → get_chat_history→连续3次超时，熔断触发
输出: {success:true, data:{result:{status:"warning", pass_count:1, fail_count:0, warning_count:1}, circuit_breaker:"open", recommendation:"xianyu-agent-mcp熔断，消息验证降级为人工检查闲鱼聊天记录"}}
```

### 示例4: 发货超SLA+分享链接安全不达标（warning）

```
输入: {task_id:"JJC-005", order_id:"XY004", link_url:"https://pan.example.com/s/ok", buyer_id:"user_001", order_created_at:"2026-05-11T10:00:00Z", share_password:"123", share_expiry:"2026-06-11T10:00:00Z"}
执行: existence→pass → completeness→pass → correctness→pass → timeliness→发货耗时45分钟超SLA30分钟→warning → safety→密码仅3位纯数字+有效期31天超7天→warning
输出: {success:true, data:{result:{status:"warning", pass_count:3, fail_count:0, warning_count:2}, recommendation:"发货超SLA(45分钟>30分钟)，建议优化发货流程；分享密码强度不足(3位纯数字)，建议重设为≥6位含字母+数字；有效期过长(31天>7天)，建议缩短至7天内"}}
```
