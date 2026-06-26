## Description: <br>
Dev Setup records, searches, summarizes, and exports local development setup notes from a command-line logbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to keep a local, searchable record of development setup activities, configuration notes, and related exports. It should be treated as a setup logbook rather than an automated macOS provisioning tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises macOS provisioning, but security evidence says it appears to be a local setup logbook rather than an automated provisioning tool. <br>
Mitigation: Review the skill before installation and do not rely on it to install or configure development tools without separate verification. <br>
Risk: Setup notes are stored locally as plaintext logs and exports, which can expose sensitive entries if users record secrets or private infrastructure details. <br>
Mitigation: Do not enter passwords, API keys, tokens, private hostnames, or sensitive command output; review or delete ~/.local/share/dev-setup before sharing exports. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or export local plaintext setup logs under ~/.local/share/dev-setup when the associated script is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
