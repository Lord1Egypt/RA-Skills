## Description:

Generates technical Excalidraw illustrations as editable .excalidraw source files and rendered PNG images, with seven diagram styles and two-panel layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryaction](https://clawhub.ai/user/jerryaction)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to turn technical article content into editable Excalidraw diagrams and PNG illustrations, including flowcharts, architecture diagrams, timelines, comparison matrices, layered diagrams, and state machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an unpinned third-party npx Excalidraw CLI package.

Mitigation: Pin or preinstall a reviewed Excalidraw CLI version before use.

Risk: The skill directs agents to move generated diagram files and update collection index.json and README files.

Mitigation: Review generated file moves and index or README diffs before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryaction/skills/excalidraw-tech-illustration)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with .excalidraw source paths, PNG render outputs, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable Excalidraw files and rendered PNG images, and may update collection index and README files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
