## Description:

CRUD operations for Alexandrie, a self-hosted Markdown note-taking app, including creating, reading, updating, deleting, and searching notes via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eth3rnit3](https://clawhub.ai/user/eth3rnit3)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage notes in a specific Alexandrie account through scripted REST API operations. It supports note listing, retrieval, search, creation, update, deletion, login, and logout workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live credentials and currently loads a password from a local shell environment file.

Mitigation: Install only in a trusted Alexandrie account environment, load the password as a single secret value rather than sourcing executable shell content, and restrict credential file access.

Risk: Session cookies are stored in a shared temporary path.

Mitigation: Store cookies in a private user-owned state directory with restrictive permissions and remove them on logout.

Risk: The delete command can remove remote notes immediately.

Mitigation: Require explicit confirmation or a clearly intentional force option before deletion, and keep recoverable backups for important notes.

## Reference(s):

- [Alexandrie ClawHub Skill Page](https://clawhub.ai/eth3rnit3/skills/alexandrie)
- [Alexandrie App](https://notes.eth3rnit3.org)
- [Alexandrie API Base URL](https://api-notes.eth3rnit3.org/api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Text]

**Output Format:** [Shell command guidance with JSON API responses and Markdown note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Alexandrie password, authenticated session cookies, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
