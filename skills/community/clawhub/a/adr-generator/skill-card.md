## Description:

Architecture Decision Record generator - analyze codebases and document technical decisions with context, alternatives, and consequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create Architecture Decision Records for significant technical choices, including framework selection, API contracts, tool adoption, and trade-off decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command placeholders such as keywords, package names, and imports may be unsafe if pasted directly into a shell.

Mitigation: Treat placeholder values as untrusted input; pass them as separate command arguments or quote them safely.

Risk: Retrospective ADRs can miss or overstate the original alternatives and rationale.

Mitigation: Have decision owners review the generated context, alternatives, and consequences before accepting the ADR.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown ADR content with optional shell command snippets for repository analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Michael Nygard ADR structure and suggests conventional docs/adr file organization.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
