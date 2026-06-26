## Description: <br>
Developer Self Improve Core helps a developer-facing agent prevent repeated mistakes, run post-response self-checks, draft memory rules for human approval, clean proposal memory, and send optional DingTalk reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelee09](https://clawhub.ai/user/joelee09) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage agent self-improvement workflows, including pre-response checks, post-response reflection, human-reviewed memory rule proposals, cleanup scans, and optional daily reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Free-form auto-confirm paths can persistently change future agent behavior. <br>
Mitigation: Do not wire chat or DingTalk replies directly to confirmation unless a stricter approval step is added; review proposal files manually before confirming rules. <br>
Risk: Automated cleanup can remove proposal files or change memory state after it is enabled. <br>
Mitigation: Back up the memory directory and keep automatic cleanup disabled until manual tests and generated files have been reviewed. <br>
Risk: Optional DingTalk reminders can send proposed rule summaries outside the local environment. <br>
Mitigation: Keep reminders disabled until the DingTalk target and OpenClaw configuration are verified and the user accepts that summaries will be sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joelee09/developer-self-improve-core) <br>
- [Publisher profile](https://clawhub.ai/user/joelee09) <br>
- [Project repository from metadata](https://github.com/lijiujiu/developer-self-improve-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated rule proposal files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local memory proposal, rule, cleanup, and log files when scripts are run; DingTalk reminders are optional and disabled by default.] <br>

## Skill Version(s): <br>
1.1.9 (source: server evidence, frontmatter, .clawhub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
