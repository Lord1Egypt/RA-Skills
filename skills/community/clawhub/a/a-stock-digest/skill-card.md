## Description: <br>
Provides A-share stock signal scoring and hotspot theme identification for pre-market briefs, intraday alerts, and post-market reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudgg82-blip](https://clawhub.ai/user/cloudgg82-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents monitoring China's A-share market use this skill to score market events, identify active themes, and prepare concise brief or alert outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to run a local Python helper. <br>
Mitigation: Inspect the referenced helper script on the local machine before allowing execution. <br>
Risk: Cron or alert workflows can produce automatic market reports. <br>
Mitigation: Enable scheduled workflows only when automatic A-share market reports are expected. <br>
Risk: The skill reads or writes report files under ~/a-digest. <br>
Mitigation: Review the local output directory and file permissions before deployment. <br>


## Reference(s): <br>
- [A Stock Digest release page](https://clawhub.ai/cloudgg82-blip/a-stock-digest) <br>
- [Publisher profile](https://clawhub.ai/user/cloudgg82-blip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefs and alerts with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to run a local Python helper, enable cron workflows, and read or write report files under ~/a-digest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-04-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
