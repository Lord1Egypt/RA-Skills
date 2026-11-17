## Description:

Doc Parse helps agents parse .doc and .docx Word documents into structured Markdown with preserved headings, lists, tables, and paragraphs using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content managers use this skill to convert Word documents from local files or URLs into structured Markdown for downstream analysis, migration, or content processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive documents may be processed through third-party MinerU/OpenDataLab tooling without clear privacy disclosure.

Mitigation: Avoid sensitive or regulated documents unless content processing and retention are verified for the intended workflow.

Risk: CLI behavior can change if users install an unpinned latest package.

Mitigation: Pin mineru-open-api to a reviewed version where possible and re-review before upgrading.

Risk: The CLI only needs the source documents and output location, but broad filesystem access can expose unrelated files.

Mitigation: Run the parser with access limited to the input files and output directory needed for the task.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU API token management](https://mineru.net/apiManage/token)
- [OpenDataLab MinerU](https://github.com/opendatalab/MinerU)
- [Doc Parse on ClawHub](https://clawhub.ai/mzlzyca/skills/doc-parse)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with bash command examples and CLI output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Markdown to stdout by default or files under an output directory when -o is used; .doc parsing requires MINERU_TOKEN.]

## Skill Version(s):

0.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
