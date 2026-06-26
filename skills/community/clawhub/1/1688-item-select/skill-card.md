## Description: <br>
1688 Item Select helps 1688 merchants identify priority products for operations by scoring products across sales contribution, traffic efficiency, growth potential, marketing ROI, and product health, and it can also search shop products by keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 merchants and agents use this skill to retrieve shop and product metrics, score products, select priority products for operation, and search products by keyword. It produces concise product lists and optional interactive table selections while avoiding optimization actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive 1688 access key and stores it for later signed API calls. <br>
Mitigation: Use a least-privileged key, restrict access to the runtime environment, and rotate or remove the key when the skill is no longer needed. <br>
Risk: The configure step is described as read-only in the artifact but changes credential state. <br>
Mitigation: Treat configuration as a credential-changing setup action and review it separately from read-only data retrieval commands. <br>
Risk: Each CLI command sends a usage report to the gateway. <br>
Mitigation: Review telemetry expectations before installation and avoid using the skill where usage reporting is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-item-select) <br>
- [Interaction specs](artifact/references/interaction-specs.md) <br>
- [Scoring rules](artifact/references/scoring_rules.md) <br>
- [Skill interaction guide](artifact/references/skill_interaction_guide.md) <br>
- [Table schema](artifact/references/table_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and JSON command output, with optional interactive table data for multi-product selections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product recommendations are limited to a user-selected count, defaulting to three; product scores and optimization actions are intentionally omitted from user-facing reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
