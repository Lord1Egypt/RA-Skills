## Description: <br>
Codex Imggen helps agents generate single, sized, or batch image assets through the Codex CLI, with optional reference images and saved PNG outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and asset creators use this skill to create game UI artwork, icons, and other image assets with Codex CLI commands. It is most useful when an agent needs prompt-driven image generation, size guidance, batch asset generation, or optional reference-image input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Codex Imggen on ClawHub](https://clawhub.ai/axelhu/codex-imggen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated PNG files are copied to the requested output directory or stored under ~/.codex/generated_images/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the codex binary. The skill uses Codex CLI image generation with default local proxy settings, a recommended timeout of at least 180 seconds, and documented image size limits; users should visually inspect generated images before relying on them.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
