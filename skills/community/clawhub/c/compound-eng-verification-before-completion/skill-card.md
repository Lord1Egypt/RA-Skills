## Description:

Requires fresh, claim-matched verification before reporting work complete or editing when a request's scope is ambiguous.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to choose and run checks that support a completion or release claim, preserve the evidence, and report verification limits clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification suites or migrations can alter data when pointed at a shared or non-disposable database or service.

Mitigation: Confirm the effective database and service targets before running checks; use a dedicated test database, container, or throwaway schema, and verify migration rollback behavior.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iliaal/skills/compound-eng-verification-before-completion)
- [Proof integrity](artifact/references/proof-integrity.md)
- [Verification oracles](artifact/references/verification-oracles.md)
- [Claims and failures](artifact/references/claims-and-failures.md)
- [Scope and sweeps](artifact/references/scope-and-sweeps.md)
- [Change strategies](artifact/references/change-strategies.md)
- [Isolated verification](artifact/references/isolated-verification.md)
- [System-wide test check](artifact/references/system-wide-test-check.md)
- [Performance measurement](artifact/references/performance-measurement.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with shell command examples and verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks and evidence depend on the repository and the claim; no fixed report template.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
