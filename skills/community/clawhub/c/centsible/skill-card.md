## Description:

Manage repository-specific micro-facts, inspect token optimization status, and record reusable discoveries to minimize context bloat and token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntrieuvi97](https://clawhub.ai/user/ntrieuvi97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository users use the skill to check token optimization and manage reusable repository facts, including recording discoveries that help future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration commands can change persisted Centsible settings, reflection behavior, or session budgets.

Mitigation: Review the current configuration and intended setting before applying changes; unset settings you no longer want.

Risk: The update command updates every Centsible installation, which may affect multiple installed copies.

Mitigation: Run `centsible update --check` first and review the reported installations before updating.

## Reference(s):

- [Centsible on ClawHub](https://clawhub.ai/ntrieuvi97/skills/centsible)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.11.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
