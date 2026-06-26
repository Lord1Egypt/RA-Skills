## Description: <br>
Health Guardian helps agents import Apple Health data, detect health patterns, and surface anomaly alerts for people with chronic conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CTsolutionsdev](https://clawhub.ai/user/CTsolutionsdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and operators use this skill to configure an agent to import Apple Health exports, analyze local readings, and produce summaries or alerts for a consenting person with chronic conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and recurring monitoring, and iCloud sync or external alert channels can expose health information outside the local machine. <br>
Mitigation: Use only with explicit consent from the person monitored, protect the local data directory, and secure any iCloud or alert-channel configuration before enabling recurring imports. <br>
Risk: The security review notes that the skill overstates privacy and reliability and should not be treated as a medical alert system. <br>
Mitigation: Treat outputs as experimental support signals, test import and analysis flows before relying on them, and route concerning alerts through human review or appropriate clinical processes. <br>


## Reference(s): <br>
- [Health Auto Export App Store listing](https://apps.apple.com/app/health-auto-export/id1115567069) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and alerts with JSON configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read iCloud-synced health export folders and write local JSON health data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
