## Description: <br>
Generates Unreal Engine blueprint and material node graphs from natural language or uploaded screenshots, with a unified tabbed app for switching between blueprint and material modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical artists use this skill to create, inspect, and refine Unreal Engine blueprint or material node structures from natural-language prompts, screenshots, or imported JSON. It is most relevant when prototyping UE visual scripting flows, material graphs, or node-level explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MiniMax API key and consumes MiniMax token plan quota. <br>
Mitigation: Use a dedicated MiniMax API key, monitor usage, and rotate or revoke the key if it is exposed. <br>
Risk: Uploaded screenshots may contain credentials, personal data, private project assets, or confidential game content. <br>
Mitigation: Avoid uploading sensitive screenshots unless the external MiniMax-backed deployment and data handling are trusted. <br>
Risk: Generated Unreal Engine JSON or node structures may be invalid or unsuitable for a project. <br>
Mitigation: Review generated node graphs and test imports in a safe project before using them in production content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tianheihei002/blueprint-generator) <br>
- [Deployed MiniMax-backed app](https://ncvbhgghna86.space.minimaxi.com) <br>
- [MiniMax API gateway](https://api.minimaxi.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, configuration snippets, and Unreal Engine node-graph JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference MiniMax model configuration and generated UE blueprint/material node metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog state 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
