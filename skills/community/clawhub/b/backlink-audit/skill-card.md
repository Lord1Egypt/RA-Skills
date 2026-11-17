## Description:

Audits inbound links to a domain, subdomain, or GitHub repo from supported sources and classifies each source as ours, organic, or ambiguous.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO operators use this skill to gather backlink or referrer data, classify controlled versus organic sources, and optionally update an inbound-links state graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backlinks source uses a backlinks.sh API key and may spend a paid API call.

Mitigation: Prefer offline urls or gsc-csv sources when possible, and use the backlinks source only when the API key and cost are acceptable.

Risk: The shipped allowlist and build-history dataset are examples from the publisher and can misclassify or overwrite a user's own backlink history if reused unchanged.

Mitigation: Review and replace the allowlist and historical series before using --write-state or build-history.mjs --yes.

Risk: GitHub source results are traffic referrers, not raw backlinks, and ambiguous hosts require human resolution.

Mitigation: Treat GitHub counts as referrer signals and manually resolve ambiguous URLs before relying on ours versus organic totals.

## Reference(s):

- [Backlink sources reference](references/sources.md)
- [TinkerClaw repository](https://github.com/globalcaos/tinkerclaw)
- [ClawHub skill listing](https://clawhub.ai/globalcaos/skills/backlink-audit)
- [backlinks.sh](https://backlinks.sh)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Console report or JSON, with setup and usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write backlink counts to an OpenClaw state file when explicitly requested.]

## Skill Version(s):

1.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
