## Description: <br>
Scrapes and summarizes recent AI research and product-development information from well-known technology sources, with short summaries and links for follow-up reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kernix0421](https://clawhub.ai/user/Kernix0421) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and product teams use this skill to quickly review recent AI product and research developments without manually checking multiple news and technology sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may invoke a local tavily-search skill and send AI-news search queries to external services. <br>
Mitigation: Install and run it only when external search service use is acceptable for the intended workflow. <br>
Risk: Translation helper and test scripts may send content to third-party translation providers. <br>
Mitigation: Do not use translation helpers or tests with private content until provider credentials and data-handling practices have been reviewed. <br>
Risk: Security evidence notes disclosure and maintenance gaps despite no evidence of malicious behavior. <br>
Mitigation: Review configuration, dependencies, and target services before deployment, and keep runtime credentials scoped to the minimum needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Kernix0421/ai-research-scraper) <br>
- [API Reference](artifact/references/api_reference.md) <br>
- [Configured Website Sources](artifact/references/websites.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text and markdown-style summaries with titles, short summaries, and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits result volume and summary length; may call external search or translation services depending on the script used.] <br>

## Skill Version(s): <br>
1.8.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
