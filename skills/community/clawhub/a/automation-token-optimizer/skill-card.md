## Description: <br>
Audits WorkBuddy scheduled automations for token usage and recommends task merges, deletions, frequency changes, and prompt or script optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to review scheduled automation cost and maintenance posture, then decide which tasks to merge, delete, reduce in frequency, or optimize. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews WorkBuddy task history and token usage. <br>
Mitigation: Install and run it only in environments where the agent is allowed to inspect scheduled automation history and usage data. <br>
Risk: The skill may propose merging, deleting, or reducing scheduled tasks. <br>
Mitigation: Require explicit human review, backup, and confirmation before any task is deleted, merged, or materially changed. <br>
Risk: Security evidence flags under-scoped deletion instructions and unrelated promotional footer links. <br>
Mitigation: Treat promotional links as unrelated third-party marketing and review generated action plans before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guipi888/skills/automation-token-optimizer) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, checklist items, and optional shell or Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, token-usage summaries, merge candidates, deletion candidates, frequency recommendations, and optimization guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
