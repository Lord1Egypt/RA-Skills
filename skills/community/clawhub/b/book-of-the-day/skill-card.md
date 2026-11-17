## Description:

Book of the Day is a daily book oracle that fetches a fresh book and produces one uplifting, poetic reading in the user's language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanluoman00007](https://clawhub.ai/user/romanluoman00007)

### License/Terms of Use:


## Use Case:

External users ask for a daily book recommendation with a short optimistic reading, optionally scheduled through OpenClaw cron for daily delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install notes may direct users to a publisher-supplied one-command installer outside the reviewed package.

Mitigation: Use the reviewed clawhub install book-of-the-day path, and only run a separate installer after reviewing its full contents, source, version, and checksum or signature.

Risk: Daily push configuration can send automated messages to a configured channel.

Mitigation: Review cron schedule, timezone, session, and channel settings before enabling daily delivery.

## Reference(s):

- [Book of the Day API](https://book-of-the-day.vercel.app)
- [ClawHub Skill Page](https://clawhub.ai/romanluoman00007/skills/book-of-the-day)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with optional inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Under 200 words for the reading, excluding the book description.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
