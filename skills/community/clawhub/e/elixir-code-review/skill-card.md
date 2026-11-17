## Description:

Reviews Elixir code for idiomatic patterns, OTP basics, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Elixir .ex and .exs files for idiomatic style, pattern matching, OTP usage, documentation, and selected security-sensitive constructs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires loading a sibling review-verification-protocol file that is not included in the artifact, so that external file can affect review behavior and outputs.

Mitigation: Install and review the expected sibling protocol before use, and only use this skill when that dependency comes from a trusted, controlled package or path.

## Reference(s):

- [Elixir Code Style](references/code-style.md)
- [Pattern Matching](references/pattern-matching.md)
- [OTP Basics](references/otp-basics.md)
- [Documentation](references/documentation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown review findings with code references and supporting evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be anchored to file locations or module/function identifiers and backed by reviewed artifacts.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
