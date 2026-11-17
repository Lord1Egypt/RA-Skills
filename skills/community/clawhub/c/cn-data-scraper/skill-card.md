## Description:

Chinese website data scraping expert with anti-bypass strategies for Baidu, Taobao, Douyin, Zhihu, WeChat, 1688, Xiaohongshu, Weibo, CSDN, and Boss Zhipin using Scrapling-oriented recipes, adaptive selectors, legal boundary guidance, and executable scraping examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and implement Chinese website data collection workflows with platform-specific scraping recipes, Scrapling configurations, adaptive selector patterns, and legal compliance checks. It is most relevant when public or authorized data access is required across Chinese search, social, ecommerce, article, and job platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes anti-crawl and login-wall bypass guidance that can be misused against protected or unauthorized data sources.

Mitigation: Use it only for authorized scraping, prefer official APIs, avoid protected or login-gated data unless explicit permission is documented, and exclude personal or private data collection.

Risk: The bundled scrape.sh script can execute injected code or overwrite files when given untrusted inputs or sensitive output paths.

Mitigation: Review the script before use, run it only with trusted arguments, choose non-sensitive output locations, and execute it in a constrained sandbox.

Risk: The workflow depends on scraping libraries and browser automation behavior that may change or introduce supply-chain exposure.

Mitigation: Install dependencies in an isolated environment, pin reviewed versions, and retest platform recipes before operational use.

## Reference(s):

- [Scrapling GitHub](https://github.com/D4Vinci/Scrapling)
- [Scrapling Chinese Documentation](https://github.com/D4Vinci/Scrapling/blob/main/docs/README_CN.md)
- [Camoufox](https://github.com/nicegamer7/camoufox)
- [ClawHub Skill Page](https://clawhub.ai/lm203688/skills/cn-data-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; the bundled CLI script prints JSON scraping results or error objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific recipes, legal boundary notes, Scrapling configuration examples, MCP integration examples, and an optional shell script for selected platforms.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
