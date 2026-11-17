## Description:

Query headlines and articles from a self-hosted FreshRSS instance with category, time range, unread, and count filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query a configured self-hosted FreshRSS reader for recent headlines, unread items, categories, and feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FreshRSS API credentials can be exposed if the skill is used with HTTP or if authenticated URLs are captured in logs.

Mitigation: Use only an HTTPS FreshRSS URL, avoid shared machines where process arguments may be observable, and prefer authentication that does not place the API password in the URL.

Risk: A previously used FreshRSS API password may already have been captured if used over HTTP or logged URLs.

Mitigation: Rotate the FreshRSS API password if it may have been exposed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FRESHRSS_URL, FRESHRSS_USER, and FRESHRSS_API_PASSWORD in the environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
