## Description: <br>
Safely clean OpenClaw old session files and rebuild sessions.json for Ubuntu ARM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccc-3po](https://clawhub.ai/user/ccc-3po) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw on Ubuntu ARM use this skill to remove old session history and rebuild the sessions.json index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup permanently deletes OpenClaw .jsonl session files older than three days without a preview. <br>
Mitigation: Confirm the target path and retention window are acceptable before execution, and back up sessions that must be retained. <br>
Risk: The automation assumes the hardcoded Ubuntu path and an available openclaw CLI. <br>
Mitigation: Verify /home/ubuntu/.openclaw/agents/main/sessions/ exists for the intended agent and that openclaw session rebuild works before deleting files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccc-3po/ccc3po-session-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports session file counts and sessions.json size before and after cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata; artifact frontmatter says 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
