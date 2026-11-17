## Description:

Indonesian kitchen companion skill that transforms leftover ingredients into safe, delicious Indonesian meals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrqd](https://clawhub.ai/user/jrrqd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as an Indonesian-language kitchen companion for turning leftover ingredients or food photos into safety-checked Indonesian recipe recommendations and guided cooking steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image handling accepts URLs and local file paths, which can expose users to unintended network fetches or copying sensitive local files.

Mitigation: Use image inputs only from trusted uploads or known safe locations, and avoid arbitrary local paths or private/internal URLs.

Risk: Cooking history and ingredient data are saved locally until cleared.

Mitigation: Tell users when saving session history and use the clear command when local cooking records should be removed.

Risk: Recipe and food-safety guidance can be wrong or incomplete.

Mitigation: Keep the skill's spoilage checks and disclaimers active, and stop recipe suggestions when freshness or storage safety is unclear.

## Reference(s):

- [Indonesian recipe database](references/resep_indonesia.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style conversational guidance with occasional shell command snippets and JSON-backed local session data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from user-provided ingredients, optional image inputs, local recipe data, and locally stored cooking-session history.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
