## Description:

Enhanced BOOK BRAIN for LYGO Havens with visual capability. Use to design and maintain a 3-brain filesystem + memory system that also integrates LEFT/RIGHT brain visual checking (browser, images, screenshots) with text and API data for deeper verification and retrieval. Recommended for agents with visual tools or browser automation; use original book-brain only on non-visual systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to set up a non-destructive 3-brain workspace memory layout and a visual/text/API checking workflow. It helps visual-capable agents organize screenshots, indexes, logs, and reference stubs for later verification and retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to create or maintain local notes, indexes, logs, and selected screenshots in a workspace that contains sensitive material.

Mitigation: Review proposed folders and files before approving setup, and avoid storing screenshots or notes that expose sensitive project data.

Risk: Visual checks can disagree with structured data or APIs.

Mitigation: Log discrepancies explicitly and prefer auditable receipts or authoritative APIs over user interface displays when sources conflict.

## Reference(s):

- [BOOK BRAIN VISUAL READER examples](references/book-brain-visual-examples.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/book-brain-visual-reader)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with filesystem trees, text snippets, setup steps, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents should propose local folder, index, log, and screenshot organization without overwriting existing files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
