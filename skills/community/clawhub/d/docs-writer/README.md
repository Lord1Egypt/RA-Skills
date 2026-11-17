# 文档编写技能库

> AI Agent Skills for Technical Writing —— 覆盖 README、Changelog、API 文档、架构图自动生成

## 架构说明

本仓库采用 **superpower 架构**（skills-repo 组织默认架构）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（文档流水线、API 撰写、图表选型）
- `skills/` — L3 四个细粒度子技能，可单独安装
- `scripts/` — L4 确定性文档检查脚本（死链/锚点、代码块标注）
- `assets/` — L5 可复用规范与 README 模板

## 定位

为开发者提供一套可安装的 AI Agent 文档技能，让 Claude Code 自动生成专业级技术文档。

## 核心理念

> 好文档是工程的另一半。用 AI 降低文档编写成本，让每个项目都有清晰、专业的文档。

- **自动化生成**——从代码中提取信息，自动生成结构化文档
- **标准化格式**——遵循 Keep a Changelog、OpenAPI 等行业标准
- **可视化优先**——用图表代替纯文本，降低理解成本

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 📘 项目文档 | `readme-generator` | README 生成：项目分析、ARCHITECTURE、API 文档、数据库 Schema | [衍生](https://skills.sh/jezweb/claude-skills/project-docs) |
| 📝 变更日志 | `changelog-writer` | Changelog 与 Release Notes：Keep a Changelog 格式、语义化版本 | [衍生](https://skills.sh/patricio0312rev/skills/changelog-writer) |
| 🔌 API 文档 | `api-doc-generator` | API 文档生成：OpenAPI/Swagger、端点说明、请求示例、鉴权文档 | [衍生](https://skills.sh/sickn33/antigravity-awesome-skills/api-documentation-generator) |
| 🗺️ 图表架构 | `diagram-architect` | PlantUML/Mermaid 图表：类图、时序图、架构图、部署图 | [衍生](https://skills.sh/markdown-viewer/skills/uml) |

## 安装

整库安装（推荐，拿到路由层 + 全部 references/scripts/assets）：

```bash
npx skills add skills-repo/docs-writer -g -y
```

单技能安装（只要某一个细粒度能力）：

```bash
npx skills add skills-repo/docs-writer@readme-generator -g -y
npx skills add skills-repo/docs-writer@changelog-writer -g -y
npx skills add skills-repo/docs-writer@api-doc-generator -g -y
npx skills add skills-repo/docs-writer@diagram-architect -g -y
```

## 内置脚本

```bash
python3 scripts/check_md_links.py --check-rules        # 链接/锚点/残留自检
python3 scripts/check_md_links.py README.md docs/       # 查死链
python3 scripts/check_code_blocks.py README.md docs/    # 查代码块标注
```

## 推荐工作流

```text
项目分析 → README 生成 → API 文档 → 架构图 → Changelog 记录
readme-    api-doc-      diagram-   changelog-
generator  generator     architect  writer
```

## 许可

MIT
