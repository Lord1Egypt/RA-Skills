## Description:

Create professional PPT presentations with python-pptx using themed layouts, mixed text and images, and HTML text-preview support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huayang0704](https://clawhub.ai/user/huayang0704)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to generate styled PowerPoint decks from command-line arguments or a Python API. It supports title, content, feature grid, comparison, image, HTML-preview, and closing slides with built-in tech, modern, and corporate themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PPTX files may overwrite existing files when an output path already exists.

Mitigation: Choose output filenames carefully and generate into a controlled working directory.

Risk: Unpinned dependencies can change behavior across environments.

Mitigation: Install dependencies in a virtual environment and prefer pinned versions of python-pptx and Pillow.

Risk: The HTML feature may be mistaken for real embedded HTML rendering.

Mitigation: Treat HTML input as a text preview and verify slide output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huayang0704/skills/dragon-ppt-maker-bak)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [PPTX presentation files with Markdown documentation and Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PPTX output is written to a user-selected path; HTML support is represented as a text preview rather than full embedded HTML rendering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
