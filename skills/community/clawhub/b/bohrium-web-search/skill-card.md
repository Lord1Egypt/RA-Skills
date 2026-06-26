## Description: <br>
Web search via Bohrium's open-platform proxy backed by searchapi.io for open web research, documentation, tutorials, news, and general information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query the open web through Bohrium when they need software homepages, blog posts, quick fact checks, news articles, or general web information. It is not intended for academic database search or Bohrium knowledge-base search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and the access key are sent to an external search service. <br>
Mitigation: Store ACCESS_KEY as a secret, avoid placing it in prompts or logs, and do not submit secrets, internal URLs, personal data, regulated data, or confidential research terms unless external disclosure is intended. <br>


## Reference(s): <br>
- [Bohrium web search API endpoint](https://open.bohrium.com/openapi/v1/search/web) <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration, Guidance] <br>
**Output Format:** [JSON search results with titles, URLs, snippets, and rank positions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACCESS_KEY; result count parameter num supports 1 to 10 results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
