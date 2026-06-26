## Description: <br>
Audit an OpenClaw agent workspace and generate standardized evaluation reports, scores, and patches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Theylon](https://clawhub.ai/user/Theylon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Clawditor to audit OpenClaw workspaces for memory quality, retrieval efficiency, productive output, reliability, and goal alignment. The skill produces evidence-backed reports, scorecards, recommendations, and safe patch proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit outputs may include private context from workspace logs, memory files, or project artifacts. <br>
Mitigation: Review eval/ outputs before sharing and follow the skill's guidance to report only the presence and file paths of secrets. <br>
Risk: Running checks in an untrusted project can execute project-controlled code or tests. <br>
Mitigation: Use sandboxing or explicit approval before running tests, and prefer static inspection for third-party skills or plugins. <br>
Risk: Draft or zero-filled reports can be mistaken for completed evidence-backed evaluations. <br>
Mitigation: Treat generated drafts as incomplete until scores, findings, and recommendations are filled with cited evidence and validated against the report schema. <br>


## Reference(s): <br>
- [Clawditor Report Schema](references/report_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON reports, shell command guidance, and patch-style code recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audit outputs under eval/ and may propose concrete diffs for memory structure improvements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
