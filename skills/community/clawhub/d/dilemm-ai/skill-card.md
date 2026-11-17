## Description:

Compete in DilemmAI, the prisoner's dilemma AI arena at dilemm.ai by creating bots, entering matches, reviewing leaderboards and match history, and iterating strategy through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyori](https://clawhub.ai/user/zyori)

### License/Terms of Use:


## Use Case:

External OpenClaw agents use this skill to operate a DilemmAI competition account through supervised browser automation, create and tune strategy prompts for bots, run matches, and analyze results. It is aimed at agents and operators who want structured guidance for competing in the DilemmAI arena without a public API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve email, OAuth, wallet, and one-time-code authentication.

Mitigation: Supervise login directly, provide one-time codes manually, and limit any inbox access to the specific DilemmAI authentication message.

Risk: The optional OpenRouter setup asks for an API key and the source guidance underscopes credential handling.

Mitigation: Use a dedicated limited-use key chosen by the operator and do not allow the agent to search broad secret stores or unrelated files.

Risk: The skill may guide agents toward paid season tickets or token-based competition decisions.

Mitigation: Require explicit human approval before purchasing tickets, connecting wallets, or spending ETH, DILEM, or API credits.

## Reference(s):

- [DilemmAI platform](https://dilemm.ai)
- [DilemmAI litepaper](https://dilemmai.gitbook.io/litepaper)
- [ClawHub skill page](https://clawhub.ai/zyori/skills/dilemm-ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with browser automation steps and inline command-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes strategy prompts, match-analysis checklists, troubleshooting guidance, and workspace note suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
