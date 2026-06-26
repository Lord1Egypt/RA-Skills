## Description: <br>
Embeds and controls a virtual avatar using the avatar-runtime npm package, with Live2D rendering, VRM 3D, vector fallback, and control-driven expression, body, and scene animation through a provider-agnostic session bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeilJo-GY](https://clawhub.ai/user/NeilJo-GY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add and control avatar sessions, browser widgets, Live2D or VRM renderers, and provider-backed avatar interactions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the avatar-runtime npm package through npx, which may download and execute remote npm code. <br>
Mitigation: Review the referenced package and setup scripts, prefer a pinned and audited package version for production, and test in a sandbox before deployment. <br>
Risk: Optional providers use API keys and external services for avatar rendering or image generation. <br>
Mitigation: Use scoped test credentials during evaluation, keep production credentials out of shared environments, and avoid logging provider API keys. <br>
Risk: Sample avatar assets and setup scripts may introduce third-party asset licensing or redistribution constraints. <br>
Mitigation: Inspect asset download scripts before use and deploy only avatar models and Live2D or VRM assets that are licensed for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Avatar Runtime listing](https://clawhub.ai/NeilJo-GY/avatar-runtime) <br>
- [Web Embedding Reference](references/WEB-EMBEDDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, JavaScript, and HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local runtime URLs, environment variable names, curl requests, and browser embedding snippets.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
