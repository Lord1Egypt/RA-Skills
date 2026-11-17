## Description:

PPT制作 helps agents generate styled PowerPoint presentations with reusable slide layouts, mixed image and text content, image slides, and HTML content previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon015](https://clawhub.ai/user/dragon015)

### License/Terms of Use:


## Use Case:

Developers, employees, and external content creators use this skill to create professional .pptx decks from command-line arguments or Python API calls when they need themed layouts for presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes presentation files to local output paths, and --openclaw mode uses a fixed Windows Desktop path.

Mitigation: Review or override output paths before execution, especially before using --openclaw.

Risk: Unpinned presentation-generation dependencies can change behavior across environments.

Mitigation: Install in a virtual environment and consider pinning python-pptx and Pillow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragon015/skills/dragon-ppt-maker)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [PowerPoint .pptx files with Markdown instructions, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks are local files; image slides can read user-supplied local image paths.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
