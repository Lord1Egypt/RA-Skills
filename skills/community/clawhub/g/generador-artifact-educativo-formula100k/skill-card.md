## Description:

Generates a single self-contained educational HTML miniapp for course or community material, with Guia, Flashcards, and Examen views that can be opened locally and shared through Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Course creators and community educators use this skill to turn source teaching material into a standalone Spanish educational miniapp with guide sections, flashcards, practical exam cases, visual patterns, and exportable markdown context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated artifacts may include confidential student data, private business material, or copyrighted course text if that material is supplied as input.

Mitigation: Use only authorized source material and avoid including confidential learner or business information in generated HTML.

Risk: The standalone HTML template depends on external CDN libraries, so the generated artifact may require internet access and exposes runtime availability to those third-party services.

Mitigation: Review CDN usage before distribution and bundle dependencies locally if offline use or stricter supply-chain control is required.

Risk: The workflow includes Telegram delivery, which can expose generated educational files outside the local workspace.

Mitigation: Confirm the intended recipient and content sensitivity before sending generated files through Telegram.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/generador-artifact-educativo-formula100k)
- [SKILL.md](artifact/SKILL.md)
- [template.html](artifact/template.html)
- [patrones-visuales.md](artifact/patrones-visuales.md)
- [paletas.md](artifact/paletas.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Guidance]

**Output Format:** [Single self-contained HTML file with embedded React, Tailwind, Babel CDN references, educational content, and markdown export text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Guia, Flashcards, and Examen views; intended output path is entregables/artifacts/ and the generated file may be sent through Telegram.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
