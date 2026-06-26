## Description: <br>
Helps agents sync local files, notes, and workspace context into Aicoo by browsing, searching, creating, editing, uploading, and deleting notes through Aicoo APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Aicoo users use this skill to keep an Aicoo shared agent's knowledge current by checking existing context, searching notes, and syncing selected local project files or notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose broad remote upload, edit, and delete operations in an Aicoo workspace. <br>
Mitigation: Ask the agent to show the exact local files, remote paths, and operation type before upload, edit, or delete, and take snapshots before major edits. <br>
Risk: Synced files or notes may contain secrets, private data, or content intended for a different workspace. <br>
Mitigation: Use only Aicoo workspaces and API credentials you trust, and exclude secrets or private data before syncing. <br>
Risk: Changes to identity files or link policy notes can alter how the shared agent represents the user or handles links. <br>
Mitigation: Avoid memory/self and links policy changes unless the user explicitly intends to update agent behavior. <br>


## Reference(s): <br>
- [Context Sync API Reference](reference/API.md) <br>
- [Example: Sync a Project Directory](examples/sync-project.md) <br>
- [Aicoo API Base URL](https://www.aicoo.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AICOO_API_KEY for authenticated Aicoo requests and may propose remote create, edit, upload, or delete operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
