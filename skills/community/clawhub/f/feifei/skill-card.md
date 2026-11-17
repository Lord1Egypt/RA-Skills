## Description:

Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaom0](https://clawhub.ai/user/zhaom0)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, creative technologists, and external users use this skill to turn art prompts into an original algorithmic philosophy and an interactive p5.js generative-art artifact with seeded variation controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may load p5.js and fonts from external CDNs, which can affect offline use and introduce third-party dependency considerations.

Mitigation: Review generated artifacts for external resource loading and replace CDN assets with approved local copies when offline operation or stricter dependency control is required.

Risk: Outputs are steered toward an Anthropic-branded viewer template, which may be inappropriate for neutral, customer, or NVIDIA-branded deployments.

Mitigation: Modify the viewer template branding before deployment when brand neutrality or specific presentation requirements apply.

Risk: The skill asks for original generative art, but user-provided references or prompts could still lead to outputs that resemble protected work too closely.

Mitigation: Review generated philosophies and artifacts for originality and rights concerns before publication or commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaom0/skills/feifei)
- [p5.js runtime dependency](https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js)
- [Viewer template](artifact/templates/viewer.html)
- [Generator template](artifact/templates/generator_template.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Markdown philosophy plus a self-contained HTML artifact with inline JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts use seeded randomness for reproducible p5.js variations and may include browser controls for parameters, seeds, colors, reset, regeneration, and PNG export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
