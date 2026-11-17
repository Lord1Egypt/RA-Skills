## Description:

Developer Self Improve Core helps an agent perform pre-response error prevention, post-response self-checks, rule proposal generation, memory cleanup review, and optional daily reminder workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelee09](https://clawhub.ai/user/joelee09)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to maintain human-reviewed agent behavior rules, generate proposed memory updates from recurring mistakes, and review cleanup suggestions before they affect long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory rules may shape future agent behavior.

Mitigation: Review each proposed rule before confirmation, keep human approval in the loop, and audit generated memory and log files regularly.

Risk: Automatic proposal cleanup can remove pending rule drafts.

Mitigation: Leave automatic cleanup disabled until tested, tune retention settings, and back up the memory directory before enabling scheduled automation.

Risk: Optional DingTalk reminders can share rule summaries outside the local workspace.

Mitigation: Enable reminders only after reviewing proposal contents and verifying the OpenClaw and DingTalk target configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joelee09/skills/developer-self-improve-core)
- [Publisher Profile](https://clawhub.ai/user/joelee09)
- [Project Repository](https://github.com/lijiujiu/developer-self-improve-core)
- [README](README.md)
- [Security Information](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell output with generated local memory files and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create proposal, rule, cleanup, and log files under the skill memory directory when commands are run.]

## Skill Version(s):

1.1.9 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
