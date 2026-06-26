# feima-lab-content-manager

把纯文本/自然语言文档转成 [feima-lab](https://github.com/fangshan101-coder/feima-lab) 博客样式的 MDX 文章，生成零依赖 preview.html 本地预览。

**Claude Code Skill** · 中文

## 能做什么

**本地构建**：
- 自然语言输入 → feima-lab 样式 MDX 文章
- 本地浏览器像素级 + 交互可用预览（file:// 协议，零依赖）
- 自动本地化图片（下载 URL / 拷贝本地）
- 元数据管理（title / author / category / tags / coverImage）
- 分级工作流：短文一把生成，长文先出结构提案

**发布到 feima-lab 后端（v1.2 完整集成）**：
- **文章 CRUD**：save（create/update） · publish · unpublish · get by-slug · list（多条件筛选+分页）
- **分类**：list，支持按 route（BLOG/NEWS）筛选，名字→id 自动映射
- **标签**：list / save，save-article 时 `meta.tags` 自动闭环（查已有→缺失的自动建→映射成 tagIds）
- **图片**：upload 到 OSS，save-article 自动上传本地封面图
- **slug 查重**：`list-articles --slug xxx` 专用接口

## 支持的组件

Callout · CodeTabs · Collapse · CompareCard · Timeline · ImageCarousel · Playground

七种 feima-lab 自定义 MDX 组件，像素级还原样式 + 交互。

## 安装

克隆到 Claude Code 的 skills 目录即可（零依赖，开箱即用）：

    cd ~/.claude/skills
    git clone git@github.com:fangshan101-coder/feima-lab-content-manager.git

**不需要 `npm install`**——`scripts/render.mjs` 是预打包的自包含文件，所有 MDX 解析依赖（unified / remark / mdast / hast）都已内联。唯一要求是 Node ≥ 18。

**调用远程 API 需要额外设置**：

    export FX_AI_API_KEY=<your-internal-key>

从 https://platform.fenxiang-ai.com/ 登录获取，**必须申请 `internal` 类型的 key**（`normal` 级会被后端直接拒绝）。如果只用本地构建（render / new-post / image-localize），不需要设置这个 env var。

## 使用

在 Claude Code 中自然语言触发：

**本地构建**：
- "把这段文字整成 feima-lab 样式"
- "帮我写一篇 feima-lab 博客，主题是 XXX"
- "编写 feima-lab 文章"

**远程发布**：
- "把这篇发布到 feima-lab"
- "推到远程"
- "这篇在远程是什么状态"
- "列一下 feima-lab 后端有哪些分类"

## 产出结构

    posts/2026-04-09-my-post/
    ├── source.md          # 非 md 输入时生成的中间稿
    ├── article.mdx        # 带组件的最终文章
    ├── preview.html       # 零依赖本地预览
    ├── images/            # 本地化的图片
    └── meta.json          # 文章元数据

## 版本

- **1.4.0** —— slug 规则放宽：不再强制 `YYYY-MM-DD-` 日期前缀，改为纯 kebab-case（例 `how-we-build-agent-skills`）。另外累积了几个视觉 bug 修复（Collapse 箭头方向、Playground/CodeTabs 内层代码块白边、卡片 hover 阴影、Video iframe 加 `referrerpolicy` 让 YouTube 在 file:// 也能播放）+ 修复 JSX 表达式 props 解析（支持 `{[...]}` 语法）。
- **1.3.0** —— 组件风格对齐 feima-lab 首页设计系统 + 新增 Video 组件。
  - 同步升级 3 个地方：`feima-lab/app/components/mdx/*.tsx`、`fx-ai-brain-cms/app/components/mdx/MdxComponents.tsx`、skill snapshot + renderer
  - Callout：糖果色背景 + 左条 → 白底 + 全边框 + 20px 圆角 + 左上角彩色圆点 badge；accent 色降饱和
  - CompareCard：糖果色双列 → 白底 + 全边框 + title 前竖条 badge
  - Collapse：F3F1ED header → 白底 header + 展开时 F0EDEA 分隔线
  - Playground：#1A1A1A 深色 → #131314（对齐首页 `--color-bg-dark`）
  - 所有组件圆角 16px → 20px，加首页 `--shadow-sm` 细阴影
  - Timeline 不动（原实现已完全对齐首页 tokens）
  - **新增 Video 组件**：支持 YouTube / Bilibili 自动转 embed iframe，其他 URL 走原生 `<video>`
  - 修 `extract-snapshot.mjs` / `check-drift.mjs` 路径：feima-lab 从 Next.js 迁到 React Router v7 后 `src/` → `app/`
  - snapshot 补齐 shadows tokens 和 bg-dark/bg-dark-secondary
- **1.2.0** —— 完整对接 ContentApiController。
  - 新增 4 个 API 脚本：`list-articles` / `list-tags` / `save-tag` / `unpublish-article`
  - `save-article` 闭环处理 `meta.tags`（查已有→缺失的自动建→映射成 tagIds）
  - `list-categories` 支持 `--route BLOG|NEWS` 过滤
  - `meta.json` schema 升到 1.2：加 `route` 字段 + `sortOrder` + `publish.last_saved_tag_ids`
  - 修复 bug：`tint` 默认值 `tint-blue` → `bg-tint-blue`（后端要求带 bg- 前缀）
  - 修复 bug：`get-article` 识别 "文章不存在" 为 `not_found`（exit 2）
  - 明确声明：API Key 必须是 `internal` 类型（后端 `@ExternalApiAuth(level=INTERNAL)`）
- **1.1.0** —— 新增 5 个 API 脚本（list-categories / upload-file / get-article / save-article / publish-article），支持从 Claude Code 一键发布到 feima-lab 后端。零 npm 依赖（Node 18+ 内置 fetch/FormData/Blob）。
- **1.0.0** —— 首版，本地预览与元数据管理。

## 开发

源码位于 `src/`（`src/render.mjs` + `src/lib/*`）。`scripts/render.mjs` 是通过 esbuild 预打包的自包含输出——**用户侧不需要这些源码**，它们只对维护者有用。

    # 开发时：安装 devDependencies，跑测试
    npm install
    npm test

    # 修改源码后：重新打包 scripts/render.mjs
    npm run build

    # 检测 feima-lab 源码是否漂移（maintainer-only，需要本地有 feima-lab 仓库）
    npm run drift

## License

MIT
