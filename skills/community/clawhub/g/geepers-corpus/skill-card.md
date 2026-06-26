## Description: <br>
Query the COCA (Corpus of Contemporary American English) linguistics API for word frequency, collocations, concordances, and historical usage trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeslp](https://clawhub.ai/user/lukeslp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and linguistics researchers use this skill to query contemporary American English usage data for word frequency, collocations, concordance examples, and historical trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends corpus queries to a third-party API service. <br>
Mitigation: Verify that api.dr.eamer.dev is the intended corpus provider and avoid sending private or sensitive text unless that service is trusted. <br>
Risk: The skill requires an API key for authenticated access. <br>
Mitigation: Use a dedicated API key when available and manage it through the DREAMER_API_KEY environment variable. <br>


## Reference(s): <br>
- [Geepers Corpus on ClawHub](https://clawhub.ai/lukeslp/geepers-corpus) <br>
- [COCA corpus API](https://api.dr.eamer.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMER_API_KEY for authenticated API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
