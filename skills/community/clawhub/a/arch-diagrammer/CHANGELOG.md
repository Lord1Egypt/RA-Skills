# Changelog

本文件记录 `arch-diagrammer` skill 的版本变更，遵循语义化版本。

## [1.0.1] - 2026-04-09

- 同步升级 `VERSION`、`SKILL.md`、`README.md` 中的版本号到 `1.0.1`
- 补充 `1.0.1` 版本变更记录
- 将文档中的版本升级命令统一为 `python3`
- 新增面向外部用户的安装与发布说明
- 新增 `scripts/build_release.py`，支持生成可分发的 skill zip 包
- 调整 `SKILL.md` 中的脚本命令，适配 `~/.cursor/skills/arch-diagrammer/` 安装路径
- 修复 `scripts/bump_version.py` 对精简版 `SKILL.md` 的兼容问题

## [1.0.0] - 2026-03-09

- 首个正式版本，完成架构图、流程图、时序图、部署图等全部核心功能

