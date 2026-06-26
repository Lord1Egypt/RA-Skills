# 安全审计清单

## 敏感信息分类

| 信息类型 | 示例 | 风险等级 | 处理方式 |
|---------|------|---------|---------|
| Access Token | `ory_at_xxx...` | 🔴 高 | 仅存 mcporter 配置，禁止硬编码 |
| 文档库 GNS | `gns://FC1B4FE2...` | 🟡 中 | 可公开，不含内容 |
| 本地文件路径 | `~/Desktop/合同/` | 🟢 低 | 用户自行提供 |
| 合同内容 | 文件正文 | 🔴 高 | 仅在 AI 审阅流程中使用，不外传 |

---

## 必须遵守

### ✅ Token 管理
- Access Token **必须**通过 `~/.openclaw/workspace/config/mcporter.json` 配置
- SKILL.md 示例中只允许出现变量名 `$ACCESS_TOKEN`，禁止出现真实 Token
- Token 失效时：更新 mcporter.json → `mcporter daemon restart`

### ✅ 目录结构
- 合同原文必须上传到「合同原文/」子目录
- 审阅报告直接放在合同名称目录下
- 禁止上传到用户未授权的目录

### ✅ 批量场景
- 批量执行时，所有失败文件须汇总报告，不单独中断
- 定时任务运行日志须包含失败原因摘要

---

## 禁止行为

### ❌ 禁止在 SKILL.md 中硬编码
```
# 错误示例
ACCESS_TOKEN="ory_at_9PsLHqgc7xlr2J..."

# 正确示例
ACCESS_TOKEN="$ACCESS_TOKEN"  # 从环境变量或 mcporter 配置读取
```

### ❌ 禁止在日志中打印 Token
- curl 命令使用 `-H "authorization: $ACCESS_TOKEN"` 时不打印实际值
- 错误信息中出现 Token 时自动脱敏

### ❌ 禁止向第三方发送合同内容
- 审阅结果只保存到用户指定的 AnyShare 目录
- 飞书通知只发送摘要信息（文件名、状态、链接），不发送合同正文

---

## 公开发布前检查

- [ ] SKILL.md 中无真实 Access Token
- [ ] 所有 Token 引用均为变量形式
- [ ] 模板文件内容不包含业务敏感信息
- [ ] workflow/main.yaml 已删除
- [ ] 示例路径为通用路径（如 `~/Desktop/合同/`）
