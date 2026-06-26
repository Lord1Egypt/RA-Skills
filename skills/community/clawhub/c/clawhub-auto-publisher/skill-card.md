## Description: <br>
Automatically package and publish local skills to ClawHub marketplace with pricing optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SASAMITTRRR](https://clawhub.ai/user/SASAMITTRRR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to scan local OpenClaw skill directories, preview publication readiness, and prepare batch publication workflows for ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can act with ClawHub publishing authority when a valid API key is provided. <br>
Mitigation: Run with --dry-run first, review every listed skill, and provide only an API key intended for the publishing action. <br>
Risk: A later version that implements upload behavior may introduce data-transfer risk not present in the reviewed artifact. <br>
Mitigation: Reassess security and publication behavior before using any version that adds real upload or network transfer logic. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SASAMITTRRR/clawhub-auto-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/SASAMITTRRR) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, Git, and ClawHub API access for publishing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
