## Description: <br>
Checks Node.js, npm, global npm packages, and project dependencies for available updates on a weekly schedule or manual request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to monitor Node.js and npm dependency drift, generate a Markdown dependency report, and send it to a trusted Feishu destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency reports sent to Feishu may include internal package names, private project identifiers, paths, or environment details. <br>
Mitigation: Confirm the Feishu destination is trusted and review the generated report for sensitive inventory details before sharing. <br>


## Reference(s): <br>
- [Dependency Tracker specification](references/spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/AxelHu/dependency-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with dependency tables and delivery status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated report under data/exec-logs/dependency-tracker/ and sends the report to Feishu, splitting messages over 3800 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
