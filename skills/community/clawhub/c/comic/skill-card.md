## Description: <br>
Generate educational or narrative comic pages with structured art, tone, layout, and language decisions and bundled generation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn source material into multi-page educational, tutorial, biography, or narrative comics with planned characters, storyboard structure, page prompts, generated images, and PDF delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images may be sent to WeryAI during generation. <br>
Mitigation: Use only non-sensitive prompts and reference images, prefer public HTTPS references, and avoid uploading private local material. <br>
Risk: Webhook and web-search options can send data outside the local project when enabled. <br>
Mitigation: Leave those options disabled unless they are required, and review any endpoint or search setting before running generation. <br>
Risk: First-run setup can create .image-skills configuration and install bundled dependencies. <br>
Mitigation: Review setup output before continuing, run in a controlled project directory, and prefer environment-provided API keys over persisted .env secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/comic) <br>
- [Comic dimensions reference](references/dimensions.md) <br>
- [Character template](references/character-template.md) <br>
- [Prompt template](references/prompt-template.md) <br>
- [Storyboard template](references/storyboard-template.md) <br>
- [WeryAI API keys](https://weryai.com/api/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, storyboard and prompt files, generated image files, batch JSON, delivery manifest, and optional PDF or ZIP outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and Node/npm plus either bun or npx; generated assets are written under project comic and .image-skills directories.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence, created 2026-03-21T11:42:05Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
