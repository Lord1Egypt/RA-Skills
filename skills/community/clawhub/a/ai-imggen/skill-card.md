## Description:

Generate images from text prompts via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request image generation from a text prompt and receive an image URL or API response for downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can be exposed through shell history, process listings, logs, or monitoring when passed as a command-line argument.

Mitigation: Use a limited or disposable API key, avoid sensitive prompts, and rotate the key if it may have been captured.

Risk: The skill setup note references skillboss.co, while execution sends the API key and prompt to api.heybossai.com.

Mitigation: Review the endpoint relationship before installation and disclose the destination service to users handling prompts or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/ai-imggen)
- [SkillBoss API key setup](https://www.skillboss.co)
- [HeyBoss image generation API endpoint](https://api.heybossai.com/v1/run)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL or JSON printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; the prompt and API key are sent to api.heybossai.com.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
