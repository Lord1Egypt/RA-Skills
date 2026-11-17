## Description:

Integrates Dub Links API endpoints to create, update, delete, retrieve, list, count, and run bulk operations on short links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferminrp](https://clawhub.ai/user/ferminrp)

### License/Terms of Use:

AGPL-3.0 license

## Use Case:

Developers and agents use this skill to manage Dub short links in an authenticated workspace, including creating, updating, deleting, retrieving, listing, counting, and bulk-operating on links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete or bulk-modify Dub links in the authenticated workspace.

Mitigation: Use a least-privilege Dub token when available and confirm exact link IDs before delete or bulk operations.

Risk: The bundled API reference includes non-link operations outside the intended scope.

Mitigation: Keep agent use limited to /links* endpoints and avoid non-link endpoints from the bundled API reference.

## Reference(s):

- [Dub Create Link API Documentation](https://dub.co/docs/api-reference/endpoint/create-a-link)
- [Dub API Token Documentation](https://dub.co/docs/api-reference/tokens)
- [Bundled OpenAPI Snapshot](references/openapi-spec.json)
- [ClawHub Skill Page](https://clawhub.ai/ferminrp/skills/dub-links-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown, JSON]

**Output Format:** [Markdown with inline curl commands, configuration snippets, and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dub Bearer token and is scoped to /links* endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
