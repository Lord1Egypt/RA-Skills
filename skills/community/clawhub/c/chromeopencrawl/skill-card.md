## Description: <br>
Crawl JavaScript-rendered webpages through distributed real Chrome browsers without requiring a local browser installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hlyylly](https://clawhub.ai/user/hlyylly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve rendered webpage text, run web searches, and inspect OpenCrawl account or platform status through the OpenCrawl API without installing a local browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default public OpenCrawl endpoint uses plain HTTP, which can expose API keys, crawled URLs, and search queries on the network. <br>
Mitigation: Use a trusted self-hosted or HTTPS OpenCrawl endpoint, and avoid sending sensitive URLs or queries through the default public endpoint. <br>
Risk: Crawl results are stored externally before the agent downloads them. <br>
Mitigation: Treat crawled content as data shared with external infrastructure, and avoid private or regulated pages unless the endpoint and storage controls are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hlyylly/chromeopencrawl) <br>
- [OpenCrawl homepage](https://github.com/hlyylly/OpenCrawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from command-line tool execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawl output may be returned as extracted text or raw JSON that includes result download metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
