## Description:

Navigate FRED categories and series using fredapi, supporting natural-language queries with intent recognition and double validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiszly](https://clawhub.ai/user/kiszly)

### License/Terms of Use:


## Use Case:

Developers and agents use FRED-Navigator to browse FRED category data, select relevant categories from natural-language requests, and retrieve series data or metadata through helper commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script disables HTTPS certificate verification while using a FRED API key.

Mitigation: Remove the SSL context override in scripts/fred_query.py so HTTPS certificates are verified before installing or running live queries.

Risk: Unpinned dependencies may change behavior across installations.

Mitigation: Pin and review dependency versions for fredapi and pandas before production use.

Risk: Live helper commands contact FRED over the network and require an API key.

Mitigation: Use a restricted FRED API key from the FRED_API_KEY environment variable and run queries in a controlled environment.

## Reference(s):

- [FRED-Navigator ClawHub release](https://clawhub.ai/kiszly/skills/fred-navigator)
- [FRED category tree](references/fred_categories_tree.json)
- [FRED categories flat index](references/fred_categories_flat.json)
- [FRED category paths index](references/category_paths.json)
- [Natural-language synonym hints](references/synonyms.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON or table output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require FRED_API_KEY and network access to FRED for live category or series queries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
