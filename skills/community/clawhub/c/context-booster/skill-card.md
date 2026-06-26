## Description: <br>
Context Booster helps agents compress, summarize, retrieve, and inject conversation context for long-running or cross-session tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve continuity in long conversations, recover prior context across sessions, and compress or retrieve relevant memory before continuing complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored context may include sensitive conversation or environment details. <br>
Mitigation: Avoid storing secrets or sensitive data, verify the storage location before use, and clear local memory when it is no longer needed. <br>
Risk: Broad cross-session retrieval can reintroduce stale, irrelevant, or misleading context. <br>
Mitigation: Review retrieved summaries before relying on them, scope use to the relevant workspace, and remove outdated memory. <br>
Risk: The security evidence flags durable context storage and reuse without clear consent, limits, or deletion controls. <br>
Mitigation: Install only when durable memory is desired, confirm available inspection and deletion commands, and prefer scoped workspace use over broad personal or project data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/context-booster) <br>
- [Publisher Profile](https://clawhub.ai/user/pagoda111king) <br>
- [README](README.md) <br>
- [FAQ](FAQ.md) <br>
- [Version History](VERSION_HISTORY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime outputs may include text, JSON, or Markdown context summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses durable local context memory according to artifact documentation; review stored content before reuse.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence and package.json; artifact documentation also mentions v0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
