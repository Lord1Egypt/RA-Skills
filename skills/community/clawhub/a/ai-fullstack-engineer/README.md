# AI 全栈应用工程师技能库 (ai-fullstack-engineer)

> AI Agent Skills for AI Full-Stack Application Engineers —— API 设计、数据库、后端架构、FastAPI 开发、前端组件、CSS 布局、Web 性能、浏览器调试，外加一条 AI-native 全栈工作流。

本仓库由 `backend-developer` 与 `frontend-engineer` 整合而来，采用 **superpower 架构**：`SKILL.md` 只做路由，深层方法论放 `references/`，细粒度能力放 `skills/`，确定性任务放 `scripts/`，可复用模板放 `assets/`。

## 定位

为独立开发者与个人/小团队提供「一个人扛下整条应用交付链路」的 AI 技能：从后端 API、数据库、架构，到前端组件、样式、性能与调试，并用 AI-native 工作流把前后端打通成一条流水线。

核心理念：

> 好的全栈不只是「能跑」——契约要稳定、类型要安全、UI 要快、代码要可维护。

- **契约优先** — 先定 OpenAPI，前后端并行
- **类型安全** — 从契约生成 TS 类型，编译期拦截联调摩擦
- **脚手架即基线** — 一键产出可运行骨架，把搭环境从 hours 降到 minutes
- **AI 辅助调试** — 浏览器自动化把调试变成可复现脚本

## 能力清单

| 维度 | 子技能 | 描述 | 来源 |
|------|--------|------|------|
| 设计 | `api-design` | REST/GraphQL 接口稳定性、版本、错误处理 | [衍生](https://skills.sh/addyosmani/agent-skills/api-and-interface-design) |
| 架构 | `backend-patterns` | Node/Express 模式、数据库优化、安全 | [衍生](https://skills.sh/affaan-m/everything-claude-code/backend-patterns) |
| 数据 | `database-design` | Schema、索引、ORM 选型、迁移 | [衍生](https://skills.sh/sickn33/antigravity-awesome-skills/database-design) |
| 开发 | `fastapi-python` | FastAPI 异步、Pydantic、DI、测试 | [衍生](https://skills.sh/mindrally/skills/fastapi-python) |
| 组件 | `component-builder` | 现代 Web 组件、React/Vue 适配 | [衍生](https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance) |
| 样式 | `css-master` | Tailwind Grid/Flexbox/容器查询 | [衍生](https://skills.sh/josiahsiegel/claude-plugin-marketplace/tailwindcss-advanced-layouts) |
| 性能 | `web-performance` | Core Web Vitals、bundle、缓存 | [衍生](https://skills.sh/sickn33/antigravity-awesome-skills/web-performance-optimization) |
| 交付 | `chrome-extension` | 浏览器扩展 MV3、权限、上架 | [衍生](https://github.com/googlechrome/modern-web-guidance) |
| 验证 | `browser-cli-agent` | CLI 驱动浏览器做真交互验证 | [衍生](https://github.com/vercel-labs/agent-browser) |
| 调试 | `browser-devtools` | Chrome DevTools 自动化审计 | [衍生](https://skills.sh/kunchenguid/chrome-devtools-axi/chrome-devtools-axi) |
| 自动化 | `ai-browser-automation` | 视觉驱动浏览器自动化：自然语言操作、抓取、断言，无需选择器 | [衍生](https://skills.sh/web-infra-dev/midscene-skills/browser-automation) |
| 自动化 | `browser-ops` | 浏览器操作方案路由：视觉驱动/选择器/CDP/MCP 四方案选型、三问决策法、登录态/上传/验证码兜底红线 | [原创](https://github.com/skills-repo/ai-fullstack-engineer) |
| 自动化 | `browser-mcp` | 浏览器能力 MCP 化：@playwright/mcp 与 chrome-devtools-mcp 接入、持久 profile 登录态、核心工具清单 | [衍生](https://github.com/microsoft/playwright-mcp) |
| 框架 | `nextjs-app-router` | Next.js App Router：布局/页面、服务端/客户端组件、路由处理器、数据缓存 | [原创](https://github.com/skills-repo/ai-fullstack-engineer) |
| 样式审计 | `tailwind-audit` | Tailwind 体检：未用类/purge、v3→v4 迁移、配置漂移、冲突类名、@apply 滥用 | [原创](https://github.com/skills-repo/ai-fullstack-engineer) |
| 多智能体 | `multi-agent-orchestration` | 多 Agent 协作编排：角色定义、编排模式（顺序/并行/层次/共识）、框架速选、通信与结果聚合 | [衍生](https://skills.sh/qodex-ai/ai-agent-skills/multi-agent-orchestration) |

## 安装

### 安装完整技能库（推荐，含 references / scripts / assets）

```bash
npx skills add skills-repo/ai-fullstack-engineer -g -y
```

### 只安装某个细粒度子技能（子路径 URL 语法）

> ⚠️ **不要用 `repo@子技能` 语法**：skills CLI（vercel-labs/skills）在仓库根存在 `SKILL.md`
> 时只识别根技能、不枚举 `skills/` 子目录（根技能遮蔽），`@` 后缀会被当作 git 分支名。
> 子技能安装必须使用完整子路径 URL：

```bash
# 后端侧
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/api-design" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/backend-patterns" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/database-design" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/fastapi-python" -g -y

# 前端侧
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/component-builder" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/chrome-extension" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/browser-cli-agent" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/css-master" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/web-performance" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/browser-devtools" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/ai-browser-automation" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/browser-ops" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/browser-mcp" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/nextjs-app-router" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/tailwind-audit" -g -y
npx skills add "https://github.com/skills-repo/ai-fullstack-engineer/tree/main/skills/multi-agent-orchestration" -g -y
```

> 只装子技能不会带上 `references/`、`scripts/`、`assets/`（子技能自带的内嵌 `references/`
> 除外，如 `browser-ops`）。需要脚手架脚本与全栈工作流 playbook 时，请安装完整技能库。

## 快速开始

```bash
# 生成全栈骨架（后端 fastapi + 前端 react）
python3 scripts/scaffold_fullstack.py --name my-saas --be fastapi --fe react

# 从 OpenAPI 生成前端类型（类型安全联调）
python3 scripts/gen_types_from_openapi.py --spec openapi.json --out src/api/types.ts
```

## 推荐工作流

```
需求/领域模型 → 契约优先(OpenAPI) → 脚手架 → 前后端并行
   → 类型安全联调 → AI 辅助调试(DevTools) → 性能/质量门禁 → 交付(compose+CI)
```

详见 [references/fullstack-workflow.md](references/fullstack-workflow.md)。

## 目录结构

```
ai-fullstack-engineer/
├── SKILL.md                     # 超级路由
├── AGENTS.md                    # Agent 入口
├── references/                  # 深层 playbook（按需加载）
│   ├── fullstack-workflow.md
│   ├── backend-playbook.md
│   ├── frontend-playbook.md
│   ├── nextjs-app-router-playbook.md
│   ├── tailwind-audit-playbook.md
│   └── multi-agent-orchestration-playbook.md
├── skills/                      # 细粒度子技能
│   ├── api-design/  backend-patterns/  database-design/  fastapi-python/
│   ├── component-builder/  css-master/  web-performance/  browser-devtools/
│   ├── nextjs-app-router/  tailwind-audit/  multi-agent-orchestration/
│   ├── ai-browser-automation/  browser-ops/   # browser-ops 内嵌 references/（单装自包含）
│   └── browser-mcp/
├── scripts/                     # 确定性脚本
│   ├── scaffold_fullstack.py
│   └── gen_types_from_openapi.py
└── assets/                      # 模板
    ├── openapi-spec-template.yaml
    ├── docker-compose.fullstack.yaml
    └── ci-fullstack.yml
```

## 许可

MIT
