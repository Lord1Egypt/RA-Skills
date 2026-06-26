## Description: <br>
Enriches prospect and company profiles by scraping their website and searching for additional context to build comprehensive profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and marketing teams use this skill through an agent to research one prospect at a time, combining website scraping and targeted web searches into an enriched company profile for outreach, deal prep, partnership research, or competitive context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospect research may share company URLs, prospect details, and local marketing context with Firecrawl/Exa-backed workflows. <br>
Mitigation: Use only approved prospecting data, avoid confidential strategy or sensitive local context unless appropriate for those workflows, and verify the referenced helper CLIs are trusted in the environment. <br>
Risk: External search results and inferred company details can be stale or incorrect. <br>
Mitigation: Prioritize the prospect's own site, clearly mark confirmed versus inferred information, and include confidence ratings for each profile section. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/abm-prospect-enrichment) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, text] <br>
**Output Format:** [Markdown profile with tables, confidence labels, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Marks confirmed versus inferred information and includes confidence ratings by section.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
