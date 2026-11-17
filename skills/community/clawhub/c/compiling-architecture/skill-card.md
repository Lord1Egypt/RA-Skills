## Description:

Guides agents through deterministic architecture pattern selection, canonical spec compilation, constraint and NFR iteration, audit review, and final approval of architecture artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inetgas](https://clawhub.ai/user/inetgas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compile, audit, and approve architecture specifications with deterministic pattern selection before implementation or architecture drift remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External compiler checkout or dependencies may not match the reviewed release evidence.

Mitigation: Verify the arch-compiler repository source and commit, review its requirements file, install dependencies in a virtual environment or container, and avoid running pip with elevated privileges.

Risk: Compiler-maintenance changes, especially vocabulary changes and new patterns, can alter architecture selection.

Mitigation: Treat compiler-maintenance actions as review-required changes and require human review before promoting vocabulary or pattern updates.

Risk: Architecture artifacts can be treated as final before provider, runtime, data, or messaging decisions are resolved.

Mitigation: Follow the provider-binding and pre-approval validation gates, then recompile and obtain fresh approval whenever those decisions change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/inetgas/skills/compiling-architecture)
- [Project Homepage from ClawHub Metadata](https://github.com/inetgas/arch-compiler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML examples, shell commands, and generated architecture artifact files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compiled architecture specifications and pattern-selection artifacts for an application repository; final architecture approval requires human review.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
