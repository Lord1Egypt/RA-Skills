## Description:

BookStack Wiki & Documentation API integration for creating, reading, updating, deleting, organizing, and searching books, chapters, pages, and shelves on a BookStack instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT

## Use Case:

Developers, documentation maintainers, and operations teams use this skill to let an agent search, read, create, update, and organize BookStack knowledge-base content through the BookStack API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad write and delete access to a live BookStack wiki.

Mitigation: Use a dedicated least-privilege BookStack API token, prefer read-only permissions unless writes are required, and require explicit confirmation before delete or bulk update requests.

Risk: BookStack credentials are configured through local environment values or a local credential file.

Mitigation: Keep the local credential file private, keep it out of synced folders and source control, and rotate the BookStack API token if exposure is suspected.

Risk: Requests can send sensitive wiki content or credentials to a configured BookStack URL.

Mitigation: Configure only an HTTPS BookStack URL and verify the target instance before allowing the agent to read or modify content.

## Reference(s):

- [BookStack API Commands Reference](references/api-commands.md)
- [BookStack](https://www.bookstackapp.com/)
- [ClawHub Skill Page](https://clawhub.ai/f-liva/skills/bookstack-api)
- [Project Homepage](https://github.com/f-liva/skill-bookstack)
- [Source URL](https://github.com/f-liva/skill-bookstack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and BookStack API command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include BookStack content in HTML or Markdown depending on command options.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
