## Description: <br>
Pub Gemini helps agents use the SkillBoss API to call chat, image, video, audio, search, document, email, SMS, and smart-routing model endpoints from shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinPollitt](https://clawhub.ai/user/MartinPollitt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover SkillBoss models and make authenticated API calls for text generation, media generation, transcription, search, document processing, messaging, and smart model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route agent requests to many third-party AI and utility providers, including paid generation endpoints. <br>
Mitigation: Use a dedicated low-limit SKILLBOSS_API_KEY and require review before paid, batch, or high-volume calls. <br>
Risk: The skill includes email, SMS, document processing, scraping, and search capabilities that may expose sensitive data or contact users. <br>
Mitigation: Avoid confidential documents, internal URLs, OTP codes, and personal contact data unless approved, and require explicit consent before email or SMS actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MartinPollitt/geminis) <br>
- [Publisher profile](https://clawhub.ai/user/MartinPollitt) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may return generated text, media URLs, parsed documents, search results, email or SMS operation results, and model metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
