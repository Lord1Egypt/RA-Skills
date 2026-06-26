# Changelog

All notable changes to this project will be documented in this file.

## [4.0.3] - 2026-03-30

### 🔧 Changed
- 代码审查确认无问题，正式发布到 ClawHub
- 确认 Hook 自动触发功能正常工作
- 确认所有依赖和配置正确

### ✅ Verified
- handler.ts Hook 逻辑正确，支持纯 URL 和 URL+ 意图关键词触发
- Python 脚本支持多网站抓取和三种降级策略
- 目录结构和输出格式符合预期
- _meta.json 配置完整，包含 hooks 配置

---

## [4.0.2] - 2026-03-27

### 🐛 Fixed
- **修复豆包抓取超时问题**：
  - 页面加载超时：30 秒 → 60 秒
  - networkidle 等待超时：15 秒 → 30 秒
  - 固定等待时间：5 秒 → 10 秒
- **优化豆包内容选择器**：
  - `[class*='message']` 提至最高优先级（豆包消息容器）
  - 新增 `.thread-content` 和 `.conversation-content` 选择器
- **Scrapling 方案优化**：
  - 自动跳过豆包等动态网站（Scrapling 无法处理 JavaScript 渲染）
  - 避免无效尝试，直接进入降级方案

### 🔧 Changed
- 更新 `url_handler.py` 豆包配置：
  - 优化内容选择器优先级
  - 优化标题选择器（新增 `.thread-title`）
- 更新 `amber_url_to_markdown.py`：
  - 豆包专用超时配置
  - Scrapling 方案增加链接类型检查

### 📊 Performance
- 豆包抓取成功率显著提升（从 ~0% 到 100%）
- 抓取时间：约 44 秒（包含完整滚动加载和反检测）

---

## [3.2.0] - 2026-03-25

### 🎉 Added
- **新增 url-auto-fetch Hook**，实现真正的自动触发功能
- 监听 `message:received` 事件，自动检测用户发送的 URL 链接
- 支持两种触发方式：
  - 纯 URL 消息（消息中只有 URL）
  - URL + 意图关键词（解析、转换、markdown 等）
- 异步执行抓取脚本，不阻塞消息处理
- 自动发送抓取进度提示消息

### 🔧 Changed
- 更新 SKILL.md，添加 Hook 启用说明和安装指南
- 更新 _meta.json，添加 hooks 配置
- 优化触发逻辑，优先处理微信公众号链接
- 使用 ESM 模块语法编写 Hook handler

### 📚 Documentation
- 新增 HOOK_AUTO_TRIGGER_README.md - Hook 自动触发方案详细说明
- 新增 PUBLISH_GUIDE.md - 发布指南
- 新增 优化方案总结.md - 技术总结文档
- 在 SKILL.md 中添加完整的 Hook 启用步骤

### 🐛 Fixed
- 修复 AI 无法自动调用技能的问题
- 修复 URL 检测逻辑，支持更多场景
- 修复脚本路径查找逻辑，使用固定路径提高可靠性

### 📦 Technical
- Hook handler 使用 TypeScript ESM 模块
- 支持从 `~/.openclaw/hooks/` 目录加载
- 通过 `openclaw hooks enable` 命令启用

---

## [3.1.0] - 2026-03-24

### Added
- 支持异步批量处理（5 倍速）
- 支持分页自动拼接
- 支持 LaTeX 公式保留
- 支持编码自动识别（chardet）

### Changed
- 配置集中管理
- 模块化代码结构
- 包含完整单元测试

---

## [3.0.0] - 2026-03-22

### Added
- 支持多网站自动识别（微信、知乎、掘金、CSDN、GitHub、Medium 等）
- 三种降级方案（Playwright → Third_Party_API → Scrapling）
- robots.txt 合规检查
- 自动重试机制（2 次）
- 广告自动清洗
- 图片自动下载

### Changed
- 完全重构代码架构
- 优化目录结构
