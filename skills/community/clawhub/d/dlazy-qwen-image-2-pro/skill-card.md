## Description: <br>
Alibaba Bailian qwen-image-2.0-pro general image generation for complex text rendering, multi-line layouts, photorealistic detail, semantic adherence, and mixed text/image designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images through the dLazy CLI with Alibaba Bailian qwen-image-2.0-pro, including designs that need detailed prompt following and mixed text rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which may be saved in local CLI configuration. <br>
Mitigation: Use per-invocation DLAZY_API_KEY when a saved credential is not desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and selected local files are sent to dLazy services for inference and media handling. <br>
Mitigation: Avoid submitting sensitive prompts or files unless the user intends them to be processed by dLazy. <br>
Risk: The skill depends on the external @dlazy/cli package and dLazy hosted service. <br>
Mitigation: Install only when the user trusts the external package and service; use the pinned package version declared by the skill. <br>


## Reference(s): <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON responses containing generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs are hosted image URLs; asynchronous calls may return a generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
