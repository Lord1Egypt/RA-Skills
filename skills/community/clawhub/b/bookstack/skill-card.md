## Description:

BookStack Wiki & Documentation API integration for managing books, chapters, pages, shelves, and full-text search through a configured BookStack API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:


## Use Case:

Developers, documentation maintainers, and automation agents use this skill to create, read, update, delete, organize, and search content in a BookStack knowledge base. It is suited for documentation workflows that need API-backed management of books, chapters, pages, and shelves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to the configured BookStack instance using API token credentials.

Mitigation: Configure only trusted HTTPS BookStack URLs and store credentials in BOOKSTACK_URL, BOOKSTACK_TOKEN_ID, and BOOKSTACK_TOKEN_SECRET.

Risk: Create, update, and delete commands can modify or remove BookStack content without an additional confirmation step.

Mitigation: Use a dedicated least-privilege API token and review command arguments before running write or delete operations.

## Reference(s):

- [BookStack skill page](https://clawhub.ai/xenofex7/skills/bookstack)
- [BookStack API documentation](https://demo.bookstackapp.com/api/docs)

## Skill Output:

**Output Type(s):** [shell commands, configuration, text, markdown, guidance]

**Output Format:** [Terminal text, Markdown content, and configuration values for BookStack API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOOKSTACK_URL, BOOKSTACK_TOKEN_ID, and BOOKSTACK_TOKEN_SECRET environment variables.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
