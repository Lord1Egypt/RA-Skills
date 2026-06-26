## Description: <br>
Provides cross-border e-commerce keyword analysis, marketplace fee and profit calculations, competitor snapshots, and optional AI listing generation for Amazon and eBay sellers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce sellers and operators use this skill to compare product opportunities, estimate Amazon or eBay margins, and draft marketplace listings. Developers can also run it as a local CLI or Flask API-backed MVP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Declared crypto and purchase capability tags are not justified by the visible code. <br>
Mitigation: Review and remove or justify those capability tags before installation or promotion. <br>
Risk: The local Flask development server may expose endpoints if bound publicly or run with debug settings. <br>
Mitigation: Run locally or behind a production server, disable debug mode for shared environments, and avoid exposing the MVP directly to the internet. <br>
Risk: AI listing generation can send product, keyword, and market context to OpenAI when an API key is configured. <br>
Mitigation: Configure an OpenAI API key only when that data sharing is acceptable; otherwise rely on the built-in simulated listing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/cross-border-ecommerce-kay) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text or JSON responses, plus local setup and API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses simulated keyword and competitor data by default; OpenAI listing generation sends product and market context to OpenAI only when an API key is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
