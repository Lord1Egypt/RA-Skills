## Description: <br>
Deploy, secure, and troubleshoot Beszel monitoring with Docker agents, alert tuning, and upgrade-safe operations for self-hosted servers <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to plan, deploy, tune, and troubleshoot Beszel monitoring for self-hosted servers. It supports topology choices, secure agent onboarding, alert calibration, incident triage, and reversible upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational notes in ~/beszel/ could accidentally include tokens, onboarding credentials, or other sensitive monitoring details. <br>
Mitigation: Ask the user to review planned saved notes, avoid storing secrets, and require explicit approval before configuring external alert integrations. <br>


## Reference(s): <br>
- [Beszel Skill Page](https://clawhub.ai/ivangdavila/beszel) <br>
- [Beszel Homepage](https://clawic.com/skills/beszel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local operational notes under ~/beszel/ only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
