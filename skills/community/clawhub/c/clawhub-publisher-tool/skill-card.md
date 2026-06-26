## Description: <br>
Helps agents publish local skills to ClawHub by checking package metadata, aligning versions, and preparing publish commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romicboy](https://clawhub.ai/user/romicboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare and publish ClawHub skill releases, including version alignment, changelog preparation, login guidance, and publish commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to use account credentials and publish content remotely. <br>
Mitigation: Confirm the ClawHub account, target skill path, slug, display name, version, changelog, and destination before running publish commands; do not paste tokens into chat or shell history. <br>
Risk: The skill may edit local skill metadata or run a target skill's publish.sh script. <br>
Mitigation: Review diffs to package.json and SKILL.md, inspect any publish.sh script, and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romicboy/clawhub-publisher-tool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/romicboy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to package.json and SKILL.md version metadata before publishing.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, SKILL.md metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
