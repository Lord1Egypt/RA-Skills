## Description: <br>
Amemo Skill connects AI coding agents to the Amemo cloud service for managing notes, tasks, health data, and assistant memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lockfeel](https://clawhub.ai/user/lockfeel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let supported AI tools save and search Amemo notes, create and query tasks, retrieve health summaries, and synchronize assistant memory through the Amemo service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account tokens, phone numbers, email addresses, notes, tasks, health data, and assistant memory. <br>
Mitigation: Install only when the user trusts skill.amemo.cn with this data and understands that content may be sent to the Amemo cloud service. <br>
Risk: Credentials, contact data, and assistant memory may persist in local markdown files. <br>
Mitigation: Rotate or clear credentials and local memory files when uninstalling the skill, changing accounts, or ending use. <br>
Risk: Consent controls are limited for cloud synchronization of notes, tasks, health data, and memory content. <br>
Mitigation: Review intended API calls and local file changes before use, especially for sensitive personal or health information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lockfeel/amemo-skill) <br>
- [Amemo service API base](https://skill.amemo.cn) <br>
- [Health templates reference](modules/amemo-last-data/references/health-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, JSON API payloads, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local user configuration and memory files and may call the Amemo cloud API.] <br>

## Skill Version(s): <br>
1.1.2 (source: target metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
