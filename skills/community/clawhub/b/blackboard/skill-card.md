## Description:

Generates vertical 9:16 dark blackboard-style poster image prompts with bold handwritten-marker Chinese text, high-contrast accent colors, and reusable layout guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative operators use this skill to turn poster or cover-image requests into structured prompts for Chinese blackboard-style vertical social graphics. The skill is best suited for slogan, tutorial-cover, campaign, and brand-style poster drafts where users can review and refine generated text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated poster text may be inaccurate, malformed, or unsuitable for formal publication.

Mitigation: Review generated Chinese text and overlay precise final typography before production use.

Risk: Confidential campaign or brand details may be included in the generated image and returned prompt.

Mitigation: Avoid confidential inputs unless the user is comfortable with the image and prompt being returned through the configured messaging channel.

Risk: The skill may trigger on broad poster or cover-image requests.

Mitigation: Confirm the requested visual style before invoking the blackboard poster workflow when user intent is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/blackboard)
- [Blackboard style guide](artifact/references/style-guide.md)
- [Layout templates](artifact/references/layout-templates.md)

## Skill Output:

**Output Type(s):** [text, guidance, API calls, image]

**Output Format:** [Markdown-style response with an image-generation request, generated image file path, and reusable English prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 9:16 poster imagery at the requested image-generation resolution; Chinese text in generated images should be reviewed before formal use.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
