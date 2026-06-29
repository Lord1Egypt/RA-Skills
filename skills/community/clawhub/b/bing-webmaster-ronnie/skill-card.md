## Description: <br>
Bing Webmaster Ronnie helps agents submit URLs to Bing Webmaster Tools and fetch search traffic, keyword ranking, crawl health, indexing, and quota data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ronnine6527](https://clawhub.ai/user/ronnine6527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO operators, and agents use this skill to submit controlled site URLs to Bing and generate Bing Webmaster reporting for search performance, query statistics, crawl health, indexing, and submission quotas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Bing Webmaster API key and can submit URLs or retrieve SEO data for connected sites. <br>
Mitigation: Use a scoped API key where possible, prefer the BING_WEBMASTER_API_KEY environment variable over command-line key arguments, and submit only URLs for sites you control. <br>
Risk: Scheduled reports or webhook delivery can expose search performance and crawl data outside the workspace. <br>
Mitigation: Review destinations and report contents before enabling scheduled sharing or sending SEO data to client channels. <br>


## Reference(s): <br>
- [Bing Webmaster Tools](https://www.bing.com/webmasters/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, JSON API responses, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bing Webmaster API key and user-supplied site URLs; generated reports may contain SEO performance data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
