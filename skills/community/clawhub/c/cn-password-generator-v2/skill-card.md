## Description:

Generate cryptographically secure random passwords with customizable character sets and configurable length, count, and character classes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to generate random passwords, API keys, or tokens from a local Python script with selectable uppercase, lowercase, digit, and symbol character classes. It is intended for straightforward command-line password generation without external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid options can silently produce empty passwords, including when no character classes are enabled or a non-positive length is supplied.

Mitigation: Validate length and enabled character classes before relying on generated values, and reject empty password output in automation.

Risk: Excessive password counts or lengths could cause avoidable local resource use in automated workflows.

Mitigation: Set reasonable maximums for count and length when wrapping this script in tooling or CI jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-password-generator-v2)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [JSON from the password generator script, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one or more generated password strings and reports the requested password length.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
