## Description: <br>
DreamAct animates faces in input images with expressions, lip movements, and head poses from a driving video using the DreamAct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure DreamAct API access, submit driving videos and face image URLs, and poll for generated face-animation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided face images and driving videos are sent to DreamAct/NewportAI for processing. <br>
Mitigation: Use only media you have rights and consent to process, and review the provider's privacy and retention terms before submitting sensitive or regulated content. <br>
Risk: The skill requires a DreamAct/NewportAI API key. <br>
Mitigation: Store DREAMACT_API_KEY in agent configuration or a secret store, and avoid sharing it in prompts, logs, or checked-in files. <br>


## Reference(s): <br>
- [DreamAct Skill Page](https://clawhub.ai/Hy-1990/dreamact) <br>
- [DreamAct API Reference](https://api.newportai.com/api-reference/dreamact) <br>
- [NewportAI API Get Started](https://api.newportai.com/api-reference/get-started) <br>
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and API endpoint snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMACT_API_KEY; works with driving video URLs and face image URL arrays; local files must be uploaded to OSS before submission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
