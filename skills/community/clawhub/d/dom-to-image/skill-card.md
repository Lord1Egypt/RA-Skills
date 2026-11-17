## Description:

Convert HTML DOM nodes to images (PNG/JPEG/SVG/Blob) with rendering options such as filter, backgroundColor, quality, and pixelRatio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to export selected browser DOM nodes as PNG, JPEG, SVG, or Blob images, including screenshots of page elements, generated cover images, and downloadable React component output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported images can include any private or sensitive content inside the selected DOM node.

Mitigation: Choose target elements carefully and use filters or redaction to exclude private content before export.

Risk: Production use depends on the external html-to-image npm package.

Mitigation: Pin and review the npm dependency before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/dom-to-image)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JavaScript, TypeScript, and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides browser-side DOM export using html-to-image options and download handling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
