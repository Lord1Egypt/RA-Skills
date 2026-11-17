## Description:

Generate and deliver a daily Agentic Payment news briefing covering Visa dynamics, China/APAC market activity, competitor protocols, and regulatory signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juncaijames](https://clawhub.ai/user/juncaijames)

### License/Terms of Use:

MIT-0

## Use Case:

Visa Greater China Agentic Payment stakeholders use this skill to curate up to 10 daily news items, deduplicate recent coverage, save an Obsidian report, generate a PDF, and prepare WeChat delivery. It is also used to set up or maintain the scheduled daily report workflow.

### Deployment Geography for Use:

Greater China and Asia-Pacific (APAC)

## Known Risks and Mitigations:

Risk: The workflow can read and write a local Obsidian vault path and create PDF files.

Mitigation: Confirm the intended vault location before use and restrict approved input and output paths.

Risk: The workflow can send generated reports to a hard-coded WeChat recipient and account.

Mitigation: Add an explicit approval step and verify the recipient and account before sending.

Risk: The PDF converter uses shell string execution and interpolates report content into HTML.

Mitigation: Replace shell string execution with safe argument passing and escape or sanitize report content before conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juncaijames/skills/ap-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown report with YAML frontmatter, PDF output path, shell command snippets, and final text reply]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to a configured Obsidian vault path, generates a PDF under /tmp, and can send the PDF to a configured WeChat recipient.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
