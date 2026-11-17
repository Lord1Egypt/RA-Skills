## Description:

Generate fixed-template daily AI news posters from five AI news items, supporting Chinese or bilingual social poster workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyacheng](https://clawhub.ai/user/caoyacheng)

### License/Terms of Use:


## Use Case:

Developers, content operators, and social media teams use this skill to normalize five AI news items and produce a ready-to-share daily poster. It is suited for recurring AI news recap images where a consistent layout, short factual summaries, and source labels are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer depends on Pillow, and installing dependencies directly into a shared Python environment can affect other projects.

Mitigation: Use a virtual environment and pin Pillow when installing the renderer dependency.

Risk: The operation manual includes an update command that removes the existing local skill directory before copying a replacement.

Mitigation: Review the target path before running the update command and keep a backup of local modifications.

Risk: Poster quality depends on receiving exactly five factual news items with source labels.

Mitigation: Validate the input JSON before rendering and ask for missing items when fewer than five are provided.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoyacheng/skills/ai-news-poster)
- [Operation manual](artifact/OPENCLAW-操作手册.md)
- [Sample input JSON](artifact/examples/input.sample.json)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [PNG poster image with optional normalized JSON and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary image output is a deterministic 1080x1350 PNG rendered from exactly five news items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
