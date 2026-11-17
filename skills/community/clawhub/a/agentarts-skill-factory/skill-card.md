## Description:

AgentArts To OfficeAce generates standard skill directories that wrap Huawei Cloud AgentArts workflows for natural-language use in OfficeAce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plovjet](https://clawhub.ai/user/plovjet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect AgentArts workflow connection details and generate reusable OfficeAce skill scaffolding for deployed AgentArts runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills can store AgentArts API keys in plaintext.

Mitigation: Require AGENTARTS_API_KEY at runtime, remove default embedded keys before sharing, and avoid production credentials until the generator is changed to never write keys to disk.

Risk: Authenticated requests can use unsafe or overly flexible network paths, including an IP-direct fallback.

Mitigation: Remove the IP-direct TLS fallback and restrict base URLs to approved HTTPS AgentArts hosts.

Risk: Generated files may be written outside the intended location if output paths or names are not controlled.

Mitigation: Use a dedicated output directory and simple skill names when generating skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plovjet/skills/agentarts-skill-factory)
- [Project homepage](https://github.com/plovjet/agentArts-to-officeAce)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Generated skill directory containing Markdown and Python files, with optional shell commands for invocation and validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SKILL.md and scripts/invoke_agentarts.py from supplied AgentArts workflow settings.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
