## Description: <br>
Chronicle lets an agent inspect the user's current screen and several hours of recent screen history to resolve ambiguous requests about visible or recent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use Chronicle when they need an agent to inspect current or recent screen context to disambiguate references to visible work, recent app state, documents, or errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using Chronicle can inspect current and recent screen history when an ordinary request is ambiguous. <br>
Mitigation: Install only if this access is acceptable; restrict use to explicit screen-context requests or visible or recent work, and require confirmation before reviewing historical recordings or memories. <br>
Risk: Screen recordings may be stale or from a previous recording session if Chronicle is not running. <br>
Mitigation: Verify Chronicle is running and compare the current UTC time with recording timestamps before relying on screen data. <br>


## Reference(s): <br>
- [Chronicle on ClawHub](https://clawhub.ai/patrick-erichsen-2/chronicle) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Analysis] <br>
**Output Format:** [Markdown instructions with filesystem paths and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to inspect screen recordings, OCR sidecars, and Chronicle memories only when preconditions are met.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
