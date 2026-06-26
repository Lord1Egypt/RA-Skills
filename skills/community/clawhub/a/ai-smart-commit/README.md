# Smart Commit 📝 — 智能 Git 提交信息生成

> 让每一次 commit 都有灵魂。

## 它是什么？

Smart Commit 是一个 [OpenClaw](https://openclaw.ai) Skill，为你的 AI Agent 添加智能 Git 提交信息生成能力。

给它一段代码 diff 或变更描述，它就能输出：
- 符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范的 commit message
- 结构化的 PR/MR 描述
- 面向用户的 Release Notes
- 变更影响分析和风险评估

## 特性

- ✅ **8 种 commit type** 精准识别（feat/fix/refactor/docs/style/test/chore/perf）
- ✅ **自动推断 scope** — 从文件路径和变更内容智能判断
- ✅ **中英文自适应** — 根据项目语言自动选择
- ✅ **BREAKING CHANGE 检测** — 自动标记破坏性变更
- ✅ **风险评估** — 🟢🟡🔴 三级风险标注
- ✅ **4 种模式** — commit / PR 描述 / Release Notes / 快速模式

## 安装

```bash
# 复制到你的 OpenClaw Skills 目录
cp -r smart-commit/ ~/.openclaw/workspace/skills/
```

## 使用

### 生成 Commit Message

直接给 Agent 发送你的代码 diff：

```
帮我写个 commit message

diff --git a/auth.go b/auth.go
+func OAuth2Login(provider string) error {
+    // OAuth2 login implementation
+}
```

Agent 会输出：
```
feat(auth): add OAuth2 social login support

Support multiple OAuth2 providers for social login.
Users can now sign in via configured providers.
```

### 生成 PR 描述

```
帮我写这个 PR 的描述，涉及这些 commit：
- feat(search): add full-text search
- fix(search): handle empty query
- test(search): add integration tests
```

### 生成 Release Notes

```
帮我把 v1.2.0 到 v1.3.0 的 commit 整理成 release notes
```

### 快速模式

```
帮我写个 commit message，改了登录页面样式
```

输出 2-3 个选项让你快速选择。

## 配置

不需要配置。Skill 会自动检测：
- 项目语言（决定中英文）
- 现有 commit 规范（commitlint/conventional commits）
- PR 模板（如果有的话）

## 兼容性

- OpenClaw >= 2026.5
- 适用于所有编程语言
- 支持 Git / Mercurial / SVN（按需适配）

## License

MIT

---

由 [小摩事业部](https://github.com/xiaomo-dev) 出品
