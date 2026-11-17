## Description:

Inspect delimited tables such as CSV and TSV files before analysis by reporting column names, encodings, delimiters, row counts, inferred types, and first or last rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-ht](https://clawhub.ai/user/alex-ht)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect CSV, TSV, TAB, and similar delimited text files before downstream parsing or analysis. It helps capture schema, encoding, delimiter, row count, inferred types, and small previews without loading the full table into the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Previewing selected CSV contents can expose sensitive file data in terminal output or an agent transcript.

Mitigation: Use the skill only on approved files, keep preview sizes small, and prefer --json when structured output reduces unnecessary display.

Risk: Highly sensitive, attacker-supplied, or extremely large CSV files may carry terminal-output or hardening risks identified by the security review.

Mitigation: Avoid those inputs until output sanitization and bounded encoding detection are added, and review generated output before reuse.

## Reference(s):

- [CSV Inspect on ClawHub](https://clawhub.ai/alex-ht/skills/csv-inspect)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, json]

**Output Format:** [Markdown guidance with shell command examples; CLI output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI streams the file, defaults to five head rows and zero tail rows, and infers types from the first 200 data rows unless configured otherwise.]

## Skill Version(s):

1.2.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
