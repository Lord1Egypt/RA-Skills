## Description: <br>
Log books, track reading habits, and review reading streaks over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Bookworm to record reading logs, plans, progress, reviews, habits, reminders, priorities, and weekly reflections from the command line. It also supports local search, summary statistics, and exports for personal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bookworm stores user-entered notes and exports in plain text on the local filesystem. <br>
Mitigation: Do not record secrets or highly sensitive personal or work information, verify the local command or alias before use, and periodically delete the data directory or old exports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Bookworm release](https://clawhub.ai/ckchzh/bookworm) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries and generated exports as local plain-text files under ~/.local/share/bookworm/.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
