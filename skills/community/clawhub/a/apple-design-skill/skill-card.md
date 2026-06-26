## Description: <br>
Guides AI assistants to generate Apple-style frontend UI code using design tokens, typography rules, layout patterns, copywriting guidance, and image curation strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaos-xxl](https://clawhub.ai/user/chaos-xxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to guide coding agents in producing Apple-style landing pages, feature pages, pricing pages, and related frontend UI. It is aimed at external agent users who want concise design-system instructions and generated HTML, CSS, or Tailwind output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pages may reference third-party fonts or image sources, which can affect privacy requirements or offline operation. <br>
Mitigation: Review generated pages before publishing and replace Google Fonts, Unsplash, or Pexels links with locally hosted or approved assets when strict privacy, compliance, or offline use is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaos-xxl/apple-design-skill) <br>
- [README](artifact/README.md) <br>
- [Core entry prompt](artifact/prompts/main.md) <br>
- [Design tokens](artifact/prompts/design-tokens.md) <br>
- [Typography](artifact/prompts/typography.md) <br>
- [Layout patterns](artifact/prompts/layout-patterns.md) <br>
- [Image curation](artifact/prompts/image-curation.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with HTML, CSS, and optional Tailwind code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages may include references to Google Fonts, Unsplash, or Pexels when the user or host environment permits third-party assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, manifest.json, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
