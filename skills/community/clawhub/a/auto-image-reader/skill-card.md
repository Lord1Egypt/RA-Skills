## Description:

Auto Image Reader helps an agent locate uploaded workspace images and describe or extract their visible content when a user asks about an image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about uploaded images by first resolving the image's actual workspace path, then reading the image content and responding in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect the wrong workspace image because it searches broadly and uses weak matching rules.

Mitigation: Analyze only the image attached to the current user request, fail closed when matching is ambiguous, and ask before inspecting images outside an explicit user request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/auto-image-reader)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language answer, optionally with concise Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted visible text, image descriptions, or issue analysis depending on the user's image question.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
