## Description:

Analyzes acceptance-rate declines by locating abnormal slices and attributing changes across customer mix, funder distribution, asset dimensions, and sensitive-funder contraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzhou1982](https://clawhub.ai/user/mzhou1982)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and operations teams use this skill to run staged day or week acceptance-rate decline analysis. It helps identify abnormal customer or product slices and attribute the decline to mix shift, funder volume or distribution changes, asset-dimension signals, or sensitive-funder contraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-derived DataWorks access tokens may be persisted or exposed during use.

Mitigation: Review token handling before installation, avoid passing tokens on the command line, keep credentials in memory or a secure credential store, and remove any persisted BIGDATA_ACCESS_TOKEN values after use.

Risk: Endpoint overrides could direct protected analytics requests away from the intended DataWorks host.

Mitigation: Use a reviewed version that removes endpoint overrides or restricts requests to an allowlisted DataWorks endpoint.

Risk: Debug or raw query logging could expose sensitive request details.

Mitigation: Keep raw query logging disabled by default and inspect logs before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzhou1982/skills/acceptance-rate-analysis)
- [DataWorks inquiry page](https://data.jirongyunke.net/data-pc-bdopr-fe/hoc-inquiry/index)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, analysis]

**Output Format:** [Markdown reports with staged status blocks, tables, shell commands, and JSON-derived analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided analysis windows and a DataWorks access token to query protected data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
