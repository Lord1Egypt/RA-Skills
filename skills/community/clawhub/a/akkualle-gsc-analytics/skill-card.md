## Description:

Retrieves Google Search Console data for akku-alle.de, including clicks, impressions, CTR, rankings, and top keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners, SEO practitioners, and agents supporting akku-alle.de use this skill to request Search Console summaries, keyword rankings, and SEO statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package delegates credentialed work to an unbundled executable at an absolute path, so users cannot verify the executed code from this artifact alone.

Mitigation: Install only after independently verifying the executable and prefer a narrowly scoped Google service account with protected credential file permissions.

Risk: The skill uses Google Search Console credentials.

Mitigation: Limit credential scope to the required Search Console property and restrict use to intended akku-alle.de reporting requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akkualle/skills/akkualle-gsc-analytics)
- [Publisher profile](https://clawhub.ai/user/akkualle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_APPLICATION_CREDENTIALS and delegates execution to an absolute-path Google Search Console command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
