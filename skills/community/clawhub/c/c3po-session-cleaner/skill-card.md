## Description: <br>
Clean up old OpenClaw session files and keep only active sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccc-3po](https://clawhub.ai/user/ccc-3po) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to remove local .jsonl session files older than three days from the main-agent sessions directory and report how many session files remain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete local OpenClaw session .jsonl files through a broad trigger and without confirmation. <br>
Mitigation: Review the command before use; add a dry-run or confirmation step and make the trigger more specific before installing it in shared or sensitive environments. <br>
Risk: The cleanup command targets a hardcoded main-agent sessions directory and may remove session history that users intended to keep. <br>
Mitigation: Confirm the target path and back up any needed session logs before running the cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccc-3po/c3po-session-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Markdown with a bash code block and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deletes matching .jsonl files older than three days from the configured OpenClaw sessions directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
