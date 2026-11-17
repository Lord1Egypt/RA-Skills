## Description:

Second-opinion consultation plus automatic skill-engineering escalation for reviews, rewrites, hardening, weak-model optimization, packaging, testing, and publish readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use Dual Thinking to run structured second-opinion review rounds for agent decisions and skill artifacts, especially reviews, rewrites, hardening, weak-model optimization, packaging, testing, and publish readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed artifacts or local context can be exposed to external or persistent consultant sessions during normal use.

Mitigation: Do not use the skill on secrets, customer data, private source, or sensitive local runtime instructions unless the content is redacted and the disclosure scope is explicitly approved.

Risk: Packaging or validation helper scripts may have unsafe dependency assumptions for unsandboxed local execution.

Mitigation: Run packaging scripts only in a sandbox or after replacing global dependency assumptions with pinned project-local dependencies.

Risk: Automatic patching or self-modifying review flows can introduce incorrect changes if accepted without oversight.

Mitigation: Require human diff review before any real artifact patch, release claim, or publish-readiness decision is accepted.

## Reference(s):

- [Dual Thinking Governance](GOVERNANCE.md)
- [Runtime Contract](references/runtime-contract.md)
- [Modes](references/modes.md)
- [Round Output Contract](references/round-output-contract.md)
- [Failure Handling](references/failure-handling.md)
- [Validator Schema](references/validator-schema.md)
- [Verification Evidence](references/verification-evidence.md)
- [Reference Test Log](references/reference-test-log.md)
- [Tests](tests/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown-style review blocks with optional code, shell commands, patch summaries, validation evidence, and resumable state snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the main agent to own synthesis and final decisions after self and consultant positions.]

## Skill Version(s):

8.5.24 (source: server release evidence, changelog, SKILL.md heading, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
