# 📦 发布到 ClawHub 操作指南

## ✅ 清理验证已完成

已完成以下清理：
- ✅ 删除 `.env` 文件
- ✅ 删除 `flomo_browser_data/` 目录
- ✅ 删除 `flomo_downloads/` 目录
- ✅ 删除 `.flomo_sync_state.json` 文件
- ✅ 替换文档中的个人信息

---

## 🚀 发布步骤

### 步骤 1：安装 ClawHub CLI

选择一种方式安装：

```bash
# 方式1：使用 npm（推荐）
npm i -g clawhub

# 方式2：使用 pnpm
pnpm add -g clawhub

# 方式3：使用 yarn
yarn global add clawhub
```

**如果没有 Node.js，需要先安装：**

```bash
# macOS（使用 Homebrew）
brew install node

# 或者从官网下载：https://nodejs.org/
```

---

### 步骤 2：登录 ClawHub

```bash
# 浏览器登录（推荐）
clawhub login

# 或使用 API Token
clawhub login --token YOUR_API_TOKEN
```

**获取 API Token：**
1. 访问 https://clawhub.ai
2. 使用 GitHub 账号登录
3. 在设置中生成 API Token

---

### 步骤 3：进入 Skill 目录

```bash
cd /Users/ryanbzhou/.box/Workspace/output/7c274e87-4317-441d-8a4c-f34a0dfcac62/flomo-to-obsidian
```

---

### 步骤 4：发布 Skill

```bash
clawhub publish . \
  --slug flomo-to-obsidian \
  --name "Flomo to Obsidian Sync Tool" \
  --version 2.0.0 \
  --changelog "v2.0: Added safe mode with browser session login (no password storage), improved security, fixed HTML file detection, tested with 514 notes successfully. Features: automatic sync, incremental updates, attachment support, dual-link support, comprehensive documentation (7 detailed guides), two sync modes (safe mode for personal use, password mode for automation)." \
  --tags latest \
  --accept-license-terms
```

**或者使用快捷脚本：**

```bash
./publish.sh
```

---

### 步骤 5：验证发布

```bash
# 搜索你的 skill
clawhub search "flomo obsidian"

# 查看详情
clawhub show flomo-to-obsidian
```

---

## 📋 发布参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--slug` | `flomo-to-obsidian` | Skill 的唯一标识符 |
| `--name` | `Flomo to Obsidian Sync Tool` | 显示名称 |
| `--version` | `2.0.0` | 版本号 |
| `--tags` | `latest` | 标签 |
| `--changelog` | 见下方 | 更新日志 |

### 推荐的 Changelog

```
v2.0: Added safe mode with browser session login (no password storage), improved security, fixed HTML file detection, tested with 514 notes successfully. Features: automatic sync, incremental updates, attachment support, dual-link support, comprehensive documentation (7 detailed guides), two sync modes (safe mode for personal use, password mode for automation).
```

**精简版（如果太长）：**

```
v2.0: Added safe mode (no password storage), improved security, 514 notes tested. Features: auto-sync, incremental updates, attachments, dual-links, 7 guides, 2 modes.
```

---

## 🌐 发布后

### 访问你的 Skill

发布成功后，你的 Skill 将出现在：
- **ClawHub 网站**：https://clawhub.ai/skills/flomo-to-obsidian
- **搜索结果**：用户可以通过 `clawhub search flomo` 找到

### 用户安装方式

```bash
# 搜索
clawhub search "flomo"

# 安装
clawhub install flomo-to-obsidian

# 在 OpenClaw 中使用
"帮我同步 flomo 到 Obsidian"
```

---

## 🔄 更新 Skill

如果需要发布新版本：

```bash
clawhub publish . \
  --slug flomo-to-obsidian \
  --version 2.1.0 \
  --changelog "你的更新说明" \
  --tags latest
```

---

## 📊 推广建议

### 1. 在 GitHub 上创建 Release

如果你的 skill 有 GitHub 仓库：
1. 创建 Release (v2.0.0)
2. 添加详细的 Release Notes
3. 包含使用截图或 GIF

### 2. 在社区分享

- OpenClaw Discord
- Twitter/X
- 知乎
- 掘金
- V2EX

### 3. 写一篇教程

标题建议：
- "如何将 Flomo 笔记自动同步到 Obsidian"
- "Flomo + Obsidian 完美同步方案"
- "不保存密码的安全同步方案"

---

## 🎯 SEO 关键词

在推广时使用这些关键词：

**中文：**
- flomo 转 Obsidian
- flomo 同步工具
- flomo 笔记导出
- Obsidian 导入 flomo
- flomo 自动同步
- 笔记迁移工具

**英文：**
- flomo to obsidian
- flomo sync tool
- flomo export
- obsidian import
- note migration
- markdown converter

---

## ❓ 常见问题

### Q1: 发布失败怎么办？

**检查以下几点：**
- ✅ 是否已登录？运行 `clawhub whoami`
- ✅ SKILL.md 文件是否存在？
- ✅ 版本号格式是否正确？（major.minor.patch）
- ✅ 网络连接是否正常？

### Q2: 如何删除已发布的 Skill？

```bash
clawhub delete flomo-to-obsidian --yes
```

### Q3: 如何查看发布状态？

```bash
# 查看你发布的所有 skills
clawhub whoami

# 搜索你的 skill
clawhub search "flomo-to-obsidian"
```

### Q4: 版本号如何管理？

使用语义化版本号：
- **Major (2.0.0)**：重大功能更新、不兼容变更
- **Minor (2.1.0)**：新增功能、向后兼容
- **Patch (2.0.1)**：Bug 修复、小改进

---

## 📞 获取帮助

如果遇到问题：
1. 查看 ClawHub 文档：https://docs.clawhub.ai
2. 在 OpenClaw Discord 提问
3. 查看 ClawHub GitHub Issues

---

## 🎉 恭喜！

完成发布后，你将成为 OpenClaw 社区的贡献者！

**Skill 特点：**
- 🔐 安全模式（不保存密码）
- 🤖 自动同步
- 📝 完整文档
- ✅ 经过充分测试

---

## 📝 发布检查清单

最后确认：

- [ ] ClawHub CLI 已安装
- [ ] 已登录 ClawHub
- [ ] 已清理所有个人数据
- [ ] SKILL.md 文件存在且格式正确
- [ ] README.md 说明清晰
- [ ] 版本号正确（2.0.0）
- [ ] Changelog 准备好
- [ ] 网络连接正常

**一切就绪！执行发布命令吧！** 🚀

```bash
clawhub publish . \
  --slug flomo-to-obsidian \
  --name "Flomo to Obsidian Sync Tool" \
  --version 2.0.0 \
  --tags latest \
  --accept-license-terms
```

祝发布顺利！🎊
