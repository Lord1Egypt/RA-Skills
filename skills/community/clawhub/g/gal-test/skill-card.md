## Description: <br>
Provides agent guidance for using Bria.ai image generation, image editing, background removal, product photography, upscaling, restyling, and related visual asset workflows through Bria API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levdavid1](https://clawhub.ai/user/levdavid1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images, remove or replace backgrounds, create product and marketing visuals, and prepare API calls for Bria.ai-powered image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles and persists reusable Bria credentials for image generation and editing workflows. <br>
Mitigation: Use a dedicated revocable Bria API key and review or remove ~/.bria/credentials when token reuse across sessions is not desired. <br>
Risk: Image prompts and source images may be sent to Bria for remote processing. <br>
Mitigation: Avoid private, regulated, or sensitive images unless the user accepts Bria's handling terms for that content. <br>
Risk: Broad activation guidance can cause many visual content requests to be routed through a remote image API. <br>
Mitigation: Confirm user intent and review the proposed API action before sending prompts, images, or credentials to Bria. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/levdavid1/gal-test) <br>
- [Bria homepage](https://bria.ai) <br>
- [Bria agent API docs](https://docs.bria.ai/llms.txt) <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_client.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Bria API result URLs or image asset URLs when the agent invokes the documented workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 1.2.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
