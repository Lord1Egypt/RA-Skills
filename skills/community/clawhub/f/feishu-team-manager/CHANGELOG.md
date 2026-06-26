# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.3] - 2026-04-27

### Fixed
- 清理所有 Unicode 控制字符（U+FE0F、U+200D）以通过安全扫描
- 更新元数据（`_meta.json` / `SKILL.md`）显式声明凭据依赖
- 更新描述提及 Discord 可选支持，消除范围不匹配问题

## [2.3.1] - 2026-04-23

### Updated
- 更新微信和支付宝赞赏码图片：替换占位符为真实图片
- 图片托管：上传至Gitee图床，确保长期可访问

## [2.3.0] - 2026-04-22

### Added
- 自动化部署流程：检测到未创建 HR Agent 时自动部署
- 独立工作空间：为 HR 大姐头创建专属工作空间
- 技能平移：自动将管理技能同步到 HR 工作空间
- 路径兼容性：支持 `~/.openclaw/` 路径，兼容多用户环境

### Fixed
- 修复硬编码路径：将 `/root/.openclaw/` 改为 `os.path.expanduser("~/.openclaw/")`
- 修复变量未定义问题：`agent_id_normalized` 改为 `agent_name`

### Changed
- 优化配置注入逻辑：增加冲突检测和自动化自愈
- 改进错误处理：更清晰的错误提示和恢复方法
- 更新文档：添加捐赠支持和更详细的使用说明

## [2.0.0] - 2026-04-21

### Added
- 基于 2026-04-21 实践通过的"账户级路由"方案
- 独立身份管理：每个机器人对应飞书开放平台独立应用
- 精准路由绑定：通过 `accountId` 实现消息精准路由
- 自动化招聘流程：一键创建新 Agent 并绑定机器人

### Initial Release
- 核心功能：Agent 招聘、飞书机器人绑定、团队状态巡检
- 技能结构：index.js 主逻辑 + Python 辅助脚本
- 模板系统：HR 身份模板（IDENTITY/SOUL/AGENTS）
- 交互卡片：招聘通知和 HR 管理卡片