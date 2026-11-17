## Description:

维护 AI 产品经理校招简历中枢，用于提炼工作日志、去重沉淀简历要点、维护要点池、生成或更新中文一页纸简历，并输出 Gap 清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[songnb1021](https://clawhub.ai/user/songnb1021)

### License/Terms of Use:

MIT-0

## Use Case:

External users maintaining Chinese AI product manager campus recruiting materials use this skill to convert logs and source experience into reusable resume points, one-page resume drafts, gap lists, dashboard previews, and PDF exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard can expose sensitive resume content through unsafe browser rendering.

Mitigation: Review dashboard output before opening it with untrusted resume content, and update the dashboard to escape embedded JSON and avoid unsafe innerHTML.

Risk: The dashboard loads unpinned browser dependencies from external CDNs.

Mitigation: Bundle dependencies locally or pin and disclose CDN use with integrity checks before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songnb1021/skills/ai-pm-resume-hub)
- [Tailwind CSS CDN runtime dependency](https://cdn.tailwindcss.com)
- [Marked CDN runtime dependency](https://cdn.jsdelivr.net/npm/marked/marked.min.js)
- [DOMPurify CDN runtime dependency](https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown files, local HTML dashboard, PDF exports, and concise chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates files under career/ai-pm-campus; dashboard and PDF generation use local scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
