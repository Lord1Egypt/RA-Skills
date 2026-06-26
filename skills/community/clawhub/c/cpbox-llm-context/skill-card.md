## Description: <br>
Returns pre-extracted web content, including text, tables, code, and structured snippets, for grounding LLM and RAG workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI engineers use this skill to call a paid x402 web-grounding service that returns extracted page content for agents, RAG pipelines, fact checking, and question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid API requests may be triggered through x402 payment middleware. <br>
Mitigation: Use a low-balance or capped payment wallet and require confirmation before paid calls. <br>
Risk: Queries and optional precise location headers can expose sensitive user context to the provider. <br>
Mitigation: Avoid private queries or precise location data unless the user explicitly agrees and trusts the provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sprintmint/cpbox-llm-context) <br>
- [Publisher Profile](https://clawhub.ai/user/sprintmint) <br>
- [CPBox API Provider](https://www.cpbox.io) <br>
- [CPPay x402 Facilitator](https://www.cppay.finance) <br>
- [LLM Context GET Endpoint](https://www.cpbox.io/api/x402/llm-context) <br>
- [LLM Context POST Endpoint](https://www.cpbox.io/api/x402/llm-context/post) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with HTTP examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for paid GET and POST API calls; service responses contain extracted grounding snippets and source metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
