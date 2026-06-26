# 安全审计清单

## 敏感信息分类

| 信息类型 | 示例 | 风险等级 | 处理方式 |
|---------|------|---------|---------|
| Access Token | `ory_at_xxx...` | 🔴 高 | 仅存 mcporter 配置，禁止硬编码 |
| 文档库 GNS | `gns://FC1B4FE2...` | 🟡 中 | 可公开，不含内容 |
| 用户上传的参考资料 | 项目文档/报告等 | 🔴 高 | 仅在全文写作流程中使用，不外传 |
| AI 生成内容 | 大纲/正文 | 🟡 中 | 保存到用户指定目录，不公开发布 |

---

## 必须遵守

### ✅ Token 管理
- Access Token **必须**通过 `~/.openclaw/workspace/config/mcporter.json` 配置
- SKILL.md 示例中只允许出现变量名 `$ACCESS_TOKEN`，禁止出现真实 Token
- Token 失效时：更新 mcporter.json → `mcporter daemon restart`

### ✅ 文件操作
- 只能操作用户明确提供的文件或 AnyShare 文档库中已有文件
- 上传文件前须确认目标目录 docid
- 下载文件须用户明确确认

### ✅ 内容处理
- AI 生成的大纲和正文仅保存到用户指定目录
- 错误信息中如涉及文件路径，自动脱敏

---

## 禁止行为

### ❌ 禁止在 SKILL.md 中硬编码 Token
```bash
# 错误
ACCESS_TOKEN="ory_at_9PsLHqgc..."

# 正确：mcporter call 时通过参数传递
mcporter call anyshare-asmcp.file_osbeginupload access_token:"$ACCESS_TOKEN" ...
```

### ❌ 禁止在日志中打印 Token
- mcporter call 工具自动注入 Token，不在 stdout 打印

### ❌ 禁止在未确认前自动执行写正文
- 大纲未经用户确认，不得调用 `__大纲写作__1`
- 批量/定时场景下，如无法等待用户确认，应跳过或标记待确认

---

## 公开发布前检查

- [ ] SKILL.md 中无真实 Access Token
- [ ] 所有 Token 引用均为变量形式
- [ ] workflow/main.yaml 已删除
- [ ] 示例路径为通用路径
- [ ] 模板文件内容不包含业务敏感信息
