## Description: <br>
Spawn and relay Cursor Agent's CLI (`agent` binary) as an interactive passthrough for running Cursor Agent in a project directory, asking questions, and sending follow-up prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waldyrious](https://clawhub.ai/user/waldyrious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run Cursor Agent from an agent session and relay its interactive output and prompts while preserving user control over trust and command-approval decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor Agent runs in the selected project directory and may request workspace trust or command approval. <br>
Mitigation: Relay Cursor trust and approval prompts exactly as shown and wait for explicit user approval before sending a choice. <br>
Risk: Project files or referenced secrets may be exposed to Cursor Agent during the session. <br>
Mitigation: Use the skill only in intended project directories, avoid referencing secrets unless Cursor should process them, and end the background session when finished. <br>


## Reference(s): <br>
- [Cursor Tui on ClawHub](https://clawhub.ai/waldyrious/cursor-tui) <br>
- [Publisher profile: waldyrious](https://clawhub.ai/user/waldyrious) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Interactive terminal text relayed from Cursor Agent with concise prompt-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cursor or cursor-agent binary on PATH and an explicit user response to Cursor trust or command-approval prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
