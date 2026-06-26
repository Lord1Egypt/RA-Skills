# Design.md Extractor

<p align="center">
  <a href="README.md">English</a>
  ·
  <a href="README.zh-CN.md"><strong>简体中文</strong></a>
</p>

<p align="center">
  <img alt="版本 0.1.0" src="https://img.shields.io/badge/version-0.1.0-2563eb?style=for-the-badge">
  <img alt="测试通过" src="https://img.shields.io/badge/tests-passing-22c55e?style=for-the-badge">
  <img alt="Node.js" src="https://img.shields.io/badge/runtime-Node.js-475569?style=for-the-badge">
  <img alt="本地优先" src="https://img.shields.io/badge/local--first-DESIGN.md-7c3aed?style=for-the-badge">
</p>

一个本地优先的 `DESIGN.md` 抽取 Skill，用于把网页链接或本地 HTML 文件转换成适合 AI 编程助手使用的设计文档。

Design.md Extractor 帮助 AI 编程助手在本地检查页面可见样式，推断实用设计 token，并生成可复用的 `DESIGN.md`。整个过程不调用模型 API，也不会上传页面数据。脚本通过 Playwright 采样 computed styles，再生成颜色、字体、间距、圆角、阴影和组件实现建议。

## 功能

- 从网页 URL 或本地 HTML 文件生成 AI 友好的 `DESIGN.md`。
- 可选写出 `design-snapshot.json`，方便追踪抽取证据和调试。
- 抽取颜色、字体、间距、圆角、阴影和基础组件模式。
- 推断语义颜色角色，例如 primary、surface、text、muted、border 和 focus。
- 识别常见 UI 组件，例如主按钮、卡片、徽标、输入框和导航链接。
- 在 `lib/design-extractor-core` 中内置抽取运行时，不依赖父级 monorepo。
- 使用 Playwright 本地运行，不调用 AI / 模型 API。
- 通过 `publish.config.json` 提供 ClawHub、SkillHub 和 OneTool 发布元数据。

## 快速开始

```bash
cd skills/design-md-extractor
pnpm install --frozen-lockfile
npm test
```

从公开网页生成：

```bash
node scripts/extract-design.mjs \
  --url https://example.com \
  --out ./design.md \
  --snapshot ./design-snapshot.json
```

从本地 HTML 文件生成：

```bash
node scripts/extract-design.mjs \
  --url file:///absolute/path/to/page.html \
  --out ./design.md \
  --snapshot ./design-snapshot.json
```

如果 Playwright 找不到浏览器，可以显式指定：

```bash
node scripts/extract-design.mjs \
  --url https://example.com \
  --out ./design.md \
  --snapshot ./design-snapshot.json \
  --executable-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

抽取完成后会写入：

- `design.md`
- 传入 `--snapshot` 时写入 `design-snapshot.json`

## 命令

```bash
node scripts/extract-design.mjs --url <url_or_file_url> [--out design.md] [--snapshot design-snapshot.json]
node scripts/extract-design.mjs --url <url_or_file_url> --viewport 1440x900
node scripts/extract-design.mjs --url <url_or_file_url> --timeout 30000
node scripts/extract-design.mjs --url <url_or_file_url> --executable-path <browser_executable>
npm run test:publish
npm run test:fixture
npm test
```

## Skill 工作流

当 Agent 在构建或重构 UI 前需要一份具体设计参考时，可以使用这个 Skill：

```bash
pnpm install --frozen-lockfile
node scripts/extract-design.mjs --url https://stripe.com --out DESIGN.md --snapshot design-snapshot.json
```

生成后先检查 `DESIGN.md`，再把其中的 token 和组件说明作为实现上下文。请把输出视为实用起点，而不是人工撰写的完整品牌手册。

## 发布包

这个仓库不会把生成产物提交到 git。可以用发布 Skill 或发布脚本生成市场上传包：

```bash
node /absolute/path/to/skill-publisher/scripts/publish-skill.mjs . \
  --platform all \
  --package minimal \
  --out dist/publish
```

minimal 包包含：

- `SKILL.md`
- `README.md` 和 `README.zh-CN.md`
- `package.json` 和 `pnpm-lock.yaml`
- `agents/`
- `scripts/`
- `references/`
- `fixtures/`
- `lib/`

生成的 zip 适合作为 GitHub Release asset 或 Skill 市场上传文件。

## 仓库说明

如果发布到公开 GitHub 仓库，建议不要把 `dist/` 等生成产物和 `node_modules/` 等依赖目录提交到 git。需要发布 zip 时，使用 GitHub Releases 更合适。

## 隐私

Design.md Extractor 只分析用户明确提供的 URL 或本地文件。它不会爬取其他页面，不调用模型 API，不上传页面 HTML、DOM、CSS、截图，也不收集浏览历史。

## 免责声明

生成的设计 token 来自页面可见 computed styles 的规则推断，可能遗漏隐藏状态、登录后页面、响应式变体、动画细节、专有素材或页面中不可见的品牌规范。
