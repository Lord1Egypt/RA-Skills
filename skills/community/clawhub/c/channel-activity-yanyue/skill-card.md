## Description: <br>
Multi-channel short-term memory for AI assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eightroad](https://clawhub.ai/user/eightroad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to record short-lived activity summaries across channels and retrieve recent context from other channels during an assistant session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent messages and identifiers can be stored locally and reused across channels. <br>
Mitigation: Require explicit user opt-in before enabling cross-channel memory and document what local data is retained. <br>
Risk: Cross-channel or family-group sharing can expose context to the wrong identity when consent and scoping controls are weak. <br>
Mitigation: Verify same-user identity across channels, disable family sharing by default, and require an explicit sharing policy for each group. <br>
Risk: Hardcoded local paths and MEMORY.md access can read or promote data outside the intended workspace. <br>
Mitigation: Replace hardcoded paths with reviewed configuration and decide whether long-term memory promotion is allowed before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eightroad/channel-activity-yanyue) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/eightroad) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub README](artifact/README_CLAWHUB.md) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Integration guide](artifact/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown guidance with Python code snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recent-channel summaries with configurable TTL, entry limits, and character limits.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
