## Description: <br>
Public OpenClaw skill for redacting private paths, secret-like strings, private URLs, and common PII from Markdown, JSON, logs, and other text artifacts before sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and release maintainers use this skill to scan local text artifacts, produce redacted copies, check the redacted output, and generate a concise report before sharing bug bundles, logs, manifests, traces, reports, or release notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex-based redaction can miss sensitive content or leave context that still identifies a person, system, or secret. <br>
Mitigation: Re-scan the redacted output, inspect the generated report, and manually review any files or findings before sharing. <br>
Risk: Unsupported or binary files such as screenshots, PDFs, videos, or non-text artifacts are not sanitized by the automatic pass. <br>
Mitigation: Treat skipped files as manual-review items and do not present a bundle as cleared while skipped files remain unresolved. <br>
Risk: Intermediate scan and redaction JSON reports can contain local absolute paths or other sensitive operational context. <br>
Mitigation: Keep intermediate reports local unless reviewed, and share the redacted output directory plus final Markdown report instead of raw artifacts. <br>
Risk: Running the tool over a broad directory can process more local material than intended. <br>
Mitigation: Use a narrow --root that points only to the files or directory intended for review. <br>


## Reference(s): <br>
- [Artifact Redactor homepage](https://github.com/zack-dev-cm/artifact-redactor) <br>
- [Artifact Redactor on ClawHub](https://clawhub.ai/zack-dev-cm/artifact-redactor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Files, Guidance] <br>
**Output Format:** [Shell commands that produce JSON scan, redaction, and check reports, a redacted output directory, and a Markdown redaction report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-selected local files or directories; supported text files are copied with redactions, while unsupported or binary files are reported for manual review.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
