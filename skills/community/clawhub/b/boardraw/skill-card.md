## Description:

Boardraw turns natural-language requests into editable Excalidraw whiteboard files for flowcharts, mind maps, architecture diagrams, org charts, wireframes, sticky-note brainstorms, and sequence diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darrenli6](https://clawhub.ai/user/darrenli6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and other users use Boardraw to convert natural-language diagram requests into editable whiteboard files for processes, systems, organizations, wireframes, and brainstorming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagrams may be uploaded to boardraw.com and could contain confidential architecture, org, workflow, or customer-data details.

Mitigation: Use the skill only when Boardraw is an approved destination, and avoid confidential diagram content unless that upload path is authorized.

Risk: The upload workflow can read BOARDRAW_API_KEY from the environment or a discovered .env file.

Mitigation: Prefer setting BOARDRAW_API_KEY explicitly in the execution environment and review .env handling before installation.

Risk: The security evidence marks the release as suspicious because upload behavior and local API-key discovery deserve review before installation.

Mitigation: Review the skill and scanner summary before deployment, especially in environments handling sensitive diagrams.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/darrenli6/boardraw.com-skill/tree/master/boardraw)
- [ClawHub skill page](https://clawhub.ai/darrenli6/skills/boardraw)
- [Excalidraw schema reference](references/excalidraw-schema.md)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with generated Python snippets and editable .excalidraw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload the generated whiteboard to boardraw.com when an API key is configured and the user confirms.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
