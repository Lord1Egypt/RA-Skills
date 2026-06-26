## Description: <br>
Audit an upstream agent skill, SKILL.md, skill repository, or lifecycle workflow before adapting it for ClawHub, Codex, Claude Code, or a public Skool skill sprint, with a PORT, REWRITE, or REJECT decision and no global install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to review upstream agent skills or workflow patterns before adapting, installing, recommending, or publishing them. It produces a PORT, REWRITE, or REJECT recommendation with a rewrite plan, redaction findings, proof checklist, and install or publish gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit inputs may contain credentials, private exports, paid content, screenshots, local paths, account identifiers, or other non-public material. <br>
Mitigation: Redact sensitive and private material before review, using placeholders or source-owned public excerpts instead. <br>
Risk: A portability recommendation could be mistaken for approval to install, run, publish, or enable the reviewed skill automatically. <br>
Mitigation: Treat the output as an audit recommendation and require explicit user approval plus static scan, duplicate-name check, redaction check, and a dry run before any non-local install or publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/agent-skills-portability-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with a verdict, portability score table, keep/rewrite/reject list, risk findings, safe adaptation plan, proof checklist, and install or publish gate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only recommendation output; it does not install, run, publish, persist, or enable runtime integrations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
