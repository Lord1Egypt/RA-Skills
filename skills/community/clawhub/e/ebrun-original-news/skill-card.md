## Description:

Fetches the latest original e-commerce news from Ebrun by mapping channel requests to configured news feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebrun-developer](https://clawhub.ai/user/ebrun-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve recent Ebrun e-commerce articles by main or sub-channel and format them for briefings, dashboards, or automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Ebrun for news and may check Ebrun, GitHub, or Gitee for version data.

Mitigation: Confirm this outbound network access is acceptable before installation and treat update prompts as advisory.

Risk: The security summary flags automatic update checks and unsafe shared temp-cache behavior.

Mitigation: Review, disable, or fix the update checker and cache behavior before use in shared or sensitive environments.

## Reference(s):

- [API Reference](artifact/references/api-reference.md)
- [Channel List](artifact/references/channel-list.json)
- [Version Metadata](artifact/references/version.json)
- [Ebrun](https://www.ebrun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news summaries and JSON-compatible article fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 latest articles by default, including title, author, summary, publish time, and source URL.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/references/version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
