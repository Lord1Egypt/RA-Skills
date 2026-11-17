## Description:

Brief Yourself helps an agent build and use a consent-gated personal context layer for a person, including bounded interviews, source authorization, calibrated claims, frozen Context Views for tasks, and user-reviewed Context Patches after tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bagel-ew](https://clawhub.ai/user/bagel-ew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to establish, update, inspect, export, and apply personal context for a person with explicit source consent and calibration. It is intended for preparing task-specific personal context for downstream work such as writing, interviews, collaboration, decisions, and post-task review without silently importing or syncing harness memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal context may disclose private or restricted information if broad source reads, audiences, purposes, or downstream persistence are approved too casually.

Mitigation: Review each authorization card, keep source scope narrow, default to public or minimum-necessary context, and require explicit approval for private, restricted, or downstream-persistent use.

Risk: Inaccurate or overconfident personal claims could become durable context if pending patches are applied without careful review.

Mitigation: Apply only specific, user-reviewed Patch proposals with explicit approval; keep unreviewed, unresolved, or inferential material pending, corrected, challenged, retired, or rejected.

Risk: A frozen Context View can be misused if it is reused after expiry or outside its approved task, purpose, audience, or allowed use.

Mitigation: Validate the View envelope, TTL, purpose, task, audience, disclosure, and allowed-use fields before use, and regenerate a fresh View when the task or permissions change.

## Reference(s):

- [Brief Yourself Skill Release](https://clawhub.ai/bagel-ew/skills/brief-yourself)
- [Context View And Patch Protocol](artifact/context-view-and-patch.md)
- [Source Consent And Disclosure](artifact/source-consent-and-disclosure.md)
- [Harness Memory, Personal Context, And Task Context Boundaries](artifact/harness-boundaries.md)
- [Personal Context Model](artifact/personal-context-model.md)
- [Store Operations](artifact/store-operations.md)
- [Interview And Calibration](artifact/interview-and-calibration.md)
- [V0.3 To 1.0.1 Migration](artifact/migration-v0.3-to-v1.0.1.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON context artifacts, schemas, and local shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces purpose-bound personal context outputs such as Human Briefs, candidate Claims, Tensions, Unknowns, frozen Context Views, and pending Context Patches.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
