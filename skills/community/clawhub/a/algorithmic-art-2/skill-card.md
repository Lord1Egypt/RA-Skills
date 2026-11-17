## Description:

Algorithmic Art helps agents create original p5.js generative art by first drafting an algorithmic philosophy, then producing seeded, interactive HTML/JavaScript artwork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinouyang](https://clawhub.ai/user/darinouyang)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, creative technologists, and external users use this skill to guide an agent through original algorithmic-art ideation and implementation. It produces a concise philosophy plus interactive p5.js artifacts with seeded variation and tunable parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML/JavaScript viewers are executable artifacts and may load public CDN resources.

Mitigation: Review generated artifacts before sharing or deployment, and bundle or integrity-pin CDN dependencies when using them in controlled environments.

Risk: Generated viewers may use an Anthropic-styled template, which can make user-generated outputs look more official than they are.

Mitigation: Treat shared HTML artifacts as user-generated content and avoid implying endorsement by Anthropic, NVIDIA, or the hosting platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darinouyang/skills/algorithmic-art-2)
- [p5.js runtime CDN](https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js)
- [Viewer template](artifact/templates/viewer.html)
- [Generator template](artifact/templates/generator_template.js)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Markdown plus self-contained HTML/JavaScript artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seeded p5.js randomness and interactive parameter controls; generated viewers may rely on public CDN resources unless modified.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
