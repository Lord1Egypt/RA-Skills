## Description:

Suggests emoji reactions for text messages based on sentiment analysis across positive, negative, funny, curious, excited, and neutral categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to suggest lightweight emoji reactions for messaging or social engagement workflows. It is best suited to simple local reaction suggestions rather than nuanced sentiment analysis or moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword matching may misclassify tone, sarcasm, multilingual text, or sensitive message content.

Mitigation: Use the suggestion as a convenience hint and review reactions before posting in sensitive or customer-facing contexts.

Risk: The skill is not designed for nuanced moderation or privacy-sensitive message handling.

Mitigation: Avoid relying on it for safety decisions, policy enforcement, or processing messages that require privacy or compliance controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, JSON, Guidance]

**Output Format:** [JavaScript API output or CLI JSON containing category, emoji, and confidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local keyword matching with randomized emoji selection within the selected category.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
