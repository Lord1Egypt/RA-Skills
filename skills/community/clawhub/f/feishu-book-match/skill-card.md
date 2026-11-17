## Description:

Fill book match results (匹配结果) and Amazon links (书籍链接) into a Feishu Bitable by querying Amazon with ISBN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakliao](https://clawhub.ai/user/jakliao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to match book records in Feishu Bitable against Amazon UK and US ISBN search results, then fill match status and clean Amazon detail links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bulk-modify live Feishu Bitable records without requiring a preview or confirmation.

Mitigation: Request a dry-run preview of affected records and proposed Amazon links, confirm the exact table and fields, and keep a rollback plan before bulk updates.

Risk: Running the skill unattended can propagate incorrect match classifications or links across many records.

Mitigation: Process records in small batches, review progress after each batch, and avoid unattended cron or background execution unless monitoring and recovery are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jakliao/skills/feishu-book-match)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jakliao)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown instructions with structured Feishu Bitable update payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces match status values and Amazon detail links; may update Feishu Bitable records in batches.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
