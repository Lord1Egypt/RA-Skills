## Description:

Autopsy a slide deck from photos or screenshots of its slides - the narrative arc, the numbers, and what each slide is hiding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and operators use this skill to review real slide images from pitches, conference talks, competitor decks, or their own presentations. It reconstructs the deck's argument, checks cross-slide numbers, identifies weak links, and surfaces avoided questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide images may contain confidential or sensitive business information.

Mitigation: Only provide slide images the user is authorized to share, and review the resulting analysis before acting on it.

Risk: Unreadable or ambiguous slide content can lead to incorrect deck analysis.

Mitigation: Require findings to be anchored to specific slide numbers and flag unreadable content instead of guessing.

## Reference(s):

- [Deck Autopsy Skill Page](https://mohitagw15856.github.io/pm-claude-skills/skill/deck-autopsy.html)
- [Deck Autopsy on ClawHub](https://clawhub.ai/mohitagw15856/skills/deck-autopsy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with slide-by-slide findings, argument reconstruction, number checks, avoided questions, and optional hardening guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires slide images as input; every finding should cite a slide number and unreadable content should be flagged rather than guessed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
