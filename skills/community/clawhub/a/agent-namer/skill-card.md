## Description:

Agent Namer helps internal teams generate and manage concise "货xx"-style agent names, check availability, list active names, and record active or retired names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxlhyx](https://clawhub.ai/user/cxlhyx)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and internal agent builders use this skill to propose role-aligned Chinese-style agent names and keep a local registry from reusing active names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry updates can fail or behave inconsistently because the helper has reliability issues noted by the security evidence.

Mitigation: Test add, revive, and kill operations in a disposable copy and fix the helper before relying on it operationally.

Risk: The tool does not enforce the documented "货xx" naming format.

Mitigation: Manually review names against the documented format or add format validation before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxlhyx/skills/agent-namer)
- [Publisher profile](https://clawhub.ai/user/cxlhyx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and local JSON registry entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 3-5 candidate names with short rationale, availability checks, and registry-management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
