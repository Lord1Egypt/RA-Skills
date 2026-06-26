## Description: <br>
Review Apollo ecosystem issues with a classify-first workflow (reproduce for behavior issues, evidence-check for consultative asks) and draft maintainer-grade replies that directly answer user asks, clarify support boundaries, and provide actionable next paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nobodyiam](https://clawhub.ai/user/nobodyiam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to review Apollo GitHub issues, classify the request type, validate repository evidence or reproductions, and draft concise maintainer-grade responses with a publish confirmation gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest local diagnostic commands while reviewing an issue. <br>
Mitigation: Run diagnostic commands only in a trusted local checkout after confirming the target repository and issue. <br>
Risk: A drafted maintainer reply could contain incorrect or incomplete guidance. <br>
Mitigation: Review the full drafted comment, including evidence and support boundaries, before approving publication. <br>
Risk: A GitHub comment could be posted to the wrong issue or before review is complete. <br>
Mitigation: Use the built-in publish gate and post only after explicit confirmation. <br>


## Reference(s): <br>
- [Diagnostic Playbook](references/diagnostic-playbook.md) <br>
- [Reply Templates](references/reply-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and an optional YAML handoff block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes issue summary, triage suggestion, draft maintainer reply, and an explicit publish gate before any GitHub comment is posted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
