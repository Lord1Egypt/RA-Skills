## Description: <br>
Clawhub Publish Workflow guides OpenClaw agents through creating, evaluating, security-scanning, and publishing skills to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to prepare skill releases by creating skill metadata, running bundled evaluators, reviewing security guidance, publishing to ClawHub, and verifying the published release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires ClawHub API-token use and the server security summary says token handling needs review. <br>
Mitigation: Use only a limited ClawHub token, do not store tokens in markdown or workspace files, and require explicit approval before login or publish commands. <br>
Risk: The server security summary says bundled tooling is broader and less consistent than advertised. <br>
Mitigation: Verify helper script paths before running them, avoid broad local scans such as --all unless intended, and review results before installing or publishing. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Review the skill before installing or executing it and follow the server guidance for manual approval and limited credential exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/clawhub-publish-workflow) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Tools & Prerequisites](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ClawHub login and publish commands that require explicit user approval and limited API-token handling.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata; artifact SKILL.md lists 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
