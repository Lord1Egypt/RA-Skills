## Description: <br>
Conversation Distill prompts at the end of substantive conversations, classifies useful takeaways, asks for confirmation, and writes only approved notes or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiing99](https://clawhub.ai/user/yiing99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Knowledge workers, developers, and teams use this skill to capture reusable decisions, judgments, insights, facts, self-observations, action items, and open questions after meaningful agent conversations. It is useful when a session produced durable knowledge and the user wants to review it before anything is saved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect the current conversation to identify takeaways, which can include sensitive or personal content. <br>
Mitigation: Use "skip" or "don't save" when a conversation should not be distilled, and review the proposed items before approving any write. <br>
Risk: Incorrect or unwanted summaries could be persisted to a notes tool if approved without review. <br>
Mitigation: The skill requires an explicit "write" or "save" confirmation after the user edits, removes, or approves the proposed list. <br>
Risk: Notes-tool integrations can store conversation-derived content outside the chat environment. <br>
Mitigation: Use only trusted notes MCP integrations, and rely on the Markdown fallback when manual handling is preferred. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yiing99/conversation-distill) <br>
- [KnowMine](https://knowmine.ai) <br>
- [KnowMine Claude plugin](https://github.com/YIING99/knowmine-claude-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API calls] <br>
**Output Format:** [Markdown confirmation lists, structured note entries, and optional MCP notes-tool writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before writing approved notes; otherwise it can output Markdown for manual use.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
