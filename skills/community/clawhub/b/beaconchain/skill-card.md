## Description:

Monitor Ethereum validator dashboard health on beaconcha.in via V2 API, focused on one-check-per-day status and BeaconScore-first triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisjeron](https://clawhub.ai/user/thisisjeron)

### License/Terms of Use:


## Use Case:

Developers, operators, and Ethereum validator owners use this skill to run concise daily checks of a Beaconcha.in dashboard and triage BeaconScore or missed-duty issues without unnecessary detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beaconcha.in API credentials are required to check dashboard health.

Mitigation: Use a scoped or revocable API key and provide credentials only through environment variables or explicit CLI flags when running the checker.

Risk: Validator monitoring output depends on Beaconcha.in API availability, account permissions, and rate limits.

Mitigation: Run the checker manually or under a schedule you control, and treat authentication, rate-limit, or endpoint failures as errors requiring operator review.

## Reference(s):

- [Beaconcha.in API Notes](references/api-notes.md)
- [Beaconcha.in](https://beaconcha.in)
- [Beaconcha.in performance-aggregate endpoint](https://beaconcha.in/api/v2/ethereum/validators/performance-aggregate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text status summaries with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BEACONCHAIN_API_KEY and BEACONCHAIN_DASHBOARD_ID; script exits 0 for good, 2 for bad, and 1 for errors.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
