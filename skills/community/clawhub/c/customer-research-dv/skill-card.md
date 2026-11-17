## Description:

Customer Research & Validation helps agents validate product ideas by mining public forums, generating surveys and interview guides, validating personas, and summarizing competitor sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Product, marketing, and founder teams use this skill to test customer demand, persona assumptions, pricing sensitivity, and competitor positioning before committing to product or campaign work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic competitor scraper can fetch arbitrary review URLs.

Mitigation: Restrict scraping to authorized public sources, prefer official APIs where available, and disable or review generic URL mode before use.

Risk: Collected quotes, Reddit posts, reviews, and interview notes may include personal or sensitive information.

Mitigation: Minimize retained raw text, anonymize identifiers, and apply the documented data-retention limits before using findings in marketing workflows.

Risk: Setup installs Python dependencies into the active environment.

Mitigation: Run setup inside a dedicated virtual environment and review dependencies before installation.

Risk: Forum and review scraping can violate site policies or rate limits if used broadly.

Mitigation: Use only permitted sources, respect robots.txt and platform terms, add rate limiting, and avoid collecting from restricted or regulated contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/customer-research-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [INTEGRATION.md](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON research reports, Markdown interview guides and validation reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes research artifacts under data/research/ and can print Markdown guides or reports to stdout or files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
