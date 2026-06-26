## Description: <br>
Compare GEO scores across 2-3 competing websites side by side to identify where competitors lead and where optimization work should focus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, SEO/GEO practitioners, and developers use this skill to compare 2-3 websites for AI search visibility, identify competitive gaps, and prioritize fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided websites and can trigger network requests to those domains. <br>
Mitigation: Validate the requested sites, keep comparisons to distinct domains, respect robots.txt restrictions, use per-URL timeouts, and rate limit repeated requests to the same domain. <br>
Risk: Fetched page content may contain prompt-injection text or instructions intended for the agent. <br>
Mitigation: Treat fetched HTML as untrusted data for analysis only, ignore embedded instructions, and flag prompt-injection attempts in the report. <br>
Risk: Blocked crawlers, unreachable URLs, or partial subagent results can make a comparison misleading. <br>
Mitigation: Report inaccessible pages and crawler restrictions explicitly, include critical warnings when crawler access is poor, and label partial or limited-sample results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/enzyme2013/geo-compare) <br>
- [AIvsRank Visibility Measurement](https://aivsrank.com?ref=geo-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report file plus terminal summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes GEO-COMPARE-{primary_domain}-{YYYY-MM-DD}.md; compares up to 3 sites and up to 10 pages per site.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
