## Description: <br>
蜂兵虾将 is a multi-agent AI collaboration skill for monitoring industry trends, generating content strategy, analyzing status, automating workflow reports, and maintaining cross-session memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to coordinate AI agents for trend monitoring, content planning, workflow capture, and personal goal or status analysis across industries. It is intended to create recurring reports and reuse local memory about preferences, history, goals, and workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically builds persistent user memory and profiles across broad use cases without clear built-in retention or deletion controls. <br>
Mitigation: Use it only with explicit user consent, define retention and deletion practices before deployment, review stored memory files regularly, and avoid regulated, confidential, medical, financial, or personal material unless suitable controls are added. <br>


## Reference(s): <br>
- [Skill instructions](SKILL.md) <br>
- [README](README.md) <br>
- [AI collaboration system manual](docs/AI协作操作系统_完整使用说明书.md) <br>
- [Module data flow](references/data-flow.md) <br>
- [Workflow design](references/workflow-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured tables, JSON-like memory records, JavaScript examples, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from and write to local memory files that store preferences, history, goals, and workflow records.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
