## Description:

Audit .env alias groups for missing required config, conflicting values, and canonical-key drift before deploy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to check .env-style configuration before deployment, especially for missing required values, conflicting aliases, and canonical-key drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print full or partial environment secret values to terminal or CI logs.

Mitigation: Run it only on local files you are comfortable exposing in terminal output, avoid production secrets unless output is changed to show only variable names and set or unset status, and rotate any credentials that may already have appeared in retained logs.

Risk: The release was flagged as suspicious by the authoritative security evidence because of possible secret exposure.

Mitigation: Review before installing or running in CI, and keep audit output out of retained logs when sensitive environment files are used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/env-alias-audit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output with OK, WARN, FAIL, summary, warnings, and failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 indicates no strict failures; exit code 1 indicates invalid input, missing required groups in strict mode, or conflicting alias values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
