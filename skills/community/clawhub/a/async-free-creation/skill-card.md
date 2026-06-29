## Description: <br>
Calls the Flyelep Image-2 async free-creation API to generate product or creative images from prompts and optional public reference image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Flyelep image-generation tasks from a prompt, optional reference image URLs, image count, and aspect ratio, then poll the task API and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, public reference image URLs, and the Flyelep API key are sent to a third-party service. <br>
Mitigation: Use the skill only when that disclosure is acceptable, provide the API key at runtime, and avoid storing the key in files or shared logs. <br>
Risk: The artifact instructs agents to poll an asynchronous API and handle task failures. <br>
Mitigation: Check task status before presenting results, show only successful executeResult URLs, and report failed task items clearly. <br>
Risk: Requests outside documented limits can fail, including more than 4 images, unsupported aspect ratios, inaccessible reference URLs, or prompts over 1000 characters. <br>
Mitigation: Validate image count, aspect ratio, prompt length, and public reference image accessibility before sending the request. <br>


## Reference(s): <br>
- [Flyelep async free-creation task endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync) <br>
- [Flyelep task result query endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult) <br>
- [Flyelep controlboard](https://www.flyelep.cn/controlboard) <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/async-free-creation) <br>
- [Publisher profile](https://clawhub.ai/user/flyelepai) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, curl examples, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous task flow returns a task ID first, then generated image URLs after polling; supports 1 to 4 images per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
