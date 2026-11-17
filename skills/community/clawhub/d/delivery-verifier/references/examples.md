# 示例 - delivery-verifier

> 来源: SKILL.md(delivery-verifier) + 01手册§五

> 虚拟商品发货结果验证器的输入输出示例。

## 示例1: 正常发货验证(全通过)

### 输入
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

### 输出
```json
{
  "success": true,
  "data": {
    "verification_id": "VR-20260511-EP02-001",
    "flow_id": "EP-02",
    "verification_type": "post_execution",
    "result": {
      "status": "pass",
      "checks": [
        {"check_id": "C001", "dimension": "existence", "expected": "HTTP 200", "actual": "HTTP 200, 文件大小:2.3MB", "status": "pass"},
        {"check_id": "C002", "dimension": "completeness", "expected": "消息含网盘链接", "actual": "找到含链接的消息", "status": "pass"},
        {"check_id": "C003", "dimension": "correctness", "expected": "shipped", "actual": "shipped", "status": "pass"},
        {"check_id": "C004", "dimension": "timeliness", "expected": "30分钟内发货", "actual": "耗时15分钟", "status": "pass"},
        {"check_id": "C005", "dimension": "safety", "expected": "密码≥6位+有效期≤7天", "actual": "密码6位含字母+数字,有效期7天", "status": "pass"}
      ],
      "pass_count": 5,
      "fail_count": 0,
      "warning_count": 0
    },
    "recommendation": null
  },
  "error": null,
  "code": null
}
```

## 示例2: 网盘链接404(验证失败)

### 输入
```json
{
  "task_id": "JJC-003",
  "order_id": "XY002",
  "link_url": "https://pan.example.com/s/expired",
  "buyer_id": "user_456"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "verification_id": "VR-003",
    "result": {
      "status": "fail",
      "checks": [
        {"dimension": "existence", "expected": "HTTP 200", "actual": "HTTP 404", "status": "fail"}
      ],
      "pass_count": 0,
      "fail_count": 1,
      "warning_count": 0
    },
    "recommendation": "网盘链接已失效，建议重新生成分享链接并补发"
  },
  "error": null,
  "code": null
}
```

## 示例3: 发货超SLA+安全不达标(warning)

### 输入
```json
{
  "task_id": "JJC-005",
  "order_id": "XY004",
  "link_url": "https://pan.example.com/s/ok",
  "buyer_id": "user_001",
  "order_created_at": "2026-05-11T10:00:00Z",
  "share_password": "123",
  "share_expiry": "2026-06-11T10:00:00Z"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "verification_id": "VR-005",
    "result": {
      "status": "warning",
      "checks": [
        {"dimension": "existence", "status": "pass"},
        {"dimension": "completeness", "status": "pass"},
        {"dimension": "correctness", "status": "pass"},
        {"dimension": "timeliness", "actual": "耗时45分钟超SLA30分钟", "status": "warning"},
        {"dimension": "safety", "actual": "密码3位纯数字+有效期31天", "status": "warning"}
      ],
      "pass_count": 3,
      "fail_count": 0,
      "warning_count": 2
    },
    "recommendation": "发货超SLA(45分钟>30分钟)，建议优化发货流程；分享密码强度不足(3位纯数字)，建议重设为≥6位含字母+数字；有效期过长(31天>7天)，建议缩短至7天内"
  },
  "error": null,
  "code": null
}
```
