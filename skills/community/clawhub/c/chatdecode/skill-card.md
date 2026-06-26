## Description: <br>
ChatDecode helps agents analyze pasted message threads for tone, subtext, emotional state, group dynamics, read receipts, and culturally specific texting cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imwyvern](https://clawhub.ai/user/imwyvern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to get structured, bilingual interpretations of chats, voice-message descriptions, social posts, group dynamics, and read-receipt patterns before deciding how to respond. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation text may include sensitive personal data or third-party private information. <br>
Mitigation: Redact names, contact details, workplace details, account information, and intimate or regulated content before use, and avoid submitting third-party conversations without permission. <br>
Risk: Interpretations of intent, flirting, manipulation, honesty, or emotional state can be overconfident or wrong. <br>
Mitigation: Treat outputs as uncertain possibilities, compare them against broader context and baseline behavior, and avoid using a single reading as proof. <br>
Risk: The linked external pro service offers relationship memory and pattern tracking outside this skill. <br>
Mitigation: Review that service separately before sharing conversation history for persistent memory or pattern analysis. <br>


## Reference(s): <br>
- [ChatDecode on ClawHub](https://clawhub.ai/imwyvern/chatdecode) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ReplyHer](https://replyher.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured analysis sections, confidence ratings, and response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies in the user's language and does not generate files, code, or shell commands.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
