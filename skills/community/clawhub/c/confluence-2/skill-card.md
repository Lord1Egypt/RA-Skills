## Description:

Helps agents manage Confluence Cloud spaces, pages, labels, comments, child pages, and CQL search through the MorphixAI Confluence integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to let an agent browse, create, update, delete, label, comment on, and search Confluence Cloud content after the MorphixAI plugin and Confluence account connection are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A leaked MorphixAI API key could allow unauthorized use of the connected integration.

Mitigation: Store MORPHIXAI_API_KEY securely, rotate it as needed, and avoid exposing it in logs, prompts, or shared files.

Risk: Create, update, and delete actions can make real changes to Confluence content.

Mitigation: Use least-privilege Confluence access and confirm target page IDs, current page versions, and intended content before executing write or delete actions.

Risk: A broadly connected Confluence account may expose more spaces than the agent needs.

Mitigation: Connect an account with access limited to the required Confluence spaces and permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/confluence-2)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with YAML-style tool call examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Confluence account.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
