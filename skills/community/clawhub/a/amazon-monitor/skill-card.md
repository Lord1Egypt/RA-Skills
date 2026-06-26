## Description: <br>
Amazon Monitor helps sellers collect and analyze Amazon product and competitor data, including prices, ratings, reviews, trend charts, and operational recommendations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[backtoyoung](https://clawhub.ai/user/backtoyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce operators use this skill to scrape Amazon product data, schedule monitoring tasks, compare competitors, and generate trend charts and comparison reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes Amazon pages and may trigger rate limits, CAPTCHA, or Terms of Service concerns. <br>
Mitigation: Use valid ASINs, keep polling frequencies reasonable, and confirm the intended use complies with Amazon's terms before running monitors. <br>
Risk: Generated history, chart, report, and task files are saved in the working directory. <br>
Mitigation: Review generated JSON, PNG, and TXT files after use, remove data that should not persist, and back up important monitoring history deliberately. <br>
Risk: The skill depends on Playwright and Chromium browser automation. <br>
Mitigation: Install and run the browser dependency only in a trusted environment where automated Amazon page access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/backtoyoung/amazon-monitor) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown-style command guidance plus local JSON, PNG, and TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save product history JSON, trend chart PNG, competitor analysis TXT, and monitoring task configuration in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
