## Description: <br>
Text-to-vector model that outputs SVG results. Suitable for logos, icons, and scalable design assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call dLazy's Recraft V4 Vector generation CLI for scalable design assets such as logos and icons from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in ~/.dlazy/config.json. <br>
Mitigation: Prefer a revocable API key or the DLAZY_API_KEY environment variable when avoiding long-lived local credentials. <br>
Risk: Prompts, parameters, and referenced local media files are sent to dLazy services for generation. <br>
Mitigation: Use the skill only with prompts and files that are appropriate to share with dLazy. <br>
Risk: The documented install target uses @latest for the dLazy CLI package. <br>
Mitigation: Review the dLazy CLI source or npm package before installation and pin a reviewed version where deployment policy requires it. <br>


## Reference(s): <br>
- [Dlazy Recraft V4 Vector on ClawHub](https://clawhub.ai/dlazyai/dlazy-recraft-v4-vector) <br>
- [dlazyai Publisher Profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [CLI command guidance and JSON result payloads with generated output URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; async calls may return a generateId and status for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
