## Description:

Audits the hook pattern of an Instagram or TikTok account by comparing top and bottom reels, analyzing textual, visual, and verbal hook signals, and producing an interactive report with editor-ready layout guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and marketing teams use this skill to audit Instagram or TikTok accounts, identify hook patterns that separate high-performing reels from low-performing reels, and turn the findings into reports, scripts, and visual layout guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send social-media account data, transcripts, captions, media URLs, generated images, and pasted first-party analytics to external services.

Mitigation: Confirm the providers, costs, retention expectations, and optional memory or Yapper actions with the user before running service calls or storing outputs.

Risk: Analysis may overstate findings when only covers, screenshots, or a small reel sample are available.

Mitigation: Label covers as covers, mark anatomy unavailable unless screenshots or Higgsfield video analysis support it, and describe small-sample carrier findings as signals rather than proof.

Risk: Paid Apify, Gemini, or Higgsfield actions can incur cost or fail without credentials and balance.

Mitigation: Report estimated cost, verify API keys or MCP balance, and wait for explicit user approval before paid scraping or image-generation steps.

Risk: Generated layout mockups can imply use of a real person's likeness or brand details.

Mitigation: Use generic creator references for layouts and avoid exact faces or real brand marks unless the user has supplied and approved those assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/auditor-ganchos-cuenta-formula100k)
- [Plantilla de REPORTE.md](references/reporte-md-template.md)
- [Plantilla del index.html interactivo](references/html-template.md)
- [Plantillas de prompt para mockups de gancho con Higgsfield](references/prompts-higgsfield.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, single-file HTML, JSON datasets, PNG layout assets, shell/API command guidance, and chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Apify, Gemini, Higgsfield, Composio, and optional Yapper or memory workflows when credentials, balance, and user approval are available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
