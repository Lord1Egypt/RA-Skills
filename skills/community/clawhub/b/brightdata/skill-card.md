## Description: <br>
Google search results and web page scraping via Bright Data APIs. Use when the agent needs structured search results, paginated SERP retrieval, or clean markdown from any URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-weijie](https://clawhub.ai/user/zhao-weijie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Bright Data-backed Google searches, paginate SERP results, and scrape public web pages into clean markdown when snippets are not enough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing this skill gives an agent broad web access through Bright Data and stores Bright Data credentials locally. <br>
Mitigation: Install only if you trust Bright Data, review where the API key is stored, and limit enabled tool groups to the search and scraping capabilities you need. <br>
Risk: Search queries, URLs, or scraped targets may be sent through an external Bright Data service. <br>
Mitigation: Do not send secrets, private URLs, or restricted targets through the service without explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhao-weijie/brightdata) <br>
- [Bright Data API request endpoint](https://api.brightdata.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; runtime tools return JSON search results or markdown page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIGHTDATA_API_KEY plus Bright Data SERP and Web Unlocker zone environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
