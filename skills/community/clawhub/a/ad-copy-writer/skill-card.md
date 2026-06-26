## Description: <br>
Create, generate, convert, and polish ad copy, marketing copy, product copy, landing page copy, headline variants, CTA variants, and promotional messaging through the WeryAI chat completion API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwwdn](https://clawhub.ai/user/fwwdn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, founders, and agents use this skill to draft or revise concise campaign copy, landing page copy, headlines, CTA variants, and promotional messaging for specific audiences and channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, product briefs, campaign details, and source copy are sent to the WeryAI service for generation. <br>
Mitigation: Use the skill only when WeryAI is approved for the data being submitted, and avoid confidential or regulated business data unless that approval is in place. <br>
Risk: API-key-funded usage may consume WeryAI credits, and an untrusted compatible endpoint could receive submitted copy or prompts. <br>
Mitigation: Use dry-run mode to inspect payloads before paid calls, keep WERYAI_API_KEY protected, and leave WERYAI_BASE_URL unset or point it only at a trusted WeryAI-compatible endpoint. <br>


## Reference(s): <br>
- [Ad Copy Writer Domain Reference](references/domain.md) <br>
- [ClawHub Release Page](https://clawhub.ai/fwwdn/ad-copy-writer) <br>
- [WeryAI API Endpoint](https://api.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples and JSON request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces copy-ready marketing text; dry-run mode can inspect request payloads without calling the API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
