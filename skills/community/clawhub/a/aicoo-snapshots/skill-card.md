## Description: <br>
Helps an agent save, list, and restore Aicoo note snapshots using Aicoo OS API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-management users can use this skill to have an agent create backups before edits, inspect note version history, restore earlier versions, and run folder-wide snapshot routines for Aicoo notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with AICOO_API_KEY can restore or modify notes and create bulk backups without built-in confirmation guardrails. <br>
Mitigation: Require explicit user confirmation before restores, direct edits, and folder-wide backups, including the target note ID, version ID, and folder scope. <br>
Risk: The skill depends on a sensitive Aicoo API key. <br>
Mitigation: Install only from a trusted publisher and keep AICOO_API_KEY in the runtime environment rather than embedding it in prompts, commands, or files. <br>


## Reference(s): <br>
- [Aicoo API base URL](https://www.aicoo.io/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/aicoo-snapshots) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICOO_API_KEY for authenticated Aicoo API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
