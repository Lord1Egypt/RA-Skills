## Description: <br>
Generate cinematic floating product shots, levitating product photography, and hovering e-commerce images with dramatic studio lighting via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, e-commerce teams, marketers, creators, and developers use this skill to generate floating product photography from short text prompts for listings, ads, catalogs, and brand content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product prompts and related request data are sent to the external Neta/TalesOfAI service. <br>
Mitigation: Do not submit confidential product information, unreleased campaign details, or sensitive customer data unless external service use is approved. <br>
Risk: The API token is accepted through a command-line flag and included in outbound API headers. <br>
Mitigation: Prefer a secure shell variable or secret manager when invoking the command, and avoid sharing command histories or logs that may contain tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/blammectrappora/floating-product-generator) <br>
- [Neta API Access](https://www.neta.art/open/) <br>
- [TalesOfAI API Service](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text URL printed to stdout, with command-line usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends prompts, token-bearing API requests, and optional reference image identifiers to the external Neta/TalesOfAI service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
