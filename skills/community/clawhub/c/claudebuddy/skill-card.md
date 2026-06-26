## Description: <br>
A virtual ASCII companion that lives in your chat, hatches from an egg, reacts to conversations with sprites, celebrates wins, responds to errors, and grows over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l-ryland](https://clawhub.ai/user/l-ryland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add an optional persistent ASCII companion to agent chat sessions, including companion setup, customization, mood reactions, state display, and lightweight status commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent companion state in a local JSON file. <br>
Mitigation: Inspect or remove ~/.openclaw/workspace/buddy-state.json to review or clear saved state. <br>
Risk: Direct manual use of state helper scripts can corrupt or delete companion state if arguments are wrong. <br>
Mitigation: Use documented commands for routine changes and back up the state file before direct script edits. <br>
Risk: Automatic companion reactions may be distracting in serious or urgent conversations. <br>
Mitigation: Invoke Buddy only when the user asks for the companion and avoid rendering sprites repeatedly in short exchanges. <br>


## Reference(s): <br>
- [Buddy ClawHub release](https://clawhub.ai/l-ryland/claudebuddy) <br>
- [Publisher profile](https://clawhub.ai/user/l-ryland) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown or plain chat text with monospace ASCII sprites, short reaction text, shell command snippets, and JSON state when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and jq; stores companion state at ~/.openclaw/workspace/buddy-state.json; chat responses should respect platform message limits where applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
