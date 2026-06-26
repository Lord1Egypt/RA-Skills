# 每日安全巡检报告 — 输出模板

完成检查后，按以下结构输出报告（简体中文），并**保存到 `workspace/docs/security-audit/security-report-YYYY-MM-DD.md`**（日期为巡检日）。括号内为填写说明，实际输出时替换为检查结果。

```markdown
## 每日安全巡检报告（YYYY-MM-DD）

### 1. 网关 loopback
（✅ 正常 / ❌ 异常 + 说明）

### 2. 防火墙
（提醒用户在本机确认已开启）

### 3. API 密钥在 .env
（✅ 正常 / ❌ 发现明文 + 位置与建议）

### 4. SOUL.md 安全监控规则
（✅ 全部就绪 / ❌ 缺失的 agent 列表）

### 5. 认证异常
（✅ 未发现 / ⚠️ 需关注 / 无法检测 + 说明）

### 6–7. 身份与访问控制 / 工具与沙箱（扩展）
（✅ 符合建议 / ⚠️ 待改进项简述）

### 8. 官方审计（openclaw security audit）
（Summary：X critical · X warn · X info；若有 critical 或重要 warn 则简述要点）

### 9. OpenClaw 健康检查（doctor）
（Summary 或结论；若有建议执行 `openclaw doctor --fix` 则标出并提醒用户本地手动执行）

---
**安全评分**：X / 10  
**结论**：（一句话）  
**待办**：（若有异常则列出，无则写「无」）
```

报告体量控制在 300–600 字内，便于快速阅读与投递到 Telegram。
