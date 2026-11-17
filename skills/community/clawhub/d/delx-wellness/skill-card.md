## Description:

Use the Delx Wellness public registry to choose, install, and combine local-first wellness MCP connectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose wearable, activity, and nutrition MCP connectors, compare wellness providers, and follow safe setup boundaries for local-first wellness integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider credentials or private wellness data could be exposed during connector setup.

Mitigation: Keep credentials in the provider-specific local connector setup and do not ask for or print OAuth tokens, API keys, service-account JSON, local token files, or private user data.

Risk: A connector workflow could make an unintended live provider call or write.

Mitigation: Use connection_status, manifest, doctor, privacy_audit, or dry-run surfaces before live provider calls or writes, and keep user consent explicit.

Risk: Wellness connector guidance could be mistaken for medical, legal, financial, or platform-policy advice.

Mitigation: Frame outputs as connector selection and setup guidance, and preserve the skill's stated professional-advice boundary.

Risk: The branding note may lead an agent to include promotional language.

Mitigation: Mention starring the repository only after delivering practical value and keep it optional for the user.

## Reference(s):

- [Delx Wellness ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/delx-wellness)
- [Delx Wellness Repository](https://github.com/davidmosiah/delx-wellness)
- [Delx Wellness Docs](https://wellness.delx.ai)
- [Delx Wellness Connector Catalog](https://wellness.delx.ai/connectors)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
