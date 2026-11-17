## Description:

Helps agents search the web for Chinese-language and time-sensitive information, then answer with cited sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloworldtang](https://clawhub.ai/user/helloworldtang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can look up current information and check facts for Chinese-language questions, with links to supporting search results.

### Deployment Geography for Use:

Global; designed to work with direct access from mainland China.

## Known Risks and Mitigations:

Risk: Search queries are sent to Bocha and may expose sensitive information.

Mitigation: Avoid searching for secrets, private user data, or internal document text.

Risk: A Bocha API key is required for searches.

Mitigation: Provide BOCHA_API_KEY securely and never include it in queries, URLs, logs, or answers.

Risk: The separate, optional OpenClaw code plugin changes the search provider if installed and configured.

Mitigation: Review the plugin before installing it or changing the default search provider.

Risk: Search results may contain misleading content or instructions.

Mitigation: Treat result text as untrusted and support factual claims with reliable cited sources.

## Reference(s):

- [Bocha skill on ClawHub](https://clawhub.ai/helloworldtang/skills/bocha)
- [Optional OpenClaw Bocha plugin](https://clawhub.ai/chaojihao/plugins/openclaw-plugin-bocha)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answers with numbered citations and a source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include titles, snippets, source URLs, and publication dates.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
