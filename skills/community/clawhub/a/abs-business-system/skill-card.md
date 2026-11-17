## Description:

Helps agents find sourced lean-management guidance, study ABS courses, draft operational plans, and diagnose business data and documents through ABS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypergraphdev](https://clawhub.ai/user/hypergraphdev)

### License/Terms of Use:

MIT-0

## Use Case:

Operations leaders and their agents use ABS to look up lean methods, obtain source-linked answers, study courses, draft implementation plans, and assess operational records or shop-floor images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An ABS access token grants the agent the user's account permissions.

Mitigation: Keep the token secret, grant access only when needed, and revoke it when no longer needed.

Risk: Business reports, spreadsheets, documents, or photos sent for diagnosis may contain confidential information.

Mitigation: Obtain approval before uploading confidential material to ABS.

## Reference(s):

- [ABS skill release](https://clawhub.ai/hypergraphdev/skills/abs-business-system)
- [ABS agent API reference](references/api.md)
- [ABS task catalog](references/tasks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Source-linked answers and Markdown plans; optional saved page images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search is available without an account; other features require an ABS access token. Plans remain drafts until reviewed and submitted in ABS.]

## Skill Version(s):

1.2.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
