## Description: <br>
Chanjing Video Compose helps agents use Chanjing video synthesis APIs to list digital-human figures, upload media, create text- or audio-driven videos, poll tasks, and download results when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamzn1018](https://clawhub.ai/user/iamzn1018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Chanjing digital-human videos from text or uploaded audio, select suitable public or customized figures, poll generation status, and optionally save completed media locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Chanjing app credentials and access tokens in ~/.chanjing/credentials.json or a CHANJING_CONFIG_DIR override. <br>
Mitigation: Keep the credentials file private, do not commit it to version control, and avoid sharing full secrets in prompts or logs. <br>
Risk: The skill uploads user-selected media and downloads URLs returned by the Chanjing API. <br>
Mitigation: Confirm upload file paths, download URLs, and output paths before running commands, and use the default API base unless you control the replacement. <br>
Risk: The optional create_task.py --callback argument can cause Chanjing to post task result payloads to a user-supplied endpoint. <br>
Mitigation: Use callback URLs only when the endpoint is trusted and intended to receive task result data. <br>


## Reference(s): <br>
- [Chanjing documentation](https://doc.chanjing.cc) <br>
- [Chanjing API base](https://open-api.chanjing.cc) <br>
- [ClawHub skill page](https://clawhub.ai/iamzn1018/chanjing-video-compose) <br>
- [Reference](artifact/reference.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return text identifiers, URLs, JSON when requested, and local file paths for explicit downloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce video task IDs, uploaded file IDs, video URLs, and downloaded media paths under outputs/video-compose/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
