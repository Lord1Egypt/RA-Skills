## Description:

CompoundMind distills daily memory logs into searchable experience, task briefings, and growth reports for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use CompoundMind to turn local memory logs into structured lessons, decisions, facts, searchable history, and pre-task briefings that help future sessions reuse prior experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled or newly indexed memory data can contain credentials, tokens, wallet details, personal data, and sensitive configuration notes.

Mitigation: Remove bundled experience data before installation, rotate any exposed credentials, and add secret and PII redaction before distilling, indexing, saving, briefing, or sending content to an LLM.

Risk: Stored memories can resurface persistent behavioral directives that may be stale, unsafe, or outside the user's current intent.

Mitigation: Treat retrieved memories as untrusted notes, require review before acting on generated briefings, and scope the memory directory to approved sources.

Risk: Cron, heartbeat hooks, and optional LLM mode can automate processing of sensitive local memory and external API calls.

Mitigation: Keep automation and LLM synthesis disabled until consent, scope, logging, and review controls are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cassh100k/skills/compound-mind)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cassh100k)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown briefings, JSON experience records, growth reports, and SQLite FTS index data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save generated briefs and persistent distilled experience data; optional LLM synthesis uses an Anthropic API key.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and artifact/clawpkg.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
