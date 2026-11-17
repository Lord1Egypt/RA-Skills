## Description:

Build or revise architecture diagrams directly in excalidraw.com from natural-language requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[energypantry](https://clawhub.ai/user/energypantry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn natural-language architecture, data pipeline, workflow, or multi-tenant system requirements into structured Excalidraw diagrams and revise those diagrams based on feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the current Excalidraw canvas when it writes scene elements.

Mitigation: Run it on a new or backed-up canvas when the current board contains important work.

Risk: The skill depends on the Excalidraw page runtime API and may fail if the page structure changes or the API is unavailable.

Mitigation: Verify the Excalidraw tab and API lookup before writing elements; refresh once and retry when lookup fails.

## Reference(s):

- [Excalidraw](https://excalidraw.com/)
- [Excalidraw API snippets](references/excalidraw-api-snippets.md)
- [ClawHub skill page](https://clawhub.ai/energypantry/skills/excalidraw-architect)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown instructions with JavaScript browser-evaluation snippets, optional shell commands, and JSON Excalidraw element data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the active Excalidraw scene and may generate element JSON files for repeatable diagram creation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
