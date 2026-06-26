## Description: <br>
Daily Diary helps an agent review a user's daily conversation history, extract key events, decisions, and insights, and draft a structured Chinese diary entry for the user to review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyu925065781](https://clawhub.ai/user/luyu925065781) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who want a private daily journal use this skill to turn daily agent conversations into a structured diary draft. It is also useful for end-of-day work review, light reflection, and scheduled diary reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews daily conversation history and may surface private or sensitive details in a diary draft. <br>
Mitigation: Use it only where the conversation owner expects diary generation, keep the built-in sensitive-data filtering active, and review drafts before saving or sharing them. <br>
Risk: Scheduled delivery can send diary drafts to a configured chat or notification channel. <br>
Mitigation: Choose a private destination, verify the channel before enabling the cron example, and avoid broadcasting drafts to shared spaces. <br>
Risk: Archived diary files may contain personal reflections or work context. <br>
Mitigation: Store diary files in a private local directory and omit credentials, tokens, infrastructure details, and other sensitive identifiers from final entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyu925065781/daily-diary-zh) <br>
- [Diary prompt library](references/quick-prompts.md) <br>
- [Diary template](assets/diary-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown diary draft with optional JSON cron configuration example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are intended for user review before archival and may be saved under ~/diary/YYYY/MM/YYYY-MM-DD.md after confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
