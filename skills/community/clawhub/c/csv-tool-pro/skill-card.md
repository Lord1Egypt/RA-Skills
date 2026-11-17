## Description:

CSV Tool Pro helps agents view, filter, sort, merge, split, deduplicate, convert, and analyze CSV files using a pure-Python local utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and data analysts use this skill to perform local CSV inspection, cleanup, conversion, aggregation, and simple analytics without external dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The utility can overwrite local files, including in-place sorting when no output path is provided.

Mitigation: Use explicit output paths, keep backups of important CSV files, and avoid in-place operations on original data.

Risk: Untrusted CSV content may be unsafe when viewed, converted, or opened in downstream tools.

Mitigation: Inspect or sanitize untrusted CSV files before conversion, and review generated Markdown, HTML, JSON, or spreadsheet-bound outputs before opening or sharing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples and generated local files such as CSV, JSON, YAML, TSV, Markdown, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may read and write local files; generated file paths depend on the selected operation and output arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
