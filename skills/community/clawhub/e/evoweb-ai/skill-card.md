## Description: <br>
Create a Website in 4 Minutes Designed to Bring Clients from ChatGPT, Gemini & Modern Search <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galizki](https://clawhub.ai/user/galizki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn concise business or project descriptions into hosted EvoWeb websites, including live and editor links. It supports both API-key-based creation and a registration-link flow when the user does not yet have an EvoWeb API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website descriptions are sent to EvoWeb, and the no-key onboarding flow can place the prompt in a registration URL. <br>
Mitigation: Avoid including secrets, credentials, regulated personal data, confidential plans, or other sensitive information in prompts. <br>
Risk: Direct website creation uses the user's EvoWeb API key and may consume account credits. <br>
Mitigation: Use only the intended EvoWeb account, confirm the user wants to create or retry a site, and communicate that generations may use credits. <br>
Risk: Generated sites are hosted by EvoWeb and may remain live while the account is active. <br>
Mitigation: Review generated content and editor settings before sharing public live URLs. <br>


## Reference(s): <br>
- [EvoWeb Website Builder](https://evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=website&utm_content=v1.0) <br>
- [EvoWeb API Base URL](https://api.evoweb.ai/openapi/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/galizki/evoweb-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, code, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON API payloads, URLs, and generated website code hosted by EvoWeb] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOWEB_API_KEY for direct API creation; users without an API key can use a pre-filled registration URL.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
