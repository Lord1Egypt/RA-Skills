## Description:

Route natural-language TikTok commerce intelligence requests into authenticated EchoTik API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and commerce analysts use this skill to turn TikTok commerce research requests into EchoTik API workflows for creator discovery, product research, seller analysis, video intelligence, live lookup, search, and business reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can store EchoTik credentials persistently as plaintext in a shell profile.

Mitigation: Prefer session-only environment variables or a secret manager, avoid passing passwords as command-line flags unless the local exposure is acceptable, and rotate credentials if they have already been stored in dotfiles or logs.

Risk: The skill performs authenticated EchoTik API calls from the user's account.

Mitigation: Review intended workflows and requested parameters before execution, and confirm that the account, quota, and data-access expectations are appropriate for the task.

Risk: Offline EchoTik endpoints may return delayed, sparse, or empty data.

Mitigation: Present results as EchoTik API snapshots and use documented realtime fallback paths or freshness caveats when the artifact rules call for them.

## Reference(s):

- [Global Atomic Rules](references/global-rules.md)
- [Routing Policy](references/routing-policy.md)
- [Scenario Cards](references/scenarios.md)
- [Business Orchestration Playbooks](references/orchestration-playbooks.md)
- [Setup And Auth](references/setup-and-auth.md)
- [Influencer Module Rules](references/influencer-rules.md)
- [Product Module Rules](references/product-rules.md)
- [Seller And Shop Module Rules](references/seller-rules.md)
- [Video Module Rules](references/video-rules.md)
- [Search Module Rules](references/search-rules.md)
- [Live Module Rules](references/live-rules.md)
- [EchoTik Documentation Index](https://opendocs.echotik.live/llms.txt)
- [EchoTik Authentication Documentation](https://opendocs.echotik.live/authentication)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON API results when execution is performed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EchoTik Basic Authentication credentials and may call EchoTik APIs through local Node.js scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
