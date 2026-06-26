## Description: <br>
AI-powered Windows memory guardian that helps agents inspect memory usage, analyze high-risk processes, start background monitoring, launch a local web dashboard, and invoke storage cleanup flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on Windows use this skill to check memory pressure, review candidate processes before cleanup, run a memory monitor, and open a local dashboard for process and memory visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can terminate processes while acting as a Windows memory guardian. <br>
Mitigation: Use dry-run first, review the target processes, and require explicit confirmation before running cleanup or enabling background monitoring. <br>
Risk: Background monitoring can repeatedly act on processes without close user supervision. <br>
Mitigation: Use conservative thresholds, keep verbose logging enabled, and stop the monitor when active remediation is no longer needed. <br>
Risk: The skill includes storage cleanup behavior outside its primary memory-management purpose. <br>
Mitigation: Review or remove the storage-clean integration unless disk scanning and cleanup are explicitly intended. <br>


## Reference(s): <br>
- [Aioom ClawHub page](https://clawhub.ai/bettermen/aioom) <br>
- [Aioom project homepage](https://github.com/bettermen/aioom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, bash, and TOML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that inspect memory, start or stop local processes, open a local web interface, or call a storage cleanup helper.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
