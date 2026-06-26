## Description: <br>
Domain-restricted full-text search over curated technical documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qsmtco](https://clawhub.ai/user/qsmtco) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical agents use this skill to search a local index of whitelisted documentation sources and return focused results without broad web search noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the optional crawler contacts each configured public site and writes a local index. <br>
Mitigation: Review config.yaml before running npm run crawl, keep the domain whitelist narrow, and confirm crawl depth, delay, and max document settings. <br>
Risk: Scheduled refresh examples can repeatedly crawl configured sites if enabled. <br>
Mitigation: Only enable cron or systemd scheduling when recurring refreshes are intended and after validating the crawl configuration. <br>
Risk: Outdated Node dependencies may inherit known package vulnerabilities over time. <br>
Mitigation: Install from the lockfile where appropriate and update dependencies as part of normal release maintenance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qsmtco/curated-search) <br>
- [README](README.md) <br>
- [Deployment & Operations Guide](docs/deployment.md) <br>
- [Domain Guide](DOMAIN_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON search results containing title, URL, snippet, domain, score, and crawl timestamp fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are generated from a local MiniSearch index; the optional crawler builds that index from configured whitelisted domains.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
