## Description:

Clawler helps agents access current web information through the Clawler OpenClaw plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxpetretta](https://clawhub.ai/user/maxpetretta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Clawler to route agent web searches through a configured OpenClaw plugin provider and to manage provider-specific search settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider credentials can be misconfigured if API keys are added without a deliberate provider choice.

Mitigation: Choose one provider, configure only the credential needed for that provider, and verify availability with the Clawler status command before use.

Risk: Adding web_search to tools.deny changes installation-wide search behavior.

Mitigation: Only deny the built-in search tool when the operator intentionally wants Clawler to replace that search surface.

Risk: Search provider filters, including domain filters, may not behave identically across providers.

Mitigation: Use provider-neutral instructions where possible and verify source quality when official or high-confidence references are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maxpetretta/skills/clawler)
- [Clawler Homepage](https://github.com/maxpetretta/clawler)
- [Release Changelog](https://github.com/maxpetretta/clawler/compare/v2026.3.11-5...v2026.3.11-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider selection, freshness filters, domain filters, and credential setup guidance for the selected search provider.]

## Skill Version(s):

2026.3.11-6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
