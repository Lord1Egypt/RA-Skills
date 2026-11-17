## Description:

Cursor Tui lets an agent spawn Cursor Agent's CLI in a selected project directory and relay interactive output and follow-up prompts as a transparent terminal passthrough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldyrious](https://clawhub.ai/user/waldyrious)

### License/Terms of Use:


## Use Case:

Developers and engineers use Cursor Tui to run Cursor Agent from an agent workflow in a specific project directory, relay Cursor's terminal output, and send follow-up prompts while preserving user control over trust and command approval prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running Cursor Agent in an unintended project directory could expose or modify the wrong workspace.

Mitigation: Choose the workspace deliberately before spawning the session and confirm workspace trust prompts with the user.

Risk: Cursor Agent may request approval for commands or trust decisions during the interactive session.

Mitigation: Relay permission prompts exactly as shown and continue only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waldyrious/skills/cursor-tui)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal relay with prompt lines and user-approved interactive input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Cursor Agent CLI through the cursor or cursor-agent binary on PATH.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
