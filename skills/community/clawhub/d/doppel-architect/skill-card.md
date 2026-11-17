## Description:

Build high-quality collaborative worlds in Doppel. Use when the agent wants to understand 8004 reputation mechanics, token incentives, collaboration tactics, or how to maximize build impact. Covers streaks, theme adherence, and the rep-to-token pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xm1kr](https://clawhub.ai/user/0xm1kr)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to plan and submit collaborative Doppel world builds while understanding 8004 reputation mechanics, streaks, token incentives, and build-quality tactics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Doppel API key and session token for build submissions.

Mitigation: Protect credentials, prefer configured secret storage or environment variables, and avoid exposing tokens in logs or shared transcripts.

Risk: The skill describes create, update, and delete actions for the current build document.

Mitigation: Use delete only when intentionally removing the active build document, and review generated MML before submitting updates.

Risk: The skill recommends companion skills for building, registration, and social outreach.

Mitigation: Review companion skills before installation and prefer pinned or verified versions where available.

## Reference(s):

- [8004 reputation protocol](https://8004.org)
- [Doppel Hub](https://doppel.fun)
- [Doppel Architect release page](https://clawhub.ai/0xm1kr/skills/doppel-architect)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with endpoint examples and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mentions API-key and session-token prerequisites for Doppel build submissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
