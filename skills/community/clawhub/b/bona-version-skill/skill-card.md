## Description: <br>
Bona Movie Production is Bona Group's film-grade production skill for image generation, image editing, and video generation using Nano Banana 2, Nano Banana Pro, Seedance, and Kling v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzipidaily](https://clawhub.ai/user/chengzipidaily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to guide and run Bona remote image and video generation workflows, including text-to-image, image editing, reference-based image generation, text-to-video, image-to-video, and media-reference video creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and task metadata are sent to Bona's remote generation service. <br>
Mitigation: Use the skill only when remote generation is intended, and avoid submitting confidential prompts or private media URLs unless sharing them with the service is allowed. <br>
Risk: The client requires an API key or access token for the remote service. <br>
Mitigation: Use a scoped API key, keep it in environment variables, and do not paste credentials into prompts or shared logs. <br>
Risk: Custom service endpoints could send requests or credentials to an unintended host. <br>
Mitigation: Keep the default service endpoints unless the replacement endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chengzipidaily/bona-version-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote image and video task creation and query results are returned by the Bona service.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact metadata.version is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
