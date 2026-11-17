## Description:

Initializes a DolphinDB Python environment by detecting an installed DolphinDB SDK across Conda, Anaconda, Miniconda, or system Python and installing it when none is found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before DolphinDB-related work to locate or prepare a Python environment with the DolphinDB SDK and expose consistent dolphin_python and dolphin_pip commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install an unpinned DolphinDB package into a local Python environment.

Mitigation: Review before installing, approve the target interpreter explicitly, and prefer a pinned DolphinDB SDK in a dedicated virtual environment.

Risk: The environment loader uses eval-based loading of shell output.

Mitigation: Review generated exports before loading and prefer a detection-only flow or a loader that avoids eval.

Risk: Example connection code includes hardcoded database credentials.

Mitigation: Replace example credentials with user-provided secrets from an approved secret-management path before connecting to DolphinDB.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/dolphindb-init)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit shell environment exports and helper command guidance for the selected Python environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
