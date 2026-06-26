## Description: <br>
Query, insert, edit, and delete flomo memos through the flomo Web UI using Chrome MCP tools in an already logged-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Undertone0809](https://clawhub.ai/user/Undertone0809) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to search, create, replace, and delete live flomo memos through Chrome MCP Web UI automation. It is intended for already logged-in flomo Web sessions where the agent should operate memos without relying on an official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates in a logged-in browser session and can modify or delete live flomo memos. <br>
Mitigation: Use a dedicated browser profile when possible, keep edit and delete actions interactive, and prefer query-only use unless write access is needed. <br>
Risk: Fallback and delete paths may be under-scoped if the page state or target controls are ambiguous. <br>
Mitigation: Lock write targets by memo_id, stop when controls or dialogs cannot be located reliably, and require explicit second confirmation before deletion. <br>
Risk: Memo contents may appear in transient agent responses or screenshots during browser automation. <br>
Mitigation: Use truncated snippets for confirmation, avoid persistent logs containing memo bodies, and store screenshots only when needed for troubleshooting. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Undertone0809/flomo-crud-skill) <br>
- [Workflow Details](artifact/references/workflows.md) <br>
- [UI Locator Strategy and Fallback Policy](artifact/references/ui-locators.md) <br>
- [Safety and Logging Policy](artifact/references/safety.md) <br>
- [Manual Validation Checklist](artifact/references/test-checklist.md) <br>
- [mcp-chrome](https://github.com/hangwin/mcp-chrome) <br>
- [flomo Web](https://v.flomoapp.com/mine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with memo candidates, action confirmations, action results, and occasional inline TOML or shell configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include memo_id, timestamp text, truncated snippets, match reasons, candidate counts, warnings, and confirmation prompts; memo body text is not persisted by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
