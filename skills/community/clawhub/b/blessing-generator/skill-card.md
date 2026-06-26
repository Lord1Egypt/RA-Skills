## Description: <br>
Generates personalized Chinese blessing messages for holidays, life events, recipients, relationships, recent context, style, and length preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who need greeting copy use this skill to generate three personalized Chinese blessing options for holidays, birthdays, weddings, graduations, workplace occasions, and custom celebrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends recipient, occasion, style, and recent-context prompts to the configured LLM provider. <br>
Mitigation: Avoid entering sensitive family, health, relationship, workplace, or financial details unless they are appropriate to share with that provider. <br>
Risk: The skill reads LLM credentials and API base settings from the environment, which can cause unintended provider or key use. <br>
Mitigation: Run it in an isolated environment with only the intended OPENAI_API_KEY or DEEPSEEK_API_KEY and matching OPENAI_API_BASE configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/blessing-generator) <br>
- [Publisher profile](https://clawhub.ai/user/antonia-sz) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with three Chinese blessing variants and a brief usage note.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an intended LLM API key and compatible API base; generated wording varies by model, prompt inputs, and style settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
