## Description:

Queries public Bilibili user profile information, including follower count, following count, and username, for a supplied user ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up basic public Bilibili account statistics for a known vmid and present the result in a readable form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Bilibili for user IDs supplied by the user.

Mitigation: Use it only when the user intends to query those public profiles, and avoid unnecessary or sensitive lookup patterns.

Risk: Bulk or high-frequency queries could conflict with Bilibili rate limits or terms.

Mitigation: Throttle requests, avoid aggressive batch runs, and stop if Bilibili returns rate-limit or interception errors.

Risk: Returned follower counts, following counts, and usernames can become stale.

Mitigation: Present results as current public data at query time rather than durable facts.

## Reference(s):

- [Bilibili API Guide](references/api_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/moxin1044/skills/bili-user-info)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown response with JSON data or inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bilibili user ID (vmid); returned public-profile data is time-sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
