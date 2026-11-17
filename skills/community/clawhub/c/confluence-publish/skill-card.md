## Description:

Publish, create, and update Confluence pages from HTML content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeincx](https://clawhub.ai/user/aeincx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to publish HTML content into Confluence Cloud, creating a new page or updating an existing page in the target space by title.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update Confluence pages using an Atlassian API token, including updating an existing page with the same title.

Mitigation: Use a scoped Atlassian API token and confirm the tenant, space key, and page title before publishing.

Risk: Dependency versions are declared as lower bounds, so installs can resolve newer package versions over time.

Mitigation: Use a locked dependency set before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeincx/skills/confluence-publish)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON status and result objects with Confluence page or connection details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Confluence Cloud credentials and writes only to Atlassian Cloud tenant URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
