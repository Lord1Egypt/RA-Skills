## Description:

Discovers potential brand ambassadors across Instagram, TikTok, and Twitter using apidojo's scrapers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brand partnership teams, DTC brands, and ambassador program managers use this skill to discover and rank creator candidates for multi-platform ambassador recruitment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill overstates cross-platform capability because the documented workflow only shows Instagram collection.

Mitigation: Review expected Instagram, TikTok, and Twitter coverage before installation, and verify that required Apify actors or equivalent workflows are available before relying on cross-platform results.

Risk: The security review flags unsafe Apify token handling in REST examples that place APIFY_TOKEN in URLs.

Mitigation: Prefer authorization headers, an Apify client, or an Apify MCP workflow with a narrowly scoped token instead of putting credentials in request URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/discovering-brand-ambassadors-across-platforms)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports creator handles, per-platform metrics, combined reach estimates, brand affinity signals, engagement metrics, scores, and ambassador tier classifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
