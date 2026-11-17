## Description:

SEO data from the terminal using DataForSEO APIs for keyword rankings, SERP analysis, site audits, backlink profiles, competitor comparisons, link gap analysis, keyword difficulty, search volume, on-page SEO, and Lighthouse checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricca91](https://clawhub.ai/user/ricca91)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, SEO practitioners, and marketing teams use this skill to run DataForSEO-backed terminal workflows for keyword research, SERP review, technical site audits, and backlink analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script installs the unpinned third-party dfseo package with pip.

Mitigation: Review before installing, use an isolated environment such as pipx or a virtual environment, avoid running installation as root, and prefer a pinned or otherwise verified dfseo package.

Risk: DataForSEO credentials may be exposed through command-line flags, environment handling, shell history, or local configuration.

Mitigation: Use safer credential handling where available, avoid pasting real API passwords into command-line flags on shared or logged systems, and inspect or remove ~/.config/dfseo/config.toml after interactive setup.

Risk: SEO workflows can send sensitive internal URLs, customer domains, private keyword lists, or regulated data to DataForSEO.

Mitigation: Confirm organizational approval before submitting sensitive or regulated data to DataForSEO-backed commands.

## Reference(s):

- [dfseo SERP Commands Reference](references/serp.md)
- [dfseo Keywords Commands Reference](references/keywords.md)
- [dfseo Site Audit Commands Reference](references/site.md)
- [dfseo Backlinks Commands Reference](references/backlinks.md)
- [DataForSEO API Access](https://app.dataforseo.com/api-access)
- [ClawHub Skill Page](https://clawhub.ai/ricca91/skills/dfseo)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ricca91)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and references to JSON, table, and CSV CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default CLI result output is JSON on stdout; table and CSV formats are also documented.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
