## Description: <br>
Create a simple, repeatable daily review workflow across whatever conversation surfaces are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panpansirius-cloud](https://clawhub.ai/user/panpansirius-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to run a recurring 24-hour review across available conversation channels, producing per-channel raw notes, one synthesized daily review, index updates, verification output, and an optional management summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-session content may be summarized into persistent local review files that could contain sensitive or business-confidential information. <br>
Mitigation: Use the skill only for intended review workflows, inspect generated summaries before sharing, and store the memory/daily-review output tree according to the user's confidentiality requirements. <br>
Risk: A preferred delivery destination may be unavailable, causing the workflow to choose a fallback destination. <br>
Mitigation: Use generate-only mode or explicitly confirm the resolved destination before external delivery when summaries may contain sensitive content. <br>
Risk: Retention and archive helpers can affect how long local review artifacts remain available. <br>
Mitigation: Review retention and archive settings before enabling lifecycle automation, and keep deletion disabled unless the policy has been hardened for the environment. <br>
Risk: Promoted review rules can make daily findings durable in local workflow memory. <br>
Mitigation: Review local rules.md promotion behavior before running the workflow on confidential or sensitive channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panpansirius-cloud/cross-channel-daily-review) <br>
- [Architecture](references/architecture.md) <br>
- [Channel Adapter Spec](references/channel-adapter-spec.md) <br>
- [Delivery Modes](references/delivery-modes.md) <br>
- [Failure Handling](references/failure-handling.md) <br>
- [Lifecycle Automation](references/lifecycle-automation.md) <br>
- [Known Limitations](references/known-limitations.md) <br>
- [Release Readiness](references/release-readiness.md) <br>
- [Validation Report](references/validation-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON index records, and command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-channel raw review files, one synthesized daily review, index metadata, optional management summary files, periodic rollups, retention plans, and verification results under memory/daily-review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
