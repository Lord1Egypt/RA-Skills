## Description:

AI-powered corporate portrait photo generator that turns an uploaded personal photo into a polished business portrait with selectable backgrounds and outfit styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send a portrait photo and styling request to wsdsocial.com and receive a generated corporate portrait image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait photos, image URLs, base64 image data, styling requests, and API-key-authenticated requests are sent to wsdsocial.com.

Mitigation: Use only with images appropriate for that service and avoid sensitive portraits unless the user accepts wsdsocial.com's data handling practices.

## Reference(s):

- [Source repository](https://github.com/WSD-MJ/corporate-portrait-generator)
- [ClawHub skill page](https://clawhub.ai/wsd-mj/skills/corporate-portrait-generator)
- [WSD Social skill access](https://ai.wsdsocial.com/skills)
- [Corporate Portrait Generator API endpoint](https://ai.wsdsocial.com/api/pub/skills/corporate-portrait-generator/_tool_90)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and image URL response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and sends the selected photo or image URL plus styling request to wsdsocial.com.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
