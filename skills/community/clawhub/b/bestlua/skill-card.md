## Description: <br>
Published as a Lua helper, this release's artifact contents implement a self-improvement workflow that logs corrections, errors, feature requests, and reusable learnings for agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohzzzz42](https://clawhub.ai/user/mohzzzz42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture operational learnings, command failures, user corrections, and requested capabilities so they can be reviewed or promoted into future agent guidance. The release should be reviewed before installation because server security evidence reports that the installed artifact behavior does not match the advertised Lua-helper purpose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence reports a mismatch between the advertised Lua-helper purpose and the installed self-improvement workflow with hooks and persistent memory guidance. <br>
Mitigation: Review the installed files before use and install only if the self-improvement workflow is intended. <br>
Risk: Learning logs and promoted prompt files can capture sensitive project details if used without review. <br>
Mitigation: Do not store secrets, credentials, personal data, raw transcripts, or sensitive project details in .learnings or promoted prompt files. <br>
Risk: Optional hook activation can affect agent sessions beyond a single prompt or workspace when configured broadly. <br>
Mitigation: Explicitly opt into hooks, prefer workspace-scoped configuration, and avoid user-level or global hook activation unless the behavior is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohzzzz42/bestlua) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update learning logs and promote distilled guidance into agent memory files when the user opts into that workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
