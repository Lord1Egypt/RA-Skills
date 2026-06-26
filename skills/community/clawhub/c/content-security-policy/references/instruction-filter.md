---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3045022100d639570cae2b891d3dfbafb33ea9a08c1d382725292b465c54c38e389bcdf01d022069001e3b3124c3ac4513f9c254febe58556a4e3b7c712553907bd87e915dd347
    ReservedCode2: 304502207f3da61656521641e33314356baf3eb4902c65a4a7a5b41a35ba69305127f403022100aedcbb186e3f198e6ea77568c700fb346e0e9842e1d283c41fba031e64f3a9ac
---

# 指令过滤详细逻辑

## 过滤流程

```
收到用户指令
    ↓
[1] 危险指令检测
    ↓
是否匹配危险指令库？
    ↓
    ├─ 是 → 根据风险等级处理
    │       ├─ P0: 直接拒绝 + 记录日志
    │       ├─ P1: 脱敏/确认后执行
    │       └─ P2: 记录日志 + 限制频率
    │
    └─ 否 → 进入动作判断流程
```

## 危险指令库

### P0 — 绝对禁止（直接拒绝）

```javascript
const P0_BLOCKED_COMMANDS = [
  // 远程连接类
  /\bssh\s+/i,
  /\bscp\s+/i,
  /\btelnet\s+/i,
  /\brdp\s+/i,
  /\bremote\s+desktop/i,

  // 系统删除类
  /rm\s+-rf\s+\//,
  /rm\s+-rf\s+\~\//,
  /rm\s+-rf\s+\$HOME/,
  /del\s+\/f\s+\/s\s+\/q\s+c:\\*/i,

  // 敏感读取类
  /cat\s+.*\.env/,
  /cat\s+.*config.*\.json/,
  /cat\s+~\/\.ssh\/id_rsa/,
];
```

**拒绝话术**：
> "出于安全考虑，我无法执行涉及SSH/远程连接/系统删除的指令。如有服务器操作需求，请联系管理员协助。"

### 🟠 P1 — 高危指令（需脱敏或确认）

```javascript
const P1_SENSITIVE_COMMANDS = [
  // 信息泄露类
  /(api[_-]?key|app[_-]?secret|password|token|secret)/i,

  // 配置修改类
  /(修改|更新|删除).*配置/i,
  /(修改|更新|删除).*技能/i,
  /重启.*gateway/i,

  // 群发消息类
  /群发.*消息/,
  /发送到.*群/,

  // 敏感信息查询类
  /查询.*密码/,
  /查询.*密钥/,
  /获取.*token/i,
];
```

**处理方式**：
- 检测是否最高权限人
- 是 → 脱敏后执行
- 否 → 向最高权限人发送确认请求

### 🟡 P2 — 中危指令（记录日志 + 限制）

```javascript
const P2_RESTRICTED_COMMANDS = [
  // 文件操作类
  /(读取|写入|修改).*文件/,
  /(上传|下载).*文件/,

  // 查询操作类
  /查询.*用户/,
  /搜索.*消息/,
  /获取.*列表/,

  // 外部通信类
  /发送.*邮件/,
  /发送.*请求/,
];
```

**处理方式**：
1. 记录操作日志
2. 检查频率限制（如1分钟不超过10次）
3. 正常执行

## 日志记录格式

```json
{
  "timestamp": "2026-03-08T12:00:00+08:00",
  "user_id": "ou_xxx",
  "user_level": "L1",
  "original_command": "查询用户列表",
  "matched_rule": "P2_RESTRICTED_COMMANDS",
  "risk_level": "P2",
  "decision": "allowed",
  "reason": "普通查询操作，在频率限制内",
  "execution_time_ms": 123
}
```

## 频率限制规则

| 操作类型 | 限制 |
|----------|------|
| 文件操作 | 1分钟 ≤ 10次 |
| 查询操作 | 1分钟 ≤ 30次 |
| 发送操作 | 1分钟 ≤ 5次 |

超限返回：
> "操作过于频繁，请稍后再试。（已记录日志）"
