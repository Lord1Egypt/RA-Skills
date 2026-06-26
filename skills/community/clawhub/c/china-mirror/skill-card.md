## Description: <br>
Adds trusted Chinese package mirror parameters when an agent generates download or installation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomiba0904](https://clawhub.ai/user/xiaomiba0904) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to prefer backed Chinese mirrors for dependency downloads, package installation, and environment setup commands when network access to default registries is slow or unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes dependency sources by preferring Chinese package mirrors for downloads and setup commands. <br>
Mitigation: Review generated install commands before running them, especially in enterprise or sensitive build environments. <br>
Risk: Mirror use may conflict with workflows that require official registries, pinned artifacts, hashes, or signatures. <br>
Mitigation: Disable or override the skill for those workflows and use the required official or verified sources instead. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaomiba0904/china-mirror) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands may add package registry flags, mirror URLs, or environment variable guidance.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
