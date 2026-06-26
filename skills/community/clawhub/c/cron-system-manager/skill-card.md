## Description: <br>
Cron System Manager helps an agent check cron task status, adjust task configuration, detect duplicate responsibilities, and optimize scheduled task assignments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review and manage an agent workspace's scheduled tasks, including cron status checks, task responsibility boundaries, Feishu notification rules, retries, and issue-record cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to change task behavior, timeouts, prompts, ownership, and issue records. <br>
Mitigation: Require user confirmation before changing schedules, timeouts, prompts, task ownership, or deleting issue records. <br>
Risk: Automatic retries and cleanup can hide operational failures or remove context needed for later review. <br>
Mitigation: Keep persistent logs or history files for retries, repairs, and issue cleanup so operators can audit what changed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/cron-system-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with operational checklists and command or configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference workspace paths, cron task IDs, notification rules, and issue records from the user's environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
