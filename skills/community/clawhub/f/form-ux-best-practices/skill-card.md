## Description:

Opinionated form UX and accessibility workflow for signup, checkout, settings, and lead-gen forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design)

### License/Terms of Use:

MIT

## Use Case:

Product teams, designers, developers, and accessibility reviewers use this skill to audit form specs or implementations and produce prioritized UX, accessibility, validation, microcopy, and implementation-readiness guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local static audit reads form HTML supplied by the user.

Mitigation: Run it only on form files intended for review, as recommended by the server security guidance.

Risk: The optional API upload example sends a packaged skill using an API key.

Mitigation: Use the upload command only in environments where sending the package to the OpenAI Skills API is intended and authorized.

Risk: Form recommendations can affect checkout, signup, consent, or accessibility behavior.

Mitigation: Review generated changes against product, legal, privacy, and accessibility requirements before shipping.

## Reference(s):

- [Form UX Canon](references/canon.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with optional semantic HTML or React pseudo-code and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the bundled report template sections for top issues, field rewrites, validation behavior, accessibility checks, ship-ready checks, and optional snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
