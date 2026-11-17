## Description:

Create, publish, and search a consent-first public dating intent using showme/v1 and the datecli registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draft, validate, publish, and search a consent-first public adult dating intent while retaining approval over public fields and publication targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public dating intent can make personal details and contact information searchable and durable.

Mitigation: Use a dedicated public contact method, exclude sensitive identifiers and exact home or work locations, and review every public field before publication.

Risk: Publication to a registry, GitHub pull request, or static page can expose information outside the local drafting session.

Mitigation: Publish only after explicit approval for the target and show the exact public text and target URLs before taking external action.

Risk: Discovery results can be mistaken for certain romantic compatibility.

Mitigation: Present candidate fit as uncertain and explain the visible reasons for a possible match without claiming compatibility is guaranteed.

## Reference(s):

- [Intent Card](references/intent-card.md)
- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/find-love)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON snippets and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user verification before publication or other external action]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
