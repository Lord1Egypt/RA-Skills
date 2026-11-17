## Description:

Ccy Txt2img is a local, offline Pillow-based image generation skill for text-to-image rendering, basic shapes, simple composition, and rule-driven Chinese/English scene drawing to PNG/JPEG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchongyong](https://clawhub.ai/user/chenchongyong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate simple local diagrams, text posters, code-image snippets, and controlled scene graphics without calling external image APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted scene JSON can reference local image layer paths.

Mitigation: Review image layer paths before rendering, avoid absolute or sensitive local paths, and use only trusted local assets.

Risk: Large canvases, many layers, or large source images can consume excessive local CPU or memory.

Mitigation: Keep width, height, layer count, and source image sizes within reasonable bounds before rendering.

## Reference(s):

- [Ccy Txt2img ClawHub release](https://clawhub.ai/chenchongyong/skills/ccy-txt2img)
- [Font source notes](assets/fonts/SOURCE.txt)
- [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)

## Skill Output:

**Output Type(s):** [Files, JSON, Code, Shell commands, Guidance]

**Output Format:** [PNG/JPEG image files, optional JSON scene specifications, and Markdown/code snippets for Python or CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local execution only; generated images are non-photorealistic and rule-driven.]

## Skill Version(s):

1.0.1 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
