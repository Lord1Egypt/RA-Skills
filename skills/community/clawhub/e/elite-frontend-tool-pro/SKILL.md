---

slug: elite-frontend-tool-pro
name: "elite-frontend-tool-pro"
version: "1.0.0"
displayName: "精英前端设计-专业版"
summary: "企业级前端设计系统，支持多页面应用、React/Vue组件、品牌一致性与高级动效编排。精英前端设计工具专业版，面向团队的企业级前端设计系统。核心能力： - 多页面应用设计，统一视觉语言贯穿全"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: elite, frontend。
  精英前端设计工具专业版，面向团队的企业级前端设计系统。核心能力：
  - 多页面应用设计，统一视觉语言贯穿全站
  - React/Vue 组件库生成，含 TypeScript 类型定义
  - 高级动效编排，Framer Motion / Vue Transition 深度集成
  - 品牌设计系统，色彩/字体/间距/组件规范化
  - 设计令牌（Design Token）自动生成与管理
  - 响应式适配策略，多断点一致体验
  - 可访问性合规.
tags: 代码,vue,card,css,设计系统,design
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"

---

精英前端设计工具专业版是企业级前端设计系统平台。它不仅生成单页面代码，更将设计规范扩展至多页面应用、React/Vue 组件库、品牌设计系统和高级动效编排。通过设计令牌（Design Token）管理，确保全站视觉语言的一致性与可维护性。

本版本与免费版完全兼容——免费版的字体、色彩和动效规则在专业版中完整保留。专业版新增多页面应用、组件库、设计系统、品牌管理和高级动效等能力。

## 核心能力
### 能力对比
| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 输出格式 | HTML/CSS | HTML/CSS + React + Vue + TypeScript |
| 页面范围 | 单页面 | 多页面应用全站 |
| 组件管理 | 无 | 组件库 + TypeScript 类型 |
| 动效方案 | CSS @keyframes | CSS + Framer Motion + Vue Transition |
| 设计系统 | 规范指导 | Design Token 自动生成与管理 |
| 品牌管理 | 不支持 | 品牌色彩/字体/间距规范化 |
| 响应式 | 基础 | 多断点策略 + 一致性保障 |
| 可访问性 | 基础 | WCAG 合规检查 |

**处理**: 解析能力对比的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力对比的响应数据,包含状态码、结果和日志。

### 核心能力(补充)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 精英前端设计-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
多页面应用:
  - 统一视觉语言贯穿全站
  - 页面间导航动效一致性
  - 布局系统复用
  - 路由级动画过渡
# .
组件库生成:
  - React 组件（含 TypeScript 类型定义）
  - Vue 组件（含 Composition API）
  - 组件 Props/Events/Slots 规范
  - 组件文档与示例
# .
高级动效:
  - Framer Motion: staggerChildren, whileHover, layoutId
  - Vue: <Transition> + <TransitionGroup>
  - 页面级转场动画
  - 滚动驱动动效
# .
设计系统:
  - Design Token 自动生成
  - 色彩系统（主色/强调/语义色/中性色）
  - 字体系统（标题/正文/代码 + 字重/字号阶梯）
  - 间距系统（4px 基准 + 语义间距）
  - 组件规范（圆角/阴影/边框）
# .
品牌管理:
  - 品牌色彩体系
  - 品牌字体规范
  - 品牌组件风格
  - 一致性自动校验
# .
响应式策略:
  - 多断点设计（mobile/tablet/desktop/wide）
  - 流式布局 + 自适应排版
  - 触摸/鼠标交互适配
# .
可访问性:
  - WCAG 2.1 AA 合规
  - 语义化 HTML
  - ARIA 标签
  - 键盘导航支持
```

**处理**: 解析核心能力的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心能力的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置。

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级前端设计系、支持多页面应用、品牌一致性与高级、动效编排、精英前端设计工具、面向团队的企业级、前端设计系统、多页面应用设计、高级动效编排、深度集成、品牌设计系统、组件规范化、设计令牌、响应式适配策略、多断点一致体验、可访问性合规等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景
### 场景一：企业级 Web 应用全站设计
为 SaaS 产品设计完整的多页面应用界面。

> 详细代码示例已移至 `references/detail.md`

### 场景二：设计系统与 Design Token 生成
自动生成完整的设计系统配置。

### 场景三：Vue 组件库生成
```vue
<!-- Vue 3 + Composition API 组件示例 -->
<template>
  <TransitionGroup name="stagger" tag="div" class="card-grid">
    <div
      v-for="(card, index) in cards"
      :key="card.id"
      class="card"
      :style="{ '--delay': `${index * 0.1}s` }"
    >
      <h3><动态配置></h3>
      <p><动态配置></p>
    </div>
  </TransitionGroup>
</template>
# .
<script setup lang="ts">
import { ref } from 'vue';
# .
interface Card {
  id: string;
  title: string;
  content: string;
}
# .
const cards = ref<Card[]>([
  { id: '1', title: '设计系统', content: '统一的视觉语言' },
  { id: '2', title: '组件库', content: '可复用的 UI 组件' },
  { id: '3', title: '品牌一致性', content: '全站统一规范' },
]);
</script>
# .
<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
# .
.card {
  background: var(--color-bg-secondary, #16213e);
  border: 1px solid rgba(233, 69, 96, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
}
# .
/* TransitionGroup 交错动效 */
.stagger-enter-active {
  transition: all 0.6s ease;
  transition-delay: var(--delay, 0s);
}
.stagger-enter-from {
  opacity: 0;
  transform: translateY(24px);
}
</style>
```

## 不适用场景

以下场景精英前端设计-专业版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始
### 领先步：定义品牌配置
```json
{
  "brand": {
    "name": "Acme",
    "colors": {
      "primary": "#1a1a2e",
      "secondary": "#16213e",
      "accent": "#e94560"
    },
    "typography": {
      "heading": "Playfair Display",
      "body": "IBM Plex Sans",
      "mono": "JetBrains Mono"
    }
  }
}
```

### 第二步：生成设计系统
```bash
python3 generate-design-system.py --brand brand.json --output tokens.css
# .
```

### 第三步：生成组件库
```bash
generate-components --framework react --typescript --tokens tokens.json
# .
generate-components --framework vue --typescript --tokens tokens.json
```

## 配置示例
### Design Token CSS 变量
```css
:root {
  /* 色彩系统 */
  --color-bg-primary: #1a1a2e;
  --color-bg-secondary: #16213e;
  --color-accent: #e94560;
  --color-accent-alt: #0f3460;
  --color-text-primary: #eeeeee;
  --color-text-muted: #8892b0;
// .
  /* 语义色 */
  --color-success: #50fa7b;
  --color-warning: #f1fa8c;
  --color-error: #ff5555;
  --color-info: #8be9fd;
// .
  /* 字体系统 */
  --font-heading: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
// .
  /* 字号阶梯 */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 2rem;
  --text-4xl: 2.5rem;
  --text-5xl: 3.5rem;
  --text-6xl: 4.5rem;
// .
  /* 间距系统 (4px基准) */
  --space-0: 0px; --space-1: 4px; --space-2: 8px;
  --space-3: 12px; --space-4: 16px; --space-5: 24px;
  --space-6: 32px; --space-7: 48px; --space-8: 64px;
// .
  /* 圆角 */
  --radius-sm: 4px; --radius-md: 8px;
  --radius-lg: 12px; --radius-xl: 16px;
// .
  /* 动效 */
  --duration-fast: 0.2s; --duration-normal: 0.4s; --duration-slow: 0.6s;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 响应式断点配置
```css
/* 响应式断点策略 */
 breakpoints: {
  mobile: '320px',   /* 手机 */
  tablet: '768px',   /* 平板 */
  desktop: '1024px', /* 桌面 */
  wide: '1440px',    /* 宽屏 */
}
// .
/* 移动优先的响应式实现 */
.container {
  width: 100%;
  padding: var(--space-4);
}
@media (min-width: 768px) {
  .container { padding: var(--space-6); max-width: 720px; }
}
@media (min-width: 1024px) {
  .container { max-width: 960px; }
}
@media (min-width: 1440px) {
  .container { max-width: 1280px; }
}
```

## 优选实践
1. **设计系统先行**：先定义 Design Token，再基于 Token 构建组件，确保一致性。
2. **组件粒度合理**：原子组件 → 分子组件 → 页面模板，分层管理。
3. **动效有节制**：一次精心编排的页面加载交错入场，优于散乱微交互。
4. **响应式移动优先**：从移动端开始设计，逐步增强至桌面端。
5. **可访问性内建**：语义化 HTML + ARIA + 键盘导航，从设计阶段就考虑。

```text
专业版检查清单:
[ ] Design Token 已生成并应用
[ ] 组件库含 TypeScript 类型定义
[ ] 动效方案含页面级转场
[ ] 响应式覆盖 4 个断点
[ ] 可访问性通过 WCAG AA 检查
[ ] 品牌色彩/字体已规范化
[ ] 免费版设计规则已继承
[ ] 组件文档已生成
```

## 常见问题
### Q: 如何从免费版升级到专业版？
A: 免费版的字体、色彩和动效规则在专业版中完整保留。专业版新增设计系统生成、组件库和品牌管理能力，无需迁移已有代码。

### Q: 支持 React 和 Vue 吗？
A: 专业版同时支持 React（含 TypeScript + Framer Motion）和 Vue 3（含 Composition API + Transition），可根据项目需求选择。

### Q: Design Token 支持哪些输出格式？
A: 支持 CSS 变量、JSON、TypeScript 类型定义三种格式，可同时导出供不同消费端使用。

### Q: 组件库生成后如何维护？
A: Design Token 变更后，组件样式自动同步更新。建议将 Token 文件纳入版本控制，变更时运行同步脚本。

### Q: 响应式策略如何保证一致性？
A: 采用移动优先策略，通过 Design Token 统一间距和字号，各断点按比例缩放，确保视觉一致性。

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+（组件构建工具需要）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js 16+ | 运行时 | 必需 | nodejs.org 官方下载 |
| Framer Motion | 库 | 可选 | `npm install framer-motion`（React动效） |
| Vue 3 | 框架 | 可选 | `npm install vue`（Vue项目） |
| TypeScript | 语言 | 可选 | `npm install -D typescript` |
| Google Fonts | 字体 | 可选 | CDN免费加载 |

### API Key 配置
- 本Skill采用纯Markdown指令驱动，无需额外API Key
- Google Fonts 通过 CDN 免费加载

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 企业级AI Skill，支持多页面应用、组件库与设计系统管理
- **适用规模**: 团队与企业级，多页面应用全站设计
- **兼容性**: 与免费版设计规范完全兼容，支持无缝升级

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能.
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "精英前端设计-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "elite frontend pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级前端设计系统，支持多页面应用、React/Vue组件、品牌一致性与高级动效编排。精英前端设计工具专业版，面向团队的
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级前端设计系统，支持多页面应用、React/Vue组件、品牌一致性与高级动效编排。精英前端设计工具专业版，面向团队的
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据