## Description:

PPT Generator helps an agent clarify presentation requirements, confirm a slide outline, generate SVG slides, and package them into a PPTX file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likegakki](https://clawhub.ai/user/likegakki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to turn a topic, outline, or source text into a confirmed slide plan and a generated PPTX presentation. It is best suited for business or technical presentations that can be represented as structured SVG slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install python-pptx from pip and run local Python scripts.

Mitigation: Run it in an isolated or approved Python environment and review dependency installation before use.

Risk: SVG slide content is embedded into the PPTX without strong sanitizer enforcement.

Mitigation: Use trusted slide content and inspect exported SVGs for unsupported or unsafe elements before sharing the PPTX.

Risk: Generated presentations may contain inaccurate, incomplete, or unsuitable slide content.

Mitigation: Confirm the slide outline before generation and review the final PPTX before using it in a business setting.

## Reference(s):

- [Gazee Glacier visual preset](references/presets/gazee-glacier.md)
- [ClawHub skill page](https://clawhub.ai/likegakki/skills/generate-pptx)
- [Publisher profile](https://clawhub.ai/user/likegakki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance, JSON slide data, SVG strings, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reuse a Python virtual environment, install python-pptx, and optionally export intermediate SVG files for inspection.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
