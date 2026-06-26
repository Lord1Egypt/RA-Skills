## Description: <br>
Automatic Skill guides an agent through a 10-stage pipeline to research, design, generate, review, test, publish, verify, and report on OpenClaw skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to automate or inspect the workflow for creating, improving, testing, and publishing OpenClaw skills. It is especially suited for staged dry runs, status checks, existing-skill iteration, and controlled publication through configured GitHub and ClawHub accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use configured GitHub and ClawHub credentials for unattended public publishing and repository updates. <br>
Mitigation: Start with dry-run, prefer the PR workflow over direct pushes, and use dedicated least-privilege tokens scoped to the intended accounts and repositories. <br>
Risk: Daily scheduled runs can continue publishing workflow outputs after initial setup. <br>
Mitigation: Review outputs before enabling the daily cron and disable the schedule with the provided toggle when automation is no longer desired. <br>
Risk: Generated or revised skills may contain incorrect, unsafe, or misleading instructions. <br>
Mitigation: Review and scan generated skills before deployment or publication, and treat final reports as review inputs rather than approval by themselves. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cosmofang/automatic-skill) <br>
- [Third-party publisher profile](https://clawhub.ai/user/cosmofang) <br>
- [Project homepage](https://github.com/Cosmofang/automatic-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-like staged instructions with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are stage-specific prompts and reports intended for agent execution; publishing steps depend on user-configured GitHub and ClawHub credentials.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
