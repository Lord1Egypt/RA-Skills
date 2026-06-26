## Description: <br>
Household and personal inventory management for adding, finding, updating, searching, or deleting items and attachments in the user's AllOurThings vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matt-harding](https://clawhub.ai/user/matt-harding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a household or personal inventory vault, including belongings, warranties, receipts, manuals, photos, and purchase history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can delete inventory records and attachments. <br>
Mitigation: Ask the agent to show exactly what will be deleted, confirm one item or attachment at a time, and keep backups for records that cannot be easily replaced. <br>
Risk: The skill depends on the configured vault path. <br>
Mitigation: Do not use inventory tools until ALLOURTHINGS_DATA_DIR points to the intended AllOurThings vault folder. <br>


## Reference(s): <br>
- [AllOurThings homepage](https://allourthings.io) <br>
- [ClawHub skill page](https://clawhub.ai/matt-harding/allourthings) <br>
- [Publisher profile](https://clawhub.ai/user/matt-harding) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALLOURTHINGS_DATA_DIR to point to the user's vault folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
