## Description:

Optimizes 1688 product titles by generating rule-based hot-keyword suggestions and LLM-based rewrites with optional user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 merchants and commerce operators use this skill to compare rule-based and LLM-generated product title improvements, inspect keyword rationale, and confirm a selected title before applying it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a 1688 merchant access key for live product-title operations.

Mitigation: Install it only for workflows where that credential use is expected, and review access-key handling before deployment.

Risk: When no shop is specified, the skill defaults to running title optimization across every bound shop.

Mitigation: Scope requests to a named shop or loginId when broad multi-shop changes are not intended.

Risk: Generated titles may be applied externally after user confirmation.

Mitigation: Review the selected title and confirm carefully before allowing any one-click title update.

Risk: The skill contacts gateway.1688.com and retrieves bound-shop metadata.

Mitigation: Confirm that these network and telemetry expectations match the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-item-title-optimizer)
- [1688AiInfra publisher profile](https://clawhub.ai/user/1688aiinfra)
- [Product selection interaction](https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html?mode=newton-select-offer&skillCode=1688-item-title-optimizer)
- [interaction-specs.md](artifact/references/interaction-specs.md)
- [title_llm_SKILL.md](artifact/references/title_llm_SKILL.md)
- [title_wo_llm_SKILL.md](artifact/references/title_wo_llm_SKILL.md)
- [title_optimizer_qa.md](artifact/references/title_optimizer_qa.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command results with Markdown summaries and interactive selection payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and a configured 1688 merchant access key for live title and keyword operations.]

## Skill Version(s):

0.83.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
