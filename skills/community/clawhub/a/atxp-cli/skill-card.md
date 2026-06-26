## Description: <br>
ATXP gives agents a funded identity and CLI access to paid tools for web search, media generation, communications, wallet funding, and LLM access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[R-M-Naveen](https://clawhub.ai/user/R-M-Naveen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ATXP to register an agent, manage a wallet and identity, and call paid tools for search, content generation, communications, and LLM access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent wallet, spending, and outbound communication capabilities. <br>
Mitigation: Use a low-balance or test account and require human approval before paid API calls, sending email or SMS, making calls, deleting data, or syncing contacts. <br>
Risk: ATXP_CONNECTION and ~/.atxp/config are sensitive credentials that grant access to the agent identity and wallet. <br>
Mitigation: Protect and rotate the config file, avoid long-lived exported credentials, and never print, log, or send the token through outbound channels. <br>
Risk: Commands commonly use npx atxp@latest, which downloads npm runtime code and may change between runs. <br>
Mitigation: Pin an exact reviewed npm version instead of @latest and verify package integrity before use. <br>


## Reference(s): <br>
- [ATXP documentation](https://docs.atxp.ai) <br>
- [atxp npm package](https://www.npmjs.com/package/atxp) <br>
- [ClawHub skill page](https://clawhub.ai/R-M-Naveen/atxp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18, npx, ATXP_CONNECTION, and HTTPS access to ATXP services.] <br>

## Skill Version(s): <br>
1.21.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
