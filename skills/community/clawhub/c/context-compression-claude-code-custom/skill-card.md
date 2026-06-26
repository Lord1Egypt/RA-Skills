## Description: <br>
Helps an agent compress long conversations by preserving important goals, decisions, preferences, and active tasks while summarizing useful context and discarding low-value exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep long-running conversations usable by compacting history into a short summary and maintaining structured memory for preferences, active tasks, decisions, and key context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation compression can persist user details, account or configuration information, and other sensitive personal context. <br>
Mitigation: Review generated memory after compression and avoid storing passwords, API keys, session tokens, private account details, or sensitive personal data. <br>
Risk: Optional automatic hook configuration can prompt memory updates during future compaction events without a separate manual request. <br>
Mitigation: Enable the automatic hook only when the user accepts future memory-update prompts, and keep manual review in the compression workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/c595390153-a11y/context-compression-claude-code-custom) <br>
- [Memory Template](artifact/memory-template.md) <br>
- [PreCompact Hook Setup](artifact/setup-hook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured memory entries and optional hook configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update a persistent memory file when compression is performed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
