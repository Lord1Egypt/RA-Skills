## Description:

Generate a launch-ready app package for App Store submission: a complete Markdown feature document plus AI-generated Apple-style UI design images for each page and a square-corner app icon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product builders use this skill to generate App Store submission planning artifacts for a Flutter 3.35.1, offline-first iOS app concept. It produces bilingual feature documentation, Apple-style UI design assets or prompt packages, and a square-corner app icon after explicit review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional AI image-generation step may send page names and design constraints from an approved feature document to OpenAI.

Mitigation: Use the non-API prompt-package path when the app concept or feature document contains sensitive product details or external model calls are not acceptable.

Risk: App Store submission copy can be rejected if it includes exaggerated claims, unclear permission use, or incomplete privacy language.

Mitigation: Apply the bundled review safety checklist and keep camera, photo library, privacy, and claims language factual, user-triggered, and local-first.

## Reference(s):

- [App Store Review Safety Checklist](references/review-safety-checklist.md)
- [OpenAI Images API endpoint](https://api.openai.com/v1/images/generations)
- [ClawHub skill page](https://clawhub.ai/chentuan7963-afk/skills/flutter-appstore-doc-ui-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, PNG and SVG assets, prompt packages, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are staged behind user approval gates; optional AI image generation requires OPENAI_API_KEY.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
