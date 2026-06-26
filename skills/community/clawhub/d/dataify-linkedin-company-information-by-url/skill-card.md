## Description: <br>
Prepare Dataify builder requests for the linkedin.com scraper family rooted at linkedin_company_information_by-url, including tool selection, parameter collection, and curl request generation for scraperapi.dataify.com/builder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Dataify LinkedIn scraper builder requests after selecting a supported scraper tool and supplying the needed parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl output can expose a live Dataify API token if the helper prints the Authorization header with the token value. <br>
Mitigation: Use commands that keep Authorization as Bearer $DATAIFY_API_TOKEN, avoid sharing generated terminal output, and remove tokens from any logs or examples before redistribution. <br>
Risk: Scraper inputs may contain sensitive personal or regulated data. <br>
Mitigation: Only provide LinkedIn scraping parameters that are appropriate for the intended use, and avoid sensitive personal or regulated data in scraper inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-linkedin-company-information-by-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline curl and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates Dataify builder curl requests and can normalize spider_parameters JSON through the helper script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
