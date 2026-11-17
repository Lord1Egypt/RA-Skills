## Description:

AI Closet helps agents use authenticated API calls for wardrobe management, outfit recommendations, fashion knowledge search, OOTD records, and virtual try-on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houdamiao](https://clawhub.ai/user/houdamiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage AI Closet wardrobe data, upload clothing images, record outfits, request AI styling recommendations, search fashion knowledge, and prepare virtual try-on API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wardrobe data, photos, outfit context, and image references to the AI Closet service.

Mitigation: Use it only with an AI Closet service and account you trust, and avoid sending sensitive personal photos, location/date context, or images you are not authorized to share.

Risk: The required API key is bound to a user account and authorizes access to that account's data.

Mitigation: Store AICLOSET_API_KEY securely, avoid exposing it in logs or shared prompts, and rotate it if it may have been disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houdamiao/skills/aicloset)
- [AI Closet API base URL](https://aicloset-dev.wxbjq.top)
- [Wardrobe and product API documentation](artifact/api-wardrobe.md)
- [Outfit and OOTD API documentation](artifact/api-outfit.md)
- [AI capability API documentation](artifact/api-ai.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AICLOSET_API_KEY; API calls send wardrobe data, outfit context, and image references to the AI Closet service.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
