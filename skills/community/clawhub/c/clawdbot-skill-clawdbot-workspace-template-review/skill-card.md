## Description: <br>
Compare a Clawdbot workspace against the official templates installed with Clawdbot (npm or source) and list missing sections to pull in, especially after upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xadenryan](https://clawhub.ai/user/xadenryan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot workspace maintainers use this skill to compare local workspace Markdown files against official Clawdbot templates and identify missing sections to review after upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated diffs may expose local agent or workspace instructions. <br>
Mitigation: Use the skill only on the intended Clawdbot workspace and avoid sharing diff output outside the intended review context. <br>
Risk: Template additions could be inappropriate for a specific workspace if accepted without review. <br>
Mitigation: Review each proposed missing block and allow edits only after confirming the change fits the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xadenryan/clawdbot-skill-clawdbot-workspace-template-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with file paths, missing blocks, brief explanations, questions to proceed, and inline shell commands when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compares local workspace Markdown against installed Clawdbot template files and asks before applying suggested additions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
