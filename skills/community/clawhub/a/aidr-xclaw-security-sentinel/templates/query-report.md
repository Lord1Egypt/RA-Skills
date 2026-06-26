# Query 安全报告

> 本报告由 AIDR-XClaw-Security-Sentinel 自动生成，基于 Gate 1 Query Audit 检测结果。
>
> 触发时机：用户每次发送消息（aidr-xclaw-security-sentinel 插件安装除外）

---

## 基本信息

| 字段 | 值 |
|------|-----|
| 扫描时间 | `{timestamp}` |
| 检测类型 | Query Audit（Gate 1） |
| 扫描对象 | 用户输入（已脱敏） |
| 会话哈希 | `{session_hash}` |

---

## 综合评分

**总分: `{safety_score}`/100**

| 等级 | 范围 | 颜色 | 状态 | Action |
|------|------|------|------|--------|
| 强通过 (strong) | 76–100 | 🟢 绿色 | 正常 | `pass` |
| 中通过 (moderate) | 41–75 | 🟢 绿色 | 正常 | `pass` |
| 边缘 (marginal) | 16–40 | 🟡 黄色 | 标记审查 | `warn` |
| 不安全 (unsafe) | 0–15 | 🔴 红色 | 拒绝执行 | `block` |

> 当前等级: **{safety_level}** — Action: `{action}`

---

## 风险发现

{findings_count} 项风险发现：

| 类型 | 描述 | 匹配内容 | 分数权重 |
|------|------|---------|---------|
{findings_table}

{finding_recommendations}

---

## 统计数据

| 指标 | 值 |
|------|-----|
| 原始文本长度 | {original_length} 字符 |
| 脱敏后文本长度 | {sanitized_length} 字符 |
| 敏感字段脱敏数 | {masked_fields_count} |
| 隐形字符移除数 | {chars_removed} |
| HTML 注释剥离数 | {html_comments_stripped} |

---

## API 响应

| 字段 | 值 |
|------|-----|
| `safety_score` | {safety_score} |
| `safety_level` | {safety_level} |
| `is_suspicious` | {is_suspicious} |
| `risk_tags` | {risk_tags} |
| `request_id` | `{request_id}` |
| 服务端处理时长 | {latency_ms} ms |

---

## 处置建议

> 根据 `{safety_level}` 等级，执行以下 Action：

| Action | 行为 |
|--------|------|
| `pass` | 继续处理用户请求 |
| `warn` | 展示警告后继续 |
| `block` | 立即停止，阻断用户请求 |

### 阻断提示模板（action=block 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Query-Audit] 检测完成
检测结论: block
════════════════════════════════════════════════════════════

🚫 安全检测阻断

安全评分: {safety_score}/100
安全等级: {safety_level}
检测结论: 检测到潜在安全威胁，建议调整提问方式或联系管理员。
```

### 通过提示模板（action=pass 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Query-Audit] 检测完成
检测结论: pass
════════════════════════════════════════════════════════════

✅ 安全检测通过

安全评分: {safety_score}/100
安全等级: {safety_level}
检测结论: 未检测到明显安全威胁，继续处理请求。
```

### 告警提示模板（action=warn 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Query-Audit] 检测完成
检测结论: warn
════════════════════════════════════════════════════════════

⚠️ 安全检测告警

安全评分: {safety_score}/100
安全等级: {safety_level}
检测结论: 检测到边缘风险，请注意提问方式。
```

---

## 免责声明

本报告基于提交时的内容生成，仅代表当时的检测结果。检测结果可能受内容表述方式影响。如有异议，请联系管理员。
