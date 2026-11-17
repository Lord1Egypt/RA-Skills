## Description:

Uses the local epub2md CLI to inspect EPUB files, convert them into chapter Markdown files, merge them into a single Markdown file, localize remote images, or unzip EPUB contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujuntao123](https://clawhub.ai/user/liujuntao123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user needs to inspect an EPUB, export it as Markdown chapter files, create a merged Markdown file, localize referenced remote images, or unpack EPUB contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing epub2md globally without pinning a reviewed version.

Mitigation: Pin epub2md to a reviewed version and prefer a local project installation over a global npm install.

Risk: The wrapper writes files and can clean existing output directories.

Mitigation: Run conversions in a dedicated disposable workspace root and avoid pointing --workspace-root at valuable project directories.

Risk: Using --localize may download remote images referenced by an EPUB.

Mitigation: Use --localize only for trusted EPUBs or when outbound network requests are acceptable.

## Reference(s):

- [Epub2md Cli on ClawHub](https://clawhub.ai/liujuntao123/skills/epub2md-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Markdown files, copied EPUB inputs, inspection text files, extracted EPUB contents, and image assets in a workspace directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
