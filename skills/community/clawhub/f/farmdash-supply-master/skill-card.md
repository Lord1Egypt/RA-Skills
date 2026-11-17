## Description:

Use when comparing lending and yield pools by net expected APY, TVL depth, stablecoin and impermanent-loss risk. Read-only; deposits need user-signed approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can compare lending and yield pools, build stablecoin ladders, or review delta-neutral spot legs using net expected yield, pool depth, risk exposure, and data quality. The skill provides read-only selection guidance; deposits require user-signed approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and incomplete coverage; two local references were reported missing, so their contents were not assessed.

Mitigation: Review the missing references and the linked security guidance before installation.

Risk: The scanner reported a low-confidence, disputed skill-enumeration pattern associated with links and companion-skill references.

Mitigation: Consider the scanner's stated limitation when reviewing the skill and its references before installation.

Risk: Yield rankings may be misleading when history, token identity, exit terms, or reward composition is missing, and pool risks can change over time.

Mitigation: Apply the documented data-quality penalties, review missing information and protocol risks, and treat stablecoin and reward-token exposure as risk rather than guaranteed yield.

## Reference(s):

- [FarmDash Agent integration documentation](https://www.farmdash.one/docs)
- [FarmDash Supply Master skill manual](https://www.farmdash.one/openclaw-skills/farmdash-supply-master/SKILL.md)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash live agent status](https://www.farmdash.one/api/v1/agent/status)
- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-supply-master)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Yield pool comparisons with rankings, risk notes, and data-quality caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only selection guidance; rankings are cross-sectional and do not establish protocol safety or guarantee yield.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
