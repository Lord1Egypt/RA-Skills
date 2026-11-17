## Description:

Guides an agent through Cue-based person-check research that cross-checks public business, regulatory, and judicial risk signals and returns sourced background-check material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to run Cue person-check workflows for due diligence, management risk review, beneficial-owner research, and batch checks of public-risk indicators. It helps the agent select a current Cue playbook option, confirm credit use, run the Cue research runner, and return the sourced report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to update or run unpinned remote Cue runner code.

Mitigation: Use a pinned, trusted checkout of cue-skills, inspect the runner before execution, and avoid automatic updates in sensitive environments.

Risk: The runner may access a local Cue API key and consume paid credits for person-check research.

Mitigation: Require explicit user confirmation for the selected subject, playbook option, and credit-consuming run before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-person-check)
- [Cue playbook API](https://cuecue.cn/api/playbook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and sourced research-report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent should preserve source links in the final report and avoid fabricating missing results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
