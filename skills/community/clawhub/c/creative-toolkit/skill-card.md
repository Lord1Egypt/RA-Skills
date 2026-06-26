## Description: <br>
This skill helps agents generate and manage AI images and videos through multi-provider routing, prompt enhancement, curated prompt search, and local ComfyUI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jau123](https://clawhub.ai/user/jau123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative teams use this skill to route image and video generation requests across configured providers, enhance prompts, search curated examples, and manage local ComfyUI workflows. It is intended for AI image and video creation workflows, not generic chat, code generation, document writing, video editing, or audio generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a pinned third-party npm package and depends on user-configured image or video providers. <br>
Mitigation: Install only after reviewing the pinned package and configure API credentials only for providers the user trusts. <br>
Risk: Reference images may be sent to the selected external provider during generation. <br>
Mitigation: Use local ComfyUI for workflows that should keep reference images local, or avoid sending sensitive reference images to external providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jau123/skills/creative-toolkit) <br>
- [Project homepage](https://github.com/jau123/MeiGen-AI-Design-MCP) <br>
- [Provider configuration](references/providers.md) <br>
- [Troubleshooting and security notes](references/troubleshooting.md) <br>
- [MeiGen model comparison](https://www.meigen.ai/model-comparison) <br>
- [meigen npm package](https://www.npmjs.com/package/meigen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, shell commands, JSON configuration snippets, and returned URLs or file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated media URLs and local save paths returned by configured providers; the skill does not inspect generated images.] <br>

## Skill Version(s): <br>
1.0.36 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
