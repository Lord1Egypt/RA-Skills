## Description:

Collects public Douyin creator videos and engagement metrics from a profile link, with optional CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and marketing teams use the skill to review public Douyin creator posts, compare account performance, and export video lists for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default service address uses plain HTTP, which can expose the saved bearer token in transit.

Mitigation: Set a verified HTTPS base URL with a valid certificate before logging in or collecting data; review the locally saved token.

Risk: Disabling TLS certificate checks permits interception of HTTPS traffic.

Mitigation: Keep insecure TLS disabled and use a service endpoint with valid certificates.

Risk: Collection consumes paid credits, and the CLI does not enforce a charge-confirmation step.

Mitigation: Check the balance and expected charge, then obtain explicit user confirmation before each collect command.

Risk: Exported creator and video records may be mishandled or used beyond the authorized purpose.

Mitigation: Collect only public or authorized data and protect any exported CSV files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cuiyunhai/skills/dy-profile)

## Skill Output:

**Output Type(s):** [JSON data, CSV files, Text summaries]

**Output Format:** [JSON task results and optional CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One public profile and 1–10 pages per task; CSV results available for seven days.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
