## Description: <br>
Summarize articles or webpages into structured bundles exported as JSON, Markdown, HTML, and PNG with consistent layout and tagging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wiseqingyang](https://clawhub.ai/user/wiseqingyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and content teams use this skill to extract article text, create a structured in-session summary with tags, and export reusable Markdown, HTML, PNG, and JSON outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional OpenClaw install helper can delete an existing destination folder when a custom destination is supplied. <br>
Mitigation: Run the installer only after verifying the destination path, or install manually by copying the skill folder to the intended location. <br>
Risk: The skill can fetch article URLs or read local files provided by the user and save derived output files. <br>
Mitigation: Use trusted article sources and file paths, and review generated outputs before sharing or publishing them. <br>


## Reference(s): <br>
- [Output Schema](references/output-schema.md) <br>
- [Article Summary Card](https://clawhub.ai/wiseqingyang/article-summary-card) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON source data with rendered Markdown, HTML, and PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs use a structured summary schema with title, source, one-sentence summary, sections, closing takeaway, and tags.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
