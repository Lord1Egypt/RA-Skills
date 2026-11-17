## Description:

Generates professional slide deck images from content by creating outlines with style instructions and then generating individual slide images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn source material into shareable slide decks with selectable visual styles, audience targeting, language handling, slide-count control, and export to PPTX or PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback runtime may download and execute an unpinned package at run time.

Mitigation: Use a trusted, already installed Bun binary, or pin and review the runtime package before allowing the npx fallback.

Risk: The skill can create and rename files in slide-deck output folders.

Mitigation: Run it in a project workspace where generated deck files are expected, and review file changes before keeping or publishing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nengnengz/skills/baoyu-slide-deck-2)
- [Publisher profile](https://clawhub.ai/user/nengnengz)
- [Homepage from ClawHub metadata](https://github.com/JimLiu/baoyu-skills#baoyu-slide-deck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance plus generated deck files such as PNG slides, PPTX, and PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and rename files under slide-deck output folders; supports style, audience, language, slide count, review, and regeneration options.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
