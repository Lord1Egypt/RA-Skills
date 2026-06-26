## Description: <br>
Creates scheduled OpenClaw cron jobs that deliver monitoring results to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up recurring OpenClaw monitoring tasks, such as release, weather, or stock checks, and send concise results to a Feishu user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring jobs can repeatedly send results to Feishu on the configured schedule. <br>
Mitigation: Confirm the cron expression, timezone, prompt, account, and recipient open_id before enabling the job. <br>
Risk: Outbound Feishu delivery can expose secrets, personal data, or internal-only information to the wrong recipient. <br>
Mitigation: Avoid prompts that collect sensitive information and verify the Feishu recipient before running or scheduling the job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bbj375767338-arch/feishu-cron-announce) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron schedule, timezone, Feishu channel, recipient open_id, account selection, and delivery verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
