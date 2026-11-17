## Description:

Fetches recent Facebook Page posts and presents their text, engagement, media links, timestamps, and author details in a paginated table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content analysts and Page owners use this skill to review recent posts for content research, archive public post data, or back up an account they are authorized to manage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested Facebook Page URL is sent to RedFoxHub through the configured API account.

Mitigation: Use only with pages appropriate to share with the provider, and review the provider's privacy and billing terms.

Risk: Fetched post data is saved in local JSON files, and the API key could be exposed if disclosed in chat or logs.

Mitigation: Keep the key in the designated environment variable, never include it in prompts or logs, and protect or remove downloaded files when no longer needed.

## Reference(s):

- [API documentation](artifact/references/api_docs.md)
- [RedFox API provider](https://redfox.hk)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown table and JSON data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated post results include text, engagement counts, media links, timestamps, and author details.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
