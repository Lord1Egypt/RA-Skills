## Description:

Sentry error tracking - list, triage, and resolve issues; manage releases and source maps via CLI and REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Sentry errors, triage issue severity, manage releases, upload source maps, and propose Sentry CLI or REST API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands and API calls that can resolve, ignore, bulk-change issues, finalize releases, record deploys, or upload source maps.

Mitigation: Require explicit user confirmation before running any state-changing Sentry command or API request.

Risk: The skill documents an unverified pip install path for sentry-cli.

Mitigation: Prefer the official, provenance-checked Sentry CLI distribution and use the pip option only after independent trust review.

Risk: Sentry credentials may grant access to issue, event, release, or organization data.

Mitigation: Use a narrowly scoped token limited to the minimum Sentry permissions needed for the requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/cm-sentry-integration)
- [Sentry REST API base URL](https://sentry.io/api/0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline bash commands and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include state-changing Sentry operations that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
