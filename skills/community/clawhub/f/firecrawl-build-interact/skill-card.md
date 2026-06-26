## Description: <br>
Integrate Firecrawl `/interact` into product code for dynamic pages and browser actions after scraping when a feature needs clicks, form fills, pagination, authentication-aware flows, or other multi-step interactions that plain `/scrape` cannot complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when to add Firecrawl `/interact` to product integrations and to draft implementation guidance for dynamic pages that require page actions after scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Firecrawl API key, which is a sensitive credential. <br>
Mitigation: Treat FIRECRAWL_API_KEY as a secret and only configure it in trusted environments. <br>
Risk: Generated browser actions may interact with authenticated sites or modify page state. <br>
Mitigation: Review code before running browser actions against authenticated pages and keep workflows scoped to the smallest necessary interaction. <br>
Risk: Persistent browser profiles may retain login state longer than intended. <br>
Mitigation: Avoid persistent profiles unless the workflow clearly requires saved authenticated state. <br>


## Reference(s): <br>
- [Firecrawl Homepage](https://www.firecrawl.dev) <br>
- [Firecrawl Node / TypeScript Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/node) <br>
- [Firecrawl Python Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/python) <br>
- [Firecrawl Rust Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/rust) <br>
- [Firecrawl Java Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/java) <br>
- [Firecrawl Elixir Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/elixir) <br>
- [Firecrawl cURL / REST Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/curl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with language-specific code and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference FIRECRAWL_API_KEY and optional FIRECRAWL_API_URL configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
