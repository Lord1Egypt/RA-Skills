## Description:

Make a recipe by giving some ingredients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demonkit](https://clawhub.ai/user/demonkit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to authenticate with cooking-recipe, manage stored recipes, and create or update grocery lists tied to those recipes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the shared backend can route authentication, recipe, and grocery-list traffic to a default external API target.

Mitigation: Prefer a self-hosted CONVEX_URL and enable the shared backend only intentionally with ALLOW_DEFAULT_BACKEND=true.

Risk: OAuth credentials or tokens could be exposed if pasted into chat or logs.

Mitigation: Keep OAuth secrets out of chat and logs, and provide only configuration next steps when authentication or setup fails.

Risk: Installing from an unexpected package source may weaken release provenance confidence.

Mitigation: Install only from the expected ClawHub package source and verify the publisher profile before use.

## Reference(s):

- [Cooking Recipe ClawHub page](https://clawhub.ai/demonkit/skills/cooking-recipe)
- [demonkit publisher profile](https://clawhub.ai/user/demonkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe authentication or backend configuration next steps without exposing secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
