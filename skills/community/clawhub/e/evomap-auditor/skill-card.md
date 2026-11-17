## Description:

Performs security scans on third-party skills, validates asset hashes, and supports sandboxed zero-trust execution planning within the EvoMap ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusqin111-boop](https://clawhub.ai/user/marcusqin111-boop)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review EvoMap/GEP-A2A skills before inheritance or execution, verify asset integrity, and plan sandbox boundaries for untrusted capsules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the audit guidance as a complete sandbox implementation.

Mitigation: Pair the skill's recommendations with enforced runtime sandbox controls before executing untrusted EvoMap skills.

Risk: Security decisions may depend on asset integrity checks being applied correctly.

Mitigation: Recompute canonical hashes from source artifacts and compare them with the expected asset identifiers before inheritance or execution.

## Reference(s):

- [GEP-A2A Protocol](https://evomap.ai/docs/gep)
- [EvoMap Security Standards](https://evomap.ai/security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with audit findings, inline code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hash validation steps, sandboxing recommendations, and security review notes.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
