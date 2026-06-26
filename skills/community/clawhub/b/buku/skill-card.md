## Description: <br>
Buku helps agents manage a local buku bookmark database from the CLI, including adding, searching, listing, tagging, importing, exporting, updating, and deleting bookmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[god4saken](https://clawhub.ai/user/god4saken) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate a user's local buku bookmark database through non-interactive CLI commands for bookmark lookup, organization, import/export, and maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deletion, range deletion, import/export, and global tag changes can alter or remove entries in the user's persistent local buku bookmark database. <br>
Mitigation: Show the exact target bookmarks or file paths and require explicit user confirmation before running destructive or bulk-changing commands. <br>
Risk: The skill includes deletion commands that use flags to bypass buku's confirmation prompts. <br>
Mitigation: Use confirmation-skipping flags only after the user has reviewed the targets and explicitly approved the operation. <br>
Risk: Bookmark title or description refreshes may contact websites to fetch metadata. <br>
Mitigation: Use offline mode when the user does not want bookmark metadata fetching to contact external websites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/god4saken/buku) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses non-interactive CLI flags; JSON output is recommended for parsing bookmark records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
