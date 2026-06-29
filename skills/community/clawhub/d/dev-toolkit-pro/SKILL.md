---
name: "dev-toolkit-pro"
description: "全功能开发工具箱：Git/脚手架/CI-CD/测试/规范管理/代码审查/技术债务/依赖分析"
metadata:
  openclaw:
    emoji: "🔧"
    version: "2.0.0"
    author: "墨鱼精@g1776933879"
    tags: ["dev", "git", "scaffold", "ci-cd", "testing", "code-review"]
---

# 🔧 Dev Toolkit Pro — 全功能开发工具箱

> **slug**: `dev-toolkit-pro` | **安装**: `clawhub install @g1776933879/dev-toolkit-pro`

## 模块总览

| 模块 | 子命令 | 说明 |
|------|--------|------|
| 🪪 Git助手 | `git` | 提交/分支/PR/回滚 |
| 🏗️ 脚手架 | `scaffold` | 项目初始化/模板生成 |
| 🚀 CI/CD | `build` | 构建/部署/Docker |
| 🧪 测试 | `test` | 测试运行/覆盖率/质量检查 |
| ✨ 格式化 | `fmt` | 代码格式化/lint修复 |
| 🔍 代码审查 | `review` | 预提交检查/深度审查 |
| 📐 规范管理 | `spec` | 项目规范定制/冲突检测 |
| 🩺 错误诊断 | `diag` | 构建/运行时错误分析 |
| 💳 技术债务 | `debt` | 债务跟踪/报告生成 |
| 🔗 依赖分析 | `dep` | 依赖图谱/循环依赖/边界检查 |
| 📊 差异对比 | `diff` | 代码变更可视化 |
| 🛠️ 重构助手 | `refactor` | 重构建议/方案生成 |

---

## 1. 🪪 Git 助手

### 自动提交
```bash
dev-tk git commit "feat: 添加用户登录"
dev-tk git commit "fix: 修复空指针"
```
类型: `feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`

### 分支管理
```bash
dev-tk git branch        # 列出分支，提示合并/删除
dev-tk git squash        # 交互式rebase压缩提交
dev-tk git pr            # 创建PR（需gh CLI）
```

### 安全回滚
- 用 `git stash` 保存当前工作
- 用 `git revert` 代替 `git reset --hard`

---

## 2. 🏗️ 脚手架

### 快速初始化
```bash
dev-tk scaffold my-app node
dev-tk scaffold my-api python
dev-tk scaffold my-web vue --typescript --with-tests --with-ci
```

### 生成模板
| 语言 | 模板内容 |
|------|---------|
| Node.js | package.json, src/, test/, .gitignore, eslint |
| Python | pyproject.toml, src/, tests/, .venv, .gitignore |
| Vue/React | Vite配置, src/, test/, TS支持 |
| Go | go.mod, main.go, handlers/, tests/ |

---

## 3. 🚀 构建与部署

```bash
dev-tk build              # 自动检测语言并构建
dev-tk build --docker     # Docker构建
dev-tk deploy             # 部署检查清单
```

### 部署检查
- [ ] 构建成功
- [ ] 测试通过
- [ ] lint无错误
- [ ] 版本号已更新
- [ ] CHANGELOG更新
- [ ] 确认部署目标

---

## 4. 🧪 测试工具

```bash
dev-tk test               # 运行测试
dev-tk test --coverage    # 覆盖率报告
dev-tk test --watch       # 监听模式
```

### 质量标准
- 覆盖率 ≥ 80%
- 无 `.skip` 跳过测试
- 测试命名规范
- 公共函数必须测试

---

## 5. ✨ 格式化

```bash
dev-tk fmt                # 全量格式化
dev-tk fmt --check        # 仅检查不修改
```

自动检测项目类型并格式化：
- JS/TS: prettier + eslint
- Python: black + isort
- Go: gofmt
- Rust: rustfmt

---

## 6. 🔍 预提交审查（pre-commit）

### 触发
```bash
dev-tk review             # 审查当前修改
dev-tk review src/        # 审查指定目录
```

### P0 检查（必须通过）
- ✅ 编译/语法通过
- ✅ 无严重安全问题
- ✅ 无严重空指针风险
- ✅ 测试通过率 100%
- ✅ 无敏感信息泄露

### P1 检查（推荐通过）
- ⚠️ 代码规范遵循
- ⚠️ 覆盖率 > 80%
- ⚠️ 无重复代码
- ⚠️ 提交信息规范

### 输出示例
```
🔍 预提交检查
P0: ✅✅✅✅✅ (5/5)
P1: ✅✅✅⚠️✅ (4/5)
结论: ✅ 可以提交 (建议提升覆盖率至80%)
```

---

## 7. 📐 规范管理（spec）

```bash
dev-tk spec               # 查看规范菜单
dev-tk spec view          # 查看当前规范
dev-tk spec customize     # 定制项目规范
dev-tk spec conflict      # 检测规范冲突
```

### 定制内容
- 命名规范（camelCase / snake_case）
- 代码格式（缩进、引号、分号）
- 注释规范（JSDoc / docstring）
- 技术栈规范
- 目录结构规范

**输出文件**: `.ads/project-specs/naming.md` `.ads/project-specs/code-style.md`

---

## 8. 🩺 错误诊断（diag）

```bash
dev-tk diag               # 诊断最近错误
dev-tk diag --cmd "npm run build"  # 诊断指定命令
```

### 诊断流程
1. 收集错误信息（命令、错误输出、上下文）
2. 分析可能原因（带概率评估）
3. 执行诊断步骤（逐步排查）
4. 给出诊断结论 + 修复方案

---

## 9. 💳 技术债务（debt）

```bash
dev-tk debt               # 查看债务菜单
dev-tk debt list          # 列出债务
dev-tk debt add           # 添加债务
dev-tk debt report        # 生成报告
dev-tk debt fix TD-001    # 标记已修复
```

### 报告内容
- 债务清单（ID/描述/优先级/状态/预计工时）
- 按优先级分组
- 修复建议（按优先级排序）
- 趋势追踪

**输出文件**: `docs/tech-debt/YYYY-MM-DD-debt-report.md`

---

## 10. 🔗 依赖分析（dep）

```bash
dev-tk dep                # 完整依赖分析
dev-tk dep --check-cycle  # 仅检查循环依赖
dev-tk dep --check-boundary  # 仅检查边界违规
dev-tk dep --module=order-service  # 指定模块
dev-tk dep --format=mermaid  # 输出图谱
```

### 分析维度
| 维度 | 检查项 | 级别 |
|------|--------|------|
| 模块依赖 | 循环依赖、单向依赖 | 🔴 |
| 服务边界 | 跨服务数据库访问 | 🔴 |
| 包依赖 | 不合理依赖 | 🟡 |
| 类依赖 | 高耦合 | 🔵 |

**输出文件**: `docs/analysis/dependencies.md`

---

## 11. 📊 差异对比（diff）

```bash
dev-tk diff               # 对比工作区变更
dev-tk diff --staged      # 暂存区变更
dev-tk diff --commit=HEAD~1  # 最近提交
dev-tk diff --file=main.js  # 指定文件
```

### 报告内容
- 概览（新增/修改/删除文件数、行数统计）
- 文件变更详情（每文件diff摘要）
- 影响分析（影响模块、接口数、风险等级）

**输出文件**: `docs/diff/YYYY-MM-DD-diff-report.md`

---

## 12. 🛠️ 重构助手（refactor）

```bash
dev-tk refactor           # 生成重构建议
dev-tk refactor --scope=points-service  # 指定模块
dev-tk refactor --type=performance,safety  # 指定类型
dev-tk refactor --apply=RF-001  # 应用指定建议
```

### 重构类型
| 类型 | 触发条件 | 建议动作 |
|------|---------|---------|
| code smell | 重复代码、过长方法 | 提取方法/类 |
| architecture | 循环依赖、边界违规 | 解耦、分层调整 |
| performance | N+1查询、循环内IO | 批量查询、缓存 |
| security | SQL注入、泄露 | 参数化查询、加密 |

**输出文件**: `docs/refactor/YYYY-MM-DD-refactor-suggest.md`

---

## 使用示例

```
用户: "帮我搭个Node项目"
→ dev-tk scaffold my-app node

用户: "检查代码能不能提交"
→ dev-tk review → 预提交检查

用户: "分析一下这个项目的依赖关系"
→ dev-tk dep --format=mermaid

用户: "git提交，feat: 添加登录功能"
→ dev-tk git commit "feat: 添加登录功能"

用户: "格式化所有代码"
→ dev-tk fmt

用户: "看看有哪些技术债务"
→ dev-tk debt list

用户: "构建并测试"
→ dev-tk build && dev-tk test

## 🛠️ 内置工具脚本

技能包含 `scripts/` 和 `bin/` 目录下的 CLI 工具：

```bash
cd scripts/
node dev-tk.js review            # 预提交检查（P0/P1检查项）
node dev-tk.js fmt                # 格式化代码
node dev-tk.js dep                # 依赖分析
node dev-tk.js debt list          # 技术债务清单
node dev-tk.js debt add "描述"    # 添加债务
node dev-tk.js scaffold <名> <型> # 脚手架（node/python/vue）
```

也可以直接用 `bin/dev-tk` 入口：

```bash
bin/dev-tk review
bin/dev-tk dep
bin/dev-tk scaffold my-app node
```

## 注意事项

- 所有文件写入前确保目标目录已存在
- 每个子命令单独执行，不要合并在一个命令中
- diff/refactor/dep 的文档输出放在 `docs/` 下
- spec 的配置文件放在 `.ads/` 下
- 标记为子命令的参数要准确解析
