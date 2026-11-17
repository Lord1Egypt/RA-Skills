## Description:

Email Url Validator validates email addresses, URLs, and domains with live DNS, HTTP reachability, DNSBL, disposable-domain, redirect-chain, and related checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vannelier](https://clawhub.ai/user/vannelier)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent pipelines use this skill to check whether submitted emails, URLs, domains, and contact files are usable before sending messages, importing contacts, or acting on links. It is most useful when live network validation and a concise recommended action are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation workflows can transmit email addresses, URLs, domains, and spreadsheet contents to a hosted third-party service.

Mitigation: Require an explicit cost quote and user approval before validation, remove unrelated columns before file upload, and self-host for sensitive or regulated datasets.

Risk: Paid validation calls consume Nevermined credits, especially for bulk lists or files.

Mitigation: Use the free batch classification endpoints before paid validation, show the item count and total cost, and use autonomous mode only for pre-authorized pipelines.

Risk: Async file workflows with arbitrary webhook URLs can disclose job status or operational data to destinations the user does not control.

Mitigation: Use webhook callbacks only with user-controlled destinations, or poll job status directly when the destination cannot be verified.

Risk: A self-hosted horizontally scaled deployment can weaken rate limiting because the bundled limiter is in memory per instance.

Mitigation: Run a single replica or replace the limiter with a shared backend such as Redis before scaling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vannelier/skills/email-url-validator)
- [Hosted validation API](https://deep-validator-production.up.railway.app)
- [Declared source code](https://github.com/nathanleclaire/Agent_Validator)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON responses and CSV/XLSX result files, with recommended actions suitable for Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include recommended_action, action_reason, risk flags, redirect chains, confidence scores, typo suggestions, and async job identifiers.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
