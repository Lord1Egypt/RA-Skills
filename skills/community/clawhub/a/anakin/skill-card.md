## Description:

Convert websites into clean data at scale - scrape URLs, batch scrape, AI search, and autonomous research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viraal-bambori](https://clawhub.ai/user/viraal-bambori)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to have an OpenClaw agent scrape web pages, batch process URLs, run Anakin web search, and produce autonomous research reports through an authenticated Anakin CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs and research queries submitted through the skill are sent to Anakin.

Mitigation: Use the skill only for URLs and research topics that are acceptable to share with Anakin.

Risk: Long-lived Anakin API keys can be exposed if pasted into agent chat or stored in plaintext shell startup files.

Mitigation: Use a secure secret store or supported interactive login flow, and avoid pasting API keys into chat.

Risk: The skill installs and runs the external anakin-cli package.

Mitigation: Review and pin the anakin-cli version before installation when the deployment requires stronger supply-chain control.

## Reference(s):

- [Anakin Website](https://anakin.io)
- [Anakin Dashboard](https://anakin.io/dashboard)
- [anakin-cli on PyPI](https://pypi.org/project/anakin-cli/)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; Anakin CLI commands produce Markdown, JSON, or raw JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the anakin CLI and ANAKIN_API_KEY; batch scraping is documented for up to 10 URLs per command.]

## Skill Version(s):

1.0.0 (source: skill.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
