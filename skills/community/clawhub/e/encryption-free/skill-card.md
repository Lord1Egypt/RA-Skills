## Description:

This skill helps agents handle file encryption, password hash checks, key rotation review, and encryption-practice auditing for data protection workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and data-protection operators can use this skill to ask an agent for encryption-related file handling, password security checks, key-management guidance, and code encryption practice reviews. It is not intended for unrelated system configuration or network administration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request file-write and command authority for encryption workflows where the changed files, output paths, algorithms, and original-file handling are not clearly specified.

Mitigation: Use backed-up test files first and require the agent to confirm the input file, output location, selected algorithm, and whether originals are preserved before execution.

Risk: The documented scoring-style result format may be mistaken for proof that encryption succeeded.

Mitigation: Verify encrypted outputs and recovery steps independently before relying on the result summary for security or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/encryption-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with optional JSON-style result summaries and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe encrypted file outputs, password hashes, key rotation records, compliance checks, and follow-up improvements.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
