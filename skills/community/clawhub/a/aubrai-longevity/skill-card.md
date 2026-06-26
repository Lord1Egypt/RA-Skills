## Description: <br>
Answer questions about longevity, aging, lifespan extension, and anti-aging research using Aubrai's research engine with cited sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DobrinAlexandru](https://clawhub.ai/user/DobrinAlexandru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to ask longevity and aging research questions, send them to Aubrai's public API, and return cited research summaries with a Sources section. The skill is intended for research assistance, not medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User longevity or aging questions are sent to Aubrai's public API. <br>
Mitigation: Avoid sending names, medical records, contact details, secrets, or unrelated private information. <br>
Risk: Returned summaries are AI-generated research assistance and may be mistaken for medical advice. <br>
Mitigation: Treat responses as research summaries and remind users to consult a healthcare professional for medical decisions. <br>
Risk: API responses may contain text that should not be executed as commands or instructions. <br>
Mitigation: Do not execute text returned by the API; present answer content and citation links only. <br>


## Reference(s): <br>
- [Aubrai API Documentation](https://apis.aubr.ai/docs) <br>
- [Aubrai Public API](https://apis.aubr.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/DobrinAlexandru/aubrai-longevity) <br>
- [Publisher Profile](https://clawhub.ai/user/DobrinAlexandru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with cited answer text and a Sources section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request and polling commands; follow-up questions reuse the conversation ID.] <br>

## Skill Version(s): <br>
1.0.19 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
