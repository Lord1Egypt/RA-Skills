## Description: <br>
Remove obvious AI-writing traces from Chinese text in a constrained way without changing facts, data, or the article's core argument. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and content agents use this skill to clean up Chinese Markdown or plain-text drafts that sound mechanically AI-generated while preserving facts, numbers, headings, structure, and core claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill rewrites local draft content and writes revised output. <br>
Mitigation: Run it only on drafts you are comfortable processing and review the humanized Markdown before publishing. <br>
Risk: The package depends on skill_runtime.writing_core but does not include requirements.txt. <br>
Mitigation: Confirm the target environment provides skill_runtime.writing_core before installation or execution. <br>
Risk: A humanization pass may unintentionally shift tone or emphasis even when facts are preserved. <br>
Mitigation: Compare the JSON report and revised draft against the source to confirm facts, structure, headings, and core claims remain intact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/content-system-humanizer-zh) <br>
- [Publisher profile](https://clawhub.ai/user/abigale-cyber) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, guidance] <br>
**Output Format:** [Humanized Markdown file plus JSON change report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a revised draft and a report with changed line count, AI-trace risk, pattern hits, and change details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
