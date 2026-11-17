## Description:

Collab Ingest Demo documents a reproducible ClawHub asset-ingest workflow that structures a workflow handoff, packages it as a skill asset, and publishes it to ClawHub.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill as a worked handoff for packaging digital content into a ClawHub skill asset and validating dry-run, publish, and search steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reproduction steps include a non-dry-run `clawhub publish` command that performs a real remote publish operation.

Mitigation: Run the dry-run first, confirm the authenticated account and unique slug, and only run the final publish command when upload is intended.

Risk: A reused or incorrect slug can fail publication or publish the asset under the wrong release identity.

Mitigation: Use a kebab-case slug, check it before publishing, and verify the published result with `clawhub search`.

Risk: A newly published item may not be immediately visible because review or indexing can be delayed.

Mitigation: Wait and search again before assuming publication failed or repeating the publish operation.

## Reference(s):

- [Content-to-asset ingest handoff](references/DESCRIPTION.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/collab-ingest-demo-20260922)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents packaging, dry-run publish, final publish, and verification steps for a ClawHub skill asset.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
