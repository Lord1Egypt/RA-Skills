## Description:

Phone number normalizer that converts local and international phone numbers to E.164 format for canonical storage or comparison without using an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to normalize user-entered phone numbers for database deduplication, SMS gateway formatting, contact workflows, and comparison. It is not a reachability or phone ownership verification service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default country behavior may normalize local numbers incorrectly when documentation, code defaults, or caller expectations differ.

Mitigation: Set the country code explicitly in CLI or Python usage and test expected locales before production use.

Risk: The skill validates format, country prefix, and length but does not prove that a number is reachable or owned by a user.

Mitigation: Use a separate phone verification or messaging provider workflow when reachability, deliverability, or ownership matters.

Risk: Country coverage and length rules may not cover every numbering-plan edge case for all deployment locales.

Mitigation: Review supported country data and add locale-specific tests before relying on the skill for high-volume or regulated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-phone-e164)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and Python examples; CLI output is plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local normalization with no network calls evidenced by security scan.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
