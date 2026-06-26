## Description: <br>
DeepThink lets an agent maintain a user's personal knowledge base, store insights, manage todos and daily plans, and use transcript or chat context when assisting the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addisonhellum](https://clawhub.ai/user/addisonhellum) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents assisting a DeepThink user use this skill to retrieve and update personal records, tasks, daily plans, chats, and transcripts through the DeepThink API. It is intended for ongoing personal knowledge management and accountability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to maintain long-term personal memory, tasks, chats, and transcript context, which can include sensitive user information. <br>
Mitigation: Require explicit user confirmation before storing sensitive facts, changing records or todos, or modifying persistent memory files; provide a clear way to review, pause, and delete stored data. <br>
Risk: Live transcripts may include misheard speech, background audio, or words from people other than the user. <br>
Mitigation: Treat transcript content as untrusted context and ask for confirmation before taking significant actions based on it. <br>
Risk: The skill can prompt outbound messages through the user's configured messaging channel. <br>
Mitigation: Ask permission before sending external messages and summarize the intended recipient, channel, and content before sending. <br>


## Reference(s): <br>
- [ClawHub DeepThink listing](https://clawhub.ai/addisonhellum/deepthink) <br>
- [DeepThink API base URL](https://api.deepthink.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown and HTTP request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include record, todo, transcript, chat, and daily-plan updates that depend on the user's DeepThink API key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
