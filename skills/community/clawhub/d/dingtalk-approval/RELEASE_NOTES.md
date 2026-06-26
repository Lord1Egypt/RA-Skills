# 发布说明 - DingTalk Approval Plugin

## v2.3.2 (2026-03-13) - 页面文案与发布说明修正

### ✅ 收尾修正

- ✅ 更新 SKILL 摘要文案，补充审批详情和假期余额能力
- ✅ 更新 README 中的发布命令说明，替换过时的 `openclaw plugins publish`

---

## v2.3.1 (2026-03-13) - 发布收尾版

### ✅ 元数据与发布一致性修复

- ✅ 统一 `package.json`、`openclaw.plugin.json`、`.clawhub/manifest.json`、`_meta.json` 版本号为 `2.3.1`
- ✅ 补充 `get_vacation_balance` 到发布清单和文档
- ✅ 移除假期权限申请提示中的硬编码应用标识
- ✅ 将空仓库地址替换为插件主页链接

---

## v2.5.0 (2026-03-11) - 🔒 安全加固版

### 🔒 安全改进（ClawHub 审核反馈）

#### 🛡️ 敏感信息保护

- ✅ **移除日志中的敏感信息输出**
  - 新增 `sanitizeConfig()` 函数，脱敏输出配置信息
  - appSecret 不再出现在任何日志中
  - 用户 ID 和 appKey 仅显示前缀 + `***`

- ✅ **附件信息脱敏处理**
  - 新增 `sanitizeAttachment()` 函数
  - 隐藏附件的 `fileId` 和 `spaceId`（敏感资源标识）
  - 仅显示文件名、大小、类型等公开信息

- ✅ **审批详情脱敏**
  - 新增 `sanitizeInstance()` 函数
  - 自动识别并脱敏附件字段
  - 附件显示为 "X 个附件 (共 X KB)" 格式

#### 🛡️ 错误处理优化

- ✅ **用户友好的错误提示**
  - 所有错误消息使用统一的 ❌/✅/ℹ️ 前缀
  - 不暴露 API 内部结构和实现细节
  - 配置错误提示联系管理员，不显示具体缺失项

- ✅ **配置验证前置**
  - 每个工具执行前检查 appKey/appSecret
  - 配置为空时返回友好提示
  - 避免空配置导致的异常

#### 🛡️ 日志规范

- ✅ **生产环境日志规范**
  - 移除所有 `console.log(config)` 类型的敏感输出
  - 错误日志使用 `console.error` 但不暴露敏感值
  - 日志仅用于调试，不包含用户数据

---

### 📋 安全审查清单

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 日志不泄露 appSecret | ✅ | 已脱敏处理 |
| 日志不泄露完整用户 ID | ✅ | 仅显示前 4 位 |
| 错误信息不暴露内部结构 | ✅ | 统一友好提示 |
| 附件 fileId 脱敏 | ✅ | 显示为 [REDACTED] |
| 配置验证前置 | ✅ | 执行前检查 |
| 无硬编码凭证 | ✅ | 全部从配置读取 |

---

## v2.4.1 (2026-03-11) - 审批详情字段优化

---

## v2.4.0 (2026-03-11) - 新增审批详情查询

### ✨ 新增功能

- ✅ **新增 get_task_details 工具**
  - 查询审批单完整详情
  - 显示申请人、申请时间、审批类型
  - 展示表单内容（请假类型、天数、事由等）
  - 显示审批流程记录（已审批人员和时间）
  - 支持查看当前审批状态

### 🔧 代码更新

- ✅ 更新 index.js - 添加 get_task_details 工具实现
- ✅ 更新 SKILL.md - 添加新工具使用说明和示例
- ✅ 更新 manifest.json - 添加新工具描述

---

## v2.3.0 (2026-03-11) - ClawHub 规范更新

### ✨ 新增功能

- ✅ 更新 SKILL.md 格式，符合 ClawHub 最新规范
  - 添加 YAML frontmatter（name 和 description）
  - 完善触发条件说明
  - 添加详细的使用示例和错误处理说明

- ✅ 新增 references 文档目录
  - `api-docs.md`: 完整的 API 接口文档和错误码说明
  - `configuration.md`: 详细的配置指南和常见问题解答

- ✅ 新增 .clawhub/manifest.json
  - 完整的插件元数据
  - 工具列表和配置 Schema
  - 分类和平台信息

- ✅ 更新 openclaw.plugin.json
  - 添加 keywords、author、license 等元数据
  - 添加 scripts 配置
  - 添加 repository 信息
  - 添加 additionalProperties: false 约束

### 📝 文档改进

- ✅ 重写 README.md
  - 更清晰的功能特性说明
  - 快速开始指南
  - 完整的目录结构说明
  - 开发和发布流程

- ✅ 更新 SKILL.md
  - 添加执行前必读提示
  - 快速索引表格
  - 核心工作流程说明
  - 配置说明和获取方式
  - 工具详细参数
  - 使用示例
  - 常见问题解答

### 🔧 技术改进

- ✅ 统一版本号：所有配置文件统一为 2.3.0
- ✅ 规范化目录结构：符合 ClawHub Skill 规范
- ✅ 添加配置验证：additionalProperties: false 防止错误配置

### 📚 参考文档

#### API 文档 (references/api-docs.md)
- 完整的 API 接口说明
- 请求/响应示例
- 错误码详解
- 最佳实践代码示例

#### 配置指南 (references/configuration.md)
- 分步配置教程
- 配置文件位置说明
- 安全建议
- 常见问题 FAQ
- 环境变量配置示例

---

## 之前的版本

### v2.2.0
- 从配置文件读取插件配置
- 支持 openclaw.json 配置方式

### v2.1.0
- 适配 OpenClaw 2026.3.2+ 版本
- 改进错误处理

### v2.0.0
- 初始版本
- 支持查询待办和执行审批

---

## 升级指南

### 从 v2.2.0 升级到 v2.3.0

1. **备份现有配置**
   ```bash
   cp -r ~/.openclaw/extensions/dingtalk-approval ~/.openclaw/extensions/dingtalk-approval.bak
   ```

2. **更新插件**
   ```bash
   cd ~/.openclaw/extensions/dingtalk-approval
   git pull  # 或手动替换文件
   ```

3. **验证配置**
   - 检查 `openclaw.json` 配置是否正确
   - 重启 OpenClaw
   - 测试查询待办功能

4. **查看新文档**
   - 阅读更新的 [SKILL.md](SKILL.md)
   - 参考 [references/configuration.md](references/configuration.md) 解决配置问题

### 兼容性说明

- ✅ **向后兼容**：v2.3.0 完全兼容 v2.2.0 的配置格式
- ✅ **配置无变化**：无需修改 openclaw.json 配置
- ✅ **API 无变化**：工具接口保持一致

---

## 发布到 ClawHub

```bash
# 1. 验证插件结构
openclaw plugins validate dingtalk-approval

# 2. 打包插件
openclaw plugins pack dingtalk-approval

# 3. 发布到 ClawHub
openclaw plugins publish dingtalk-approval
```

发布后，用户可以通过以下命令安装：

```bash
openclaw plugins install dingtalk-approval
```

---

## 反馈与支持

如有问题或建议，请：
1. 查看 [references/configuration.md](references/configuration.md) 常见问题
2. 查看 [references/api-docs.md](references/api-docs.md) API 文档
3. 联系作者：Yang

---

**最后更新**: 2026-03-11
