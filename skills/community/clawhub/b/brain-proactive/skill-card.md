## Description: <br>
Proactive Obsidian vault maintenance and review that finds stale tasks, orphan notes, projects needing attention, and connection opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabebac](https://clawhub.ai/user/gabebac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian vault users use this skill to review personal knowledge-base maintenance issues, including overdue tasks, pending staged files, open project follow-ups, orphan notes, and connection opportunities. It reports findings and suggestions while requiring approval before any vault changes are made through a separate push workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects sensitive local Obsidian vault areas, including health and therapy-related metadata. <br>
Mitigation: Install only for vaults where this inspection is expected, and keep therapy-note reporting limited to metadata rather than note contents. <br>
Risk: Note enrichment can cause private note topics or search terms to leave the vault through web search. <br>
Mitigation: Avoid enrichment on private notes unless approved, and review staged drafts before applying them. <br>
Risk: Approved writes depend on a separate vault-push workflow. <br>
Mitigation: Inspect and approve the separate vault-push skill before allowing staged changes to be written back to HumanVault. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Telegram-style Markdown bullet report with optional inline shell commands and wikilink suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caps review reports at 10 items and summarizes remaining findings] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
