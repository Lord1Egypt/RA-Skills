# AGENTS.md — AI 全栈应用工程师技能库

> 本仓库是 skills-repo 组织下的 **AI 全栈应用工程师** 技能库（superpower 架构）。Agent 在处理「前后端一起做、搭一个完整应用、设计 API、写数据库、做前端组件/性能/调试」类任务时加载本文件。

## 技能入口

顶层 `SKILL.md` 为超级路由，按需加载 `references/` 深层 playbook，细粒度能力在 `skills/` 子技能。

## 能力清单

| 维度 | 子技能 | 路径 |
|------|--------|------|
| 后端-设计 | api-design | [skills/api-design/SKILL.md](skills/api-design/SKILL.md) |
| 后端-架构 | backend-patterns | [skills/backend-patterns/SKILL.md](skills/backend-patterns/SKILL.md) |
| 后端-数据 | database-design | [skills/database-design/SKILL.md](skills/database-design/SKILL.md) |
| 后端-开发 | fastapi-python | [skills/fastapi-python/SKILL.md](skills/fastapi-python/SKILL.md) |
| 前端-组件 | component-builder | [skills/component-builder/SKILL.md](skills/component-builder/SKILL.md) |
| 前端-样式 | css-master | [skills/css-master/SKILL.md](skills/css-master/SKILL.md) |
| 前端-性能 | web-performance | [skills/web-performance/SKILL.md](skills/web-performance/SKILL.md) |
| 前端-调试 | browser-devtools | [skills/browser-devtools/SKILL.md](skills/browser-devtools/SKILL.md) |
| 浏览器-路由 | browser-ops | [skills/browser-ops/SKILL.md](skills/browser-ops/SKILL.md) |
| 浏览器-MCP | browser-mcp | [skills/browser-mcp/SKILL.md](skills/browser-mcp/SKILL.md) |
| 浏览器-视觉 | ai-browser-automation | [skills/ai-browser-automation/SKILL.md](skills/ai-browser-automation/SKILL.md) |

## 深层 playbook（渐进式加载）

| 任务 | 读取 |
|------|------|
| AI-native 全栈工作流 | [references/fullstack-workflow.md](references/fullstack-workflow.md) |
| 后端深度 playbook | [references/backend-playbook.md](references/backend-playbook.md) |
| 前端深度 playbook | [references/frontend-playbook.md](references/frontend-playbook.md) |
| 浏览器操作横切 playbook（登录态/上传/动态表单/验证码兜底/合规） | [skills/browser-ops/references/browser-ops-playbook.md](skills/browser-ops/references/browser-ops-playbook.md) |

## 内置脚本

- [scripts/scaffold_fullstack.py](scripts/scaffold_fullstack.py) — 生成全栈骨架
- [scripts/gen_types_from_openapi.py](scripts/gen_types_from_openapi.py) — OpenAPI → TS 类型

## 适用场景

- 独立开发者 / 小团队从零构建 SaaS / Web 应用
- 需要一条把前后端并联交付的 AI-native 工作流
- 既做后端 API/数据库，又做前端组件/性能/调试
- 需要契约优先、类型安全、可复现脚手架

## 技能来源

由 `backend-developer` 与 `frontend-engineer` 整合而来，子技能改编自 skills.sh 社区成熟技能（见各 SKILL.md 的 source 字段）。
