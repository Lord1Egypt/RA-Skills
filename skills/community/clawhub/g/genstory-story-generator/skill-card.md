## Description: <br>
Use when the user wants to generate a story through Genstory with an API key, submit a Genstory story task, poll task status, and return the final Genstory online story URL plus cover image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muryanice](https://clawhub.ai/user/muryanice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate hosted Genstory stories from prompts, configure a Genstory API key, submit story tasks, poll status, and return the resulting story URL and cover image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story prompts, settings, and generated story content are sent to Genstory and may be hosted by that service. <br>
Mitigation: Avoid submitting private content unless Genstory processing and hosting are acceptable for the workflow. <br>
Risk: The skill requires a Genstory API key. <br>
Mitigation: Use a dedicated, revocable API key and store it in environment or configuration rather than chat. <br>


## Reference(s): <br>
- [Genstory Story Task API](references/api.md) <br>
- [Genstory API Keys](https://www.genstory.app/api-keys) <br>
- [Genstory Story Tasks API](https://www.genstory.app/api/v1/story-tasks) <br>
- [ClawHub Skill Page](https://clawhub.ai/muryanice/genstory-story-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/muryanice) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with structured JSON result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, story ID, title, hosted story URL, cover image URL, and locale when generation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
