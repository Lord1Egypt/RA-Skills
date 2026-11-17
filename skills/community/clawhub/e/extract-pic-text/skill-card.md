## Description:

Extracts specified-position text from image filenames using custom delimiters, with support for batch processing, sorting, deduplication, and multiple image formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llyouc](https://clawhub.ai/user/llyouc)

### License/Terms of Use:


## Use Case:

Developers, operations staff, and data workers use this skill to extract IDs, dates, SKU values, or other structured tokens from consistently named image files during batch organization or data preparation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional output path writes a result file and can overwrite an existing file at that path.

Mitigation: Review the output path before running the script and write to a temporary or dedicated results file when possible.

Risk: The helper script reads filenames from directories supplied by the user and reports extracted filename tokens.

Mitigation: Run it only on directories whose filenames are appropriate to disclose in command output or result files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted values to a user-specified output file or print comma-separated values to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
