## Description:

Converts an AI/tech news item into an eight-slide Instagram news carousel for creators, using interchangeable HTML themes rendered to 1080x1350 PNGs plus static or animated cover assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to turn a confirmed AI or technology news source into a publish-ready Spanish Instagram carousel with actionable framing, CTA copy, rendered slide assets, and cover animation components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The carousel can mislead readers if the source news item is incomplete, unverified, or embellished during rewriting.

Mitigation: Use a confirmed source before generating copy, keep dates, names, and numbers tied to that source, and omit or qualify unsupported claims.

Risk: Local rendering requires Chromium and puppeteer-core, which adds installation and execution surface on the operator machine.

Mitigation: Install only the declared dependency, run rendering in a controlled workspace, and review generated HTML before opening or rendering it.

Risk: Optional media generation may use API tokens and paid credits for Gemini, Higgsfield, or Apify.

Mitigation: Confirm credentials and cost approval before calls, generate cover media once, and reuse the resulting assets when re-rendering.

Risk: The animated cover may require manual assembly even when the workflow describes final MP4 output.

Mitigation: Deliver the raw video and transparent title overlay separately when server-side composition is unavailable, then verify the final MP4 before publication.

## Reference(s):

- [Animated cover reference](reference.md)
- [Theme authoring template](themes/_template.md)
- [Scrapbook theme](themes/scrapbook.md)
- [ClawHub skill page](https://clawhub.ai/formula100k/skills/carrusel-noticiero)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML templates, shell commands, and generated asset paths for PNG and MP4 outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces eight 1080x1350 PNG carousel slides, optional animated cover components, transparent title overlay assets, and editable HTML sources.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
