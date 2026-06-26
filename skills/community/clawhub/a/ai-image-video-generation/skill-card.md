## Description: <br>
Generates images and videos through the VibeVideo API, checks generation status, lists available models, and estimates credit costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytevirts](https://clawhub.ai/user/bytevirts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create, monitor, estimate, or cancel VibeVideo image and video generation tasks using their own VIBEVIDEO_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation parameters, and supplied image URLs are sent to VibeVideo. <br>
Mitigation: Submit only media and prompts intended for that provider, and avoid private or internal media URLs unless sharing them is acceptable. <br>
Risk: Generation requests can spend paid VibeVideo credits. <br>
Mitigation: Use the cost endpoint before generating when cost matters, and monitor credit usage. <br>
Risk: The skill depends on a sensitive VIBEVIDEO_API_KEY. <br>
Mitigation: Keep the API key in an environment variable, do not paste it into prompts or logs, and rotate it if exposed. <br>


## Reference(s): <br>
- [VibeVideo](https://vibevideo.app) <br>
- [ClawHub skill page](https://clawhub.ai/bytevirts/ai-image-video-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON response examples, and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIBEVIDEO_API_KEY; generation tasks are asynchronous and can spend VibeVideo credits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
