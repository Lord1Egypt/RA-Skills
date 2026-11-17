## Description:

Check domain availability and brainstorm names. Checks .com/.net/.org/.io/.ai/.co/.app/.dev and more. Suggests alternatives when taken. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephflu](https://clawhub.ai/user/josephflu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to check candidate domain names across common TLDs, generate alternatives when a .com is taken, and optionally brainstorm available names from a project description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brainstorm mode sends the user's description to OpenRouter when OPENROUTER_API_KEY is configured.

Mitigation: Avoid confidential product details, customer data, or secrets in brainstorm prompts.

Risk: DNS and whois availability checks can be inconclusive or differ from registrar availability.

Mitigation: Treat results marked available or unknown as preliminary and verify with a registrar before purchasing a domain.

## Reference(s):

- [Domain Name Checker Homepage](https://github.com/eagerbots/domain-name-checker)
- [Popular TLDs Reference](references/tlds.md)
- [OpenClaw Project](https://github.com/eagerbots/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal tables and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Basic checks use DNS and optional whois results; brainstorm mode uses OpenRouter when OPENROUTER_API_KEY is configured.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
