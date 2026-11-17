## Description:

Search Google Jobs for job and recruitment listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Google Jobs through Dataify, map job-search intent into supported request parameters, and return compact listings or raw output when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Dataify API token could be exposed if pasted into chat, printed, or passed directly on the command line.

Mitigation: Use a session-scoped DATAIFY_API_TOKEN environment variable and verify only that it is present, never its value.

Risk: Google Jobs searches may consume Dataify credits, especially when bypassing cache or requesting additional pages.

Mitigation: Review consequential parameters before high-volume or cache-bypassing requests and keep no_cache disabled unless fresh results are needed.

## Reference(s):

- [Dataify Google Jobs API](references/google_jobs_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-jobs)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; API responses may be summarized text, JSON, or HTML when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dataify API token and may consume Dataify credits.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
