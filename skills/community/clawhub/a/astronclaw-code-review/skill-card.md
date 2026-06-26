## Description: <br>
Astronclaw Code Review analyzes code quality, security, and performance issues and generates review reports with recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review JavaScript and TypeScript code for quality, security, and performance concerns, then turn the findings into actionable reports. It supports focused scans as well as combined review workflows for local project files or supplied code snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read arbitrary local file paths when a filePath argument is supplied. <br>
Mitigation: Use it only on intended workspace files and avoid home directories, secret files, and regulated or proprietary code unless workspace path restrictions are added. <br>
Risk: The security review says the AI-provider behavior is overstated and underexplained. <br>
Mitigation: Treat recommendations as local or mock heuristic output unless the publisher documents a real provider integration, what code is sent off-device, and how to disable it. <br>
Risk: The authoritative security verdict is suspicious, although the scan does not identify clear malicious behavior. <br>
Mitigation: Review the skill before installing and run it first in a controlled workspace with non-sensitive test code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shixiangyu2/astronclaw-code-review) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JSON review results and Markdown, HTML, or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes issue summaries, scores, prioritized recommendations, and optional detailed findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
