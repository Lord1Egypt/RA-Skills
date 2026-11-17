---
name: docs-writer
description: >-
  文档编写技能库：覆盖 README/项目文档生成、Changelog 与 Release Notes、API 文档（OpenAPI）、PlantUML/Mermaid 图表四类技术写作能力，并附 Markdown 死链/锚点与代码块标注的确定性检查脚本。
  当用户说"写 README"、"生成文档"、"Changelog"、"API 文档"、"架构图"、"Markdown 检查"时触发。
agent_created: true
metadata:
  version: 1.0.0
  category: 文档
  difficulty: 进阶
  architecture: superpower
---

# 文档编写专家

> 把 AI 变成一名「读懂代码、产出专业技术文档」的写作搭档，让每个项目都有清晰、可维护的文档。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性检查交给 `scripts/`，可复用规范放在 `assets/`。

## 何时使用

- 为新项目或文档缺失的项目生成 README / ARCHITECTURE 等文档时
- 发布前从 Git 历史生成 Changelog 与 Release Notes 时
- 需要从代码生成或补全 API 文档（OpenAPI/Swagger）时
- 需要画架构图、时序图、ER 图表达系统设计时
- 想自动核查文档死链、锚点、代码块标注（CI 门禁）时
- 文档跨文件一致性（命名/版本/链接）需要系统化保障时

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 文档生命周期、生成顺序、自动vs手写、跨文档一致性 | [references/doc-lifecycle-and-pipeline.md](references/doc-lifecycle-and-pipeline.md) | 文档流水线 生成顺序 一致性 自动生成 受众 |
| API 文档撰写质量、REST/GraphQL 策略、版本演进 | [references/api-doc-authoring-playbook.md](references/api-doc-authoring-playbook.md) | OpenAPI REST GraphQL 版本 示例 鉴权 |
| 图表选型、PlantUML/Mermaid 决策、绘制与渲染坑 | [references/diagram-selection-guide.md](references/diagram-selection-guide.md) | 图表 PlantUML Mermaid 时序图 架构图 渲染 |
| README/项目文档生成（细粒度调用） | [skills/readme-generator/SKILL.md](skills/readme-generator/SKILL.md) | readme generator 项目文档 ARCHITECTURE |
| Changelog/Release Notes 生成（细粒度调用） | [skills/changelog-writer/SKILL.md](skills/changelog-writer/SKILL.md) | changelog release notes Keep a Changelog |
| API 文档生成（细粒度调用） | [skills/api-doc-generator/SKILL.md](skills/api-doc-generator/SKILL.md) | api doc OpenAPI swagger 端点 |
| 图表架构设计（细粒度调用） | [skills/diagram-architect/SKILL.md](skills/diagram-architect/SKILL.md) | diagram architect PlantUML Mermaid ER |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，纯标准库、零依赖、只读、不联网，规则来自 `assets/`：

- [scripts/check_md_links.py](scripts/check_md_links.py) — 校验 Markdown 内部锚点链接与相对路径是否存活、残留 token
- [scripts/check_code_blocks.py](scripts/check_code_blocks.py) — 校验 Markdown 围栏代码块是否标注语言、是否配平

运行示例：

```bash
python3 scripts/check_md_links.py --check-rules          # 自检规则（0 错误）
python3 scripts/check_md_links.py README.md docs/         # 查死链/残留
python3 scripts/check_code_blocks.py README.md docs/      # 查代码块标注
```

## 模板资源

`assets/` 提供可直接套用的规范与模板（被上述脚本读取执行、且自检 0 错误）：

- [assets/markdown-lint-rules.json](assets/markdown-lint-rules.json) — 链接/代码块检查规则（允许协议、必检 token）
- [assets/readme-template.md](assets/readme-template.md) — README 标准模板（锚点/代码块均合规的范本）

## 核心原则（始终遵循）

1. **渐进式加载**：先读本路由表与对应 `references/`，再动手；不凭记忆猜语法。
2. **README 优先**：任何项目先有入口文档，其余按「有接口/要发布」决定是否生成。
3. **自动产出是草稿**：机器生成的结构化内容需人工润色关键场景与坑。
4. **一致性是底线**：跨文档命名/版本/链接必须一致，靠脚本而非人肉核对。
5. **图是补充**：先想清表达哪种关系再画图，一图一主题、节点不过载。
6. **明确边界**：脚本只做确定性检查、只出报告不替你写文档；文档表述与决策由人定。

## 与其他技能协作

- 提交/版本规范 → `skills-repo/productivity-master`（`git-workflow` 提供 Conventional Commits 源）
- 办公文档处理 → `skills-repo/office-master`
- 本仓库所有子技能来源见各自 `source` 字段，均为 skills.sh 社区成熟技能衍生
