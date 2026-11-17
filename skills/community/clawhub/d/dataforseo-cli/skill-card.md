## Description:

dataforseo-cli helps agents perform SEO keyword research with the DataForSEO API, including search volume, CPC, keyword difficulty, competition, related keywords, and competitor ranking analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexgusevski](https://clawhub.ai/user/alexgusevski)

### License/Terms of Use:

MIT

## Use Case:

Developers, SEO practitioners, and content teams use this skill to guide agents through keyword research, content planning, and competitive keyword analysis with dataforseo-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an npm package and configure DataForSEO API credentials.

Mitigation: Pin the npm package version, avoid elevated privileges during installation, treat credentials as secrets, protect ~/.config/dataforseo-cli/config.json, and rotate credentials if exposure is suspected.

Risk: SEO metrics and competitor analysis can be used incorrectly if stale cached results or the wrong location and language settings are used.

Mitigation: Review command parameters before use, set the intended location and language explicitly, and refresh cached results when current metrics are required.

## Reference(s):

- [dataforseo-cli npm package](https://www.npmjs.com/package/dataforseo-cli)
- [dataforseo-cli GitHub repository](https://github.com/alexgusevski/dataforseo-cli)
- [ClawHub skill page](https://clawhub.ai/alexgusevski/skills/dataforseo-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and TSV or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers DataForSEO credential setup, command selection, output formats, caching, and SEO research workflow steps.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact metadata reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
