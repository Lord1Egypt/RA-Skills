## Description:

Convert Word documents (.doc and .docx) to HTML with MinerU while preserving document structure and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content managers, and publishing teams use this skill to convert Word documents into HTML for web publishing, CMS integration, and email templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and authenticating a third-party MinerU CLI.

Mitigation: Prefer a pinned or locally scoped mineru-open-api version when possible, avoid administrator/root installation, and review the CLI before use.

Risk: Documents processed with MINERU_TOKEN configured may be handled through the MinerU CLI/API.

Mitigation: Only process documents you are comfortable sending through that third-party service and confirm token handling policies before use.

## Reference(s):

- [Doc To HTML on ClawHub](https://clawhub.ai/mzlzyca/skills/doc-to-html)
- [MinerU](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU Open API CLI package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct HTML output to stdout or saved files through the MinerU CLI; requires MINERU_TOKEN for extract-based HTML output.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
