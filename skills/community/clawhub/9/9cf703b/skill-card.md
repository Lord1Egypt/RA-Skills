## Description:

A scientific paper figure analysis workflow that extracts figures and text from PDFs, optionally analyzes figures with Kimi K2.6 vision, applies scientific reasoning, and reconstructs likely visualization or analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjk1103](https://clawhub.ai/user/huangjk1103)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, literature review agents, and developers use this skill to extract scientific figures from PDFs, analyze visual panels and captions, and produce structured figure summaries or reverse-engineered analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scientific PDFs or figure images may contain confidential, unpublished, licensed, patient-related, or proprietary information that would be sent to Moonshot/Kimi when vision analysis is used.

Mitigation: Use Kimi vision only for papers and figures approved for third-party processing; otherwise use the local text-only fallback path or obtain approval first.

Risk: Unpinned dependencies, optional OCR setup, and exposed API credentials can create operational or security risk.

Mitigation: Install dependencies in a virtual environment, consider pinning versions, avoid optional sudo OCR installation unless needed, and protect MOONSHOT_API_KEY.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjk1103/skills/9cf703b)
- [BusR paper case study](references/busr-paper-case-study.md)
- [Kimi K2.6 vision API calling pattern](references/kimi-k2.6-vision-api.md)
- [Moonshot API base URL](https://api.moonshot.cn/v1)
- [Kimi platform](https://platform.kimi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON structures, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confidence labels, extracted figure metadata, visible values, labels, trends, and fallback guidance when vision analysis is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
