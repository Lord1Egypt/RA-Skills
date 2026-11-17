## Description:

Researches App Store / Google Play keywords for one app with live AppGoat data (current ranks, competitor keyword gaps, popularity, difficulty, relevance) and rewrites the title, subtitle, keyword field and description within the store character limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT-0

## Use Case:

App publishers and developers use this skill to research keyword opportunities for one app and prepare store listing metadata for a selected country. It provides ranked keyword analysis, title and subtitle options, and a character-limit-aware keyword field or description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional scheduled automation can have broader repository write access than the metadata update requires.

Mitigation: Limit repository permissions and allowed tools to the intended metadata output and review workflow.

Risk: The automation example handles an AppGoat API key in a temporary configuration file.

Mitigation: Keep the key out of command arguments and logs, and restrict access to temporary files that contain credentials.

## Reference(s):

- [REST fallback guide](reference/api.md)
- [AppGoat API](https://api.appgoat.ai/v1)
- [AppGoat dashboard](https://dash.appgoat.ai)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Configuration instructions]

**Output Format:** [Markdown tables and metadata proposals, with optional YAML or shell automation examples]

**Output Parameters:** [1D (one app and storefront country per run)]

**Other Properties Related to Output:** [Includes two title and subtitle variants, keyword placement rationale, and store character-limit guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
