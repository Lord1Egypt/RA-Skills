## Description: <br>
ARTA is an in-memory awareness layer that helps agents track and query their own activity across sessions within a single process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palxislabs](https://clawhub.ai/user/palxislabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ARTA to add local cross-session awareness so an agent can answer questions about its own active sessions, channels, humans, tasks, and status. It is best suited for agents where sharing session metadata across contexts is intended and governed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In shared or multi-user deployments, ARTA can reveal active session metadata such as channel, identity, or task details. <br>
Mitigation: Install only where cross-session awareness is intended; add authorization and redaction so one user cannot learn another user's metadata unless explicitly allowed. <br>
Risk: ARTA stores awareness in memory within a single process and does not provide cross-process or cross-instance sharing. <br>
Mitigation: Use it for same-process awareness only, or add a shared backend before relying on cross-instance behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/palxislabs/arta) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable guidance and a drop-in JavaScript in-memory awareness class.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
