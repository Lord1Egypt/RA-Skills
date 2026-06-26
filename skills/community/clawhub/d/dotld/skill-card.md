## Description: <br>
dotld helps agents search domain availability and registration prices by running the dotld CLI against the Dynadot API for real-time availability and pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tedstonne](https://clawhub.ai/user/tedstonne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and domain buyers use this skill to check exact domains, expand brand keywords across common TLDs, compare availability and USD pricing, and present registration links or structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer runs mutable remote code before the dotld binary is available. <br>
Mitigation: Review or pin the upstream installer and binary before installation. <br>
Risk: Passing a Dynadot production API key with --dynadot-key can persist the key to a local config file. <br>
Mitigation: Prefer DYNADOT_API_PRODUCTION_KEY in the environment; if a config file is created, restrict it to owner-only permissions such as 0600. <br>
Risk: The skill depends on a production Dynadot API key for live availability and pricing checks. <br>
Mitigation: Use an appropriately scoped key, avoid sharing outputs that expose secrets, and rotate the key if local config storage or command history is suspected to be exposed. <br>


## Reference(s): <br>
- [dotld CLI Reference](references/cli-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tedstonne/dotld) <br>
- [Dynadot API Settings](https://www.dynadot.com/account/domain/setting/api.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands; CLI results may be tree-formatted text or structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dotld CLI and DYNADOT_API_PRODUCTION_KEY; prices are reported in USD for v1.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
