## Description:

Converts office documents, spreadsheets, presentations, ebooks, CSV files, and PDFs to GitHub-Flavored Markdown so agents can read document contents as text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to convert local document formats into GitHub-Flavored Markdown before reading, summarizing, or analyzing the contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A lasting PATH-first wrapper can shadow an existing anydoc command.

Mitigation: Check whether an anydoc command already exists before creating the wrapper, and review PATH ordering before use.

Risk: The wrapper runs a mutable remote package through bunx.

Mitigation: Prefer a pinned, locally installed anydoc version for production or repeatable workflows.

Risk: The hosted Parse API can involve uploading documents to a third-party service.

Mitigation: Avoid hosted parsing for confidential documents unless third-party upload is acceptable.

## Reference(s):

- [Firecrawl Parse](https://firecrawl.dev/parse)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write converted Markdown to stdout or a file; large documents should be written to a file before selective reading.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
