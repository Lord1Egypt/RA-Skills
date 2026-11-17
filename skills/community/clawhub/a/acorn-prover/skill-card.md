## Description:

Verify and write proofs using the Acorn theorem prover for mathematical and cryptographic formalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingnobita](https://clawhub.ai/user/flyingnobita)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, verify, troubleshoot, and maintain Acorn proof files for mathematical and cryptographic formalization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied Acorn library or project paths could be written into a shell config file and later interpreted as shell code.

Mitigation: Use only trusted, ordinary local paths without shell metacharacters or newlines, inspect config.env before sourcing it, and update the setup script to quote or data-encode configuration values.

Risk: The skill runs local proof, training data, and documentation commands that may operate on user-selected project directories.

Mitigation: Review commands before execution and show full command output so users can verify results and diagnose failures.

## Reference(s):

- [Acorn Syntax Reference](references/syntax.md)
- [ClawHub skill page](https://clawhub.ai/flyingnobita/skills/acorn-prover)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Acorn code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full command output, verification results, troubleshooting notes, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
