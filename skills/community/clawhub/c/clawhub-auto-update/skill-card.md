## Description: <br>
Checks installed ClawHub skills for updates and runs bulk updates, with guidance for manual or scheduled operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmieting](https://clawhub.ai/user/jimmieting) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ClawHub users use this skill to keep locally installed ClawHub skills up to date through manual checks or scheduled update jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended bulk updates can overwrite local modifications or introduce changed skill behavior. <br>
Mitigation: Review before installing, run the updater manually first, keep backups of locally modified skills, and only add the cron job when unattended all-skill updates are acceptable. <br>


## Reference(s): <br>
- [ClawHub Auto Update release page](https://clawhub.ai/jimmieting/clawhub-auto-update) <br>
- [jimmieting ClawHub profile](https://clawhub.ai/user/jimmieting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs npx clawhub update --all and appends update logs under ~/.openclaw/logs when the script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
