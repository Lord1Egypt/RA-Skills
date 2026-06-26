## Description: <br>
Daily Mood helps an agent generate bilingual, mood-aware morning, evening, and on-demand life messages for registered users based on their current emotional state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive warm, language-aware daily mood messages, register lightweight mood preferences, and manage scheduled morning or evening prompts. Agents can use it to produce immediate emotional-support messages or scheduled push-message content without calling an external API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores each registered user's mood label, language preference, push setting, and timestamps in local profile files. <br>
Mitigation: Register users only with explicit consent, explain what profile data is stored, and delete or disable profiles when users opt out. <br>
Risk: Scheduled morning and evening messages can create recurring notifications for registered users. <br>
Mitigation: Require user opt-in before adding cron jobs or enabling push delivery, and provide a clear path to turn push messages off. <br>
Risk: Broad trigger keywords may activate the skill in environments with many installed skills. <br>
Mitigation: Review and narrow trigger keywords for the deployment context if accidental activation would be disruptive. <br>
Risk: Mood-aware messages may be mistaken for therapeutic or diagnostic support. <br>
Mitigation: Keep messages non-diagnostic, avoid clinical claims, and route users to appropriate professional or emergency support when needed. <br>


## Reference(s): <br>
- [Daily Mood ClawHub release](https://clawhub.ai/cosmofang/daily-mood) <br>
- [cosmofang publisher profile](https://clawhub.ai/user/cosmofang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style prompts with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be in Chinese or English and may reflect stored user mood, language, and push preferences.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact package.json and _meta.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
