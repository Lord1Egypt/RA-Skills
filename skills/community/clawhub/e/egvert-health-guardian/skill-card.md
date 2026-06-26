## Description: <br>
Proactive health monitoring for AI agents. Apple Health integration, pattern detection, anomaly alerts. Built for agents caring for humans with chronic conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CTsolutionsdev](https://clawhub.ai/user/CTsolutionsdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to import Apple Health export data, analyze recent health readings, and generate alerts or summaries for humans with chronic conditions or caregiver workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive health data and may store imported readings locally. <br>
Mitigation: Install only with explicit consent from the person whose health data is involved, and protect the local data directory with appropriate filesystem permissions and access controls. <br>
Risk: The privacy claim that nothing leaves the machine may not hold if external alert channels such as Telegram are enabled. <br>
Mitigation: Disable external notifications by default, or tightly limit alert content and recipients before enabling any external alert channel. <br>
Risk: Automated cron imports and alerts can create medical-safety risk if configuration paths, thresholds, or notification behavior are wrong. <br>
Mitigation: Verify the import directory, configuration, and alert thresholds before enabling automation, and treat outputs as monitoring aids rather than medical advice. <br>
Risk: Importer and analyzer behavior is inconsistent: the importer writes vitals-style records while the analyzer expects readings organized by metric and timestamp. <br>
Mitigation: Fix and test the importer/analyzer data schema before relying on summaries, anomaly detection, or alerts. <br>


## Reference(s): <br>
- [Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console text with JSON configuration and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local health-data imports, anomaly alerts, and human-readable summaries when configured with user health export data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
