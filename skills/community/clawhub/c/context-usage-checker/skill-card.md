## Description: <br>
Checks the current conversation's estimated token usage, remaining context, usage percentage, progress bar, and threshold-based guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect current conversation context usage and decide when to continue, compact, or start a new session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token counts are estimates and may differ from platform-reported usage. <br>
Mitigation: Treat the output as planning guidance and rely on platform usage reporting for exact limits. <br>
Risk: The skill reads current session history to estimate context usage. <br>
Mitigation: Install and run it only in workspaces where inspecting session context is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/context-usage-checker) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status message with token counts, percentage, progress bar, and usage advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token counts are estimated from current session history and model-specific context limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json, source header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
