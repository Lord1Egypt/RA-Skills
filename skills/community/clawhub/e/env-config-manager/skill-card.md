## Description:

Manage environment configuration files with loading, switching, validation, diffing, and documented secret-handling workflows for .env, YAML, and JSON formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage local and multi-environment configuration files, validate required variables, compare environments, and work with secret-bearing settings during application development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles secret-bearing environment data and may print raw values to logs or transcripts.

Mitigation: Review commands before execution, avoid running against production .env files by default, and redact or suppress secret values in shared transcripts.

Risk: The release evidence says advertised encryption and export features are overstated or not fully implemented.

Mitigation: Do not rely on the documented encryption, key rotation, or team-sharing workflows until the implementation is independently reviewed and tested.

Risk: Environment files may be written with inappropriate local permissions.

Mitigation: Use restrictive file permissions and store generated configuration files only in approved, access-controlled locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/env-config-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or print environment variable values; review outputs before using with real secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
