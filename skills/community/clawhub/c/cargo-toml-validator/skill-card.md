## Description:

Validate Rust Cargo.toml manifests for dependency issues, missing metadata, feature conflicts, workspace config, and crates.io publishing readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate Rust Cargo.toml manifests, audit dependency and feature configuration, and prepare crates for publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted Cargo.toml values could affect terminal display in default text or summary output.

Mitigation: Prefer JSON output for untrusted manifests or automated processing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional text, summary, or JSON validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit CI-friendly exit codes and strict-mode validation results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
