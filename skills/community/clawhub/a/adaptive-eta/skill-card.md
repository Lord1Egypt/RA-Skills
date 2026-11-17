## Description:

Give the user an honest time estimate before long-running work, re-estimate when it runs over, and ask before blowing far past it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghe1941](https://clawhub.ai/user/yanghe1941)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long-running agent work time-boxed and communicative. It guides an agent to estimate multi-step work, run a local timer, revise ETAs at step boundaries, and ask before continuing after major overruns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timer labels and history are written locally and could expose sensitive task details if users put secrets or confidential context in labels.

Mitigation: Avoid secrets and sensitive details in timer labels; relocate or clear history with ADAPTIVE_ETA_HOME or by deleting ~/.adaptive-eta/.

Risk: The helper persists state and history on disk, which may be undesirable in ephemeral, shared, or tightly controlled environments.

Mitigation: Use ADAPTIVE_ETA_HOME to point state at an approved location, or remove the directory when timing history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanghe1941/skills/adaptive-eta)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text guidance with shell commands for the local timer helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timer state and history under ~/.adaptive-eta/ unless ADAPTIVE_ETA_HOME is set.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
