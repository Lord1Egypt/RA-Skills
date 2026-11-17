<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/design-guide-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/design-guide-logo-light.svg">
    <img alt="design-guide - 前端设计总控" src="assets/design-guide-logo-light.svg" width="560">
  </picture>
</p>

# design-guide

[English](README.md) | 简体中文

[![Validate](https://github.com/GrubbyLee/design-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/GrubbyLee/design-guide/actions/workflows/validate.yml)
[![Sync to Gitee](https://github.com/GrubbyLee/design-guide/actions/workflows/sync-to-gitee.yml/badge.svg)](https://github.com/GrubbyLee/design-guide/actions/workflows/sync-to-gitee.yml)
[![Release](https://img.shields.io/github/v/release/GrubbyLee/design-guide)](https://github.com/GrubbyLee/design-guide/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 面向 Codex、Claude Code、Cursor、Qwen Code 及其他 AI 开发环境的前端设计总控 skill。

`design-guide` 不是又一个 UI 风格预设，而是一个前端设计与生产工程总控 skill：它帮助 AI 编程助手理解仓库、判断并呈现设计方向、锁定可执行契约、完成实现，并在交付前验证行为与质量。

当前版本：**v0.1.1**。不同环境的“已安装、已同步、模型实际调用”证据分开记录在 [AIDE 兼容性报告](COMPATIBILITY.zh-CN.md) 中。

它的目标是减少模板化、AI 味明显的前端界面，让前端设计和开发形成稳定闭环。

## 它解决什么

- 作为前端入口 skill 和能力导航器。
- 支持两种模式：
  - **导航模式**：没有具体需求时，不写代码，主动列出当前环境可做的前端任务和辅助 skill。
  - **执行模式**：有具体需求时，按设计判断、设计系统、v0、实现、截图 QA 的流程推进。
- 根据不确定性与返工成本，将设计过程分为直接修复、定向设计和探索式设计。
- 必要时产出并呈现线框稿、独立 HTML 原型、参考板、图片或动效样片等可评审材料。
- 在共享本机桌面自动打开独立 HTML；需要 HTTP 时管理后台评审服务；远程环境使用宿主可访问链接或截图。
- 在明确的确认门暂停，让用户在高成本实现前确认、选择方向或提出修改。
- 能分流后台、管理端、工具界面、落地页、重设计、截图还原、移动端、动效、3D、UI 审查等任务。
- 能按类型评估已有产品/页面设计，识别模板化 AI 设计痕迹，给出优缺点评分、证据、取舍、按优先级排列的可落地优化方案、验收标准和验证步骤。
- 在较大实现前盘点框架、路由、组件、Token、数据契约、测试工具与项目风险。
- 将已确认设计转成机器可校验的契约，覆盖流程、状态、断点、可访问性、性能预算、数据 Schema、视觉基线和确认凭证。
- 使用 Playwright 在各响应式断点验证交互，并检查控制台、溢出、axe 可访问性、截图差异、浏览器指标和可选 Lighthouse 门槛。
- 提供状态/数据规范，以及 React/Next/Remix、Vue/Nuxt、SvelteKit、Angular、静态 HTML 和移动 WebView 的适配指南。
- 以受管理方式启动真实开发服务器，支持健康检查、自动开浏览器、日志、状态查询和安全清理。
- 支持项目级和本机级偏好文件，不把个人偏好写死进开源 skill。
- 内置项目扫描、设计稿呈现、契约校验、应用预览、交互 QA、视觉差异、截图和跨 AIDE 同步脚本。
- 内置行为回归样例、三条产品旅程验收、运营型 UI 专项评审模板，以及基于文件摘要的跨 AIDE 版本诊断。

## 快速开始

安装到 Codex：

```bash
git clone https://github.com/GrubbyLee/design-guide.git ~/.codex/skills/design-guide
```

将同一 skill 同步到 Codex、Claude Code、Cursor、Qwen Code 的本地 skill 目录：

```bash
bash ~/.codex/skills/design-guide/scripts/sync-aide.sh
python3 ~/.codex/skills/design-guide/scripts/design-guide-doctor.py --strict
```

目标 `design-guide` 目录按受管理镜像处理：同步会删除过期文件，同时排除 `.git`、`.codex`、Python 缓存和私有 `.design-guide/profile.md`。

同步目标如下；若源目录本身就是某个目标，该目标会自动跳过：

```text
~/.codex/skills/design-guide
~/.claude/skills/design-guide
~/.cursor/skills/design-guide
~/.qwen/skills/design-guide
```

## 调用方式

不同 AIDE 的 skill 调用语法不完全一致。最通用的方式是：要求 agent 使用 `design-guide`。

| 环境 | 推荐调用 |
|---|---|
| Codex | `use design-guide`、`design-guide`、`$design-guide`，或界面支持时用 `@design-guide` |
| Claude Code | 安装为 Claude skill 后用 `/design-guide`，或直接说 `use design-guide` |
| Cursor | 说 `use design-guide`，或让 agent 读取 `SKILL.md` |
| Qwen Code | 说 `use design-guide`，或让 agent 读取 `SKILL.md` |
| 其他 AIDE | 让 agent 读取 `SKILL.md` 并遵循 `design-guide` |

## 模式一：导航

当你只输入：

```text
design-guide
```

agent 不应该直接写代码，而应该列出可用前端能力，例如：

```text
design-guide is ready. Pick a frontend task:

1. Build a product screen / dashboard / tool
   Primary: design-guide
   Helpers if available: web-design-engineer, webapp-testing

2. Improve visual taste of an existing page
   Primary: design-guide
   Helpers if available: design-taste-frontend, web-design-guidelines

3. Evaluate an existing product/page design / 评估已有产品或页面设计
   Primary: design-guide
   Helpers if available: web-design-guidelines, webapp-testing, design-taste-frontend

4. Add complex animation
   Primary: design-guide
   Helpers if available: gsap, animejs

5. Build 3D / WebGL
   Primary: design-guide
   Helpers if available: three
```

## 模式二：执行

当你给出具体任务：

```text
使用 design-guide 帮我做一个用于审核生成媒体的创作者后台。
```

也可以要求它评估已有产品设计：

```text
使用 design-guide 评估这个已有仪表盘设计，并给出按优先级排列的改良报告。
输入：<URL/截图/HTML/仓库路径>
输出：评分表、优点、问题、可执行改动、验收标准。
```

评估流程会区分营销页、产品工作台、数据仪表盘、表单流程、移动端、重设计审计、可访问性审计和竞品对照，避免用落地页审美规则误判高密度产品 UI。

数据表、仪表盘、复杂表单、移动导航和高风险批量操作还有独立专项模板，用于补充证据要求与验收标准。只有移动端被明确纳入范围或产物本身是移动优先时，才加载移动模板。

Agent 应该按这个流程推进：

1. 盘点项目并读取产品上下文。
2. 选择 Level 0、1 或 2 的设计深度。
3. 明确用户任务、信息优先级、页面结构、状态、数据和成功标准。
4. 选择最少但必要的辅助能力。
5. 对探索式任务制作最低成本但足以判断的评审产物，自动打开或以其他方式呈现后等待用户确认。
6. 记录已确认的设计系统和可执行实现契约。
7. 对较大任务先做可浏览 v0。
8. 按检测到的框架和仓库规范完成实现。
9. 必要时启动并呈现受管理的应用预览。
10. 完成交互、状态、可访问性、响应式、视觉、控制台和性能 QA。
11. 运行仓库的 build、lint、typecheck 和测试。
12. 通过 No-Ship Gates 后再声称完成。

确认机制按风险启用，不是每一步都打断用户。孤立修复和方向明确的任务可以连续推进；新产品、重大重设计、工作流变化、品牌关键页面，以及明确提交给用户评审的中间产物，必须在完整实现前获得确认。创建文件不等于完成呈现：必须让用户获得已打开的浏览器页面、会话内媒体，或可立即访问的绝对链接或 URL。

## 偏好文件

`design-guide` 把开源默认规则与个人/项目偏好分离。

读取顺序：

```text
1. 当前项目的 .design-guide/profile.md
2. 本机的 ~/.design-guide/preferences.md
3. skill 自带的 references/design-defaults.md
```

模板：

```text
references/project-profile.example.md
references/local-overrides.example.md
```

不要把私人姓名、路径、API Key 或个人偏好提交到公开 skill。

## 脚本

生成结构化项目情报：

```bash
python3 scripts/inspect-project.py . --format markdown
```

创建并校验可执行设计契约：

```bash
python3 scripts/design-contract.py init --out .codex/design-guide/design-contract.json
python3 scripts/design-contract.py validate .codex/design-guide/design-contract.json --project-root . --require-approved
```

启动、检查并停止真实应用预览：

```bash
python3 scripts/run-preview.py start --command "npm run dev" --url http://127.0.0.1:3000
python3 scripts/run-preview.py status
python3 scripts/run-preview.py stop
```

运行契约驱动的浏览器 QA：

```bash
python3 scripts/verify-ui.py http://127.0.0.1:3000 \
  --contract .codex/design-guide/design-contract.json --project-root .
```

将当前截图与视觉基线比较：

```bash
python3 scripts/visual-diff.py baseline.png current.png --diff-out diff.png
```

运行轻量前端环境探测：

```bash
bash scripts/detect-frontend-env.sh .
```

截取桌面、平板、手机截图：

```bash
python3 scripts/capture-audit.py http://localhost:3000 --out .codex/frontend-audit
```

自动打开一个或多个独立 HTML 评审产物并立即返回：

```bash
python3 scripts/present-design.py open \
  ".codex/design/<design-id>/direction-a.html" \
  ".codex/design/<design-id>/direction-b.html"
```

确实需要 HTTP 时，启动、检查并停止受管理的后台服务：

```bash
python3 scripts/present-design.py serve ".codex/design/<design-id>/prototype.html"
python3 scripts/present-design.py status
python3 scripts/present-design.py stop
```

同步本地 AIDE 副本：

```bash
bash scripts/sync-aide.sh
```

检查四个 AIDE 的版本、必需文件和公开文件摘要：

```bash
python3 scripts/design-guide-doctor.py --strict
```

显式运行真实模型调用冒烟测试（可能消耗模型额度）：

```bash
python3 scripts/smoke-aides.py --aide codex --yes-consume-provider-quota
```

运行设计确认、评估隔离和跨 AIDE 三条确定性产品旅程：

```bash
python3 scripts/verify-product-journeys.py
```

显式选择 CLI 语言，或通过 `F_DESIGN_LOCALE` 设置默认语言：

```bash
python3 scripts/present-design.py --locale zh-CN --help
F_DESIGN_LOCALE=zh-CN python3 scripts/design-guide-doctor.py
```

根据 Scope Gate 契约评估一次真实 agent 输出：

```bash
python3 scripts/evaluate-review-output.py \
  tests/fixtures/review-behavior/image-review-isolated.json \
  response.md
```

## 仓库结构

```text
.
├── SKILL.md
├── SKILL.zh-CN.md
├── VERSION
├── design-guide.json
├── CHANGELOG.md
├── CHANGELOG.zh-CN.md
├── COMPATIBILITY.md
├── COMPATIBILITY.zh-CN.md
├── RELEASE_NOTES.md
├── RELEASE_NOTES.zh-CN.md
├── UPGRADING.md
├── UPGRADING.zh-CN.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── aide-integration.md
│   ├── internationalization.md
│   ├── internationalization.zh-CN.md
│   ├── anti-ai-design-tells.md
│   ├── artifact-presentation.md
│   ├── design-contract.schema.json
│   ├── design-defaults.md
│   ├── design-process.md
│   ├── framework-adapters.md
│   ├── helper-registry.md
│   ├── implementation-contract.md
│   ├── local-overrides.example.md
│   ├── project-intelligence.md
│   ├── project-profile.example.md
│   ├── product-design-review.md
│   ├── end-to-end-journeys.md
│   ├── review-templates/
│   ├── quality-gates.md
│   ├── state-and-data.md
│   └── review-rubric.md
├── scripts/
│   ├── i18n.py
│   ├── capture-audit.py
│   ├── check-secrets.py
│   ├── design-contract.py
│   ├── evaluate-review-output.py
│   ├── design-guide-doctor.py
│   ├── detect-frontend-env.sh
│   ├── present-design.py
│   ├── inspect-project.py
│   ├── run-preview.py
│   ├── smoke-aides.py
│   ├── sync-aide.sh
│   ├── verify-ui.py
│   ├── verify-product-journeys.py
│   └── visual-diff.py
├── locales/
│   ├── en.json
│   └── zh-CN.json
└── tests/
    ├── fixtures/quality/
    ├── fixtures/review-behavior/
    ├── test_behavior_evaluations.py
    ├── test_documentation_contract.py
    ├── test_i18n.py
    ├── test_present_design.py
    ├── test_quality_pipeline.py
    ├── test_release_tooling.py
    └── test_support_scripts.py
```

## 校验

本地校验：

```bash
bash -n scripts/*.sh
python3 -m py_compile scripts/*.py
python3 scripts/present-design.py --help >/dev/null
python3 scripts/capture-audit.py --help >/dev/null
python3 scripts/design-contract.py validate tests/fixtures/quality/design-contract.json --project-root . --require-approved
python3 -m unittest discover -s tests -v
python3 scripts/verify-product-journeys.py
python3 scripts/check-secrets.py .
bash scripts/detect-frontend-env.sh .
```

GitHub `validate.yml` 还会对测试契约执行严格浏览器质量任务，覆盖 Playwright Chromium、axe-core、响应式状态/键盘流程、截图与 Lighthouse，并将验证报告和截图上传为 workflow artifact。

## 版本与发布

当前版本同时记录在 `VERSION` 与 `design-guide.json`。变更记录见 [CHANGELOG.zh-CN.md](CHANGELOG.zh-CN.md)，本次发布摘要见 [RELEASE_NOTES.zh-CN.md](RELEASE_NOTES.zh-CN.md)，安全升级步骤见 [UPGRADING.zh-CN.md](UPGRADING.zh-CN.md)。真实 AIDE 模型调用可能消耗外部额度，因此作为独立检查明确报告，不与本地安装和同步混为一谈。

## Gitee 镜像

本仓库配置了将 `main` 和 tags 同步到：

```text
https://gitee.com/synovation/design-guide
```

同步 workflow 需要 GitHub 仓库 Secrets：

```text
GITEE_USERNAME
GITEE_TOKEN
```

`GITEE_TOKEN` 需要具备仓库/项目写入权限。

## License

MIT。见 [LICENSE](LICENSE)。
