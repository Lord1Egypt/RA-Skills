## Description: <br>
睡眠改善工具。睡眠分析、改善建议、作息规划、睡眠环境优化、小睡指南、睡眠日记。Sleep tracker with analysis, improvement tips, schedule planning, environment optimization, nap guide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and wellness-focused users can use this skill to record sleep or health entries, review recent history, calculate sleep duration and cycles, and get sleep-improvement suggestions. It is intended for local command-line tracking and guidance, not clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive sleep or health notes may be stored in local files, including an under-disclosed temporary journal file. <br>
Mitigation: Use only on a private machine, avoid entering sensitive medical or personal notes, set SLEEP_TRACKER_DIR to a private directory, and manually review or delete /tmp/sleep_journal.txt when using the journal feature. <br>
Risk: Reset or deletion behavior may be misleading and should not be relied on to erase records. <br>
Mitigation: Confirm stored files manually and delete records directly until reset behavior is fixed and verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/bytesagain-sleep-tracker) <br>
- [Publisher Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local CLI output may include logged sleep or health notes; users can redirect exported records to files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
