## Description: <br>
Retrieve Amazon product data including pricing, reviews, sales estimates, stock levels, search results, deals, and more via the Canopy API REST endpoints using Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhino88](https://clawhub.ai/user/rhino88) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate Python-based Canopy API requests for Amazon product lookup, pricing, reviews, sales and stock estimates, search, offers, deals, category, seller, and author data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canopy API usage sends product identifiers, URLs, GTINs, seller IDs, author terms, and search terms to a third-party API. <br>
Mitigation: Use the skill only for approved Canopy workflows and avoid submitting secrets or sensitive internal research terms as request parameters. <br>
Risk: Misuse or leakage of the Canopy API key could allow unauthorized access or unexpected billing. <br>
Mitigation: Use a dedicated or limited Canopy API key, keep it in the API_KEY environment variable, and monitor API usage and billing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rhino88/amazon-data) <br>
- [Canopy API](https://canopyapi.co) <br>
- [Canopy REST API base URL](https://rest.canopyapi.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Canopy API key supplied through the API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
