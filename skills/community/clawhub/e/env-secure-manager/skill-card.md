## Description:

Manages environment variables and secrets for agents with encryption, redaction, listing, deletion, retrieval, and environment import actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayalili](https://clawhub.ai/user/ayalili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can store, retrieve, list, delete, redact, and bulk-load environment variables or API keys during agent workflows. Because the security review flags possible exposure of protected values, use only in tightly controlled environments until key handling and retrieval authorization are addressed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The encryption key can be exposed, which can compromise stored secrets.

Mitigation: Do not print or persist generated keys in logs; inject keys through a managed secret channel and rotate any key that was exposed.

Risk: A broad environment import can collect more sensitive variables than intended.

Mitigation: Use narrowly scoped prefixes and review allowed variable names before loading process environment values.

Risk: Stored secrets can be returned when documented retrieval flags are set.

Mitigation: Restrict secret retrieval to trusted callers and add real authorization checks before enabling secret-returning actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayalili/skills/env-secure-manager)
- [Deno zod module](https://deno.land/x/zod@v3.22.4/mod.ts)
- [Deno standard crypto module](https://deno.land/std@0.214.0/crypto/mod.ts)
- [Deno standard hex encoding module](https://deno.land/std@0.214.0/encoding/hex.ts)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [JSON-compatible objects containing status fields, strings, redacted text, or environment-variable maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return stored secret values when documented retrieval flags are enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
