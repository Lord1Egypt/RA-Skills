## Description:

Faktum Android helps agents build the Faktum News Android app with Android CLI, Kotlin, Jetpack Compose, Navigation 3, edge-to-edge UI, and the existing Faktum web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and validate a Kotlin and Jetpack Compose Android client for Faktum News. It guides project setup, Android CLI usage, official Android skill chaining, and reuse of the existing Faktum web API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad reads from private local project, vault, and memory paths.

Mitigation: Require the agent to list each external path before access, get explicit approval, and skip unrelated vault or memory content.

Risk: The skill can alter Android CLI skill or tooling state without clear version pinning.

Mitigation: Pin Android CLI skills and updates to reviewed versions before use.

Risk: The skill discusses distributing updated skills across multiple agent directories.

Mitigation: Avoid cross-agent skill distribution unless the operator explicitly intends it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Kotlin/Compose guidance, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing development guidance for Android project creation, SDK setup, emulator execution, API integration, and implementation workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
