## Description: <br>
Use as the top-level guide for ALab agent-facing role skills. It explains how to install the ALab CLI package, the root/project/experiment skill hierarchy, when to use each subskill, and how the three role skills differ without loading every command reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bebetterest](https://clawhub.ai/user/bebetterest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using ALab use this skill bundle to choose the least-privileged role skill, install and invoke the ALab CLI, and coordinate root, project, and experiment workflows without mixing credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed ALab administration can expose or misuse root, project admin, or worktree tokens. <br>
Mitigation: Keep keys and tokens out of prompts, logs, tracked files, screenshots, and reports; prefer stdin, ignored secret files, or approved secret storage. <br>
Risk: Using a broader ALab role than needed can mutate the wrong layer or expose unnecessary authority. <br>
Mitigation: Use the narrowest matching ALab role skill and hand work across root, project, and experiment layers with only the credential needed for that layer. <br>
Risk: Visible artifacts or logs may contain sensitive details that are not guaranteed to be redacted. <br>
Mitigation: Inspect only task-relevant content and avoid copying raw artifact bytes, hidden-log content, tokens, or secrets into feedback or final reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bebetterest/alab-skills) <br>
- [ALab Global Admin Commands](alab-global-admin/references/commands.md) <br>
- [ALab Project Controller Commands](alab-project-controller/references/commands.md) <br>
- [ALab Experiment Worker Commands](alab-experiment-worker/references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Role-specific ALab command guidance; no generated artifacts are required by the skill itself.] <br>

## Skill Version(s): <br>
0.1.9 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
