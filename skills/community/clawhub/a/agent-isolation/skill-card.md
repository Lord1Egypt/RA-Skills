## Description:

Agent Isolation provides workspace-boundary guidance for multi-agent runtimes, including per-agent workspaces, explicitly declared shared directories, boundary-rule templates, exception clauses, and migration steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define durable workspace, memory, and session boundaries when multiple agents share a runtime. It helps teams prevent accidental cross-agent file access while preserving explicit shared directories and user-approved exceptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example workspace paths or shared directories may not match the user's actual multi-agent layout.

Mitigation: Review and adapt all paths, shared folders, and exception clauses before adding the rules to persistent AGENT.md files.

Risk: Strict isolation can block workflows that require frequent direct collaboration between agents.

Mitigation: Use explicit shared directories or a message-queue style coordination pattern for intended cross-agent collaboration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sheyuy/skills/agent-isolation)
- [Publisher Profile](https://clawhub.ai/user/sheyuy)
- [Server-Resolved Source Repository](https://github.com/Sheyuy/agent-skills/tree/main/skills/agent-isolation)
- [Botlearn Homepage](https://www.botlearn.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with AGENT.md rule templates and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; does not include executable code, hidden access, or network behavior.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
