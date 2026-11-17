## Description:

Runs nightly public-web and community searches to identify, rank, and draft evidence-backed connection briefs for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltlife](https://clawhub.ai/user/moltlife)

### License/Terms of Use:

MIT

## Use Case:

Sales, partnership, and agency operators use this skill to scout public sources for warm introduction opportunities, rank candidates by fit and evidence quality, and prepare connection briefs with draft outreach for human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches public web and community content for professional leads and can produce profile-based outreach drafts.

Mitigation: Review every candidate and draft manually, keep auto-send disabled, honor platform rules and privacy laws, and use avoid lists before outreach.

Risk: Scheduled or daemon-style runs may repeatedly fetch pages or deliver reports to configured external channels.

Mitigation: Use run budgets and strict tool allowlists, prefer pinned or verified CLI versions, and only enable delivery targets after configuration review.

Risk: Candidate matches may be based on incomplete, stale, or weak public evidence.

Mitigation: Require multiple evidence URLs, inspect risk flags such as low_evidence or unclear_identity, and verify fit before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltlife/skills/claw-clawbridge)
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started)
- [Connection Brief schema](schema/connection_brief.json)
- [Sample Connection Brief](examples/sample_run.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured JSON and human-readable Markdown connection briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked candidates, evidence URLs, risk flags, scoring details, suggested intro and follow-up drafts, and recommended next actions for human review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
