## Description:

Helps agents implement or configure animation-style toon and cel shaders using presets, feature mappings, and reference material for lilToon, Poiyomi, UTS2, RToon, SToon, and ToonShadingCollection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuki001](https://clawhub.ai/user/yuki001)

### License/Terms of Use:


## Use Case:

Developers and technical artists use this skill to ask agents for shader design guidance, configuration suggestions, and code-oriented implementation support for toon and stylized rendering effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some detailed reference files are Chinese or bilingual, which can lead to misunderstanding for English-only users.

Mitigation: Ask the agent to translate or summarize source passages before applying them, and review shader settings against the target project's language and terminology.

Risk: The skill may cause the agent to read several bundled reference files before answering, increasing context use and response time.

Mitigation: Start with a specific preset or shader feature list so the agent can limit reference reads to the relevant files.

Risk: Shader configuration or code guidance can be incorrect for a specific engine version, render pipeline, or avatar constraint.

Mitigation: Review generated guidance and test shader changes in the target rendering environment before release.

## Reference(s):

- [Animation Shader Skill](SKILL.md)
- [Standalone Workflow](workflow-standalone.md)
- [lilToon Shader Features](references/lilToon/Features.md)
- [Poiyomi Toon Shader Features](references/PoiyomiShaders/Features.md)
- [RToon Shader Features](references/RToon/Features.md)
- [SToon Features](references/SToon/Features.md)
- [UnityChanToonShaderVer2 Features](references/UnityChanToonShaderVer2/Features.md)
- [ToonShadingCollection Features](references/ToonShadingCollection/Features.md)
- [AudioLink](https://github.com/llealloo/vrc-udon-audio-link)
- [ClawHub Skill Page](https://clawhub.ai/yuki001/skills/animation-shader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown prose with shader configuration notes and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to read several bundled reference files before responding; some references are Chinese or bilingual.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
