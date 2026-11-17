## Description:

Creates Emar-branded horizontal web presentation decks as single HTML files for internal presentations, reports, event decks, and Swiss Style or electronic magazine style slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixinyi546-maker](https://clawhub.ai/user/jixinyi546-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and presentation authors use this skill to turn supplied material into Emar-branded internal HTML slide decks with template-driven layouts, navigation, animation fallback, and optional Swiss validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentations may make outbound requests and run CDN-hosted browser JavaScript.

Mitigation: For confidential internal decks, remove or vendor the remote Lucide, Motion, font, MapLibre, and tile dependencies before sharing or opening the output.

Risk: Swiss Style decks can become inconsistent or hard to read if locked layouts are changed incorrectly.

Mitigation: Run the bundled Swiss deck validator for Style B decks when Node is available and fix reported layout issues before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jixinyi546-maker/skills/emar-ppt-skill)
- [Project Homepage](https://github.com/op7418/emar-ppt-skill)
- [Final QA Checklist](references/checklist.md)
- [Shared Components](references/components.md)
- [Image and Cover Prompts](references/image-prompts.md)
- [Style A Layouts](references/layouts.md)
- [Style A Themes](references/themes.md)
- [Swiss Layouts](references/layouts-swiss.md)
- [Swiss Layout Constraints](references/swiss-layout-lock.md)
- [Swiss Map Component](references/swiss-map-component.md)
- [Swiss Themes](references/themes-swiss.md)
- [Screenshot Framing](references/screenshot-framing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Single HTML presentation deck with concise Markdown delivery notes and optional shell validation command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces index.html from bundled templates; may include local image paths and optional Node-based Swiss deck validation.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
