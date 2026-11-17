## Description:

Recommends three meal options based on a user's location, weather, mood, budget, dining mode, and taste preferences, with reasons and image references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pancat009](https://clawhub.ai/user/pancat009)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to quickly decide what to eat by turning a short natural-language preference into practical dish recommendations for takeaway, dining in, or cooking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional image hydration script can make outbound requests to Bing and Pollinations and write downloaded files into local assets.

Mitigation: Run the normal local recommendation command by default; use image hydration only after reviewing the destination path and accepting network downloads.

Risk: The optional --external-ai-cmd path can execute a local shell command and is unsafe with untrusted workspaces or untrusted menu and image filenames.

Mitigation: Do not use --external-ai-cmd unless the command template and input filenames are trusted; prefer a reviewed integration that avoids shell execution.

Risk: The skill provides meal suggestions and explicitly does not handle medical advice or serious dietary restriction diagnosis.

Mitigation: Treat recommendations as preference-based suggestions and route medical, allergy, or severe dietary questions to appropriate professional guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pancat009/skills/eat-what-today-skill)
- [Publisher profile](https://clawhub.ai/user/pancat009)
- [Image asset repository noted by README](https://github.com/Pancat009/eat-what-today-skill)
- [Reference project noted by README](https://github.com/A-kirami/whattoeat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown meal recommendations with reasons, price range, dining mode, and local image references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command-line examples and image paths for agent workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
