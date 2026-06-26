## Description: <br>
Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningzimu](https://clawhub.ai/user/ningzimu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to turn articles, reports, papers, notes, or outlines into visually unified image-based PowerPoint decks with slide images, speaker notes, and assembled PPTX output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create local project files and install or use a small Python runtime. <br>
Mitigation: Review the generated project directory and runtime setup before deployment, and install only in environments where local file creation is acceptable. <br>
Risk: Slide prompts or source images may be sent to OpenAI or a configured compatible image provider when API fallback is used. <br>
Mitigation: Prefer the built-in image tool for sensitive decks when available, verify OPENAI_BASE_URL before API fallback, and avoid sending confidential source material to untrusted providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningzimu/codex-ppt) <br>
- [Project homepage from metadata](https://github.com/ningzimu/codex-ppt-skill) <br>
- [Backend selection](artifact/docs/backend-selection.md) <br>
- [CLI/API fallback](artifact/docs/cli-api-fallback.md) <br>
- [Workflow gates and progress](artifact/docs/workflow-gates-and-progress.md) <br>
- [Project assembly and reporting](artifact/docs/project-assembly-and-reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON project artifacts, PNG slide images, speaker notes, and PPTX assembly output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project files and may call a configured image-generation provider when API fallback is selected.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
