## Description:

Generate meme captions using trending templates and viral reaction formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft meme captions, browse common meme templates, and generate reaction-format caption ideas for a supplied topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a local data manager that can retain user input and command history as plaintext under the meme-generator data directory.

Mitigation: Avoid private, customer, or proprietary text; inspect the retained files before sharing a system; set MEME_GENERATOR_DIR to an isolated location when testing.

Risk: The local data-manager behavior is under-disclosed relative to the meme-caption use case.

Mitigation: Review the installed scripts before use and prefer a release that removes or clearly documents the data-manager and logging behavior.

## Reference(s):

- [Meme Generator on ClawHub](https://clawhub.ai/loutai0307-prog/skills/bytesagain-meme-generator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; default local data directory is ~/.local/share/meme-generator/ unless MEME_GENERATOR_DIR is set.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
