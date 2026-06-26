## Description: <br>
Factory Floor is a startup coaching skill that helps founders and early-stage teams diagnose constraints, route to stage-specific guidance, and choose focused weekly experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmichelli](https://clawhub.ai/user/mmichelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders and early-stage teams use this skill with agent platforms to diagnose the current business bottleneck, avoid premature prescriptions, and select one concrete experiment for the week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer writes files into an agent skills directory and runs npm to fetch renderer dependencies. <br>
Mitigation: Review the installer before running it, install in an isolated environment when possible, and proceed only if those filesystem and network actions are acceptable. <br>
Risk: The diagram renderer dependency installation is not backed by a lockfile or exact dependency pinning in the evidence. <br>
Mitigation: Pin and review dependency versions, or make the diagram renderer dependency explicit and optional before broad deployment. <br>


## Reference(s): <br>
- [Factory Floor README](README.md) <br>
- [ClawHub listing](https://clawhub.ai/mmichelli/factory-floor) <br>
- [Publisher profile](https://clawhub.ai/user/mmichelli) <br>
- [npm package](https://www.npmjs.com/package/@swiftner/factory-floor) <br>
- [Open agent skills standard](https://agentskills.io) <br>
- [Jobs To Be Done](references/jtbd.md) <br>
- [Theory of Constraints](references/pillar-goldratt.md) <br>
- [Customer Factory](references/pillar-maurya.md) <br>
- [How Brands Grow](references/pillar-sharp.md) <br>
- [Marketing Strategy Discipline](references/pillar-ritson.md) <br>
- [Strategic Thinking](references/pillar-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown conversational coaching with focused questions, constraint statements, and experiment assignments; installation guidance may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes to stage and reference files based on startup context; no API keys or MCP tools were detected in the release evidence.] <br>

## Skill Version(s): <br>
3.5.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
