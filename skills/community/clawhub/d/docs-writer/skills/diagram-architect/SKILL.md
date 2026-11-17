---
name: diagram-architect
description: 图表架构设计：PlantUML/Mermaid 流程图、时序图、ERD、架构图、部署图
source:
  type: derived
  repo: skills-repo/docs-writer
  path: skills/diagram-architect/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/markdown-viewer/skills/uml
metadata:
  category: 文档
  platform: Web
  difficulty: 入门
---

# 图表架构师

> 图表生成：支持 PlantUML 文本语法和 Mermaid 标记，覆盖类图、时序图、活动图、状态机、组件图、部署图等。

## 能力

- **PlantUML 图表**：类图、时序图、活动图（含泳道）、状态机图、组件图、用例图、部署图、包图、对象图
- **Mermaid 图表**：流程图、时序图、ERD、架构图、甘特图
- **mxgraph 图标**：支持 9500+ AWS/Azure/Cisco/K8s 等 stencil 图标
- **样式定制**：skinparam 全局样式、元素级颜色、方向控制
- **Markdown 嵌入**：所有图表均可嵌入 Markdown 文档

## 使用方式

```text
/diagram-architect 为这个登录流程画一个时序图
/diagram-architect 生成数据库 ER 图
/diagram-architect 用泳道图描述这个跨团队审批流程
/diagram-architect 画一个 AWS 架构部署图
```

## 图表类型速查

| 类型 | 用途 | 语法 |
|------|------|------|
| 类图 | 类结构与关系 | `class`, `interface`, `<\|--` |
| 时序图 | 消息交互时序 | `participant`, `->`, `-->` |
| 活动图 | 工作流和流程 | `start`, `:action;`, `if/else` |
| 泳道图 | 多角色活动 | `\|Lane\|`, `:action;` |
| 状态机 | 对象生命周期 | `state`, `[*] -->` |
| 组件图 | 系统组件组织 | `component`, `[name]` |
| 部署图 | 物理部署架构 | `node`, `database` |

## 适用场景

- 技术文档中的流程图
- API 对接的时序设计
- 数据库设计文档
- 系统架构文档
- 云架构部署图

## 限制

- 复杂图表需手动美化布局
- 非 PlantUML/Mermaid 格式（Graphviz/D2）需手动转换
- 部分高级 PlantUML 特性需要特定渲染器支持

## 相关参考（Playbook）

- [references/diagram-selection-guide.md](../../references/diagram-selection-guide.md) — 核心 playbook：选型矩阵、画清楚原则、渲染坑（PlantUML 中文乱码/Mermaid 语法）
- [references/doc-lifecycle-and-pipeline.md](../../references/doc-lifecycle-and-pipeline.md) — 架构图在生成顺序第 4 步、与代码目录一致性、受众分层
- 强制核查：[scripts/check_code_blocks.py](../../scripts/check_code_blocks.py)（代码块必须标 `mermaid`/`puml`，否则渲染失败）
- 模板范本：[assets/readme-template.md](../../assets/readme-template.md)（图只放架构类，避免堆截图）