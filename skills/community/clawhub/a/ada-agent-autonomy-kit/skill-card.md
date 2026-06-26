## Description: <br>
Stop waiting for prompts. Keep working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up proactive task queues, heartbeat routines, and scheduled work sessions so agents can continue useful work between human prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages recurring or unattended agent work sessions. <br>
Mitigation: Define an allowed task queue, maximum runtime, and approval rules before enabling recurring execution. <br>
Risk: The workflow can edit coordination files and create follow-up tasks without a prompt each time. <br>
Mitigation: Limit writable paths to approved task, memory, and coordination files and review queue changes regularly. <br>
Risk: Optional Slack or Discord updates may expose sensitive project information. <br>
Mitigation: Disable external reporting or restrict posted content and channels when working in repositories with secrets or customer data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanford/ada-agent-autonomy-kit) <br>
- [Publisher profile](https://clawhub.ai/user/seanford) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task queue and heartbeat workflow templates for recurring or unattended agent work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
