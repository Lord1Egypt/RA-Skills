## Description:

Creates original algorithmic art workflows using p5.js with seeded randomness, interactive parameters, and reproducible generative sketches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunhe730](https://clawhub.ai/user/xunhe730)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to turn creative prompts into an algorithmic philosophy and a self-contained p5.js generative art viewer with reproducible seed controls and adjustable parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a named-user restriction that is not necessary for its generative art purpose.

Mitigation: Review and remove or rewrite the named-user restriction before using the skill as a general ClawHub release.

Risk: The skill pushes generated viewers toward Anthropic-branded structure and styling.

Mitigation: Replace the viewer branding with neutral or organization-approved UI before distribution when brand alignment matters.

Risk: Generated HTML viewers may load p5.js and fonts from external CDNs and support browser-side PNG export.

Mitigation: Approve the external dependencies and export behavior, or pin and mirror assets for environments that restrict third-party network loads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xunhe730/skills/algorithmic-art-blocked)
- [p5.js 1.7.0 CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js)
- [viewer.html template](templates/viewer.html)
- [generator_template.js reference](templates/generator_template.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown plus self-contained HTML/JavaScript using p5.js]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seeded randomness and interactive browser controls; generated HTML may load p5.js and fonts from CDNs and can export PNG files in the browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
