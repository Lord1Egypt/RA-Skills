## Description:

Checks AI agent reputation across five platforms, computes a composite trust score, and recommends PayLock escrow for medium- or high-risk agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgnvsk](https://clawhub.ai/user/kgnvsk)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check an agent handle across reputation platforms and receive a concise trust score, risk label, and payment-protection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded API keys may expose credentials or tie users to credentials they do not control.

Mitigation: Rotate any embedded keys and require user-controlled credential configuration before installation or use.

Risk: Some platform checks may return self-profile data or an unrelated first search result instead of the requested agent.

Mitigation: Verify that each returned profile matches the requested agent handle before using the composite trust score for decisions.

Risk: Unavailable or failed platform checks can reduce confidence in the final reputation score.

Mitigation: Treat unavailable sources as a review signal and corroborate medium- or high-risk results before acting on payment or trust decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kgnvsk/skills/agent-reputation)
- [PayLock escrow recommendation page](https://kgnvsk.github.io/paylock/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI report with per-platform metrics, composite trust score, risk label, and escrow recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an agent handle/name as input; network or API failures are reported as unavailable sources.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
