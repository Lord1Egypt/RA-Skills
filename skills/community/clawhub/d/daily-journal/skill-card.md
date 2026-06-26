## Description: <br>
Daily Journal helps users write, review, search, summarize, and export personal journal entries stored locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to keep a local daily journal, log moods and gratitude, search past entries, view statistics, and export entries for backup or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal entries, mood logs, gratitude logs, search results, statistics, and exports may contain personal information. <br>
Mitigation: Use only in a trusted local environment, review terminal output before sharing agent sessions, and protect or relocate the journal directory when handling sensitive content. <br>
Risk: The skill stores personal journal data under ~/.journal by default. <br>
Mitigation: Set JOURNAL_DIR to a controlled location when a different storage path, backup policy, or retention boundary is needed. <br>


## Reference(s): <br>
- [Daily Journal ClawHub page](https://clawhub.ai/ckchzh/daily-journal) <br>
- [Daily Journal tips](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Terminal text, Markdown entries, and optional Markdown, JSON, or HTML export output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes journal, mood, and gratitude files under ~/.journal by default, unless JOURNAL_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
