## Description:

FinResearchClaw helps agents run finance, accounting, and investment research workflows through the FinResearchClaw repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and finance researchers use this skill to select and run event-study, factor-model, accounting, forecast-error, valuation, and investment research workflows. It prefers coding-agent execution and uses direct CLI/config execution only as a fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can fetch or clone mutable code from the FinResearchClaw GitHub repository.

Mitigation: Review the checked-out commit before execution and run in a sandbox or least-privilege workspace without unnecessary credentials.

Risk: The direct CLI fallback can run a finance workflow with approvals disabled.

Mitigation: Avoid `--auto-approve` unless operating in a controlled environment, and review configs, plans, and generated outputs before relying on them.

## Reference(s):

- [FinResearchClaw Examples](references/examples.md)
- [FinResearchClaw repository](https://github.com/ChipmunkRPA/FinResearchClaw)
- [ClawHub skill page](https://clawhub.ai/chipmunkrpa/skills/finresearchclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May clone or update a local FinResearchClaw repository and run selected example workflows when invoked by the agent.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
