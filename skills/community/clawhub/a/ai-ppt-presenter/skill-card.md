## Description:

Creates reveal.js HTML presentations with planned slide structure, whiteboard-style AI illustrations, and complete word-for-word speaker scripts in presenter view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewislulu](https://clawhub.ai/user/lewislulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and business presenters use this skill to turn topics, notes, or Markdown into polished HTML slide decks with speaker scripts and optional AI-generated whiteboard illustrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide prompts or notes may be sent to Gemini during image generation.

Mitigation: Avoid confidential notes in prompts unless the user approves sending that content to Google.

Risk: Gemini API key handling can be exposure-prone when passed through commands or environments.

Mitigation: Use tightly restricted, low-quota API keys and avoid persisting keys in generated presentation files.

Risk: The generated presentation template is Chinese-localized by default.

Mitigation: Review and adjust template language, speaker scripts, and audience framing before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lewislulu/skills/ai-ppt-presenter)
- [SKILL.md](artifact/SKILL.md)
- [Reveal.js presentation template](artifact/assets/reveal-template.html)
- [Gemini slide image generation script](artifact/scripts/generate_slide_images.py)
- [Google Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent)
- [Reveal.js 5.1.0 CDN stylesheet](https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown planning drafts, HTML/reveal.js slide files, image files, shell commands, and speaker notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided Gemini API key for optional image generation and produces Chinese-localized presentation templates unless adapted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
