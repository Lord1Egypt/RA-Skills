## Description:

Install and configure the native Unlimited-OCR plugin for DeepSeek Harness (DSH) from its Settings GUI, using Baidu Cloud or a local SGLang/OpenAI-compatible service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenwu0209](https://clawhub.ai/user/aidenwu0209)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this setup skill to install, configure, verify, and troubleshoot the DSH Unlimited-OCR plugin for long-document OCR and conversion of PDF, OFD, Office, text, and scanned-image inputs to Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands fetch mutable remote code, which can change between review and execution.

Mitigation: Pin the GitHub plugin reference to a reviewed commit and pin @deepseek-ai/dsh to an exact version before installation.

Risk: The setup flow may involve OCR providers and API credentials.

Mitigation: Verify the installed plugin source and permissions before entering production or high-value credentials, and store secrets only through DSH Credentials.

## Reference(s):

- [Skill page](https://clawhub.ai/aidenwu0209/skills/dsh-unlimited-ocr-skill-setup)
- [Project homepage](https://github.com/Aidenwu0209/dsh-Unlimited-OCR-Skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prerequisite checks, install commands, GUI verification steps, provider configuration guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
