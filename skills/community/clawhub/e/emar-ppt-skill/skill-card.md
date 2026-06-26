## Description: <br>
Creates Emar-branded horizontal web presentation decks as single HTML files for internal slides, event decks, reports, image-backed covers, and Swiss or electronic-magazine styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixinyi546-maker](https://clawhub.ai/user/jixinyi546-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and presentation authors use this skill to create Emar Online internal HTML slide decks from bundled templates, choosing between editorial and Swiss-style layouts and validating Swiss decks when applicable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated internal decks may contact third-party services or run CDN-hosted JavaScript when opened. <br>
Mitigation: Review decks before use with internal or confidential material; prefer locally vendored fonts and JavaScript, removed or pinned and disclosed CDN fallbacks, and bundled relative references. <br>
Risk: Absolute local reference paths can reduce portability and expose local environment assumptions. <br>
Mitigation: Replace absolute local paths with bundled relative references before distributing generated decks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jixinyi546-maker/emar-ppt-skill) <br>
- [Project Homepage](https://github.com/op7418/emar-ppt-skill) <br>
- [Checklist](artifact/references/checklist.md) <br>
- [Components](artifact/references/components.md) <br>
- [Image Prompts](artifact/references/image-prompts.md) <br>
- [Style A Layouts](artifact/references/layouts.md) <br>
- [Swiss Layouts](artifact/references/layouts-swiss.md) <br>
- [Screenshot Framing](artifact/references/screenshot-framing.md) <br>
- [Swiss Layout Lock](artifact/references/swiss-layout-lock.md) <br>
- [Swiss Map Component](artifact/references/swiss-map-component.md) <br>
- [Style A Themes](artifact/references/themes.md) <br>
- [Swiss Themes](artifact/references/themes-swiss.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Single-file HTML deck plus concise Markdown delivery summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local image asset paths and optional Swiss validation results.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
