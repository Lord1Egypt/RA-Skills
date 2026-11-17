# Git 规范分析指引 | Git Spec Analyzer

> 指导 AI 分析项目 Git 规范，提取 `git-spec.md` 规范。

## 分析流程

1. **先读 `references/git-spec.md`** 了解条目编号
2. **读 `project_context.json`** 获取语言信息；用 `exec` 运行 git 命令获取分支/提交/hooks 信息（如 `git -C <project> log --oneline -30`、`git -C <project> branch`、`git -C <project> tag`）
3. **写入 `.code-spec/git-spec.md`**

## 各条目分析要点

### 分支管理 [GIT-01 ~ GIT-02]

#### [GIT-01] 分支命名
- 用 `exec` 运行 `git -C <project> branch` 和 `git -C <project> log --oneline -30` 获取当前分支和提交历史中的分支名
- 常见模式：feature/xxx, fix/xxx, hotfix/xxx, release/xxx, develop, main/master
- 是否有分支类型前缀

#### [GIT-02] 分支策略
- GitFlow (main/develop/feature/release/hotfix)
- Trunk-based (feature branch → main)
- GitHub Flow (feature branch → PR → main)

### 提交规范 [GIT-03 ~ GIT-04]

#### [GIT-03] Commit Message 格式
- 用 `exec` 运行 `git -C <project> log --oneline -30` 抽样 30 条，分析格式
- Conventional Commits：type(scope): description
  - type: feat/fix/docs/style/refactor/perf/test/chore/ci
  - scope：影响范围
- 是否有 subject 长度限制（默认 72 字符）
- body 和 footer 使用情况

#### [GIT-04] 提交粒度
- 观察 commit 消息内容，判断提交粒度
- 一次 commit 通常包含多少文件改动
- 是否有"WIP"/"fixup"等草案提交

### 合并/PR [GIT-05 ~ GIT-07]

#### [GIT-05] PR 标题格式
- 同 commit 格式还是更简洁
- 是否有自动化标签（如 `[WIP]`）

#### [GIT-06] PR 描述模板
- 检测 .github/PULL_REQUEST_TEMPLATE.md 或 .github/pull_request_template.md
- 模板包含哪些 section（背景/方案/测试/截图/checklist）

#### [GIT-07] Code Review
- 是否有 CODEOWNERS 文件
- PR 合并策略（squash/merge/rebase）
- 是否有必须的 reviewer 数量

### 工程化 [GIT-08 ~ GIT-10]

#### [GIT-08] Git Hooks
- 用 `exec` 检查 `.husky/` 目录和 `.git/hooks/` 目录中的文件
- pre-commit：做什么检查
- commit-msg：commitlint 规则
- pre-push：做什么检查

#### [GIT-09] lint-staged
- 用 `read` 读 `package.json` 中的 `lint-staged` 字段（或检查 `.lintstagedrc` 文件）
- 对哪些文件类型执行什么操作

#### [GIT-10] .gitignore 模式
- 用 `read` 读 `.gitignore` 文件
- 忽略目录：node_modules, dist, .env, .DS_Store
- 是否有项目特定的忽略项

### 发布 [GIT-11 ~ GIT-14]

#### [GIT-11] 版本号策略
- 用 `exec` 运行 `git -C <project> tag --sort=-creatordate` 获取 tag 列表
- 从 tag 分析版本号格式
- SemVer (major.minor.patch)
- 是否有预发布版本号（alpha/beta/rc）

#### [GIT-12] 发布分支
- 从 tag 关联分析发布分支
- release 分支生命周期

#### [GIT-13] Tag 命名
- 格式：v1.0.0 vs 1.0.0 vs release-1.0.0
- 轻量标签还是注释标签

#### [GIT-14] Release 流程
- changelog 生成方式（conventional-changelog / changesets）
- 自动化发布（CI/CD pipeline 触发）
- 发布审批流程
