## Description: <br>
Imports OpenAI ChatGPT and Anthropic Claude conversation exports into agent episodic memory, writing dated summaries and deduplicating repeat imports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to import ChatGPT or Claude export files into searchable daily episodic memory for onboarding, recall, and preserving important conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation exports may contain private conversations, secrets, client data, or regulated information. <br>
Mitigation: Run a dry run first, redact sensitive chats, and import only the files and dates that should be written into persistent memory. <br>
Risk: Imports can be written into the wrong agent workspace if the workspace target is misconfigured. <br>
Mitigation: Confirm OPENCLAW_WORKSPACE points to the intended workspace before running a write import. <br>
Risk: Historical conversations may create more persistent memory than intended. <br>
Mitigation: Use date filtering such as --since and review dry-run output before committing imported summaries. <br>


## Reference(s): <br>
- [Supported Export Formats](references/export-formats.md) <br>
- [ClawHub listing](https://clawhub.com/djc00p/chat-history-importer) <br>
- [Related chat-learnings-extractor skill](https://clawhub.ai/djc00p/chat-learnings-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory summaries to memory/episodic/YYYY-MM-DD.md and tracks imported chat IDs for deduplication.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata, released 2026-05-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
