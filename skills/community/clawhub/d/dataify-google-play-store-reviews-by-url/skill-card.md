## Description:

Collects Google Play app reviews from a known Play Store app URL without supporting app discovery, rankings, or general Google Play search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder tasks for known Google Play app URLs, wait for completion, and return collected review JSON. It is scoped to URL-based Google Play review collection rather than search or ranking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, parameters, task metadata, and results are sent to Dataify.

Mitigation: Use only with data appropriate for Dataify processing, prefer a session-scoped DATAIFY_API_TOKEN, and avoid permanent shell-profile storage unless needed.

Risk: Security evidence flags under-scoped and runtime-import risk.

Mitigation: Review or patch the sys.path import behavior and URL validation before using the skill with paid or sensitive account credentials.

Risk: The workflow can submit asynchronous Dataify tasks that consume account credits.

Mitigation: Preview parameters for uncertain requests, preserve task IDs after submission, and resume polling rather than resubmitting after timeout or interruption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-play-store-reviews-by-url)
- [Tool parameter catalog](artifact/references/tool-params.json)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a Dataify task, poll asynchronously, and summarize large JSON while preserving access to the raw result.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
