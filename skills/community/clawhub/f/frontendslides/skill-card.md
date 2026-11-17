## Description:

Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presenters, educators, and other external users use this skill to create browser-based HTML slide decks, enhance existing presentations, or convert PPT/PPTX files into web slides with guided visual style selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may load fonts from third-party CDNs, which can expose network requests when a presentation is opened.

Mitigation: Review or replace remote font links before opening sensitive decks or presenting in environments where network privacy matters.

Risk: Optional inline editing stores slide text in browser localStorage.

Mitigation: Avoid enabling inline editing for confidential slide content on shared browsers, or clear localStorage after use.

Risk: PPT and image workflows may require unpinned Python packages.

Mitigation: Install Python dependencies in a virtual environment and review package versions before processing decks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/frontendslides)
- [Skill demo deck](https://github.com/user-attachments/assets/ef57333e-f879-432a-afb9-180388982478)
- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML, CSS, JavaScript, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce self-contained HTML presentation files, extracted PPT content JSON, local image assets, and optional browser-editing behavior.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
