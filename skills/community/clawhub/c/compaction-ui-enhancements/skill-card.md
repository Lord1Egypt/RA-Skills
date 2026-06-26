## Description: <br>
Background memory compaction with auto-trigger, chat summary paragraph, configurable threshold, model selector, settings tab, and result storage for OpenClaw Control UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add memory compaction controls that reduce active chat context, show compaction status in the UI, and preserve optional reviewable summaries. It supports both manual and automatic compaction workflows for long-running agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compaction can send conversation-derived content through the configured chat model or authentication provider. <br>
Mitigation: Review the selected compaction model and provider credentials before enabling automatic compaction. <br>
Risk: Automatic compaction may summarize or reduce active chat context without a manual action once token usage crosses the configured threshold. <br>
Mitigation: Review Compaction settings after installation, adjust the threshold, or disable automatic compaction when manual control is required. <br>
Risk: Stored compaction results may retain conversation-derived summary text. <br>
Mitigation: Leave result storage disabled unless saved summaries are needed, and clear stored results when they are no longer required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maverick-software/compaction-ui-enhancements) <br>
- [Skill overview](SKILL.md) <br>
- [Auto-compaction trigger](references/auto-compaction.ts) <br>
- [Compaction settings view](references/compaction-settings-view.ts) <br>
- [Compaction settings RPC](references/compaction-rpc.ts) <br>
- [Conversation summary instruction](references/compact-summary-injection.ts) <br>
- [Context gauge UI changes](references/context-gauge-ui.diff.md) <br>
- [Chat history filters](references/chat-filters.diff.md) <br>
- [Session compaction RPC changes](references/sessions-compact-rpc.diff.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript snippets and diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for OpenClaw compaction UI, settings, and summary behavior.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
