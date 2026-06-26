# Build Plan

## Completed

- 抽出 `factory-skill-builder/scripts/schema_rules.cjs`
- 接入 `render_skill_from_spec.cjs`
- 接入 `validate_platform_skill.cjs`
- 增加 builder 单元测试和回归脚本
- 增加三个第二层预设
- 增加 `utils/cli/reference-skill.py`
- 更新主 Skill、设计指南、调研指南和 PRD 说明

## Verification

- `npm test`
- `npm run regression`
- `python3 -m py_compile` 检查 CLI 脚本
- `reference-skill.py fetch --source local`
- `reference-skill.py analyze`

## Follow-Up

- 后续可以把 `search-registry.py` 的 normalized result 直接接到 `reference-skill.py fetch`。
- 后续可以为 `reference-skill.py` 增加 ClawHub 或 Cocoloop 安装源适配。
- 后续可以把第二层预设纳入自动任务域路由器。
