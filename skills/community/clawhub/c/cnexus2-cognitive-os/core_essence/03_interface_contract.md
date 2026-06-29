# 03_interface_contract — 对外接口契约

## 一、原则

| 原则 | 定义 |
|------|------|
| 接口最小化 | 系统对外只暴露必须的接口，不暴露内部结构 |
| 无泄漏 | 接口不承诺实现细节，不暴露 slot / memory / state 内部 |
| 任何状态都有响应 | 系统在任何状态下（正常、降级、异常）都必须能返回响应 |
| 完整交互 | POST /chat 是一次完整的 OBSERVE → REFLECT 回路 |

## 二、端点定义

### 2.1 POST /chat（必须）

系统的唯一主入口。每次调用触发一次完整的认知回路。

### 2.2 GET /status（必须）

返回系统存活状态、运行模式、关键指标。不暴露内部实现细节。始终返回响应。

### 2.3 GET /memory（可选，管理用途）

外部管理工具读取内部记忆的接口。只读，不修改。返回内容不超过摘要长度。

### 2.4 POST /reset（可选，管理用途）

清空非核心记忆，重置状态到初始值。保留 persona block 和其他核心 identity 数据。

## 三、Schema 定义

### 3.1 POST /chat

**Request：**
```json
{
  "message": "string（用户输入）",
  "session_id": "string（可选，不传则自动生成）",
  "meta": {}
}
```

**Response（正常）：**
```json
{
  "ok": true,
  "data": {
    "response": "string（系统回复）",
    "session_id": "string",
    "state": {},
    "meta": {}
  }
}
```

**Response（降级）：**
```json
{
  "ok": false,
  "error": "not_ready",
  "error_message": "string"
}
```

### 3.2 GET /status

**Response：**
```json
{
  "ok": true,
  "data": {
    "alive": true,
    "uptime_seconds": 0,
    "version": "string",
    "state": {
      "system_state": "ACTIVE|DEGRADED|REPAIRING|IDLE|BOOTING",
      "degradation_level": "L0|L1|L2|L3"
    },
    "metrics": {},
    "llm": {}
  }
}
```

### 3.3 GET /memory

**Response：**
```json
{
  "ok": true,
  "data": {
    "total": 0,
    "blocks": []
  }
}
```

### 3.4 POST /reset

**Response：**
```json
{
  "ok": true,
  "data": {
    "status": "reset_complete",
    "preserved_identity": true
  }
}
```

## 四、不变量

1. 所有接口在任何状态下都返回响应（不 hang）
2. 接口不暴露 slot、memory store、cognitive state 的实现细节
3. POST /chat 的响应中不包含 trace log 级别的信息
4. 端点和 schema 变化必须向前兼容（只增字段，不删不改）

## 五、不在本文件范围内

| 概念 | 所属层级 |
|------|---------|
| 错误处理逻辑 / 重试策略 | L1 runtime_spec |
| 降级时的响应格式细节 | L1 runtime_spec |
| 认证方式 / token 校验 | L1 runtime_spec |
| 频率限制策略 | L1 runtime_spec |
| HTTP 状态码细节 | L1 runtime_spec |
| 开发/生产模式配置 | L1 runtime_spec |
