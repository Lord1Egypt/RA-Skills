## Description:

Local text cleanup and inspection toolkit that helps agents extract structured items, redact PII-like patterns, normalize text, inspect lines and word counts, compare text, render simple templates, generate slugs, and process Markdown or HTML using Python 3 standard library scripts with no remote calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to clean, inspect, transform, redact, and compare local text files before passing the results into downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML sanitization and Markdown-to-HTML output may not make untrusted content safe for browser or web application use.

Mitigation: Use the toolkit for local text processing, and pass untrusted HTML through a maintained allowlist sanitizer before rendering it in a browser or web app.

Risk: The scripts can write or overwrite caller-specified output paths.

Mitigation: Review output paths before execution and run commands in a working directory where overwrites are acceptable.

## Reference(s):

- [Clean Text Toolkit ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/skills/clean-text-toolkit)
- [Clean Text Toolkit OpenClaw homepage](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit)
- [Clean CSV Toolkit companion skill](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)
- [OpenClaw Prompt Shield companion skill](https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and local script guidance; scripts can produce plain text, JSON, JSONL, TSV, HTML, and diff output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local file or stdout results from Python 3 standard library utilities; some operations write or overwrite caller-specified paths.]

## Skill Version(s):

0.4.0 (source: server release metadata and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
