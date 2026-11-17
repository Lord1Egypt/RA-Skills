## Description:

Identifies Chinese express couriers from tracking numbers, guides official or aggregator lookup, parses shipment timelines, flags abnormal logistics states, and suggests next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhili007](https://clawhub.ai/user/zhili007)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers, support agents, and agent developers use this skill to identify the carrier for a package tracking number, choose a trustworthy lookup path, summarize logistics status, and decide what to do when delivery appears delayed, returned, or incorrectly marked as signed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers may be shared with courier websites or aggregators such as kuaidi100 during lookup.

Mitigation: Share only the tracking number needed for the query and avoid adding extra personal or verification details unless the user understands which official site is requesting them.

Risk: Some courier lookups may request phone-number suffixes, login, or captcha verification.

Mitigation: Use official courier channels where possible, stop before providing verification details, and ask the user to confirm whether they want to continue.

Risk: Carrier identification can be ambiguous for some tracking-number formats.

Mitigation: Show confidence or multiple candidates, prefer official lookup results, and double-check outcomes when postal-carrier identification matters.

## Reference(s):

- [Carrier Identification Rules](artifact/references/carriers.md)
- [Official Courier Source Configuration](artifact/config/official_sources.json)
- [ClawHub Skill Page](https://clawhub.ai/zhili007/skills/express-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text status summaries, with optional JSON from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include courier candidates, confidence, query paths, source URLs, logistics timelines, abnormal-status checks, and recommended next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
