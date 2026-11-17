## Description:

File format converter. Detect formats, convert between JSON/YAML/XML/CSV/Markdown, minify and prettify code. Commands: detect, json2yaml, yaml2json, csv2md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use File Converter to inspect local files and convert common data formats during development, debugging, and documentation workflows. It supports local conversions and utilities for JSON, YAML, XML, CSV, Markdown, URLs, base64, SQL snippets, and file metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented commands and available script commands do not fully match, which can mislead users about the skill's actual behavior.

Mitigation: Review the installed scripts and invoke only expected commands for the release being evaluated.

Risk: The skill operates on local filenames and arguments and may process untrusted file contents.

Mitigation: Run it in a constrained workspace and avoid passing untrusted filenames, arguments, or files from sensitive directories.

Risk: Generated SQL output could be unsafe if executed without review.

Mitigation: Treat SQL output as a draft and inspect table names, column names, values, and escaping before using it with a database.

Risk: Generated HTML or XML may be unsafe in sensitive rendering contexts.

Mitigation: Sanitize generated HTML/XML and review it before rendering in browsers, applications, or privileged documentation systems.

## Reference(s):

- [File Converter ClawHub listing](https://clawhub.ai/ckchzh/skills/file-converter)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Plain text, JSON, YAML, XML, CSV, Markdown, HTML, SQL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file inputs are processed on the user's machine; conversion results are generally printed to stdout.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
