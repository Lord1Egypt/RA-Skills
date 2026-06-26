## Description: <br>
Generates professional infographics by analyzing content, recommending layout and visual style combinations, and producing publication-ready infographic outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn source material into structured infographic content, visual layout recommendations, prompts, and generated raster infographics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves infographic prompts, source analysis, structured content, preferences, and generated assets locally. <br>
Mitigation: Review the generated local files before sharing or committing them, and avoid including secrets or sensitive source material in infographic inputs. <br>
Risk: Chosen content or reference images may be sent to the selected image-generation backend. <br>
Mitigation: Use only content and reference images that are approved for the selected backend, and confirm backend selection before generation. <br>
Risk: Pinned backend preferences, custom style fragments, or a Codex CLI wrapper path can change the execution path. <br>
Mitigation: Review EXTEND.md preferences before use, especially custom backend and style settings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-infographic) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-infographic) <br>
- [Analysis Framework](references/analysis-framework.md) <br>
- [Structured Content Template](references/structured-content-template.md) <br>
- [Codex Image Generation](references/codex-imagegen.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown workflow artifacts, saved prompt files, local preference configuration, backend invocation guidance, and raster infographic files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can save prompts, source analysis, structured content, preferences, reference images, and generated infographic assets locally.] <br>

## Skill Version(s): <br>
1.117.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
