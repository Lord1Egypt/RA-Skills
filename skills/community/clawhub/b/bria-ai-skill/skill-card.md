## Description: <br>
Helps agents generate, edit, upscale, restyle, and remove backgrounds from images through Bria AI's hosted image APIs for product photography, visual assets, and batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to guide image generation, background removal, image editing, product lifestyle-shot creation, upscaling, and batch visual-asset workflows with Bria AI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, masks, or local image paths may be sent to Bria's hosted API for processing. <br>
Mitigation: Use the skill only where policy permits external API processing, and avoid sensitive or regulated images unless that use is approved. <br>
Risk: The Bria API key could be exposed if pasted into chat or committed into files. <br>
Mitigation: Store BRIA_API_KEY in an environment variable or secret manager and avoid including the secret in prompts, examples, or source files. <br>


## Reference(s): <br>
- [Bria AI homepage](https://bria.ai) <br>
- [ClawHub skill page](https://clawhub.ai/galbria/bria-ai-skill) <br>
- [Bria.ai API Reference](references/api-endpoints.md) <br>
- [Bria AI Workflows & Advanced Patterns](references/workflows.md) <br>
- [Python Client](references/code-examples/bria_client.py) <br>
- [TypeScript Client](references/code-examples/bria_client.ts) <br>
- [Bash/curl Reference](references/code-examples/bria_client.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and Python, TypeScript, and bash code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIA_API_KEY for API-backed image generation and editing workflows.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
