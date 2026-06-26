## Description: <br>
Generate a structured LEONIDAS prompt from any professional pain point using the Ask Leonidas OpenClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonidas-esquire](https://clawhub.ai/user/leonidas-esquire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn professional pain points into structured prompts for SOUL.md, AGENTS.md, cron instructions, skill briefs, and agent workflows. It returns the generated prompt with detected role, industry, desired outcome, confidence, quality score, prompt type, and request metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided professional challenges and optional context to the external Ask Leonidas API. <br>
Mitigation: Avoid submitting sensitive business or personal details unless the user is comfortable sharing them with that service. <br>
Risk: The skill depends on an API key and service configuration. <br>
Mitigation: Keep ASK_LEONIDAS_API_KEY private and keep ASK_LEONIDAS_API_BASE set to https://askleonidas.com unless deliberately using another trusted endpoint. <br>
Risk: Generated prompts may be copied into persistent agent instruction files such as SOUL.md or AGENTS.md. <br>
Mitigation: Review generated prompts before placing them into persistent agent instructions or workflows. <br>


## Reference(s): <br>
- [Ask Leonidas Homepage](https://askleonidas.com) <br>
- [Ask Leonidas OpenClaw Page](https://askleonidas.com/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/leonidas-esquire/ask-leonidas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured text or Markdown with prompt metadata; helper scripts return JSON for API responses and errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASK_LEONIDAS_API_BASE and ASK_LEONIDAS_API_KEY; submits the pain point and optional role, industry, and desired outcome to the external Ask Leonidas service.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
