## Description:

Auth Guard standardizes API credential handling, startup auth checks, helper-script usage, and fallback policy to prevent missing-key and unauthorized-call regressions across agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adainthelab](https://clawhub.ai/user/adainthelab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create a consistent credential source, authenticated helper command, startup probe, and fallback policy for services that return intermittent 401/403 errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auth probe can send a local API token to a caller-supplied HTTPS URL.

Mitigation: Run the probe only with trusted service auth endpoints, add a fixed host allowlist before using real tokens, and keep credential paths limited to canonical service locations.

Risk: Policy snippets can change future agent behavior through HEARTBEAT.md, AGENTS.md, or workspace/.pi/ helper scripts.

Mitigation: Review proposed policy and helper changes before adoption, especially rules that affect credential handling or recurring authenticated requests.

## Reference(s):

- [Keychain Contract](references/contract.md)
- [Drop-in Snippets](references/snippets.md)
- [Service Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and reusable policy snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Auth probe output uses concise status strings such as AUTH_OK, AUTH_MISSING, AUTH_FAIL_UNAUTHORIZED, and AUTH_FAIL_OTHER.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
