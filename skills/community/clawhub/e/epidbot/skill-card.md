## Description: <br>
Interact with EpidBot - AI-powered assistant for Brazilian public health data (DATASUS/SINAN). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fccoelho](https://clawhub.ai/user/fccoelho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and public-health analysts use this skill to query EpidBot, retrieve Brazilian and international health data, manage analysis sessions, and download generated reports through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, public-health analysis requests, session history, generated reports, and API keys may contain sensitive information. <br>
Mitigation: Install only when the EpidBot service is trusted, avoid sending secrets or unnecessary personal health information, and retrieve prior sessions or reports only when intended. <br>
Risk: WebSocket URLs can include the API key. <br>
Mitigation: Avoid copying, sharing, or logging WebSocket URLs that contain credentials. <br>
Risk: Complex EpidBot queries may take several minutes and can appear stalled if polling stops too early. <br>
Mitigation: Use exponential backoff polling up to the documented 5 minute maximum before treating an asynchronous chat job as incomplete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fccoelho/epidbot) <br>
- [Publisher Profile](https://clawhub.ai/user/fccoelho) <br>
- [EpidBot Homepage](https://github.com/fccoelho/EpiDBot) <br>
- [EpidBot Documentation](https://github.com/fccoelho/EpiDBot/tree/main/docs) <br>
- [EpidBot API Base URL](https://api.epidbot.kwar-ai.com.br/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples, shell commands, JSON response shapes, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EPIDBOT_API_KEY and EPIDBOT_BASE_URL; asynchronous chat responses should be polled with exponential backoff for up to 5 minutes.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
