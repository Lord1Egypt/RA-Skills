## Description:

Extracts and returns plain text from PDF, Word, and Excel bid documents for analysis, search, or summarisation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezhencacao-dotcom](https://clawhub.ai/user/ezhencacao-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bid/tender analysts use Bid Reader to extract plain text from PDF, Word, and Excel bid documents so agents can search, summarize, or analyze the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may change behavior or introduce vulnerable transitive packages over time.

Mitigation: Install in a dedicated virtual environment or container, and pin and review dependency versions before use.

Risk: Extracted bid document text may be exposed to the surrounding agent workflow.

Mitigation: Run the skill only on documents whose full text is appropriate for the intended workflow.

## Reference(s):

- [Bid Reader ClawHub listing](https://clawhub.ai/ezhencacao-dotcom/skills/bid-reader)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local PDF, DOCX, XLSX, or XLS files and returns extracted document text; tables are flattened and complex formatting is not preserved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
