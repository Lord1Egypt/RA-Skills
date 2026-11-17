## Description:

Manage recipes and grocery lists with ingredient tracking and meal plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Chefpad to maintain a local recipe collection, track ingredients and cooking steps, rate recipes, search by ingredient or cuisine, and build grocery-oriented meal suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted recipe text could cause code to run on the user's machine.

Mitigation: Review recipe text before use and avoid untrusted or automatically imported recipe content until the publisher fixes argument handling.

## Reference(s):

- [Chefpad on ClawHub](https://clawhub.ai/bytesagain-lab/skills/chefpad)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create and update local JSON recipe files under ~/.chefpad when executed.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
