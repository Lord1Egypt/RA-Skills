## Description:

Update the installed SEO + GEO skills and the seogeo CLI to the latest release, report current and latest versions, summarize changes, and reinstall the skill set across detected agent tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check and update a local SEO + GEO toolkit, then verify which supported agent tools received refreshed bundled skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update flow runs remote installer commands that replace a local CLI.

Mitigation: Review or pin the installer before execution, prefer dry-run checks where available, and stop if checksum verification fails.

Risk: The default reinstall command can overwrite bundled skill files across every detected agent tool.

Mitigation: Use a single explicit target when possible, review detected targets before writing, and preserve any locally edited bundled skill under a new name before updating.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-update)
- [Publisher profile](https://clawhub.ai/user/asale-ai)
- [Latest release metadata](https://api.github.com/repos/asale-ai/seo-geo-skill/releases/latest)
- [Unix installer script](https://raw.githubusercontent.com/asale-ai/seo-geo-skill/main/install.sh)
- [Windows installer script](https://raw.githubusercontent.com/asale-ai/seo-geo-skill/main/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include version comparisons, detected installation targets, dry-run results, update status, and verification steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
