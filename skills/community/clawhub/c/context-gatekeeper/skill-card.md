## Description: <br>
Keeps the conversation token-friendly by summarizing recent exchanges, surfacing pending actions, and delivering a compact briefing for each turn before calling the model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Davienzomq](https://clawhub.ai/user/Davienzomq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long OpenClaw conversations compact by generating a current Markdown briefing, recent-turn log, and pending-action list before the next model call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local chat history and generated summaries may contain secrets or regulated personal data if users log sensitive conversations. <br>
Mitigation: Keep the history short, remove sensitive data before logging, inspect current-summary.md before reuse, and clear the context files when finished. <br>
Risk: The background monitor can continuously refresh summaries from the local history file. <br>
Mitigation: Run the monitor only when continuous updates are needed and review the generated summary before using it as model context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Davienzomq/context-gatekeeper) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary files with concise text guidance and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a compact summary, pending-action list, and recent-turn excerpt from local chat history.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
