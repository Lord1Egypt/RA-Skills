## Description:

Finds, ranks, and shortlists directories, listing sites, and launch platforms where software product teams can submit SaaS products, apps, tools, or startups for backlinks, referral traffic, and launch-day reach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, marketers, and launch operators use this skill to identify product directories and launch platforms, compare them by authority and reach, and prepare prioritized submission shortlists. It is intended for software products and startups, not agency hiring, local business listings, or finding products inside directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback described by the artifact sources a local .env file, which can execute unintended shell code or expose unrelated secrets.

Mitigation: Prefer the ServiceGraph MCP/OAuth path; if REST is used, load only SERVICEGRAPH_API_KEY through a narrow wrapper that does not source arbitrary shell files.

Risk: Unlocking directory rows can spend ServiceGraph credits.

Mitigation: Confirm the exact unlock batch and cost with the user before making paid unlock requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-product-directories)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with ranked lists, concise guidance, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API call plans, filter expressions, unlock-cost notes, and submission-prioritization rationale.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
