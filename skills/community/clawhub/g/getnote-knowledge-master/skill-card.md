## Description:

Get笔记·六步抄作业版 helps agents run a six-step Getnote knowledge-management workflow for creating knowledge bases, saving content, organizing notes, searching, preserving analysis, and generating health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to turn natural-language requests into Getnote workflows for collecting, organizing, searching, and re-saving knowledge artifacts. It is especially oriented toward repeated knowledge-management routines that combine note retrieval, summarization, tagging, and report creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad note collection can include all Getnote knowledge bases and local memory during the Cron workflow.

Mitigation: Use the Cron workflow only when that scope is intended, and confirm the selected knowledge bases and local memory sources before running it.

Risk: Write actions can save reports or summaries to Getnote, local files, Feishu documents, or Feishu knowledge bases.

Mitigation: Require a preview and explicit destination confirmation before any write or external sharing action.

Risk: Duplicate cleanup guidance can delete notes if applied without enough review.

Mitigation: Require a deletion preview that lists affected note IDs and preserve the most complete copy only after user approval.

Risk: Credentialed Getnote and Feishu operations increase impact if credentials are over-scoped.

Mitigation: Install with tightly scoped Getnote and Feishu credentials and review the skill before deployment.

## Reference(s):

- [Getnote six-step implementation guide](references/6steps.md)
- [Getnote OpenAPI base endpoint](https://openapi.biji.com)
- [ClawHub skill release page](https://clawhub.ai/binhuatochina/skills/getnote-knowledge-master)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue Getnote CLI commands, produce reports, suggest tags, and save generated summaries when credentials and user confirmation allow.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
