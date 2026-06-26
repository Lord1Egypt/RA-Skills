# M14 — 外部接口规范

> 统一调用接口 + 预留扩展点 — 面向系统集成与第三方对接

## 14.1 统一接口协议

### 调用方式

所有模块统一使用 `sessions_send` 工具调用：

```
sessions_send(
  label: "ai-company-{module}",   // 模块标签
  message: "#[部门-主题] 任务描述\n优先级：P0/P1/P2/P3\n截止时间：ISO8601"
)
```

### 模块标签映射

| 模块 | 标签 | 注册编号 |
|------|------|---------|
| CEO | `ai-company-ceo` | CEO-001 |
| CFO | `ai-company-cfo` | CFO-001 |
| CMO | `ai-company-cmo` | CMO-001 |
| CHO | `ai-company-cho` | CHO-001 |
| CPO | `ai-company-cpo` | CPO-001 |
| CLO | `ai-company-clo` | CLO-001 |
| CTO | `ai-company-cto` | CTO-001 |
| CQO | `ai-company-cqo` | CQO-001 |
| CISO | `ai-company-ciso` | CISO-001 |
| CRO | `ai-company-cro` | CRO-001 |
| COO | `ai-company-coo` | COO-001 |

## 14.2 标准 Interface Schema

每个模块遵循统一的接口定义规范：

```yaml
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        task:
          type: string
          description: "任务描述"
        context:
          type: object
          description: "可选上下文信息"
      required: [task]
  outputs:
    type: object
    schema:
      type: object
      properties:
        decision:
          type: string
          description: "决策结论"
        action_plan:
          type: array
          description: "执行计划"
        risk_alerts:
          type: array
          description: "风险预警"
      required: [decision]
  errors:
    - code: "{MODULE}_001"
      message: "错误描述"
      action: "建议处理方式"
```

## 14.3 权限矩阵（最小权限原则）

| 权限 | CEO | CFO | CMO | CHO | CPO | CLO | CTO | CQO | CISO | CRO | COO |
|------|-----|-----|-----|-----|-----|-----|-----|-----|------|-----|-----|
| 系统命令 | — | — | — | — | — | — | ✅ | — | ✅ | — | — |
| 文件-只读 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 文件-写入（自身模块） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 文件-写入（他人模块） | ✅ | — | — | — | — | — | ✅ | — | — | — | — |
| 网络API（内部） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 网络API（外部） | — | — | ✅ | — | ✅ | — | ✅ | — | ✅ | — | — |
| MCP工具（只读） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MCP工具（写入） | — | — | — | — | — | — | ✅ | — | ✅ | — | — |
| 人工审批触发 | ✅ | ✅ | — | — | — | ✅ | ✅ | — | ✅ | ✅ | — |
| 终极裁决 | ✅ | — | — | — | — | — | — | — | — | — | — |

## 14.3.1 sessions_send 调用失败处理

| 策略 | 参数 | 说明 |
|------|------|------|
| 重试 | `retry_count: 2`, `retry_delay: 5s` | P0/P1 级调用失败自动重试 |
| 降级 | `fallback_agent: "<module>"` | 目标不可用时路由至代理 Agent |
| 熔断 | `circuit_breaker: {threshold: 3, window: 60s}` | 连续 3 次失败触发 60s 熔断 |
| 超时 | `timeout: {P0: 200ms, P1: 2s, P2: 30s, P3: 300s}` | 按优先级分级超时 |
| 告警 | 熔断触发 → 通知 CEO + CISO | 升级路径 |

## 14.4 预留扩展点

### Hook 机制

```
pre_decision_hook   → 决策前拦截（审计/合规）
post_decision_hook  → 决策后处理（日志/通知）
pre_action_hook     → 行动前拦截（权限/熔断）
post_action_hook    → 行动后处理（监控/回滚）
error_handler_hook  → 异常处理（恢复/告警）
```

### 中间件扩展

```yaml
middleware_chain:
  - name: audit_logger          # 审计日志（内置）
    stage: pre_decision
  - name: compliance_checker    # 合规检查（内置）
    stage: pre_decision
  - name: custom_validator      # 自定义校验（扩展点）
    stage: pre_decision
    config: external             # 外部配置
  - name: circuit_breaker       # 熔断器（内置）
    stage: pre_action
  - name: external_notifier     # 外部通知（扩展点）
    stage: post_action
    config: external             # 外部配置
```

### 外部集成预留

| 接口类型 | 用途 | 状态 |
|---------|------|------|
| REST API | 外部系统数据同步 | 预留 |
| Webhook | 事件通知推送 | 预留 |
| MCP Server | 工具扩展 | 预留 |
| Plugin | 自定义模块加载 | 预留 |

## 14.5 安全审查合规

### Skill Vetter 检查清单（发布前必检）

```
✅ 无 curl/wget 到未知 URL
✅ 无发送数据到外部服务器
✅ 无请求凭据/令牌/API 密钥
✅ 无读取 ~/.ssh, ~/.aws 等
✅ 无 eval() / exec() 处理外部输入
✅ 无修改工作区外系统文件
✅ 无混淆代码
✅ 无请求提升权限
✅ 无访问浏览器 cookies/sessions
✅ 权限范围与功能匹配（最小权限原则）
```

### ClawHub Schema v1.0 合规

- ✅ Frontmatter: name + description（必填）
- ✅ License: MIT-0
- ✅ Tags: 标准化标签集
- ✅ Interface: inputs/outputs/errors 完整定义
- ✅ Dependencies: skills 声明明确
- ✅ Quality: saST Pass + vetter Approved
- ✅ Metadata: category/layer/cluster/maturity
