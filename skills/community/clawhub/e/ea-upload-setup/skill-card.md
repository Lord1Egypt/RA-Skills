## Description:

Standardized EA deployment for MT5: copy, compile, restart, verify. One command to deploy your MetaTrader Expert Advisor and confirm it is running with heartbeat verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system operators use this skill to deploy a MetaTrader 5 Expert Advisor, restart the MT5 service, and verify that the advisor is running with a fresh heartbeat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a live MT5 trading service by copying files, compiling an Expert Advisor, restarting mt5.service, and activating the advisor.

Mitigation: Use only on a controlled MT5 host, require explicit operator confirmation before execution, and schedule deployment when service interruption is acceptable.

Risk: The deployment depends on an unbundled deploy_ea.sh script whose current behavior is not contained in the skill artifact.

Mitigation: Inspect or pin deploy_ea.sh before every run and confirm it only performs the intended copy, compile, restart, and verification steps.

Risk: The skill text tells the agent not to perform broader code review, which could miss unsafe or incorrect changes before live activation.

Mitigation: Review the relevant source diff and deployment script before compile, restart, or live activation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/ea-upload-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes state-changing deployment and verification guidance for a controlled MT5 host.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
