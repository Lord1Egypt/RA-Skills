## Description:

Bulk-runs render-and-parse over every URL in a JSON file of job or link objects and records rendered and parsed output paths back into that file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umerkha2007](https://clawhub.ai/user/umerkha2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to batch scrape a known list of URLs from a JSON file, preserve resumable progress, and attach rendered and parsed result paths to each input object.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill depends on PyPI packages and a Playwright browser binary.

Mitigation: Confirm the packages are trusted in the target environment before installation.

Risk: A normal run visits every URL listed in the input JSON file and creates rendered and parsed JSON outputs.

Mitigation: Run --dry-run first to review scope before making network requests or writing output files.

Risk: The CLI modifies the input JSON file as it records rendered_page and parsed_page paths.

Mitigation: Use a versioned or backed-up input file when preserving the original data matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/umerkha2007/skills/bulkurlscraper-skill)
- [Server-resolved source repository](https://github.com/umerkha2007/BulkUrlScraper-Skill)
- [scrape-applied-links PyPI package](https://pypi.org/project/scrape-applied-links/)
- [render-url PyPI package](https://pypi.org/project/render-url/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; runtime output updates the input JSON file with rendered_page and parsed_page paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI processes URLs sequentially, skips entries that already have rendered_page unless --force is used, and saves progress after each successful URL.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
