# Reference Skill Analysis

## Local References

- `cocoloop-skill-factory/factory-skill-builder/scripts/render_skill_from_spec.cjs`
- `cocoloop-skill-factory/factory-skill-builder/scripts/validate_platform_skill.cjs`
- `cocoloop-skill-factory/utils/cli/search-registry.py`
- `cocoloop-skill-factory/presets/index.md`
- `codex-prd/skill-domain-landscape.md`

## Reusable Patterns

- 现有 builder 已经按脚本拆分 render、validate、package，适合继续加共享规则层和回归脚本。
- 现有 preset 文件结构稳定，新增第二层预设应沿用 `domain_id`、`common_jobs`、`default_question_pack`、`recommended_execution_planes`、`risk_and_gates`、`default_outputs`。
- `search-registry.py` 已经负责搜索归一化，新的参考工具应接在它之后，处理证据固化和目录分析。

## Gaps Closed

- render 与 validate 共享规则缺口已由 `schema_rules.cjs` 承接。
- 第二层业务域缺口已由三个新 preset 文件承接。
- 候选 Skill 本地分析缺口已由 `reference-skill.py` 承接。
