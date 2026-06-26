## Description: <br>
Character consistency across AI-generated images with reference sheets and LoRA techniques. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, artists, and developers use this skill to plan consistent AI-generated character reference sheets for games, comics, illustration, animation, and visual novels. It provides prompt patterns, reference-sheet structures, LoRA guidance, and inference.sh CLI examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a remote CLI installer one-liner. <br>
Mitigation: Prefer manual installation and checksum verification before running the CLI, and log in to inference.sh only when intending to use that service. <br>
Risk: Generated character images may drift in identity, colors, outfit details, or proportions across prompts. <br>
Mitigation: Reuse a detailed description anchor, document color values, specify proportions, and use LoRA or seed-based methods for higher consistency. <br>


## Reference(s): <br>
- [Character Design Sheet on ClawHub](https://clawhub.ai/okaris/character-design-sheet) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example JSON inputs for inference.sh app runs and character-reference planning tables.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
