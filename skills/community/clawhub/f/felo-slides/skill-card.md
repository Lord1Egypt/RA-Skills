## Description:

Generates PPT/slides with the Felo PPT Task API in Claude Code, including API key checks, task creation, polling, theme support, task resume, and final ppt_url output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to create presentation decks from prompts or outlines through Felo's asynchronous PPT Task API. It is intended for slide generation workflows that need task creation, polling, resume support, and a returned PPT or live document URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends an unpinned npx install command.

Mitigation: Install from a pinned or manually reviewed source before using the skill in production.

Risk: API traffic can be redirected by setting FELO_API_BASE.

Mitigation: Use the default Felo API endpoint and set FELO_API_BASE only when the destination is fully trusted.

Risk: Prompts and slide-generation inputs are sent to Felo's API.

Mitigation: Use a dedicated, revocable Felo API key and avoid sending sensitive content unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/felo-slides)
- [Felo PPT Task API](https://openapi.felo.ai/docs/api-reference/v2/ppt-tasks.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [Felo API key setup](https://felo.ai)
- [Felo skills repository](https://github.com/Felo-Inc/felo-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown result with slide URL and optional JSON task metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ppt_url or live_doc_url, task_id, terminal status, and optional Felo metadata; requires FELO_API_KEY.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
