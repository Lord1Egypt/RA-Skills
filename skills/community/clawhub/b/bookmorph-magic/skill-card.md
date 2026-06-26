## Description: <br>
Orchestrate book-to-content workflows that generate video, audio, cover images, and a manifest for episode or campaign packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OiiOAI](https://clawhub.ai/user/OiiOAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflow builders use this skill to connect book selection, longform media generation, and cover generation adapters, then bundle the outputs into an episode or campaign package with an auditable manifest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preparing a destination with clear-existing can delete existing files in the selected episode directory if the output root or prefix is wrong. <br>
Mitigation: Run in a dedicated workspace or throwaway output directory, verify the exact destination path, and avoid clear-existing unless the target is confirmed. <br>
Risk: Generated manifests can include local source, prompt, checkpoint, and output paths that may reveal sensitive filesystem details. <br>
Mitigation: Review manifests before sharing them and remove or avoid sensitive local paths when distributing generated packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OiiOAI/bookmorph-magic) <br>
- [Adapter contracts](references/integration-template.md) <br>
- [Manifest schema](references/manifest-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON manifest output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When adapters are supplied, the helper script packages video, audio, three cover images, and manifest.json into a configurable episode directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
