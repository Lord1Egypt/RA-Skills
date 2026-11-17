## Description:

Deploy an HTML page to the internet and return a public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiantoucn](https://clawhub.ai/user/jiantoucn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish a selected HTML file or supported site archive to Dropage and return a public URL with expiry and optional visit-limit settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files or archives are uploaded to a public Dropage URL and may expose secrets, private links, proprietary assets, or embedded credentials.

Mitigation: Review the exact file or archive contents before upload and do not deploy material that should not be public.

Risk: Public access expiry is separate from temporary uploaded-file retention and retained database metadata.

Mitigation: Use the shortest suitable expiry and optional visit limit, and avoid uploading sensitive or regulated content.

Risk: Rate limits and long-expiry daily quotas can reject uploads or delay publishing.

Mitigation: Report quota and rate-limit details from the API response, honor Retry-After and reset times, and do not silently change the requested expiry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiantoucn/skills/dropage-deploy)
- [Dropage deploy skill document](https://dropage.online/dropage-deploy.md)
- [Dropage upload API](https://dropage.online/api/upload)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance, Markdown]

**Output Format:** [Markdown with inline curl commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a public URL, expiration time, and visit limit on successful upload.]

## Skill Version(s):

1.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
