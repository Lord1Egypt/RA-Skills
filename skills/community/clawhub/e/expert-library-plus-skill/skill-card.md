## Description: <br>
Expert Library Plus installs and manages an AI expert library that uses name-based quality anchors for 43+ professional experts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalluche](https://clawhub.ai/user/kalluche) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install, verify, update, and operate the Expert Library Plus prompt library for OpenClaw-style expert workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer writes files under ~/.openclaw/experts and may change an existing local expert library. <br>
Mitigation: Review the installer and require explicit user confirmation before install, update, rollback, or overwrite actions. <br>
Risk: Skipping backups can remove the user's rollback protection for an existing expert library. <br>
Mitigation: Keep backups enabled unless the user intentionally chooses --no-backup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalluche/expert-library-plus-skill) <br>
- [Expert Library Plus Homepage](https://github.com/kalluche/expert-library-plus) <br>
- [Expert Library Plus Repository](https://github.com/kalluche/expert-library-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with step-by-step instructions and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation status, file paths, verification commands, platform notes, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
