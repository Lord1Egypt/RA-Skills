# 代码风格分析指引 | Code Style Analyzer

> 本文件指导 AI 如何分析项目代码风格，提取 `code-style.md` 规范。

## 分析流程

1. **先读 `references/code-style.md`** 了解所有条目编号和结构
2. **读 `project_context.json`** 获取语言和框架信息；如需更多文件信息，用 `exec` 列目录、`read` 读配置文件
3. **逐条目分析**，每一条从源码中找证据
4. **写入 `.code-spec/code-style.md`**，严格使用 `[CODE-NN]` 编号

## 各条目分析要点

### [CODE-01] 变量命名
- 抽样 5-10 个 .js/.ts 文件，统计变量声明风格
- 区分：普通变量（camelCase）、常量（UPPER_CASE 或 camelCase）、私有（_prefix / #prefix）
- 依据：代码抽样 + ESLint naming-convention 规则

### [CODE-02] 函数命名
- 查看函数声明/箭头函数的命名模式
- 判断动词前缀偏好（get/set/handle/fetch/use/create）
- 判断异步函数是否有特殊前缀

### [CODE-03] 常量命名
- 搜索 `const UPPER_CASE` vs `const camelCase`
- 检查 ESLint 的 naming-convention 或 prefer-const 规则

### [CODE-04] 文件命名
- 列出 src/ 下典型文件路径作为证据
- 判断：kebab-case vs camelCase vs PascalCase
- 特殊规则：测试文件（.test.ts）、样式文件（.module.css）、类型文件（.d.ts）

### [CODE-05] 类/接口/类型命名
- 搜索 class/interface/type 声明
- TypeScript：interface 用 I 前缀？Props 类型命名风格？
- 依据：类型声明文件 + 抽样

### [CODE-06] 组件命名
- Vue：搜索 `<script setup>` 中组件名、template 中标签名（PascalCase vs kebab-case）
- React：搜索组件文件名和 default export 名称
- 检查 index.vue / index.tsx 的使用模式

### [CODE-07] 缩进
- 权威来源：用 `read` 读 `.editorconfig` / `.prettierrc` / ESLint 配置文件（`project_context.json` 的 `configs` 中已有片段）
- 如有 ESLint indent 规则直接引用
- 抽样验证是否一致

### [CODE-08] 引号
- 权威来源：从 `project_context.json` → `configs` 中读 `.prettierrc` 和 ESLint 配置片段；如片段截断，用 `read` 读完整文件
- 抽样验证 import/string 中引号类型
- 模板字符串 vs 普通字符串使用场景

### [CODE-09] 分号
- 权威来源：从 `project_context.json` → `configs` 中读 Prettier/ESLint 配置片段
- 抽样验证是否项目内一致

### [CODE-10] 大括号
- 检查 Prettier 的 `bracketSameLine` / `jsxBracketSameLine`
- 抽样观察 if/function/JSX 的大括号风格

### [CODE-11] 行宽
- 来源：从 `project_context.json` → `configs` 中读 `.editorconfig` / Prettier 配置片段
- 抽样统计长行占比（>120 字符的行数 / 总行数）

### [CODE-12] Trailing Comma
- 来源：从 `project_context.json` → `configs` 中读 Prettier 配置片段
- 抽样对象/数组多行最后一个逗号

### [CODE-13] 箭头函数 vs function
- 抽样统计箭头 `() =>` 和 `function` 声明比例
- 看场景：回调全箭头/顶层用 function 声明/React 组件用 function
- 是否有 ESLint 强制（prefer-arrow-callback / func-style）

### [CODE-14] async/await vs Promise
- 抽样搜索 `.then(` vs `await` 出现频率
- 看 API 调用 + 错误处理模式

### [CODE-15] 解构偏好
- 搜索 `const {prop} = props`、`const [value, setter] =` 频率
- 导入解构（`import { named } from`）vs 全量导入

### [CODE-16] Import 方式
- 统计 ES import vs require、default vs named 比例
- 用 `read` 读 `tsconfig.json`（或从 `project_context.json` → `configs` 中获取片段）检查 module/moduleResolution

### [CODE-17] Import 排序
- 从 `project_context.json` → `configs` 中读 ESLint 配置片段看 import/order 规则
- 用 `read` 抽样几个源文件看实际排序模式
- TypeScript path aliases（@/）使用

### [CODE-18] 导出方式
- default export vs named export 比例
- 组件文件倾向于 default，工具函数倾向于 named？
- 是否有 barrel export（index.ts 重导出）

### [CODE-19] 类型注解覆盖率
- 用 `exec` 搜索 `: any` 出现频率，或抽样 .ts 文件统计
- 从 `project_context.json` → `configs` 中读 `tsconfig.json` 片段检查 `noImplicitAny` / `strict`

### [CODE-20] any 使用情况
- 搜索 `: any` 出现频率
- tsconfig 是否禁用了隐式 any

### [CODE-21] 注释风格
- 统计 JSDoc `/** */`、行内注释 `//`、TODO/FIXME/HACK 各出现频率
- 看是否有文件头注释模板

### [CODE-22] 特殊标记
- 搜索 TODO/FIXME/HACK/XXX/OPTIMIZE 使用模式
- Issue/任务编号引用格式
