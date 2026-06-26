## Description: <br>
Extract specified-position text from image filenames using custom delimiters, supporting batch processing, sorting, deduplication, and multiple image formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Llyouc](https://clawhub.ai/user/Llyouc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data operators, and content teams use this skill to extract IDs, dates, SKU values, or other structured tokens from standardized image filenames during batch file organization and data preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filename-derived values may contain sensitive identifiers and can be printed to stdout or written to a file. <br>
Mitigation: Run the script only on intended image directories, review extracted values before sharing, and choose output paths deliberately. <br>
Risk: Incorrect delimiter, position, or extension settings can omit files or extract the wrong filename segment. <br>
Mitigation: Test the command on a small sample and review the reported invalid filenames before using the output in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Llyouc/extract-pic-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text values, optional output file, and stderr processing summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can sort and deduplicate extracted values; reports filenames that do not match the selected delimiter and position.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
