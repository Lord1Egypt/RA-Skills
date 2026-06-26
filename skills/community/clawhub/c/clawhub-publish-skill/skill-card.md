## Description: <br>
Publishes a local skill directory to ClawHub and helps an agent check required inputs, run the ClawHub CLI, handle common publish errors, and verify the published listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to publish local OpenClaw skill directories to ClawHub with required metadata, duplicate checks, retry guidance, and post-publish verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to perform state-changing actions such as global CLI installation or patching, token-backed publication, and remote release updates. <br>
Mitigation: Require a dry-run summary and explicit user confirmation before installing or patching CLI files, using a token, or publishing to ClawHub. <br>
Risk: Publishing the wrong local directory, slug, display name, or changelog could expose unintended skill content or create an incorrect public listing. <br>
Mitigation: Confirm the skill path, publisher account, slug, display name, version, changelog, and target listing URL before executing the publish command. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/antonia-sz/clawhub-publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawHub CLI commands, token-use instructions, retry guidance, and publication verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
