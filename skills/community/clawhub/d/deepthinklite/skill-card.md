## Description:

Local-first deep research like OpenAI Deep Research: generates questions.md + response.md artifacts and enforces a time budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajsanghvi1](https://clawhub.ai/user/virajsanghvi1)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and agents use DeepthinkLite to structure deep research tasks into local questions.md, response.md, and meta.json artifacts with a time budget and untrusted-source handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research runs may handle sensitive or untrusted source material, especially when raw snippets are allowed.

Mitigation: Use summary-only mode for sensitive material and include raw snippets only after explicit user approval.

Risk: The workflow may involve web browsing or reading non-obvious local paths during research.

Mitigation: Ask the user for permission and state the planned sources or paths before browsing or reading those locations.

Risk: Local Markdown and JSON artifacts may retain research material after the run.

Mitigation: Choose an appropriate output directory and review generated artifacts before sharing or committing them.

## Reference(s):

- [DeepthinkLite ClawHub skill page](https://clawhub.ai/virajsanghvi1/skills/deepthinklite)
- [Project repository listed in artifact](https://github.com/VirajSanghvi1/deepthinklite-skill)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Run directory containing Markdown and JSON files, with a shell command returning the created path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates questions.md, response.md, and meta.json; default time budget is 10 to 60 minutes; summary-only mode is available for sensitive source material.]

## Skill Version(s):

1.2.3 (source: server release metadata, artifact manifest, plugin manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
