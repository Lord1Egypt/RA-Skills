## Description: <br>
Manage task lists via cognary-cli. Use for listing, adding, updating, completing, uncompleting, and deleting tasks. Triggers on any request about tasks, to-dos, task lists, reminders-as-tasks, or tracking action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dboyne](https://clawhub.ai/user/dboyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage Cognary task lists through cognary-cli, including listing, adding, updating, completing, reactivating, and deleting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing cognary-cli from npm may install an unintended package if the package identity is not checked. <br>
Mitigation: Verify that cognary-cli is the intended npm package before installation. <br>
Risk: The skill requires a Cognary API key and can modify or delete user tasks. <br>
Mitigation: Use a dedicated Cognary API key when possible and confirm the exact task ID and title before updates or deletion. <br>


## Reference(s): <br>
- [Cognary Tasks App](https://tasks.cognary.ai) <br>
- [ClawHub skill page](https://clawhub.ai/dboyne/cognary-ai-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Text] <br>
**Output Format:** [Markdown with inline shell commands and readable task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses cognary-cli JSON output internally and presents task title, status, priority, category, due date, and ID to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
