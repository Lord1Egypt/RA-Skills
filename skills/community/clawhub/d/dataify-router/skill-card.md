## Description:

Routes broad collection requests to the smallest suitable Dataify workflow across search, scraping, monitoring, marketplace, social, travel, jobs, and maps capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a broad data-collection goal into a small Dataify capability plan and route execution through the appropriate search, web access, scraping, monitoring, or task-lifecycle skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may spend credits, run multiple pages, download media, or set up recurring monitoring.

Mitigation: Review and confirm materially credit-sensitive, high-volume, multi-page, media-download, irreversible, or recurring requests before execution.

Risk: A Dataify API token could be exposed if credentials are pasted into chat or printed in commands.

Mitigation: Keep DATAIFY_API_TOKEN in the environment and verify only whether it is present without printing its value.

Risk: Broad requests can be routed to an unsuitable capability if the target sources, scope, freshness, or output format are ambiguous.

Mitigation: Restate the desired deliverable and ask only for missing required inputs or material ambiguities before selecting capabilities.

## Reference(s):

- [Dataify capability map](references/capability-map.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown guidance with capability plans, source coverage, limitations, and asynchronous task state when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session-scoped credential setup commands when authentication is missing; does not expose token values.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
