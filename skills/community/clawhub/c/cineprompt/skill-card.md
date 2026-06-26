## Description: <br>
CinePrompt builds structured AI video prompts and share links from natural language shot descriptions or CinePrompt state JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BelafonteLabs](https://clawhub.ai/user/BelafonteLabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Filmmakers, prompt designers, and agents use this skill to convert shot ideas or CinePrompt state JSON into structured cinematography prompts and share links for AI video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text, state JSON, media references, and provider-generation data may be sent to CinePrompt and third-party providers. <br>
Mitigation: Avoid confidential or regulated content and review provider data handling before use. <br>
Risk: The artifact includes a privileged Supabase service-key path intended for internal or owner use. <br>
Mitigation: Use scoped CinePrompt API keys for normal workflows and expose service-role credentials only in verified internal environments. <br>
Risk: The security summary says sensitive uploads are under-disclosed. <br>
Mitigation: Confirm expected data flows with the publisher documentation before installing or running workflows that include media or provider generation. <br>


## Reference(s): <br>
- [CinePrompt](https://cineprompt.io) <br>
- [CinePrompt Guides](https://cineprompt.io/guides) <br>
- [CinePrompt Models](https://cineprompt.io/models) <br>
- [CinePrompt on ClawHub](https://clawhub.ai/BelafonteLabs/cineprompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON state examples and shell commands; CLI operations return JSON share-link payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CinePrompt API key for public share-link creation; generated prompts and state may be sent to CinePrompt and third-party providers.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
