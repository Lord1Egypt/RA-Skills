## Description: <br>
Context Slimmer audits always-loaded context files, measures their token cost, and identifies content to move, remove, or compress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunDevilATB](https://clawhub.ai/user/SunDevilATB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent maintainers use this skill to measure token usage in persistent context files and generate recommendations for slimming them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Bash script reads always-loaded context files in the selected workspace and reports audit information. <br>
Mitigation: Run it only in workspaces where those context files may be inspected, and keep any sensitive audit output local. <br>
Risk: Trimming persistent context can change future agent behavior if important instructions are removed or compressed too aggressively. <br>
Mitigation: Review recommendations manually before editing context files, and preserve instructions that affect required agent behavior. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal report and Markdown-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports current size, projected size, savings per file, and recommendations grouped by move, remove, or compress.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
