## Description: <br>
Publishes skills to the ClawHub registry while handling acceptLicenseTerms, tag-array formatting, token path detection, and per-file upload formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish one ClawHub skill or batch-publish local skill directories to the ClawHub registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local ClawHub token to upload selected skill files, so publishing the wrong directory can expose secrets, private notes, or build artifacts. <br>
Mitigation: Inspect the target skill directory before running it and remove secrets, environment files, private notes, and generated artifacts. <br>
Risk: Batch mode can attempt to publish multiple skill directories without asking for confirmation for each one. <br>
Mitigation: Use batch mode only on reviewed parent directories, or use single-skill publishing when contents need individual review. <br>


## Reference(s): <br>
- [ClawHub Push Skill release page](https://clawhub.ai/bg1avd/clawhub-push-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local ClawHub token and can upload selected skill files to the ClawHub registry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
