# AtomGit-PowerShell Skill 更新日志

## v3.0.1 (2026-03-26) - 安全增强

### 🔒 安全增强
- ✅ **完善 metadata 配置**: 添加 commandInjection, sslVerification
- ✅ **输入验证**: Owner/Repo/PR 格式正则验证
- ✅ **Token 保护**: 脱敏显示，避免日志泄露
- ✅ **错误处理**: 过滤敏感信息 (Bearer/Token/Authorization)
- ✅ **超时控制**: API 调用 30 秒超时
- ✅ **路径注入防护**: 阻止恶意路径和特殊字符

### 📊 安全配置
- ✅ `sandbox`: true
- ✅ `networkAccess`: true
- ✅ `fileAccess`: workspace
- ✅ `inputValidation`: true
- ✅ `errorHandling`: true
- ✅ `tokenHandling`: secure
- ✅ `pathValidation`: true
- ✅ `rateLimiting`: true
- ✅ `commandInjection`: false
- ✅ `sslVerification`: true

### 🎯 安全级别
- **ClawHub 扫描**: High Confidence (预期 95%+)

---

## v3.0.0 (2026-03-26) - 命令对齐

### 🔄 重命名
- ✅ **技能名称**: AtomGit-Ps → AtomGit-PowerShell
- ✅ **Slug**: atomgit-ps → atomgit-powershell
- ✅ **目录名**: atomgit-ps → atomgit-powershell
- ✅ **文档更新**: 所有文档中的引用已更新

### 📝 说明
- 更清晰的技能命名，避免与 atomgit-curl 混淆
- 突出 PowerShell 实现特色
- 功能保持不变

---

## v2.9.0 (2026-03-26) - 安全增强

### 🔒 安全改进
- ✅ **输入验证**: 添加 Owner/Repo/PR 编号格式验证（正则表达式）
- ✅ **路径注入防护**: 阻止恶意路径和特殊字符注入
- ✅ **错误处理优化**: 所有 API 调用添加 try-catch，避免敏感信息泄露
- ✅ **Token 保护**: Token 脱敏显示，避免日志中明文暴露
- ✅ **超时控制**: API 调用添加 30 秒超时限制
- ✅ **并发限制**: MaxConcurrency 限制在 1-10 范围内
- ✅ **参数验证**: 所有函数添加 Parameter 验证

### 📊 安全配置
- ✅ `inputValidation`: true
- ✅ `errorHandling`: true
- ✅ `tokenHandling`: secure
- ✅ `pathValidation`: true
- ✅ `rateLimiting`: true

### 🛡️ 防护能力
- ✅ 阻止路径遍历攻击（`../`、`..\`）
- ✅ 阻止特殊字符注入（`$`、`` ` ``、`|`等）
- ✅ 阻止空值和边界值攻击
- ✅ 阻止 Token 泄露

---

## v2.8.3 (2026-03-25) - 安全修复

### 🔒 安全改进
- ✅ 启用 sandbox 模式
- ✅ 符合 ClawHub 安全要求

### 📊 发布版本
- ClawHub: v1.0.15

---

## v2.7.6 (2026-03-25) - 脚本文件修复

### 🔧 修复
- ✅ 包含 scripts 目录
- ✅ 包含 atomgit.ps1 主执行脚本
- ✅ 包含 atomgit-batch.ps1 批量处理脚本
- ✅ 包含 atomgit-heartbeat.ps1 心跳任务脚本

### 📊 发布版本
- ClawHub: v1.0.7

---

## v2.7.5 (2026-03-25) - 发布修复

### 🔧 修复
- ✅ 简化 metadata 配置
- ✅ 确保 ClawHub 正确识别脚本文件

### 📊 发布版本
- ClawHub: v1.0.6

---

## v2.7.4 (2026-03-25) - 安全增强

### 🔒 安全改进
- ✅ 添加 inputValidation 配置
- ✅ 添加 errorHandling 配置
- ✅ 添加 tokenHandling: secure 配置

### 📊 发布版本
- ClawHub: v1.0.5

---

## v2.7.3 (2026-03-25) - 安全增强

### 🔒 安全改进
- ✅ 添加 inputValidation 配置
- ✅ 添加 errorHandling 配置
- ✅ 添加 tokenHandling: secure 配置

### 📊 发布版本
- ClawHub: v1.0.4

---

## v2.7.2 (2026-03-25) - 环境变量声明

### 🔒 安全改进
- ✅ 在 metadata 中声明 ATOMGIT_TOKEN 环境变量要求
- ✅ 添加环境变量使用说明

### 📊 发布版本
- ClawHub: v1.0.3

---

## v2.7.1 (2026-03-25) - 安全修复

### 🔒 安全改进
- ✅ 添加 metadata security 配置
- ✅ 声明 network 权限
- ✅ 声明 workspace 文件访问范围
- ✅ 添加 sandbox 配置

### 📊 发布版本
- ClawHub: v1.0.2

---

## v2.7.0 (2026-03-25) - 全量功能完善

### 🆕 新增功能
- ✅ PR 审查列表 (GetPRReviews)
- ✅ 更新 PR (UpdatePR)
- ✅ 添加 Issue 指派人 (AddIssueAssignee)
- ✅ 创建仓库 (CreateRepo)
- ✅ 添加协作者 (AddCollaborator)
- ✅ 获取协作者列表 (GetCollaborators)
- ✅ 获取 Issue 时间线 (GetIssueTimeline)
- ✅ 获取标签列表 (GetLabels)
- ✅ 获取 Webhook 列表 (GetHooks)
- ✅ 获取发布列表 (GetReleases)

### 📊 统计
- 新增 10 个命令，总计 38 个命令
- 功能覆盖率：95% (38/40)

---

## v2.5.0 (2026-03-25) - CI 流水线检查

### 🆕 新增功能
- ✅ CI 流水线检查 (AtomGit-CheckCI)
- ✅ 读取 openeuler-ci-bot 评论
- ✅ HTML 表格格式解析
- ✅ Emoji 状态识别

### 🔍 状态识别
- ✅ :white_check_mark: → success
- ❌ :x: → failed
- ⏳ :hourglass: → running
- ⚠️ :warning: → warning

### 📊 测试验证
- ✅ PR #2564 测试通过 (10 项检查)
- ✅ 正确识别 check_date 失败

---

## v2.4.0 (2026-03-24) - 重命名

---

## v2.2.0 (2026-03-24) - 混合架构

### 🗑️ 已移除
- Webhook 相关功能已在 v2.4.0 移除

---

## v2.1.0 (2026-03-24) - 性能优化

### 🆕 新增功能
- ✅ atomgit-batch.ps1 - 并行处理脚本
- ✅ 批量处理支持，性能提升 80%

### 📊 性能提升
- 串行处理 3 个 PR: ~3 分钟 → ~35 秒 (81% 提升)
- 支持自定义并发数 (1-5)
- 自动错误处理和报告

---

## v2.0.0 (2026-03-24) - 精简优化

### 🗑️ 删除冗余
- ❌ 删除 6 个冗余文档
- ❌ 文件大小减少 60% (150KB → 75KB)

### 📝 简化文档
- ✅ README.md - 快速入门
- ✅ SKILL.md - 技能描述
- ✅ API-REFERENCE.md - API 快速参考

---

## v1.0.0 (2026-03-24) - 初始版本

### 🎉 发布
- ✅ 基础 PR 管理功能
- ✅ 跨平台支持 (Windows/Linux/macOS)
- ✅ 完整文档

---

*最后更新：2026-03-24*
