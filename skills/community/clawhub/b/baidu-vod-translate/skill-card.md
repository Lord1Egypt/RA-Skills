## Description:

百度智能云VOD视频翻译 helps an agent guide users through Baidu Cloud VOD subtitle translation, voice dubbing, subtitle styling, batch video handling, result downloads, and optional Baidu Netdisk transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhx121619](https://clawhub.ai/user/lhx121619)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate video subtitles or speech with Baidu Cloud VOD, including user-supplied SRT subtitles, custom subtitle styling, batch processing, project and task lookup, and result export to local storage or Baidu Netdisk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video media may be uploaded to Baidu Cloud VOD and, when enabled, Baidu Netdisk.

Mitigation: Use the skill only with media that may be sent to those services, and confirm whether netdisk upload or download is enabled before running commands.

Risk: The workflow requires Baidu cloud access credentials.

Mitigation: Use least-privileged Baidu credentials in environment variables and do not paste AK/SK values into chat transcripts or files.

Risk: Baidu Cloud VOD video translation is a paid service and batch jobs can multiply processing charges.

Mitigation: Review the official pricing documentation and confirm the video list, translation mode, and wait behavior before creating tasks.

Risk: The scripts support project deletion and task update operations.

Mitigation: Confirm project and task identifiers before delete-project or update-task commands, and avoid granting credentials broader authority than needed.

Risk: Security evidence reports weak disclosure and URL scoping concerns.

Mitigation: Review the skill before installation and verify network destinations and command effects before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lhx121619/skills/baidu-vod-translate)
- [Baidu Cloud VOD pricing documentation](https://cloud.baidu.com/doc/VOD/s/Zmheig5gv)
- [Baidu Cloud VOD product page](https://cloud.baidu.com/product/vod.html)
- [Baidu Cloud VOD project management API](https://cloud.baidu.com/doc/VOD/s/Dmh0j7ldd)
- [Baidu Cloud VOD task management API](https://cloud.baidu.com/doc/VOD/s/ymh0j93u8)
- [Baidu Cloud IAM access key management](https://console.bce.baidu.com/iam/#/iam/accesslist)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local translated video files and remote Baidu Cloud VOD or Baidu Netdisk tasks; requires python3, Baidu VOD credentials, and optional bdpan for netdisk workflows.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
