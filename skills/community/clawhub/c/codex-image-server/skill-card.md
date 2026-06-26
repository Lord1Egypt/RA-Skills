## Description: <br>
Exposes local Codex image generation as a local HTTP API for apps such as Photoshop plugins, design tools, and internal image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catrefuse](https://clawhub.ai/user/catrefuse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or validate a local Codex-backed image generation HTTP server for trusted desktop apps, design tools, or internal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included server template exposes powerful local image-generation endpoints broadly. <br>
Mitigation: Review before installing or copying the template, use it only in trusted projects, bind it to 127.0.0.1, add authentication, and restrict CORS to trusted origins. <br>
Risk: Prompts or reference images can be sent to OpenAI automatically when the remote backend is selected by environment configuration. <br>
Mitigation: Choose the backend explicitly and remove OPENAI_API_KEY from the environment unless remote processing is intended. <br>
Risk: Serving generated files can expose absolute paths or unsafe image identifiers. <br>
Mitigation: Avoid returning absolute paths and sanitize image IDs before serving files. <br>


## Reference(s): <br>
- [HTTP Contract](references/http-contract.md) <br>
- [Codex Image Server ClawHub Page](https://clawhub.ai/catrefuse/codex-image-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, configuration details, and HTTP contract references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local server routes, request and response shapes, validation checks, and smoke-test commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
