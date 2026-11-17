## Description:

Turns chapters, subtitles, and summaries visible on a Bilibili video page into timestamped study notes with page evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External users can organize the chapters, subtitles, or summaries currently visible on one Bilibili video page into learning notes tied to page text, timestamps, and the video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting setup instructions leave unclear who selects the signed-in browser environment.

Mitigation: Require the user's explicit browserId choice before page access or environment substitution; prefer a dedicated browser profile, authorize draft entry separately, and review or pin installer and dependency revisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/bilibili-video-chapter-notes-free)
- [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [Easy WebBridge project](https://github.com/aiispower/easy-webbridge)
- [OpenCLI Bilibili adapter documentation](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table with notes, visible page evidence, and timestamps when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most 100 visible rows per run; reports unavailable subtitles or summaries and collection gaps.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
