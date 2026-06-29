## Description: <br>
Creates concise, age-appropriate, personalized daily campus morning briefs with local weather, verified current news, a bilingual quote, study guidance, reminders, and an action prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[my12121-beep](https://clawhub.ai/user/my12121-beep) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, educators, families, and agent builders use this skill to generate short, source-backed student morning briefs tailored by city, age group, language, interests, and reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student profiles or reminders could include unnecessary personal information. <br>
Mitigation: Use the minimum profile data needed, keep credentials and private schedules outside the skill directory, and avoid sensitive reminders. <br>
Risk: Weather or news content could be stale, incorrect, or insufficiently sourced. <br>
Mitigation: Fetch current information, preserve publisher names, dates, and direct URLs, and cross-check claims that affect safety. <br>
Risk: Generated news summaries could include age-inappropriate, sensational, or copied content. <br>
Mitigation: Apply the content guidelines, exclude unsuitable topics, use calm original wording, and separate reported facts from advice. <br>
Risk: Generated briefs could be sent, posted, printed, or reused without appropriate review. <br>
Mitigation: Review generated files and require explicit approval before delivery unless an existing scheduled automation authorizes it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/my12121-beep/skills/campus-morning-brief) <br>
- [Publisher Profile](https://clawhub.ai/user/my12121-beep) <br>
- [Brief Payload Schema](references/brief.schema.json) <br>
- [Profile Configuration Example](references/config.example.json) <br>
- [Content Guidelines](references/content-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, and JSON files with a concise source list and optional shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current weather and news lookup; delivery, posting, or printing requires explicit approval unless an established automation authorizes it.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
