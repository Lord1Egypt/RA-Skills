## Description:

Extracts the main content from webpages with Defuddle and converts it to Markdown for scraping, text processing, and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeholdon](https://clawhub.ai/user/yeholdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to extract readable article content from URLs or local HTML files and produce Markdown or JSON for downstream processing. It can also send extracted Markdown to WeChat or Telegram when those delivery scripts are intentionally used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted webpage content can be sent to WeChat or Telegram by optional scripts.

Mitigation: Review destination settings before use and confirm the extracted page content contains no sensitive, private, or regulated information before sending.

Risk: The scripts run Defuddle through an unpinned npm invocation at runtime.

Mitigation: Pin or locally lock the Defuddle dependency before using the skill in controlled or repeatable environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeholdon/skills/defuddle-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, JSON, shell commands, and Node.js code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send extracted webpage content to configured WeChat or Telegram targets when the corresponding scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
