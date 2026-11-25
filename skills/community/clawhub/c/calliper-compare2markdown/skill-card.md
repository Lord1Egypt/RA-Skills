## Description:

Compare two local documents and convert differences into LLM-ready Markdown in one synchronous call. Supports PDF, Word, PPT, and image documents accepted by Calliper, and returns a structured markdown diff table suitable for change review, clause comparison, downstream extraction, and rule-based validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paodingai](https://clawhub.ai/user/paodingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can compare two local documents and review the returned Markdown diff table for changes, clause differences, or downstream extraction and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious because the workflow uploads documents, includes an install command that adds external skills, and has an unpinned download source; one script was only partially inspected.

Mitigation: Before installing or using it, verify the external CLI and repository source, understand where documents are sent, confirm uploads are acceptable, and account for the incomplete script inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paodingai/skills/calliper-compare2markdown)
- [PDRouter platform API](https://platform.paodingai.com/platform/)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown diff table or returned API text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print the result and optionally save it to a Markdown file.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
