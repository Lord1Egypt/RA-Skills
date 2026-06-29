## Description: <br>
Generates structured illustration prompts for novel chapters by analyzing story context, character references, tone, and visual style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors and creative teams use this skill to turn novel chapters or scene excerpts into one to three consistent image-generation prompts. It helps preserve character appearance, story tone, visual style, composition, lighting, and optional in-scene text treatment across a series. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local novel project files to infer character details, style references, and prior illustration records. <br>
Mitigation: Use it only in project workspaces where that story context is appropriate for the agent to inspect. <br>
Risk: The skill may write reusable character notes for future prompt consistency. <br>
Mitigation: Review generated notes and prompt outputs before committing them to a project or using them in downstream image-generation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/brushtrace) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured Markdown, JSON prompt objects, and plain text prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one to three illustration prompts per chapter or scene; prompts may include optional embedded text-layer guidance and aspect-ratio controls.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
