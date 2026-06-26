## Description: <br>
Dynamic context preprocessor for OpenClaw agents that selects relevant memory, collapses timelines, detects forbidden patterns, and injects task-specific context before agent reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to generate compact task-specific context blocks from local memory, timelines, and configured task profiles before an agent starts reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw memory files that may contain private notes or sensitive operational context. <br>
Mitigation: Use it only in workspaces where those files are intended for agent context, and keep secrets, credentials, personal data, and proprietary content out of memory notes. <br>
Risk: The bundled script appends raw task descriptions and run metadata to a persistent local JSONL feedback log. <br>
Mitigation: Disable or modify feedback logging before routine use, or periodically review and purge the log according to local retention needs. <br>


## Reference(s): <br>
- [Context Assembler ClawHub page](https://clawhub.ai/wudi488/context-assembler) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text context block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a token budget from command-line input or genome task profiles; debug mode can emit diagnostics separately.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
