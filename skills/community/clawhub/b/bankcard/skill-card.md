## Description: <br>
根据银行卡号查发卡行与归属地，可做卡号格式校验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query the issuing bank, region, card type, and format-check result for a bank card number through JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank card numbers submitted to the skill are sent to JisuAPI. <br>
Mitigation: Use BIN prefixes or test numbers when possible, avoid real customer card data unless there is a proper basis to share it with the provider, and disclose the external API dependency to users. <br>
Risk: The JISU_API_KEY credential is required for API access. <br>
Mitigation: Keep JISU_API_KEY private, provide it through the environment, and avoid logging or sharing the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/bankcard) <br>
- [JisuAPI bank card API documentation](https://www.jisuapi.com/api/bankcard) <br>
- [JisuAPI service site](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON returned by the local Python command, with agent-facing guidance for setup and result interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY. Queries are sent to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
