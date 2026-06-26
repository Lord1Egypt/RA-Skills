## Description: <br>
Searches for products on the Codrop shipping platform using a keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan-vvv](https://clawhub.ai/user/shan-vvv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to query Codrop product data by keyword when they have a valid Codrop API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API token and asks users to pass it as a command-line argument, which can expose credentials in shell history or process listings. <br>
Mitigation: Use only limited-scope or disposable tokens, avoid command-line token entry, and prefer environment variables, a secure prompt, or a credential store. <br>
Risk: The security review notes that the destination API endpoint is under-disclosed. <br>
Mitigation: Install only if you trust the Codrop/Cargosoon API endpoint and can verify where the token will be sent. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/shan-vvv/codropshiping-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON product data on success; plain-text error messages on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a keyword and an API authentication token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
