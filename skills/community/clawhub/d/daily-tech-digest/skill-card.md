## Description: <br>
Generates a daily technology news digest by collecting AI, digital product, and technology headlines, organizing them in Obsidian, and pushing a short summary to a phone negative-screen card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajawpwinner-del](https://clawhub.ai/user/ajawpwinner-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate a daily Chinese-language technology news workflow: gather recent items, summarize and categorize them, save Obsidian notes, and send a mobile-friendly digest notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically modifies an Obsidian vault and can overwrite or delete generated digest files during organization. <br>
Mitigation: Run it first on a copy of the vault, update the vault path intentionally, and confirm the overwrite/delete behavior before scheduling it. <br>
Risk: The skill can run broad Git synchronization that stages and pushes the whole vault, which may include unrelated private notes. <br>
Mitigation: Disable Git sync or narrow it to the intended files, and review repository status before allowing automatic commits and pushes. <br>
Risk: The workflow depends on companion skills for news collection and mobile push delivery. <br>
Mitigation: Confirm that daily-tech-broadcast and today-task are trusted and working before enabling cron jobs or notifications. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ajawpwinner-del/daily-tech-digest) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown notes and mobile-card text, with JSON execution status and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes files in an Obsidian vault and may run Git synchronization and device push commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact changelog also lists v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
