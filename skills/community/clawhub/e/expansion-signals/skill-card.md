## Description:

Helps customer teams identify expansion and renewal opportunities from won deals and dated public events, then records each signal and posts a weekly Slack digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations teams and account managers adapt this workflow to identify customers nearing renewal, review expansion or at-risk signals, and share an internal weekly digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer renewal status and expansion reasons may be exposed in account records or Slack.

Mitigation: Authorize the Slack and Anthropic connectors intentionally, verify the destination channel is internal, and limit access to customer records and the digest.

Risk: An unreviewed workflow could write inaccurate expansion judgments to customer accounts.

Mitigation: Review the deployment plan and diff, verify source-backed reasons, and pilot on a few records before enabling the play.

## Reference(s):

- [Expansion plays example](references/expansion-plays.md)
- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/expansion-signals)
- [Project homepage listed in skill metadata](https://github.com/getcargohq/gtm-skills)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When deployed, records customer expansion signals and reasons on account records and posts a weekly Slack digest.]

## Skill Version(s):

0.1.2 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
