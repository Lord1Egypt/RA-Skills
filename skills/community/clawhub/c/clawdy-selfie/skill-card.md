## Description: <br>
Generate a Clawdy selfie with the installed local helper script and the configured FAL_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users and agent operators use this skill to generate reference-based Clawdy images or videos and send the generated media to a target OpenClaw channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, generated media, captions, and channel names may be sent to external services and OpenClaw destinations. <br>
Mitigation: Use only when that data sharing is acceptable, review requests before running, and confirm target channels before media is posted. <br>
Risk: The security summary reports public uploads and channel posting beyond the short skill description. <br>
Mitigation: Prefer a revised release that documents every remote service, avoids public temporary file hosts, and asks before posting media. <br>
Risk: The security summary reports an unsafe command execution path. <br>
Mitigation: Avoid untrusted channel names or captions and revise command execution to avoid shell interpolation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawdy-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>
- [fal.ai Grok Imagine image edit endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>
- [fal.ai Grok Imagine image endpoint](https://fal.run/xai/grok-imagine-image) <br>
- [Seedance API base URL](https://api.outai.top/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, files] <br>
**Output Format:** [Shell command execution with JSON status output and generated image or video media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured service credentials and a target OpenClaw channel; generated media may be downloaded to temporary files before posting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
