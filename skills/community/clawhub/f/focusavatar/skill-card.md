## Description: <br>
focusavatar is a CLI skill that uses accessKeyId/accessKeySecret credentials to submit digital-human video generation jobs from MP3, MP4, and text inputs, and to query job results by orderNo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lintqiu](https://clawhub.ai/user/lintqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to submit FocusAvatar digital-human video generation jobs and retrieve generated video links or job status from a command-line or agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send API credentials to an endpoint configured by FOCUSAVATAR_API. <br>
Mitigation: Keep FOCUSAVATAR_API unset unless the alternate endpoint is deliberately trusted, and use least-privilege or disposable credentials when available. <br>
Risk: The skill sends supplied media URLs and text to the FocusAvatar backend for processing. <br>
Mitigation: Submit only content that is appropriate for the service and that the user has rights to process. <br>
Risk: Broad invocations could submit generation jobs without enough user intent. <br>
Mitigation: Confirm the selected mode, media inputs, text, and destination service before running the submission flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lintqiu/focusavatar) <br>
- [FocusAvatar credential console](https://login.joycoreai.com/) <br>
- [FocusAvatar service endpoint](https://yunji.focus-jd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Interactive CLI prompts and text output with video URLs, order numbers, progress, or JSON-like status details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and FocusAvatar API credentials; video generation can take several minutes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
