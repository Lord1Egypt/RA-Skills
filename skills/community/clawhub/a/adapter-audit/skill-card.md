## Description: <br>
Use this skill to audit CLI adapter projects for missing output fields, batch-generate fixes, and prepare PR-ready summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allens0104](https://clawhub.ai/user/allens0104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit CLI adapter registries for missing standard output fields, classify fix strategies, apply additive source changes, run verification commands, and prepare a documented pull request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to edit adapter source files and prepare PR content, which may introduce incorrect fields or unintended behavior. <br>
Mitigation: Use a clean branch, review the generated diff and PR text, and approve submission manually. <br>
Risk: Verification commands may execute project build or test scripts from repositories the user does not fully trust. <br>
Mitigation: Inspect the repository and commands before running them, and use an isolated environment for unfamiliar projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allens0104/adapter-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown audit summaries with tables, code patches, shell commands, and PR-ready text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include before/after coverage metrics, per-adapter fix classifications, changed-file lists, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
