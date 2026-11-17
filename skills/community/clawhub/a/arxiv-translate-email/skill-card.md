## Description:

Downloads papers from arXiv, translates them into Chinese, and emails the resulting PDF, with synchronous and queued execution modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckqiao](https://clawhub.ai/user/ckqiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to fetch arXiv papers, translate PDFs into Chinese, and send translated PDFs by email through either a queue or a direct run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded API and SMTP credentials may expose accounts or be reused outside the intended environment.

Mitigation: Rotate or remove embedded credentials before installation and supply secrets through a managed secret store or environment variables.

Risk: The email helper can send existing local PDF attachments with weak user controls.

Mitigation: Constrain attachment paths to generated translation outputs and validate recipients before sending.

Risk: Detached cron or nohup operation can make job tracking and cancellation unclear.

Mitigation: Use tracked queue jobs with status checks and cancellation, and avoid detached runs unless operations are monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckqiao/skills/arxiv-translate-email)
- [arXiv API query example](https://export.arxiv.org/api/query?search_query=ti:SearchR1&max_results=3)
- [arXiv paper example](https://arxiv.org/abs/2503.09516)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and Python invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger PDF translation jobs and send translated PDF attachments by email when executed in a configured environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
