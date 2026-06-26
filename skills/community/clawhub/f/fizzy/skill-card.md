## Description: <br>
Manages Fizzy boards, cards, steps, comments, and reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Portavion](https://clawhub.ai/user/Portavion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage Fizzy project-management workspaces, including boards, cards, steps, comments, reactions, tags, users, notifications, and attachments through the Fizzy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through delete, upload, and download operations in a Fizzy workspace. <br>
Mitigation: Confirm destructive and file-transfer operations explicitly before execution, and use exact card numbers, resource IDs, and file paths. <br>
Risk: The skill requires a Fizzy API token and account configuration for CLI access. <br>
Mitigation: Store the token with least privilege and restrictive local access, and avoid exposing credential values in chat or command output. <br>


## Reference(s): <br>
- [Fizzy skill page](https://clawhub.ai/Portavion/fizzy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs often include Fizzy card numbers, resource IDs, jq filters, command results, and concise operation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
