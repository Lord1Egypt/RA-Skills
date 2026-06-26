## Description: <br>
Fetches Amazfit GTR3 health data from HCGateway and writes a daily Obsidian log note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwebgit](https://clawhub.ai/user/sanwebgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Amazfit GTR3 health metrics from HCGateway and generate daily Obsidian health log notes, either on demand or through a scheduled cron job. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses HCGateway credentials from a local config file. <br>
Mitigation: Keep config.json private and install only when the publisher and local HCGateway endpoint are trusted. <br>
Risk: The skill writes generated health metrics into a configured Obsidian vault path. <br>
Mitigation: Review vault_path and log_dir before running so personal health data is written only to the intended location. <br>
Risk: The artifact includes optional Docker and cron commands for unattended data collection. <br>
Mitigation: Run Docker commands only for a controlled HCGateway deployment and add the cron entry only when daily unattended logging is desired. <br>


## Reference(s): <br>
- [Amazfit Health Log on ClawHub](https://clawhub.ai/sanwebgit/amazfit-health-log) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown health log note and terminal status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one dated Obsidian note per run using configured HCGateway credentials, locale, timezone, vault path, and log directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
