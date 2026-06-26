## Description: <br>
Generates a Codex-compatible custom pet from a source image by using RunComfy GPT Image 2 for a canonical pose and ImageMagick to assemble pet.json and spritesheet.webp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to create and install custom Codex Pets without Codex Pro or the internal imagegen skill, using a RunComfy token, the RunComfy CLI, and ImageMagick. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RunComfy token and may store credentials through the RunComfy CLI. <br>
Mitigation: Install only when comfortable with RunComfy credential handling; prefer RUNCOMFY_TOKEN in CI and protect local RunComfy configuration files. <br>
Risk: Source image URLs are processed by RunComfy's remote service. <br>
Mitigation: Use non-sensitive, shareable image URLs and avoid private or confidential source images. <br>
Risk: The install step writes generated files into the Codex pets directory. <br>
Mitigation: Review the generated pet name and destination path before running copy commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/codex-pet) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet) <br>
- [RunComfy GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=codex-pet) <br>
- [OpenAI hatch-pet skill reference](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Codex Pet manifest and WebP spritesheet for installation under the user's Codex pets directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
