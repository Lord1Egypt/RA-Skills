## Description:

Inspect a real public website and design a runnable Dataify-based scraper when no suitable prebuilt scraper exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect public target pages, choose a Dataify collection route, and generate a starter scraper with sample evidence and validation output. It is intended for read-only public web extraction workflows where an existing platform skill does not already cover the requested fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send target URLs, search queries, and task identifiers to Dataify services and write fetched samples or results into the workspace.

Mitigation: Use it only with public, non-sensitive targets; review generated samples and result files before sharing or committing them.

Risk: The authoritative security guidance notes credential and URL-handling risk, including a polling path that places the Dataify token in request URLs.

Mitigation: Use short-lived or least-privilege Dataify API tokens, avoid logging request URLs, and rotate tokens if exposure is suspected.

Risk: The package includes business-intelligence collection workflows in addition to the disclosed scraper-builder behavior.

Mitigation: Review or remove the business workflow path when only scraper generation is needed.

## Reference(s):

- [Dataify documentation](https://doc.dataify.com)
- [Dataify support](https://www.dataify.com/)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-scraper-builder)
- [Prebuilt routing](references/prebuilt-routing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, generated Python starter code, and JSON evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace files such as scraper specifications, site profiles, samples, validation reports, and generated scraper code.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
