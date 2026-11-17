## Description:

Generate banners, boxes, cowsay-style art, tables, and image-to-ASCII with multiple fonts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, CLI authors, and documentation writers use this skill to create terminal-friendly banners, boxed notes, cowsay-style messages, tables, and image-to-ASCII output for logs, scripts, and Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command downloads mutable remote Python code that may differ from the reviewed packaged artifact.

Mitigation: Prefer the packaged artifact/ascii_art.py file or a pinned, checksummed release before execution.

Risk: Processing untrusted or extremely large image files may consume excessive local resources.

Mitigation: Apply file size and runtime limits when converting images from untrusted sources.

Risk: The CI verifier can run self-tests while checking third-party folders.

Mitigation: Run verification for third-party folders inside a sandbox.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/ascii-art-creator)
- [Packaged README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown containing ASCII/Unicode art and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline Python 3.8+ tool; image conversion depends on readable local image files.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
