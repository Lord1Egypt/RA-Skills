## Description:

Batch-download formal A-share annual and semiannual report PDFs from CNInfo using a stock-code CSV, with dry-run preview, resume-on-failure, force-redownload, and configurable year, filter, and timeout options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gclyde768-arch](https://clawhub.ai/user/gclyde768-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to fetch or preview CNInfo annual and semiannual PDF reports for A-share listed companies from a stock-code CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File writes may be influenced by untrusted remote metadata during report download.

Mitigation: Run dry-run first, keep output and runtime directories in a disposable workspace, and review generated paths before using downloaded files.

Risk: Generated CSV manifests may contain remote metadata that is unsafe to open directly in spreadsheet software.

Mitigation: Inspect manifests as text or import them with spreadsheet formula execution disabled.

Risk: The default stock CSV fallback may select an unintended local file.

Mitigation: Pass a trusted stock CSV path explicitly with --stock-csv.

## Reference(s):

- [Filter Rules](references/filter_rules.md)
- [CNInfo Full-Text Search](https://www.cninfo.com.cn/new/fulltextSearch)
- [ClawHub Skill Page](https://clawhub.ai/gclyde768-arch/skills/cninfo-report-downloader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; runtime outputs include PDF files, CSV manifests, SQLite state, and logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can run in dry-run mode to preview matches before writing downloaded report files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
