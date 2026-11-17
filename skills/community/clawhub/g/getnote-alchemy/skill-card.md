## Description:

Get笔记炼金术 helps agents turn Get笔记 recording notes into reusable knowledge assets by reviewing privacy sensitivity, distilling summaries and structured knowledge, and archiving results to Feishu with optional IMA or Feishu Wiki sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingclaw](https://clawhub.ai/user/qingclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External professionals such as lawyers, consultants, trainers, and sales teams use this skill to process recording transcripts into privacy-reviewed summaries, knowledge points, tags, tasks, and searchable Feishu records. Developers or workspace administrators configure credentials, categories, privacy defaults, batch behavior, and optional IMA or Feishu Wiki destinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically process sensitive recording transcripts and write derived summaries, metadata, tags, tasks, and privacy status into external knowledge systems.

Mitigation: Review before installing, use least-privilege credentials, disable scheduled processing and optional IMA or Wiki sync unless needed, and avoid privileged or regulated recordings until consent, transcript handling, validation, and rollback controls are clearer.

Risk: The security verdict is suspicious because consent and prompt-injection guardrails are weak for untrusted transcript content.

Mitigation: Require explicit per-run review for high-risk recordings, keep P1 confirmation enabled with a default desensitize action, and manually inspect outputs before they are shared or used as knowledge sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingclaw/skills/getnote-alchemy)
- [Get笔记 homepage](https://biji.com)
- [Get笔记 note list API](https://openapi.biji.com/open/api/v1/resource/note/list?cursor=0)
- [Get笔记 note detail API](https://openapi.biji.com/open/api/v1/resource/note/detail?id={note_id})
- [Bitable setup guide](references/bitable-setup.md)
- [Distillation prompt templates](references/distill-prompts.md)
- [Privacy review rules](references/privacy-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries and structured record fields for Feishu Bitable, with JSON configuration state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GETNOTE_API_KEY and GETNOTE_CLIENT_ID; optional IMA credentials are used only when IMA sync is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
