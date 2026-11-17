## Description:

Audits an email program or pre-send campaign using a typed 20-item SEND profile covering authentication, consent, opt-out, engagement, lifecycle fit, claims, and outcome evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, email program owners, and agents use this skill to audit a campaign or email program before release, identify SEND scoring gaps, and report verified blockers without sending email or changing provider settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may require sensitive marketing evidence such as consent, suppression, engagement, provider, and outcome data.

Mitigation: Provide only the evidence needed for the audit and verify before authorizing any audit artifact to be saved.

Risk: Incomplete evidence can lead to an unsupported send decision.

Mitigation: Report missing qualified items as unknown and return NOT_SCORED or UNDECIDED when full SEND evidence or the deterministic scorer is unavailable.

Risk: An audit workflow could be confused with an email execution or provider-configuration task.

Mitigation: Use the skill only for evidence-based review; it explicitly avoids sending email or changing provider settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/email-quality-auditor)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone auditor runtime](references/auditor-runtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with explicit status, verdict, score_state, SEND item states, unknown inputs, and fix owners.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist a permissioned v3 audit artifact only after explicit authorization; standalone installs fail closed without scoring.]

## Skill Version(s):

19.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
