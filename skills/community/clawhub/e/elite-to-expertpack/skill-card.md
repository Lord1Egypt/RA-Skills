## Description: <br>
Convert Elite Longterm Memory data into a structured ExpertPack for portable, Obsidian-compatible agent knowledge migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to migrate Elite Longterm Memory workspaces into ExpertPack folders for backup, review, portability, and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated ExpertPack may include local agent memory and user profile information. <br>
Mitigation: Review the generated folder, especially relationships/primary-user.md, before committing, syncing, sharing, or publishing it. <br>
Risk: The built-in secret stripping may not remove all sensitive information. <br>
Mitigation: Treat secret stripping as a first pass only and perform a manual privacy and secret review before distribution. <br>
Risk: The security review says the skill overstates parts of the generated package. <br>
Mitigation: Verify overview.md, manifest.yaml, generated directories, and skipped sources before relying on the converted pack. <br>


## Reference(s): <br>
- [ExpertPack](https://expertpack.ai) <br>
- [ExpertPack skill on ClawHub](https://clawhub.com/skills/expertpack) <br>
- [Elite To Expertpack on ClawHub](https://clawhub.ai/brianhearn/elite-to-expertpack) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [ExpertPack folder with Markdown and YAML files plus command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and pyyaml; generated packs should be reviewed before sharing or publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
