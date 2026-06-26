## Description: <br>
Aoju Memory provides long-term local memory, learning capture, recall, reporting, and self-evolution workflows for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaibaoqing](https://clawhub.ai/user/chaibaoqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to maintain local long-term memory for OpenClaw agents, recall relevant past context, record lessons from feedback, and generate advisory evolution reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive user, project, or personal data. <br>
Mitigation: Do not store secrets or sensitive personal data, and review MEMORY.md, memory/, SOUL.md, USER.md, and AGENTS.md regularly. <br>
Risk: Stored memory and advisory evolution reports can influence future agent behavior without clear retention, approval, or rollback controls. <br>
Mitigation: Keep evolution outputs advisory, review proposed behavioral changes before applying them, and maintain manual rollback options for memory and agent guidance files. <br>
Risk: Recall and report outputs may expose stored memory content. <br>
Mitigation: Run recall and report commands only in trusted contexts, and review generated reports before sharing them. <br>
Risk: Running the evolution workflow without dry-run can archive old learning entries. <br>
Mitigation: Run mem_evolve.py with --dry-run first and back up memory/learnings before applying archive operations. <br>


## Reference(s): <br>
- [Aoju Memory ClawHub listing](https://clawhub.ai/chaibaoqing/aoju-memory) <br>
- [Publisher profile](https://clawhub.ai/user/chaibaoqing) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, plain text or JSON script output, and optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local memory files under ~/.openclaw/workspace, including MEMORY.md, daily logs, learnings, and patterns.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
