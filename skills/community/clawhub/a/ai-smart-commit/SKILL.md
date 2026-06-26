---
name: ai-smart-commit
description: |
  智能 Git 提交信息生成工具。根据代码 diff 自动生成规范的 commit message、PR 描述和 Release Notes。

  **当以下情况时使用此 Skill**:
  (1) 需要根据代码变更生成 commit message
  (2) 需要编写 PR/MR 描述
  (3) 需要生成 Release Notes / Changelog
  (4) 用户提到"commit"、"提交"、"PR描述"、"changelog"、"发布说明"
  (5) 想让 git log 更规范、更有价值
  (6) 需要分析代码变更的影响范围
metadata:
  openclaw:
    emoji: "📝"
    version: "1.0.0"
    author: "小摩事业部"
    tags: ["git", "commit", "pr", "changelog", "developer-tools", "chinese"]
---

# 📝 Smart Commit — 智能 Git 提交信息生成

> 让每一次 commit 都有灵魂，不再 `git commit -m "fix bug"`。

## 🎯 核心功能

1. **Commit Message 生成** — 分析 diff，输出符合 Conventional Commits 规范的提交信息
2. **PR 描述生成** — 自动生成结构化的 Pull Request 描述（变更摘要、影响范围、测试建议）
3. **Release Notes 生成** — 汇总多个 commit，生成面向用户的版本更新说明
4. **变更影响分析** — 评估代码变更的风险等级和影响范围

## 📋 使用方式

### 模式一：Commit Message 生成

当用户提供代码 diff 或描述变更内容时，执行以下流程：

```
1. 读取 diff 或变更描述
2. 分析变更类型（feat/fix/refactor/docs/style/test/chore/perf）
3. 识别影响范围（哪些模块/文件受影响）
4. 判断是否为 BREAKING CHANGE
5. 生成 commit message
```

**输出格式：**
```
<type>(<scope>): <description>

[可选 body：详细说明为什么这样做]

[可选 footer：BREAKING CHANGE / 关联 issue]
```

### 模式二：PR 描述生成

当用户要求生成 PR 描述时：

```
1. 收集所有相关 commit
2. 按功能分组（新功能/修复/重构/文档）
3. 评估风险等级
4. 生成结构化 PR 描述
```

**输出格式：**
```markdown
## 📌 变更摘要
[一段话概括这个 PR 做了什么]

## 🔧 主要变更
- **[类型]** 具体变更1
- **[类型]** 具体变更2
- ...

## 📁 影响范围
- `path/to/file` — 变更说明
- ...

## ⚠️ 风险评估
[低/中/高] — 说明原因

## ✅ 测试建议
- [ ] 测试项1
- [ ] 测试项2

## 🔗 相关
- Closes #xxx
```

### 模式三：Release Notes 生成

当用户要求生成 Release Notes 或 Changelog 时：

```
1. 收集版本区间内所有 commit
2. 按类型分组（Features/Bug Fixes/Breaking Changes/其他）
3. 过滤无意义的 commit（如 "wip"、"fix typo"）
4. 生成面向用户的版本说明
```

**输出格式：**
```markdown
## [版本号] - 日期

### ✨ 新功能
- 具体功能1
- 具体功能2

### 🐛 修复
- 具体修复1

### 💥 破坏性变更
- 具体变更及迁移指南

### 🔧 其他改进
- 具体改进
```

### 模式四：快速模式

当用户只是快速问"帮我写个 commit message"时：

直接输出一行或三行 commit message，不输出额外解释。提供 2-3 个选项让用户选择。

---

## 🧠 Commit 规范

### Type 枚举

| Type | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 login support` |
| `fix` | 修复 bug | `fix(api): handle null response from upstream` |
| `refactor` | 重构（不改变功能） | `refactor(utils): extract date formatting to helper` |
| `docs` | 文档变更 | `docs(readme): update installation guide` |
| `style` | 代码格式（不影响逻辑） | `style(lint): fix indentation in auth module` |
| `test` | 测试相关 | `test(auth): add unit tests for token refresh` |
| `chore` | 构建/工具链 | `chore(deps): upgrade webpack to v5` |
| `perf` | 性能优化 | `perf(query): add index for user search` |
| `ci` | CI/CD 变更 | `ci(github): add macOS build target` |
| `build` | 构建系统 | `build(webpack): configure code splitting` |

### Scope 建议

Scope 应该是模块名或功能域，不要用文件名：

- ✅ `auth`, `api`, `db`, `ui`, `payment`
- ❌ `index.js`, `controller`, `model`

### 风格规则

1. **subject 行**：不超过 72 字符，用祈使句（"add" 不用 "added"）
2. **body**：说明「为什么」而不是「做了什么」（diff 已经展示了做了什么）
3. **中文项目**：subject 可以用中文，但 type 和 scope 保持英文
4. **避免无意义 commit**：不要生成 `fix: update code` 这种废话

### 中英文选择

根据项目语言自动判断：
- 项目 README/代码注释是中文 → commit message 用中文
- 项目是英文 → commit message 用英文
- 用户明确要求 → 跟用户走

---

## 🔄 变更分析规则

### 影响范围判定

| 变更模式 | 影响范围 | 风险等级 |
|---------|---------|---------|
| 只改文档/注释 | 低 | 🟢 低 |
| 新增独立功能模块 | 局部 | 🟢 低 |
| 修改工具函数/公共组件 | 广泛 | 🟡 中 |
| 修改 API 接口/数据模型 | 全局 | 🔴 高 |
| 修改配置文件/构建脚本 | 全局 | 🟡 中 |
| 修改认证/权限逻辑 | 全局 | 🔴 高 |
| 数据库 migration | 数据层 | 🔴 高 |

### BREAKING CHANGE 判断

以下情况标记为 BREAKING CHANGE：
- 删除或重命名公开 API
- 修改函数签名（参数/返回值）
- 修改配置文件格式
- 修改数据库 schema
- 升级主要依赖版本

---

## 💡 使用技巧

### 自动获取 diff

如果用户在工作目录中有 git 仓库，主动建议：

```bash
# 查看暂存区变更
git diff --cached

# 查看工作区变更
git diff

# 查看最近一次 commit
git show HEAD
```

### 批量 commit 整理

当用户说"帮我整理一下这周的 commit"时：
1. 用 `git log --oneline --since="1 week ago"` 获取 commit 列表
2. 合并同类 commit
3. 生成整理后的 commit message 建议

### 与代码审查结合

生成 commit message 后，可以顺便做：
- 检查是否有遗漏的文件
- 建议需要补充的测试
- 提示潜在的副作用

---

## 📌 质量检查清单

生成的 commit message 必须满足：
- [ ] Type 准确反映变更性质
- [ ] Scope 合理（不过宽也不过窄）
- [ ] Subject 清晰描述了"做了什么"
- [ ] Body 解释了"为什么这样做"（如果需要）
- [ ] 没有废话（"update code"、"fix stuff"）
- [ ] 中英文与项目风格一致
