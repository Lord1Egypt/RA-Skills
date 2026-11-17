## Description:

Performs structured semantic searches against the Datayes gptMaterials/v2 API for news, research reports, announcements, meeting summaries, industry updates, and indicator background materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datayes](https://clawhub.ai/user/datayes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Datayes search results for current news, sell-side research, official announcements, meeting summaries, and macro or industry indicator material through a token-authenticated Python helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redirect handling could leak the Datayes bearer token outside the intended Datayes host allowlist.

Mitigation: Review before installation; use a revocable least-privilege Datayes token, avoid highly sensitive queries, and prefer a version that disables redirects or revalidates every redirect before sending Authorization headers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/datayes/skills/datayes-web-search)
- [Datayes Authentication](https://r.datayes.com/auth/login)
- [Datayes API Metadata Endpoint](https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api)
- [Datayes gptMaterials v2 Endpoint](https://gw.datayes.com/aladdin_info/web/gptMaterials/v2)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Raw JSON arrays from the API, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAYES_TOKEN and python3; search results default to 15 items and are capped at 50 items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
