## Description:

Routes AI image-editing tasks such as object removal, background removal, upscaling, outpainting, restoration, and retouching to suitable tools while requiring human review, rights checks, and disclosure where applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and social-media operators use this skill to classify an image-editing request, choose an appropriate editing route, draft prompts or settings, and hand off reviewed assets for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide use of external image tools and publishing workflows before credentials, source-image rights, or disclosure requirements are confirmed.

Mitigation: Confirm connected API credentials, source-image licenses, applicable legal disclosures, and human approval before public posting or commercial use.

Risk: Creative upscaling or generative edits can introduce details that misrepresent products, people, documents, or results imagery.

Mitigation: Use faithful editing modes for accuracy-critical images, prohibit defect concealment or provenance stripping, and require 100% human QA before handoff.

## Reference(s):

- [The TOUCH Framework](references/the-touch-framework.md)
- [AI Image Editing 2026 Reality](references/ai-image-editing-2026-reality.md)
- [Task Router and Templates](references/taREDACTED-SECRET.md)
- [Scope and Connections](references/scope-and-connections.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with task routing, edit specifications, QA checks, and optional command or API-call suggestions when tools are connected.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory workflow artifacts; final image quality, legal disclosure, rights clearance, and publication require human approval.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
