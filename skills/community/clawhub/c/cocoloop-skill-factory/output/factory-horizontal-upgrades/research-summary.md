# Research Summary

## Scope

本轮围绕三个方向加固 `cocoloop-skill-factory`：

- builder 可测性与协议规则复用
- 第二层横向业务预设
- 参考 Skill 拉取与分析证据化

## Findings

- `factory-skill-builder` 已经能完成 `spec.yaml -> Skill -> validate` 的最小闭环，但 render 与 validate 之间存在重复协议规则。
- 现有第一层任务域预设覆盖工程、前端、浏览器、文档与研究，第二层业务域仍缺正式预设入口。
- 搜索结果进入设计比较前需要本地证据，但此前只有搜索工具，缺少拉取和结构分析工具。

## Stable Conclusions

- 协议规则应进入共享模块，供 render、platform validate 和测试共用。
- `workflow_integration`、`deploy_platform_ops`、`security_risk_review` 可以作为正式第二层预设。
- 参考 Skill 分析应输出 JSON 和 Markdown 两种证据，便于自动处理和人工审查。
