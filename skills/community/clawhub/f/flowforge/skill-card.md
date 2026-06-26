## Description: <br>
Autonomously breaks coding tasks into spec, plan, code, and QA phases, executing heavy work via Claude Code with multi-account rate-limit rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use FlowForge to turn a task or GitHub issue into a specification, implementation plan, code changes, and QA report while Claude Code performs the coding work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives Claude Code broad authority to edit repositories and run planned verification commands. <br>
Mitigation: Use it in a disposable clone or container on a clean branch, inspect the generated plan, and review diffs before trusting results. <br>
Risk: Project context may be sent to Claude Code during autonomous coding phases. <br>
Mitigation: Avoid running it on repositories containing secrets or sensitive data unless that exposure is acceptable for the environment. <br>
Risk: Account rotation relies on locally saved Claude credential files. <br>
Mitigation: Protect saved credential JSON files, inspect forge.env and account configuration before use, and remove credentials that are no longer needed. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [FlowForge Spec Writer Prompt](references/spec-prompt.md) <br>
- [FlowForge Planner Prompt](references/planner-prompt.md) <br>
- [FlowForge Coder Prompt](references/coder-prompt.md) <br>
- [FlowForge QA Prompt](references/qa-prompt.md) <br>
- [FlowForge Generic Rubric](references/rubric-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, JSON plans, code changes, shell command output, and progress logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped forge workspace with spec.md, implementation_plan.json, qa_report.md, project-context.md, and progress.log.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
