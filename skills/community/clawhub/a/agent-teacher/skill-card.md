## Description:

Agent Teacher trains new or existing agents on studio conduct, identity setup, foundational tools, and optional advanced skills in a required conduct-first sequence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and workspace maintainers use this skill to onboard new agents or refresh existing agents on required conduct, identity files, persistent memory practices, collaboration tools, and optional role-specific training.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent core-instruction and memory-policy changes can alter an agent's long-term behavior.

Mitigation: Require explicit approval before editing SOUL.md, IDENTITY.md, AGENTS.md, or memory policy.

Risk: Unpinned skill and MCP package installation can introduce unreviewed behavior.

Mitigation: Pin and audit installed skills and MCP packages before deployment.

Risk: Broad backups, Feishu recipients, Chrome profiles, and API-key-backed tools can expose sensitive data.

Mitigation: Restrict backup paths and message recipients, and avoid sensitive data use without clear consent.

## Reference(s):

- [Studio Rules of Conduct](references/rules-of-conduct.md)
- [Identity Setup](references/phase-0-identity.md)
- [Foundation Course Details](references/phase-1-foundation.md)
- [Advanced Course Details](references/phase-2-advanced.md)
- [Programmer Learning Guide from Gstack](references/learning-from-gstack-programmer.md)
- [Producer Learning Guide from Gstack](references/learning-from-gstack-producer.md)
- [Designer Learning Guide from Gstack](references/learning-from-gstack-designer.md)
- [Artist Learning Guide from Gstack](references/learning-from-gstack-artist.md)
- [Gstack Project](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces onboarding curricula and setup instructions; installation and configuration steps require an agent or user to execute proposed commands.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
