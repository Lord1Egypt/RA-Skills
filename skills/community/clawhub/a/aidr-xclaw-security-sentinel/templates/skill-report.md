# Skill 安全报告

> 本报告由 AIDR-XClaw-Security-Sentinel 自动生成，基于 Gate 2 Skill Audit 检测结果。
>
> 触发时机：用户提及或安装 Skill 时（aidr-xclaw-security-sentinel 插件安装除外）

---

## 基本信息

| 字段 | 值 |
|------|-----|
| Skill 名称 | `{skill_name}` |
| Skill 版本 | `{version}` |
| Skill 分类 | `{category}` |
| 扫描时间 | `{timestamp}` |
| 检测类型 | Skill Audit（Gate 2） |
| 扫描类型 | `{scan_type}` |

---

## 综合评分

**总分: `{final_score}`/100**

| 等级 | 范围 | 颜色 | 状态 | Action |
|------|------|------|------|--------|
| 通过 (CLEAR/MINOR) | 85–100 | 🟢 绿色 | 正常 | `approve` |
| 警告 (ELEVATED) | 60–84 | 🟡 黄色 | 需关注 | `warn` |
| 隔离 (SEVERE) | 30–59 | 🟠 橙色 | 谨慎使用 | `reject` |
| 拒绝 (CRITICAL) | 0–29 | 🔴 红色 | 拒绝 | `reject` |

> 当前等级: **{level_badge}** — Verdict: **{verdict}** — Action: `{action}`

---

## 审计结论

**最终判定**: **{verdict}** / **{level}**

| verdict | 说明 | Action |
|---------|------|--------|
| `allow` | 通过审计，可安全安装/调用 | `approve` |
| `confirm` | 需要用户确认，存在一定风险 | `warn` |
| `block` | 禁止安装/调用，存在严重安全风险 | `reject` |

### 审计评分明细

| 评分维度 | 分值 |
|---------|------|
| 综合评分 | {final_score}/100 |
| 行为评分 | {behavioral_score}/100 |
| 源码评分 | {source_score}/100 |

---

## 安全发现

{finding_count} 项安全发现：

| 标签 | 描述 | 风险等级 |
|------|------|---------|
{findings_table}

{finding_recommendations}

---

## 指纹信息

| 层级 | 指纹值（SHA-256） |
|------|------------------|
| L2 — 内容指纹 | `{l2_hash}` |
| L3 — 元数据指纹 | `{l3_hash}` |
| Final — 设备指纹 | `{final_hash}` |

**注册状态**: `{registry_status}`
**注册时间**: `{registered_at}`
**最后扫描**: `{last_scan}`

---

## 内容统计

| 指标 | 值 |
|------|-----|
| 扫描文件数 | {total_files} |
| 总行数 | {total_lines} |
| 敏感字段脱敏数 | {sensitive_paths_masked} |

---

## 处置建议

> 根据 `{verdict}` + `{level}` 等级，执行以下 Action：

| Action | 行为 |
|--------|------|
| `approve` | 正常执行 Skill |
| `warn` | 展示警告，等待用户确认后执行 |
| `reject` | 立即停止，不执行该 Skill |

### 阻断提示模板（verdict=block / level=SEVERE/CRITICAL 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Skill-Audit] 检测完成
检测结论: reject
════════════════════════════════════════════════════════════

🚫 Skill 安全检测阻断

综合评分: {final_score}/100
风险等级: {level}
检测结论: 检测到严重安全风险，禁止安装/调用此 Skill。

安全发现: {finding_count} 项
{finding_recommendations}
```

### 警告提示模板（verdict=confirm / action=warn 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Skill-Audit] 检测完成
检测结论: warn
════════════════════════════════════════════════════════════

⚠️ Skill 安全检测告警

综合评分: {final_score}/100
风险等级: {level}
检测结论: 检测到一定风险，请确认后再执行。

安全发现: {finding_count} 项
{finding_recommendations}

是否继续执行此 Skill？
```

### 通过提示模板（verdict=allow / action=approve 时）

```
════════════════════════════════════════════════════════════
[AIDR-XClaw-Security-Sentinel][Skill-Audit] 检测完成
检测结论: approve
════════════════════════════════════════════════════════════

✅ Skill 安全检测通过

综合评分: {final_score}/100
风险等级: {level}
检测结论: 未检测到明显安全风险，可正常安装/调用。

安全发现: {finding_count} 项
```

---

## 免责声明

本报告基于提交时的 Skill 内容生成。安全风险随时间变化（依赖更新、API 变更等），建议定期重新检测。本报告不构成任何形式的安全性保证。
