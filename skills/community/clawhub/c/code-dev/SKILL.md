---
name: code-dev
displayName: 🔧 代码开发
description: |
  规范的 Git 开发流程：分支管理 → 开发 → PR → Review → 合并。
  支持新 feature 开发和 bug 修复，强制禁止直接推送到 main。
  
  **触发条件（需同时满足）**：
  1. 用户要求"开发"、"实现"、"新功能"、"修复"、"提交 PR"
  2. 预估工作量 > 30 分钟 **或** 涉及 > 3 个文件
  
  **简单修改不触发**：
  - 单文件小改动（如修复 typo、正则表达式）
  - 配置文件更新
  - 文档修改
author: LuciusCao
license: MIT
version: 1.2
tags:
  - git
  - workflow
  - development
  - pr
  - code-review
repository: https://github.com/LuciusCao/openclaw-skills/tree/main/code-dev
compatibility: |
  Required tools: git, gh (GitHub CLI)
  Optional env: GITHUB_TOKEN (for GitHub authentication)
  Permissions: read/write current working directory, execute git and gh commands
metadata:
  openclaw:
    emoji: "🔀"
    category: development
---

# Git Workflow Skill

**安全的 Git 开发流程，通过 Subagent 执行。**

---

## ⚠️ 核心规则（不可违反）

```
┌─────────────────────────────────────────────────────────┐
│  ❌ 禁止直接推送到 main 分支                              │
│  ❌ 禁止跳过 PR 流程                                     │
│  ❌ 禁止在未理解代码库的情况下开发新功能                    │
│  ❌ 禁止在未找到 Bug 根因的情况下修复 Bug                  │
│                                                          │
│  ✅ 必须从 develop 创建新分支                             │
│  ✅ 必须通过 PR 合并到 develop                            │
│  ✅ 必须使用 code-review 技能审查代码                     │
└─────────────────────────────────────────────────────────┘
```

**安全提示：** 本 skill 应在项目根目录（git 仓库）下执行，cwd 会被限制在项目目录内。

---

## 🔍 触发判断（重要！）

**执行任何代码修改前，先评估是否触发此技能：**

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 用户是否使用了触发词？                           │
│  - "开发"、"实现"、"新功能"、"修复"、"提交 PR"            │
│                                                          │
│  Step 2: 评估复杂度                                      │
│  - 预估工作量 > 30 分钟？                                │
│  - 涉及 > 3 个文件？                                     │
│                                                          │
│  判断：                                                  │
│  ✅ 触发词 + (高复杂度 OR 多文件) → 使用此技能            │
│  ❌ 无触发词 或 简单修改 → 直接执行                       │
└─────────────────────────────────────────────────────────┘
```

**简单修改示例（不触发）**：
- 修复正则表达式（1 文件，5 分钟）
- 修改配置文件（1 文件，2 分钟）
- 文档 typo 修复（1 文件，1 分钟）

**复杂修改示例（触发）**：
- 新增功能模块（3+ 文件，1+ 小时）
- 重构架构（5+ 文件，2+ 小时）
- 复杂 Bug 修复（需要调试定位，30+ 分钟）

---

## 执行方式

**⚠️ 所有开发任务必须通过 Subagent 执行：**

```javascript
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  task: "{任务描述}"
});
```

**模型配置（可选）：**
- 默认使用系统配置的模型
- 如需指定模型，可在任务描述中说明，例如：`使用 thinking 模式审查代码`

---

## 完整流程

### Phase 1: 任务分析

```
1. 确定任务类型（feature / fix / docs / refactor）
2. 生成分支名称（feature/xxx, fix/xxx）
3. 确认目标分支 = develop（永远是 develop！）
```

### Phase 2: 代码库理解（Feature 必须执行）

**⚠️ 对于新 Feature，必须先充分理解当前代码库：**

```
┌─────────────────────────────────────────────────────────┐
│  检查清单：                                              │
│                                                          │
│  □ 是否已有类似的 helper/util 方法？                      │
│  □ 会影响哪些现有功能？                                   │
│  □ 需要修改哪些文件？                                     │
│  □ 哪些代码是不必要修改的？                               │
│                                                          │
│  避免：                                                  │
│  ❌ 重复实现 helper/util 方法                             │
│  ❌ 影响当前功能                                          │
│  ❌ 修改不必要的代码                                      │
└─────────────────────────────────────────────────────────┘
```

**执行步骤**：
1. 搜索相关代码文件（grep, find）
2. 阅读相关模块的实现
3. 识别可复用的 helper/util
4. 确定最小修改范围

### Phase 3: Bug 根因调研（Fix 必须执行）

**⚠️ 对于 Bug 修复，必须完全充分调研找到 Bug 的产生原因：**

```
┌─────────────────────────────────────────────────────────┐
│  调研清单：                                              │
│                                                          │
│  □ Bug 的具体表现是什么？                                 │
│  □ Bug 在什么条件下触发？                                 │
│  □ Bug 的根因在哪里？（代码位置）                          │
│  □ 修复方案是什么？是否会影响其他功能？                     │
│                                                          │
│  禁止：                                                  │
│  ❌ 在未找到根因的情况下修复                               │
│  ❌ 只修复表面症状而不修复根因                             │
└─────────────────────────────────────────────────────────┘
```

**执行步骤**：
1. 复现 Bug（如果能）
2. 定位 Bug 代码位置
3. 分析根因
4. 设计修复方案
5. 评估影响范围

### Phase 4: 分支创建

```bash
# 1. 确保 develop 是最新的
git checkout develop
git pull origin develop

# 2. 创建新分支（规范命名）
git checkout -b {type}/{name}

# 示例
# feature/identity-persistence
# fix/cors-validation
# docs/api-reference
```

### Phase 5: 开发实施

**必须包含**：
- ✅ 代码实现（最小修改范围）
- ✅ 单元测试
- ✅ 文档更新（API、README、CHANGELOG）
- ✅ 类型检查通过
- ✅ Lint 通过

**注意业务边界**：
- 只修改必要的代码
- 不影响无关功能
- 测试覆盖新逻辑和边界情况

### Phase 6: Code Review（必须执行）

**⚠️ 实现完成后，必须使用 code-review 技能进行自动审查：**

```javascript
// 触发 code-review skill
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  task: `使用 code-review 技能审查当前变更：
         - 分支: {branchName}
         - 对比: develop...HEAD`
});
```

**审查循环**：
1. 运行 code-review
2. 修复发现的问题
3. 再次审查，直到无新问题

### Phase 7: 提交 PR

**审查通过后提交 PR 到 develop：**

```bash
# 推送分支
git push origin {branchName}

# 创建 PR
gh pr create --base develop --head {branchName} \
  --title "{type}: {简短描述}" \
  --body "{PR 描述}"
```

**PR 描述模板**：
```markdown
## 变更内容

- 变更 1
- 变更 2

## 代码库理解（Feature）

- 已有的 helper/util：xxx
- 影响的功能：xxx
- 最小修改范围：xxx

## Bug 根因分析（Fix）

- Bug 表现：xxx
- 触发条件：xxx
- 根因位置：xxx
- 修复方案：xxx

## 测试

- [ ] 单元测试通过
- [ ] 类型检查通过
- [ ] Lint 通过
- [ ] Code Review 通过

## 相关 Issue

Closes #{issue-number}
```

---

## 流程结束

**提交 PR 后流程结束。**

后续由用户决定：
- 手动 Review PR
- 让其他 Agent Review PR
- 合并 PR

---

## 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| Feature | `feature/{name}` | `feature/identity-persistence` |
| Fix | `fix/{name}` | `fix/cors-validation` |
| Docs | `docs/{name}` | `docs/api-reference` |
| Refactor | `refactor/{name}` | `refactor/message-queue` |

**命名规则**：
- 使用 kebab-case（小写 + 连字符）
- 简短但描述性强

---

## Commit Message 规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
{type}({scope}): {description}

[optional body]

[optional footer]
```

**类型**：
| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖 |

---

## Subagent Task 模板

**启动开发任务时使用此模板：**

```javascript
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  cwd: "{projectDir}",
  task: `你是 Git Workflow 开发助手。

## 任务信息
- 类型：{feature|fix}
- 描述：{taskDescription}
- 分支名称：{branchName}

## ⚠️ 如果是 Feature，必须先理解代码库：

1. 搜索相关代码文件
2. 阅读相关模块实现
3. 识别可复用的 helper/util
4. 确定最小修改范围

避免：
- 重复实现 helper/util 方法
- 影响当前功能
- 修改不必要的代码

## ⚠️ 如果是 Fix，必须先找到 Bug 根因：

1. 复现 Bug（如果能）
2. 定位 Bug 代码位置
3. 分析根因
4. 设计修复方案
5. 评估影响范围

## 开发流程

1. 从 develop 创建分支：{branchName}
2. 实现变更（最小修改范围）
3. 编写测试
4. 更新文档
5. 运行检查（typecheck, lint, test）

## 完成后

1. 使用 code-review 技能审查代码
2. 修复发现的问题
3. 再次审查，直到无新问题
4. 提交 PR 到 develop

## 安全规则

- ❌ 不要推送到 main
- ❌ 不要跳过 code-review
- ✅ 必须从 develop 创建分支
- ✅ 必须 PR 到 develop`
});
```

---

## Key Points

1. **Subagent 执行** - 所有开发任务通过 subagent 完成，使用系统默认模型
2. **Feature 先理解** - 避免重复实现、影响现有功能
3. **Fix 先找根因** - 禁止只修复表面症状
4. **develop 分支** - 所有 PR 都合并到 develop
5. **Code Review** - 实现完成后必须审查
6. **PR 结束流程** - 提交 PR 后等待人工或其他 Agent Review