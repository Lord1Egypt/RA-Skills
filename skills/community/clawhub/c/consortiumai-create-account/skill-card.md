## Description: <br>
Create a custodial wallet account on Consortium AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WebCraft3r](https://clawhub.ai/user/WebCraft3r) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create a Consortium AI custodial wallet account for a supplied wallet address through the Consortium AI API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the supplied wallet address and TRADING_ANALYSIS_API_KEY to Consortium AI's API. <br>
Mitigation: Run it only when you trust Consortium AI, intend to create the custodial wallet account, and are comfortable sharing those values; use a restricted or revocable API key when available. <br>
Risk: Running the command with the wrong wallet address can create an account for an unintended address. <br>
Mitigation: Verify the wallet address before execution and review the JSON response before relying on the created account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WebCraft3r/consortiumai-create-account) <br>
- [Consortium AI](https://consortiumai.org/) <br>
- [Consortium AI create custodial wallet endpoint](https://api.consortiumai.org/api/custodial-wallet/create-with-api-key) <br>
- [Consortium AI on X](https://x.com/Consortium_AI) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRADING_ANALYSIS_API_KEY and a supplied wallet address to call Consortium AI's account creation API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
