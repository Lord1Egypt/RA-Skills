## Description: <br>
Geepers Data helps agents fetch structured data from 17 external sources, including arXiv, Census Bureau, GitHub, NASA, Wikipedia, PubMed, news, weather, finance, FEC, and more, through a single API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeslp](https://clawhub.ai/user/lukeslp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, researchers, and data analysts use Geepers Data to discover and query multiple authoritative external data sources for research, visualizations, and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party API, so sensitive queries or credentials could be exposed to the API operator or to logs if handled carelessly. <br>
Mitigation: Trust the Dreamer API operator before use, keep DREAMER_API_KEY out of prompts and logs, and avoid confidential queries unless the service's privacy and retention practices are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lukeslp/geepers-data) <br>
- [Dreamer Data API source listing](https://api.dr.eamer.dev/v1/data) <br>
- [Dreamer Data API search endpoint](https://api.dr.eamer.dev/v1/data/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell snippets, endpoint examples, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMER_API_KEY and sends data queries to the Dreamer Data API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
