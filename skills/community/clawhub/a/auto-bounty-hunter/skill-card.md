## Description: <br>
Automatically scan GitHub repositories for open issues with 0 comments, evaluate their value, claim them, and submit PRs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers can use this skill to find low-comment GitHub issues, queue candidate work, and track pull request outcomes. It is intended for users who deliberately want GitHub issue automation under their own account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes unattended GitHub issue automation under the user's account without enough approval or repository scoping. <br>
Mitigation: Run only after setting DRY_RUN=true and AUTO_CLAIM/AUTO_SUBMIT=false, review queued issues manually, and limit use to repositories where the user has permission and understands contribution rules. <br>
Risk: Cron-based operation can repeatedly scan and queue public GitHub issues before the user has reviewed behavior. <br>
Mitigation: Avoid scheduled execution until the user has tested the scripts in dry-run mode and confirmed the configured repository, language, and organization filters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/auto-bounty-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local JSON queue/history files and a log file when the shell scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
