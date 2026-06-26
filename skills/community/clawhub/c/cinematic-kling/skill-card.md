## Description: <br>
Generate 5-second cinematic AI videos using Kling via ComfyDeploy. Takes a character image, item image, and location image, then produces a character sheet, item sheet, and a short cinematic video showing them interacting. Use when creating short ads, film clips, music videos, or any scene where a character interacts with an item in a specific location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, filmmakers, and developers use this skill to generate short cinematic clips where a character interacts with a product or item in a chosen location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected character, item, and location images are uploaded to ComfyDeploy/S3 and processed by third-party services. <br>
Mitigation: Use only images you have permission to process, avoid private or biometric images, and review the provider's handling terms before use. <br>
Risk: The skill requires a ComfyDeploy API key and can create API usage or cost exposure. <br>
Mitigation: Use a dedicated API key where possible, keep it in environment configuration, and monitor usage and billing. <br>
Risk: Incorrectly assigning character, item, and location images can produce wrong or misleading outputs. <br>
Mitigation: Use image inspection to verify each file role before submitting a run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/cinematic-kling) <br>
- [Publisher profile](https://clawhub.ai/user/PauldeLavallaz) <br>
- [ComfyDeploy run queue API endpoint](https://api.comfydeploy.com/api/run/deployment/queue) <br>
- [ComfyDeploy file upload API endpoint](https://api.comfydeploy.com/api/file/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands and API request examples; generated run artifacts are image and video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful runs produce character sheet, item sheet, and location sheet images plus a fixed 5-second video.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
