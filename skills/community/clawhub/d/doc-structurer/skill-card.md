## Description:

Doc Structurer classifies parsed Korean business documents and converts key fields into structured JSON for downstream document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill after document parsing to classify documents, extract dates, entities, financial fields, action items, and summaries, and prepare a JSON array for Notion or calendar follow-up workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Structured output can contain document metadata, dates, financial fields, summaries, and other sensitive business content that may later be sent to external tools.

Mitigation: Review structured_results.json before passing the output to Notion, calendar sync, or any other external service.

Risk: Keyword-based classification and field extraction may produce low-confidence document types or missing fields.

Mitigation: Check the processing summary for low-confidence classifications and missing fields, then correct important records before using them operationally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkbeomjun-gkgkgk/skills/doc-structurer)
- [Publisher Profile](https://clawhub.ai/user/parkbeomjun-gkgkgk)

## Skill Output:

**Output Type(s):** [json, text, shell commands]

**Output Format:** [JSON file plus a concise text processing summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes structured_results.json by default when an output path is not provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
