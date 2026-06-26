## Description: <br>
A comprehensive ClawHub skill installer that bypasses API rate limits. Search, install single skills, or batch install multiple skills with automatic retry logic and version management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search ClawHub and install one or more skills into an OpenClaw skills directory. It is intended for command-line skill discovery, download, extraction, and batch installation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports unsafe command-execution paths. <br>
Mitigation: Run only in an isolated or disposable OpenClaw profile until shell-string execution is replaced with argument-array process execution and skill names are validated. <br>
Risk: The installer can overwrite local skills in the configured skills directory. <br>
Mitigation: Back up existing skills and require confirmation before overwriting or deleting installed skill folders. <br>
Risk: The installer downloads and extracts skill ZIP archives. <br>
Mitigation: Verify the source of each skill ZIP before installation and review downloaded skill contents before enabling them. <br>
Risk: The artifact contains a hardcoded skills path. <br>
Mitigation: Change the configured skills directory to the intended isolated OpenClaw profile before running installation commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/clawhub-skill-installer) <br>
- [Publisher Profile](https://clawhub.ai/user/sunnyhot) <br>
- [ClawHub Marketplace](https://clawhub.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-line guidance for search, single-install, and batch-install workflows; installation commands can modify local skill directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
