## Description:

Use blind-review-sanitizer for academic writing workflows that need structured anonymization, explicit assumptions, and clear output boundaries for double-blind submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Academic authors, editors, and review-support agents use this skill to prepare manuscripts for double-blind peer review by removing or highlighting likely identity cues and separating automated changes from remaining manual checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removed identifying information can be re-exposed in console summaries or captured logs.

Mitigation: Run only in a local, trusted workspace and avoid shared CI, transcript capture, or agent logs when processing sensitive manuscripts.

Risk: Output paths may overwrite existing writable files if they are chosen carelessly.

Mitigation: Inspect input and output paths before execution and write sanitized files to a reviewed location.

Risk: The declared dependency is under-specified for normal .docx processing.

Mitigation: Correct and pin the document-processing dependency before routine use, and fall back to .md or .txt processing if the dependency is unavailable.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/blind-review-sanitizer-1)

## Skill Output:

**Output Type(s):** [files, text, markdown, shell commands, guidance]

**Output Format:** [Sanitized manuscript files with Markdown or plain-text summaries and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supported manuscript inputs are .docx, .md, and .txt; final anonymity still requires human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
