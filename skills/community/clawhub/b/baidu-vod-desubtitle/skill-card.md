## Description:

Guides an agent through Baidu Intelligent Cloud VOD subtitle erasure for local or netdisk videos, including global, dialog-only, and custom-region modes, batch processing, task management, and result download or netdisk upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhx121619](https://clawhub.ai/user/lhx121619)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow operators use this skill to prepare commands and configuration for Baidu VOD subtitle erasure, including single-video, batch-folder, netdisk, task query, and task deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos are uploaded to Baidu Cloud VOD as part of the subtitle-erasure workflow.

Mitigation: Process only videos you are authorized to send to Baidu Cloud VOD, and avoid private or sensitive videos unless Baidu's service terms and retention practices are acceptable.

Risk: The workflow uses Baidu VOD AK/SK credentials and may use an existing bdpan session for netdisk transfers.

Mitigation: Keep credentials in environment variables, limit credential scope where possible, and use the netdisk features only from an intended logged-in bdpan session.

Risk: Task deletion commands can remove Baidu VOD subtitle-erasure task records.

Mitigation: Review task IDs and deletion requests carefully before executing deletion commands.

Risk: Processed outputs may overwrite or be confused with originals in downstream workflows.

Mitigation: Keep original videos separate from generated outputs and review output paths before upload or download steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lhx121619/skills/baidu-vod-desubtitle)
- [Baidu VOD product page](https://cloud.baidu.com/product/vod.html)
- [Baidu VOD subtitle erasure API documentation](https://cloud.baidu.com/doc/VOD/s/fmhiy9vqk)
- [Baidu VOD subtitle erasure pricing documentation](https://cloud.baidu.com/doc/VOD/s/Zmheig5gv)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce command lines for Python scripts that call Baidu VOD APIs and optionally interact with bdpan.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
