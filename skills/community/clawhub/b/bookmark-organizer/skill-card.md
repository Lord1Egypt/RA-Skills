## Description:

Imports a browser bookmark HTML file and transforms it into a structured, categorized, and time-sorted Markdown knowledge base with deduplication, optional dead-link checking, and customizable classification rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[farhigh233](https://clawhub.ai/user/farhigh233)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to convert browser bookmark exports into categorized Markdown files for review, search, cleanup, and reuse as a local knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional dead-link checking can contact every saved bookmark URL from the user's machine, including private or internal URLs.

Mitigation: Run without --check-links for sensitive bookmark exports, or review and remove private URLs before enabling link checks.

Risk: Generated Markdown can include bookmark titles and URLs that may contain sensitive or misleading content.

Mitigation: Review generated reports before publishing them or using them as input to another agent.

## Reference(s):

- [Bookmark Organizer on ClawHub](https://clawhub.ai/farhigh233/skills/bookmark-organizer)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces categorized bookmark lists, summary reports, and optional dead-link reports in a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
