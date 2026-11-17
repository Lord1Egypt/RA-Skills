## Description:

Reviews Elixir code for security vulnerabilities including code injection, atom exhaustion, and secret handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to review Elixir code that handles user input, external data, or sensitive configuration and to identify issues such as code injection, unsafe atom creation, exposed secrets, and process data exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpackaged sibling review-verification-protocol skill before reporting findings, which could suppress or alter valid security review output if that dependency is unavailable or untrusted.

Mitigation: Install only with a trusted review-verification-protocol skill in the same environment, or require the publisher to package the full protocol with this skill before use.

## Reference(s):

- [Atom Exhaustion](references/atom-exhaustion.md)
- [Code Injection](references/code-injection.md)
- [Process Exposure](references/process-exposure.md)
- [Secrets and Configuration](references/secrets.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown security review findings with file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to follow the skill's issue format and hard-gate verification checklist.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
