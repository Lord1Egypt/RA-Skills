---
name: find-orphans
description: Finds orphaned files, unused components, and dead code in projects. Use when 清理代码, 查找孤儿文件, 删除无用代码, cleanup, find unused, or removing legacy code.
---

# 孤儿文件与无效代码清理（Find Orphans）

系统化分析项目中的孤儿文件、未使用的组件和无效代码，帮助清理历史遗留。

## 触发场景

- 用户说「清理无用代码」「查找孤儿文件」「删除未使用的文件」「项目瘦身」
- 重构前的准备工作、代码审计
- 项目历史遗留清理

## 执行流程

### 1. 项目结构分析

读取 package.json，识别：
- 框架类型（React/Vue/Angular/Next.js）
- 构建工具（Vite/Webpack/Rollup）
- 入口文件（main 字段、scripts.dev/build 指向的文件）

扫描目录结构，识别：
- 源码目录：`src/`、`app/`、`lib/`
- 组件目录：`components/`、`views/`、`pages/`
- 工具目录：`utils/`、`helpers/`、`hooks/`
- 样式目录：`styles/`、`css/`

### 2. 孤儿文件检测

**步骤一：收集所有源码文件**

用 Glob 扫描所有 `.ts`、`.tsx`、`.vue`、`.js`、`.jsx`、`.css`、`.scss` 文件，排除：
- `node_modules/`、`dist/`、`build/`、`.next/`
- `*.config.*`、`*.d.ts`
- `*.test.*`、`*.spec.*`（除非用户要求包含）

**步骤二：提取所有 import 引用**

用 Grep 搜索所有 import/require 语句，将相对路径解析为绝对路径，构建「被引用文件集合」。

**步骤三：比对找出孤儿**

所有源码文件 - 入口文件 - 被引用文件集合 = 孤儿文件

**特殊检测**：
- **路由孤儿**：读取路由配置文件（`router/index.ts`、`routes.ts`），找出 `pages/` 目录下未在路由中注册的组件
- **样式孤儿**：检查 `.css/.scss/.less` 是否被任何文件 import 或在 HTML 中 `<link>` 引用
- **资源孤儿**：检查 `assets/` 中的图片/字体是否在代码或样式中被引用

### 3. 未使用组件检测

**导入但未使用**：

对每个文件，提取 import 的标识符，检查该标识符是否在文件其余部分出现（排除 import 行本身）：
- React：检查是否出现在 JSX 标签中（`<Button`）
- Vue：检查是否在 `components: {}` 注册且在 `<template>` 中使用

**Barrel exports 未使用**：

找到所有 `index.ts` barrel 文件，提取其 export 的标识符，全局搜索这些标识符是否被其他文件 import。未被引用的即为无效导出。

### 4. 无效工具函数检测

扫描 `utils/`、`helpers/`、`hooks/`、`lib/` 目录：

**导出但未被 import**：
- 找到所有 `export function` / `export const` 定义
- 全局搜索是否有文件 import 了这个名字
- 未被 import 的标记为无效

**文件内定义但未调用的私有函数**：
- 找出所有非 export 的 `function xxx` 定义
- 检查函数名是否在文件其他位置被调用

**重复工具函数**：
- 在 utils 目录中搜索功能相似的函数（相同参数类型、相似函数名）
- 标记为「可能重复，建议合并」

### 5. 安全验证

在标记为「可删除」前，对每个候选文件验证：
- 不在 package.json 的 `files` 或 `exports` 字段中
- 不是动态 import 的目标（搜索 `import(` 中的字符串拼接）
- 不在 vite.config / webpack.config 的 `entry` 中
- 不被 `.gitignore` 的反向规则保护（`!filename`）

### 6. 输出清理报告

按以下格式输出，并询问用户是否生成删除脚本：

## 输出模板

```markdown
## 孤儿文件清理报告

### 📊 统计摘要
- 扫描文件总数：N
- 孤儿文件：N 个
- 未使用组件：N 个
- 无效工具函数：N 个
- 预计可删除代码：~N 行

---

### 🔴 建议立即删除

#### 完全未引用的文件
| 文件 | 行数 | 最后修改 | 备注 |
|------|------|----------|------|
| `src/components/OldModal.tsx` | 312 | 2023-08 | 可能被 NewModal.tsx 替代 |
| `src/utils/legacy.ts` | 89 | 2022-11 | 导出 3 个函数，全部未使用 |

#### 路由未注册的页面组件
- `src/pages/TestPage.tsx` — 未在 router/index.ts 中注册

#### 孤儿样式文件
- `src/styles/old-theme.scss` — 无任何文件 import

---

### 🟡 需要人工确认

#### 可能被动态引用
- `src/plugins/dynamicLoader.ts` — 项目中存在动态 import 模式，无法静态分析确认

#### 导入但未在 JSX 中使用的组件
- `src/pages/Dashboard.tsx` 中导入了 `<Chart>` 但未使用（可能是注释掉的功能）

---

### 🟢 已排除（自动跳过）
- 配置文件：vite.config.ts、tsconfig.json 等
- 类型声明：*.d.ts
- 公共入口：main.tsx、App.tsx

---

### 🔧 下一步

是否生成删除脚本？运行前建议先：
1. `git checkout -b cleanup/remove-orphans`
2. 审查脚本中的每个文件
3. 执行脚本后运行构建验证：`npm run build`
```

如果用户确认，生成 `cleanup-orphans.sh`：

```bash
#!/bin/bash
# 孤儿文件清理脚本 - 生成于 YYYY-MM-DD
# 回滚：git checkout backup-before-cleanup
set -e

git rm src/components/OldModal.tsx
git rm src/utils/legacy.ts
git rm src/pages/TestPage.tsx
git rm src/styles/old-theme.scss

echo "清理完成，请运行 npm run build 验证"
```

## 误报场景（需人工判断）

| 场景 | 原因 | 处理方式 |
|------|------|----------|
| 动态路由文件 | `pages/[id].tsx` 通过约定路由加载 | 检查框架路由约定 |
| `require.context` | Webpack 批量加载目录 | 搜索 `require.context` 用法 |
| 环境变量控制的功能 | feature flag 动态引用 | 检查 `process.env` 条件分支 |
| 测试 mock 数据 | 仅在测试中使用 | 加 `--include-tests` 重扫 |
| Service Worker / PWA | 通过 public/ 直接引用 | 检查 public/ 目录配置 |

## 注意事项

- **不要删除**：正在开发的功能分支文件、feature flag 控制的实验性功能
- **分批清理**：先删高置信度文件，构建验证通过后再处理中置信度
- **保留 git 历史**：用 `git rm` 而非直接删除

## 与其他 Skill 配合

- `/simplify`：清理后简化剩余代码
- `/refactor-safely`：重构前先用本 skill 清理孤儿
- `/health`：清理后检查整体代码质量
- `/review`：清理 PR 提交前的安全审查
