---
name: agent-skill-publisher
description: 创建、更新、检查和打包可分发的 Agent 技能与 WorkBuddy 专家，适配 WorkBuddy、Trae、Codex、Claude Code、Cursor、GitHub Copilot、Hermes 的技能入口与资源结构，并按授权发布 GitHub。用于技能/专家制作、导入失败修复和跨客户端迁移；不用于开发普通业务工作流或仅修改应用文案。
license: MIT
metadata:
  version: "1.2.0"
  author: EnderZhou
---

# 多平台Skill技能生成器

把已有经验整理为可复用技能，维护一份通用源码，并为实际目标客户端制作独立包。先判断用户需要的是技能、专家、插件还是连接器，不把它们当成同一种 ZIP。版本事实位于 [版本清单](assets/skill-version.json)。

对外能力简介：为 WorkBuddy、Trae、Codex、Claude Code、Cursor、GitHub Copilot、Hermes 等等平台制作 Skill 技能！把工作经验变成可复用技能，支持 WorkBuddy 专家生成、跨平台适配、打包校验、导入排错与 GitHub 发布。WorkBuddy 支持技能与专家；其余已列平台支持技能适配，其他平台按实际规范评估。

## 从任务选择资料

- 优化名称、简介、吸引力与搜索发现：读 [命名与搜索发现](references/discovery.md)，同步更新所有目标包，遵守字段长度与真实支持范围。
- 提炼经验或更新技能：读 [技能编写与资源组织](references/authoring.md)。保留用户目标、已授权范围和真正影响结果的经验，不复制整个聊天历史。
- WorkBuddy 技能/专家制作及解析报错：读 [WorkBuddy 适配](references/workbuddy.md)，对应检查实际 ZIP。
- 迁移到其他 Agent：读 [客户端适配矩阵](references/platforms.md)，确认客户端版本、入口和实际发现路径。Codex 元数据只在 Codex 适配中使用。
- 目录改造、资源遗漏、脚本运行和包验证：读 [打包与验证](references/packaging.md)。
- 新建开源项目、发布或更新 GitHub：读 [发布与回滚](references/releasing.md)。
- 从用户测试、对话日志或多模型对比改进技能：读 [证据与迭代](references/evidence-and-iteration.md)，按需使用 [分阶段测试提示词](references/acceptance-prompts.md)。
- 判断某条经验是否应成为规则：读 [故障案例与证据](references/lessons.md)。来源链接及核对日期见 [来源记录](assets/source-records.json)。

## 操作要点

1. 先找最新源码、已有安装包、版本清单与实际报错，避免用旧包覆盖新改动。技能机器名保持稳定，展示名、专家版本、内置技能版本分别管理。
2. `SKILL.md` 保留明确触发条件、任务流程和资料入口。详细规则放 references，可重复操作放 scripts，可复用输出放 assets。自动选择默认启用，除非用户明确要求仅手动调用。
3. 标准源码保留 `name`、`description` 及允许的可选字段；客户端扩展在打包副本中注入，不反写源文件。所有核心资源一起交付，不默认用户已安装作者电脑上的另一份技能。
4. 平台文档与上传器冲突时，记录实际版本、错误与日期，按目标环境修复；把“官方规则”“本地项目约定”“上传器观察结果”分开记录。不要把 WorkBuddy 技能 ZIP 的层级限制套用到专家嵌入技能的目录。
5. 名称应先说明平台或用途。WorkBuddy 专家默认将中英文展示名称各控制在 15 字符内，拉丁字母和空格也计数；这是上传器实测兼容规则，不是对所有 Agent 名称的统一限制。名称、头衔、卡片简介、详细介绍与推荐提问分别填写。
6. 工具不可用时交付离线包和明确的待验证项，不编造工具调用、客户端导入、召唤或审核结果。无凭据的本地打包不需要外部连接；真实发布按当前授权继续，用户已明确要求开源建库时无需重复请求发布确认。
7. WorkBuddy 专家头像必须随专家 ZIP 打包，并由隐藏 `plugin.json` 的 `avatar` 引用；该平台专家入口不能手动上传头像（2026-11-13 用户确认）。生成或替换头像后同步打包源码并核对实际 ZIP，不能仅交付独立图片后让用户在平台补传。独立技能入口另按其实际规则处理。

## 内置工具

Python 3.10+ 和 PyYAML 6.x；安装方式与离线限制见打包指南。以下命令相对于本技能目录，所有输出使用独立目录。

```text
python scripts/publish.py check /path/to/skill
python scripts/publish.py package /path/to/skill /path/to/output.zip --profile workbuddy --metadata /path/to/market.json
python scripts/publish.py package /path/to/skill /path/to/output.zip --profile folder
python scripts/publish.py check /path/to/output.zip --profile workbuddy
python scripts/publish.py expert /path/to/expert.json /path/to/agent-body.md /path/to/avatar.png /path/to/output.zip --skill /path/to/skill
python scripts/publish.py check /path/to/expert.zip --profile expert --expected-avatar /path/to/avatar.png
python scripts/verify_install.py /path/to/release.zip /path/to/installed/expert --profile expert
```

支持 `standard`（根 SKILL.md）、`trae`（根 SKILL.md）、`workbuddy`（扩展元数据、最多两段资源路径）和 `folder`（一层技能目录）。标准目录包适用于按目录发现技能的客户端；不生成含糊的“万能导入包”。

打包器不自动平铺深层资源、不执行技能代码、不安装到客户端、不连接服务、不创建 GitHub 项目。遇到深层资源先在适配副本中调整引用/加载器并验证，或保留目录交付其他 profile。专家构建器处理单 Agent、自包含技能包；专家团、任意 MCP 依赖需按当前官方 schema 另行处理。

## 完成标准

交付源技能、目标包、SHA256 与验证记录；必要时交付专家介绍。分别报告：文件结构检查、解压脚本运行、客户端发现/导入、实际调用、市场审核/发布、GitHub 发布。结构检查通过不能推断后续阶段。更新本地安装时保留备份并避免重复发现；不要为缓存刷新擅自重启服务或清理用户目录。
