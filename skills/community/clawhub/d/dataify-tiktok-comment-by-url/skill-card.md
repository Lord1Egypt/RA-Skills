## Description:

Collect TikTok comments from a known TikTok content URL. Do not use for video download, profile collection, or general TikTok discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and optionally submit Dataify scraper requests for TikTok comment collection from a known content URL, then monitor the asynchronous task and return JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact catalog exposes broader TikTok profile, shop, and post collection beyond the declared comment-by-URL task.

Mitigation: Narrow the catalog to the declared comment-by-URL task or require explicit tool selection review before execution.

Risk: Credential setup guidance and helper scripts involve DATAIFY_API_TOKEN handling.

Mitigation: Use environment or secret-management controls, never paste or commit tokens, and verify only token presence rather than printing token values.

Risk: Submitting Dataify tasks may spend credits and may collect profile-level data when broader tools are selected.

Mitigation: Require explicit confirmation before submissions that may spend credits, use high-volume settings, or collect profile-level data.

Risk: Generated curl commands and task IDs can expose sensitive task access details.

Mitigation: Treat generated commands, task IDs, and result files as sensitive and avoid sharing them in public logs or tickets.

## Reference(s):

- [Tool parameter catalog](references/tool-params.json)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-tiktok-comment-by-url)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN; generated curl commands, task IDs, and returned data should be treated as sensitive.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
