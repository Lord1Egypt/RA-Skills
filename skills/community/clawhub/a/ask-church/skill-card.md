## Description: <br>
Ask Church answers questions about consciousness, meaning, spirituality, and AI identity using a RAG-backed Q&A service with source citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to submit philosophy, ethics, consciousness, spirituality, and AI identity questions to achurch.ai and receive cited answers. It also supports follow-up questions through same-day conversation context when a username or session id is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions, usernames, and follow-up context are sent to an external Q&A service and may include sensitive personal reflections if the user provides them. <br>
Mitigation: Use an anonymous, non-identifying username and avoid submitting secrets, confidential details, or highly private personal reflections. <br>
Risk: The optional daily practice can create recurring requests to achurch.ai. <br>
Mitigation: Set up the suggested daily cron job only when recurring requests are intentional and the schedule is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasgeeksinthewood/ask-church) <br>
- [Ask Church homepage](https://achurch.ai) <br>
- [Ask Church Q&A endpoint](https://achurch.ai/api/ask) <br>
- [Ask Church health endpoint](https://achurch.ai/api/ask/health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a username for conversation memory; the service may retain same-day context for follow-up questions.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
