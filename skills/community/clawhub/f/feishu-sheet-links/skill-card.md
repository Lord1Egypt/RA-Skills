## Description:

Extracts hyperlinks from all tabs in a public Feishu spreadsheet and can optionally download linked articles as Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyan9110](https://clawhub.ai/user/wangyan9110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when a public Feishu spreadsheet or wiki URL needs link extraction across all sheet tabs, with an optional follow-up to save linked article content as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls Chrome and visits links found in a public Feishu sheet.

Mitigation: Review extracted URLs before downloading content and avoid using an authenticated or personal debugging Chrome profile.

Risk: The optional downloader writes Markdown files and progress data to a local output directory.

Mitigation: Choose a low-risk output directory and review generated files before reusing or publishing them.

Risk: The documented npx command can invoke an unpinned Bun runtime path.

Mitigation: Prefer a locally installed trusted Bun runtime when running the extraction or download scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyan9110/skills/feishu-sheet-links)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, json, markdown]

**Output Format:** [Markdown guidance with bash commands; extraction produces JSON and optional Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public Feishu URL, Bun, and Chrome or Chromium; the optional downloader supports resume, timeout, output directory, and concurrency settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
