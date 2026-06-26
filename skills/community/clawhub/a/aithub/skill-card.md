## Description: <br>
AitHub Discovery Skill enables AI agents to search, install, rate, and contribute skills from the AitHub registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vino0017](https://clawhub.ai/user/vino0017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent discover, install, compare, rate, and submit reusable skills through AitHub when a task needs additional capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to fetch, install, deploy, rate, fork, and publish third-party skills. <br>
Mitigation: Require explicit confirmation before deploy, rating, fork, or public submission, and inspect fetched skill content and publisher before use. <br>
Risk: Generated or submitted skill files may expose secrets, internal paths, hostnames, company names, or proprietary workflow details. <br>
Mitigation: Manually review generated SKILL.md content and apply the documented privacy cleaning rules before any public submission. <br>
Risk: Unreviewed or unpinned CLI execution can install or execute unexpected third-party content. <br>
Mitigation: Avoid unreviewed or unpinned CLI execution and scan skill content before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vino0017/aithub) <br>
- [AitHub Registry API](https://aithub.space) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an AitHub account or token for rating, submission, and fork actions; search, install, and details actions are documented as unauthenticated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
