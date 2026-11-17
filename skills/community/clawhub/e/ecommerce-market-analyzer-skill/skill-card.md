## Description:

Scrapes e-commerce homepages in a target market, handles popups, captures screenshots and HTML, extracts product data, and generates market analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nepp-an](https://clawhub.ai/user/nepp-an)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to collect e-commerce homepage evidence, extract products and prices, and produce market research reports for selected regional websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically visit third-party e-commerce sites and save screenshots and HTML locally.

Mitigation: Confirm the target sites, locale, output directory, and retention plan before use; review site terms and robots.txt.

Risk: The artifact includes anti-bot evasion guidance and browser automation behavior.

Mitigation: Do not bypass CAPTCHAs, paywalls, or anti-bot controls; stop when manual verification or site restrictions appear.

Risk: Extracted prices and product trends can be incomplete, stale, or affected by dynamic page rendering.

Mitigation: Verify important prices against captured screenshots or source pages and cite the underlying screenshot or HTML evidence in reports.

## Reference(s):

- [Skill README](README.md)
- [Skill Summary](SKILL_SUMMARY.md)
- [HTML Parsing Patterns](references/html_parsing_patterns.md)
- [Popup Patterns](references/popup_patterns.md)
- [Report Template](assets/report_template.md)
- [ClawHub Skill Page](https://clawhub.ai/nepp-an/skills/ecommerce-market-analyzer-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline code, generated files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write screenshots and HTML files to a local output directory during scraping.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
