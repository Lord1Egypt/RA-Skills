## Description: <br>
Search, evaluate security, and install OpenClaw skills. Helps your human find the right skills safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmythril](https://clawhub.ai/user/0xmythril) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to find OpenClaw skills, evaluate security and community signals, and fetch installable skill files with safety checks before adding them to an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch and install remote skill files into an agent environment. <br>
Mitigation: Review the exact skill name, source, security flags, and full file list before allowing installation. <br>
Risk: Fetched files could be written outside the intended skill directory if paths are not checked. <br>
Mitigation: Confirm every file path stays inside the intended skills directory before writing files. <br>
Risk: High or critical risk skills may be installable only through explicit override flows. <br>
Mitigation: Require explicit user acknowledgement before using risky install overrides. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xmythril/clawdtm-advisor) <br>
- [ClawdTM homepage](https://clawdtm.com) <br>
- [ClawdTM API base](https://clawdtm.com/api/v1) <br>
- [Advisor skill definition](https://clawdtm.com/api/advisor/skill.md) <br>
- [Advisor skill metadata](https://clawdtm.com/api/advisor/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples, JSON response examples, and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security risk context should be shown before any fetched skill files are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
