## Description: <br>
Auto Improve helps an agent scan learnings, errors, and memory for recurring patterns, then update skills and operating protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use Auto Improve to help an agent identify repeated mistakes, stale guidance, and useful prior wins, then maintain its own playbook, skills, memory, and reminder files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to change its own memory and operating instructions, which can introduce incorrect, stale, or unsafe guidance. <br>
Mitigation: Run it in a controlled maintenance workflow, keep it proposal-only by default, and review diffs before accepting changes. <br>
Risk: Automatic writes to skills, memory, AGENTS.md, and related files can affect future agent behavior beyond the current session. <br>
Mitigation: Restrict writable targets to a small allowlist, keep backups or version control available, and maintain a clear rollback path. <br>


## Reference(s): <br>
- [Auto Improve on ClawHub](https://clawhub.ai/dodge1218/dsb-auto-improve) <br>
- [Publisher profile: dodge1218](https://clawhub.ai/user/dodge1218) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and proposed or applied file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce direct edits or proposals depending on assessed risk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
