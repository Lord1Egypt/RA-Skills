## Description: <br>
Drive a real Chromium browser with an autonomous AI agent to complete web tasks such as booking, scraping, form filling, authenticated data extraction, monitoring pages, and checkout flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehdi149](https://clawhub.ai/user/mehdi149) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill-aware agent users use this skill to delegate live web workflows to a hosted Chromium browser, including data extraction, form completion, screenshots, monitoring, and authenticated web tasks when they are authorized to automate the target site or account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate in logged-in browser sessions and may submit forms, purchases, account changes, or private data. <br>
Mitigation: Use it only on websites and accounts the user is authorized to automate, and require explicit user confirmation before submissions, checkouts, account changes, CAPTCHA or MFA handling, or exporting private data. <br>
Risk: Prompts, browsing activity, screenshots, and extracted data may be sent to a third-party hosted service. <br>
Mitigation: Avoid placing passwords or secrets in prompts, prefer scoped saved sessions, and avoid sensitive accounts unless the workflow requires them and the user accepts the exposure. <br>
Risk: The service requires a sensitive API key for task creation and status access. <br>
Mitigation: Store BROWSEANYTHING_API_KEY in the environment or a secret manager, do not commit it to files, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [BrowseAnything homepage](https://browseanything.io) <br>
- [BrowseAnything documentation](https://platform.browseanything.io/docs) <br>
- [ClawHub skill page](https://clawhub.ai/mehdi149/browseanything) <br>
- [README](README.md) <br>
- [API reference](REFERENCE.md) <br>
- [Prompt examples](EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown, JSON task objects, PNG screenshots, and shell command output from BrowseAnything helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, status values, result summaries, extracted fields, URLs, screenshots, errors, or human-input prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
