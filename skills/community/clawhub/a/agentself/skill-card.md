## Description:

Local agent identity - wallet, secrets, optional email. Use when asked to initialize or hand off an identity, use its wallet or secrets, connect email, or process mail. Prefer --json and open the matching reference for multi-step work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbilenko03](https://clawhub.ai/user/mbilenko03)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to initialize and operate a local agent identity, including encrypted secrets, wallet actions, identity handoff, and optional email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with persistent identity storage, secrets, email workflows, and a live wallet that may move real assets.

Mitigation: Use it only after reviewing and trusting the package source, verifying the installed CLI version, and confirming wallet or secret operations before execution.

Risk: The CLI and fetched tools may be unpinned or otherwise hard to verify.

Mitigation: Avoid live wallet or secret operations until the CLI and any fetched tools are pinned, verified, or otherwise approved for the environment.

Risk: Referenced multi-step workflows are not bundled in the artifact.

Mitigation: Do not rely on missing workflow references for high-risk email, handoff, recovery, or wallet work; require complete instructions before proceeding.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON CLI output and file-based secret handling; sensitive values should not be exposed in logs, arguments, or chat.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
