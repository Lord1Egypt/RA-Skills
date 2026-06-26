# Publishing Guide

本文档说明如何将 `ai-market-research` 技能发布到 GitHub 和 ClawHub。

## 📦 Release 准备

### 1. 本地检查

```bash
cd ~/.openclaw/workspace/.agents/skills/ai-market-research

# 验证所有文件存在
ls -la SKILL.md README.md LICENSE Requirements.md CHANGELOG.md CONTRIBUTING.md .gitignore bin/ engine.py

# 本地测试运行
bin/run --topic "OpenClaw" --depth quick --sources "https://openclaw.ai" --compare_previous false

# 检查输出
ls -la output/ai-market-research/
```

### 2. 更新版本号

编辑 `SKILL.md` 的 frontmatter：
```yaml
version: 0.1.0  # → 0.2.0 或其他
```

同时更新 `CHANGELOG.md`（为新版本添加条目）。

### 3. 提交到 Git

```bash
cd ~/.openclaw/workspace/.agents/skills/ai-market-research

git init
git add .
git commit -m "chore: prepare v0.1.0 release"
```

## 🚀 GitHub 发布

### 创建远程仓库

1. 登录 GitHub
2. 点击 New repository
3. 仓库名：`ai-market-research-skill`
4. 选择 Public（开源）或 Private
5. **不要** 初始化 README、.gitignore、LICENSE（已有本地）
6. 创建仓库

### 关联并推送

```bash
# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/ai-market-research-skill.git
git branch -M main
git push -u origin main
```

### 创建 Release

1. 进入仓库 → Releases → Create a new release
2. Tag 版本：`v0.1.0`
3. Release title: `AI Market Research Skill v0.1.0`
4. Description: 复制 `CHANGELOG.md` 中对应版本内容
5. 可选：附加二进制包（无需）
6. Publish release

✅ GitHub 发布完成！用户可以通过：
```bash
git clone https://github.com/YOUR_USERNAME/ai-market-research-skill.git \
  ~/.openclaw/workspace/.agents/skills/ai-market-research
```

---

## 🏛️ ClawHub 上架（可选）

ClawHub 是 OpenClaw 官方技能市场。上架后用户可一键安装。

### 提交 PR

1. Fork [openclaw/skills](https://github.com/openclaw/skills) 仓库
2. 将本技能复制到 `skills/ai-market-research/` 目录
3. 提交 PR 并填写：
   - 技能名称：`ai-market-research`
   - 简要描述
   - 依赖说明（crawl4ai + trendradar 需用户自备）
   - 测试情况（已手动测试）
4. 等待审核（通常 1-3 天）

### 审核要点

- ✅ 结构符合 OpenClaw Skill Standard
- ✅ 文档完整（README + SKILL.md）
- ✅ 许可证清晰（MIT）
- ✅ 无敏感信息硬编码
- ✅ 依赖声明明确

通过后，用户将能在 ClawHub 中搜索安装。

---

## 📢 宣传建议

- 在 OpenClaw Discord 社区宣布发布
- 提交到awesome-openclaw 列表（如存在）
- 撰写使用案例博客/推文
- 添加 GitHub Topics: `openclaw`, `market-research`, `crawl4ai`, `trendradar`

---

**祝发布顺利！** 🎉

如有问题，请在仓库 Issues 中提问。
