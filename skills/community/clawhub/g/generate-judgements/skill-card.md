## Description: <br>
Creates or updates fine-grained yes/no judge definitions for an agent skill evaluation YAML config by analyzing a skill's SKILL.md and reference files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluation engineers use this skill to generate or maintain mlflow-skills judge_definitions for testing agent skill behavior. It helps identify execution scopes, draft one-requirement-per-judge checks, and write or update YAML after user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated judge definitions or scope choices may be incomplete, duplicated, or misleading for the target skill. <br>
Mitigation: Review the proposed scopes and generated judgements before approving YAML changes. <br>
Risk: Generated evaluation configuration may reference sensitive credential variables such as API keys. <br>
Mitigation: Keep real credentials in environment variables or a secret manager, and review the exact YAML path before approving writes. <br>


## Reference(s): <br>
- [Judgement Writing Patterns](references/judgement-patterns.md) <br>
- [YAML Config Specification](references/yaml-config-spec.md) <br>
- [mlflow-skills](https://github.com/panlm/mlflow-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown discussion plus YAML configuration content or YAML file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before finalizing scopes, judgements, and file writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
