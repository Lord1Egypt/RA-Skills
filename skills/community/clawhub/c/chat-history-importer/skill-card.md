## Description:

Import AI conversation exports (OpenAI ChatGPT and Anthropic Claude) into your agent's episodic memory. Parses export files, writes daily memory summaries, and deduplicates on re-runs. Trigger phrases: import chat history, ingest conversation export, import chatgpt export, import claude export, load AI conversation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to import selected ChatGPT and Claude conversation exports into dated episodic memory files that an agent can search later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat exports may contain credentials, client details, or other sensitive information.

Mitigation: Redact sensitive content first, restrict the import folder and date range, and set OPENCLAW_WORKSPACE explicitly.

Risk: Unreviewed imported text can affect what the agent recalls later.

Mitigation: Run a dry run first, then inspect the generated daily memory files before relying on them.

## Reference(s):

- [Export Formats](references/export-formats.md)
- [ClawHub Skill Page](https://clawhub.ai/djc00p/skills/chat-history-importer)
- [Chat Learnings Extractor](https://clawhub.ai/djc00p/chat-learnings-extractor)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Dated Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily files organized by date; repeated imports are deduplicated by chat ID.]

## Skill Version(s):

1.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
