## Description:

通过内置脚本获取B站视频信息并总结。

This skill is ready for commercial/non-commercial use.

## Publisher:

[raise7727](https://clawhub.ai/user/raise7727)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a Bilibili video URL or BV ID to retrieve public video metadata and generate a concise summary from the returned title, uploader, play count, likes, and description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BV video ID from the user's request is sent to Bilibili's public API.

Mitigation: Use the skill only with public Bilibili video identifiers that are appropriate to share with Bilibili's API.

Risk: The summary is based on metadata and description fields, not full transcript or video-content analysis.

Mitigation: Treat summaries as metadata-based and verify against the source video when content-level accuracy matters.

Risk: The artifact script filename is scripts/fecth.js while the skill instructions refer to scripts/fetch.js.

Mitigation: Confirm or correct the script path before deployment so the agent can call the intended helper reliably.

## Reference(s):

- [Bilibili API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/raise7727/skills/bilibili-summary-raise)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown summary with title, uploader, play count, likes, and content summary fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary is based on public Bilibili metadata and description fields rather than a full video transcript.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
