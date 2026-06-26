## Description: <br>
Audit Homebrew installation for outdated packages, cleanup opportunities, and health checks on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS users use this skill to inspect Homebrew package status, cleanup opportunities, and brew doctor health findings before deciding on maintenance actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may reveal local Homebrew package inventory and system health details in the chat. <br>
Mitigation: Review where the audit output is shared and avoid posting local package details in sensitive channels. <br>
Risk: Follow-up Homebrew maintenance commands such as upgrades or cleanup can change or remove installed package versions. <br>
Mitigation: Review the audit results before approving any separate brew upgrade or brew cleanup action. <br>


## Reference(s): <br>
- [Homebrew](https://brew.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output, with JSON available for outdated-package audits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with Homebrew installed; supports outdated, cleanup, doctor, and full audit sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
