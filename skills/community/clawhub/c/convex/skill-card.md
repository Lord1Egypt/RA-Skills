## Description:

Build and maintain Convex backends with schema-safe modeling, query and mutation patterns, auth guards, and production rollout checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when building, debugging, or scaling Convex backends. It supports schema-safe modeling, query and mutation design, authorization checks, index planning, deployment readiness, and incident learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist Convex project context under ~/convex/, which may accidentally include secrets, personal data, or sensitive tenant details if users save them.

Mitigation: Keep memory concise, redact sensitive identifiers, and do not store secrets, tokens, personal data, or sensitive tenant details in Convex memory files.

Risk: The skill may engage on incidental Convex mentions if configured broadly.

Mitigation: Choose a narrow activation preference during setup when automatic engagement on incidental mentions is not desired.

Risk: Incorrect schema, authorization, index, or rollout guidance could affect production data integrity, tenant boundaries, or availability.

Mitigation: Review proposed schema and permission changes, verify authorization at every entry point, and rehearse rollback before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/convex)
- [Skill Homepage](https://clawic.com/skills/convex)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local project memory under ~/convex/ when the user confirms activation and storage preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
