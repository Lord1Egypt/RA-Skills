## Description:

Dog Slide helps agents convert source documents into high-quality SVG presentation pages and export editable PPTX decks through a multi-role workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use Dog Slide to turn source documents or topics into SVG-based slide decks, with optional image generation, live preview, quality checks, and PPTX export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted documents or web captures can trigger broad local-file, network, credential, and file-moving behavior.

Mitigation: Use the skill only in trusted workspaces, avoid untrusted HTML or web captures, and prefer copying source files unless relocating originals is intended.

Risk: Provider API keys and custom base URLs can expose credentials or send requests to unintended endpoints.

Mitigation: Keep provider API keys scoped, avoid untrusted .env files in working directories, and use custom BASE_URL values only for trusted endpoints.

## Reference(s):

- [Dog Slide Skill Page](https://clawhub.ai/yz6214589-hash/skills/dog-slide)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Dog Slide Toolset](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, generated SVG files, and PPTX export artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured provider APIs for image generation, web image search, and text-to-speech.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
