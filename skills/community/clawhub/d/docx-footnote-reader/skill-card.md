## Description:

Extract footnotes, endnotes, and body text from .docx files using Node.js. Use this skill when you need to read footnote/endnote content from Word documents, such as technical specifications, legal documents, or academic papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landylai0604](https://clawhub.ai/user/landylai0604)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, technical writers, legal reviewers, and academic users use this skill to extract Word document body text, footnotes, and endnotes for review or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm install may resolve newer dependency versions over time because word-extractor is specified with a range and no lockfile is included.

Mitigation: Pin word-extractor and commit a lockfile before relying on the skill for sensitive or repeatable document processing.

Risk: Local DOCX parsing may expose sensitive document content to the local runtime and dependency code.

Mitigation: Run the skill under a normal unprivileged account and review where extracted document text is printed or stored.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces body text plus arrays of footnote and endnote strings when used through the Node.js API.]

## Skill Version(s):

1.0.0 (source: package.json and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
