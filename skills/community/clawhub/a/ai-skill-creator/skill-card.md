## Description: <br>
Guides agents through creating ClawHub/OpenClaw skills, including directory setup, SKILL.md authoring, references, scripts, security review, quality gates, packaging, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, review, package, and publish new ClawHub/OpenClaw skills with explicit security and quality gates. It is most relevant when a user asks to create a new skill package or evaluate a skill design before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands for packaging, publishing, dependency checks, or local review workflows. <br>
Mitigation: Review commands before running them and use accounts or credentials with the least privilege needed. <br>
Risk: The skill may guide creation or modification of skill files and release artifacts. <br>
Mitigation: Keep file writes scoped to the intended workspace or skills directory and scan the resulting skill before deployment. <br>
Risk: The artifact includes security-review and quality-gate procedures that depend on correct human or agent interpretation. <br>
Mitigation: Treat the procedures as guidance and confirm security decisions against the authoritative ClawScan summary and release policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-skill-creator) <br>
- [Publisher profile](https://clawhub.ai/user/johnsmithfan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, shell command, and checklist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially commands related to publishing, package installation, moderation, or broad local review.] <br>

## Skill Version(s): <br>
1.1.0-en2 (source: server release metadata; artifact frontmatter version 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
