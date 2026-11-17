## Description:

Save web pages and memos to Cubox using the Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liam8](https://clawhub.ai/user/liam8)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use this skill to save web URLs and memo text to their Cubox account with optional titles, descriptions, tags, and folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Cubox API URL functions as a secret token.

Mitigation: Store CUBOX_API_URL only in a private environment variable and avoid committing it or exposing it in shared logs.

Risk: Selected URLs, memo text, titles, descriptions, tags, and folder names are sent to the configured Cubox API endpoint.

Mitigation: Use the skill only for content you are comfortable sending to Cubox, and verify the API URL points to the expected Cubox HTTPS endpoint before use.

## Reference(s):

- [Cubox](https://cubox.pro)
- [Cubox API Help](https://help.cubox.pro/save/89d3/)
- [ClawHub skill page](https://clawhub.ai/liam8/skills/cubox)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cubox Premium API URL in CUBOX_API_URL; Cubox Premium users are limited to 500 API calls per day.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
