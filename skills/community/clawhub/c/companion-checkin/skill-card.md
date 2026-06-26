## Description: <br>
Runs warm, adaptive personal check-ins for habits, mood, sleep, meals, focus, daily progress, and recap summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqizzo](https://clawhub.ai/user/sqizzo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run companion-style daily wellness check-ins, log answers, and generate short recaps that surface patterns across mood, sleep, meals, energy, focus, and daily progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private wellness check-in answers are saved locally in data/checkins.jsonl. <br>
Mitigation: Install only if local retention is acceptable; review folder access, backups, and delete or protect the file when long-term retention is not desired. <br>


## Reference(s): <br>
- [Companion Check-In Data Schema](references/data-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local check-in entries to data/checkins.jsonl.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
