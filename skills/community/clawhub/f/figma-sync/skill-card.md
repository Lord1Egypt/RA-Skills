## Description: <br>
Read Figma files, extract design tokens, generate React Native Expo TypeScript or Web React with Tailwind code, prepare patch specs for Figma, and diff local models against Figma. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kristinadarroch](https://clawhub.ai/user/kristinadarroch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and design engineers use this skill to turn Figma file data into local design models, tokens, generated UI code, and reviewable patch specs for syncing design changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Figma token may grant access to private files reachable by that token. <br>
Mitigation: Use a token with the narrowest practical access and run the skill only against files the user intends to process. <br>
Risk: Generated design models, cache files, exported images, and plugin specs may contain private design data. <br>
Mitigation: Store outputs in approved locations, avoid committing sensitive artifacts, and remove generated cache or output files when no longer needed. <br>
Risk: Patch specs can affect Figma content when loaded into a companion Figma plugin. <br>
Mitigation: Review preview output and patch specs before execution, and keep dry-run behavior until changes are approved. <br>


## Reference(s): <br>
- [API Guide](references/api-guide.md) <br>
- [DesignSpec Schema](references/design-spec-schema.json) <br>
- [Figma API access tokens](https://www.figma.com/developers/api#access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands, plus JSON design models, token files, code plans, generated component files, patch specs, and preview reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local output files and a .figma-cache directory; write-back specs are dry-run by default and node mutations require a companion Figma plugin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
