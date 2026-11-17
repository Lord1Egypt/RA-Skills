## Description: <br>
Baidu Youjia Car Query lets agents answer natural-language questions about car brands, model details, price trends, dealer quotes, discounts, total cost, and owner transaction references, with key setup through phone verification or manual configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changxueyi](https://clawhub.ai/user/changxueyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and car-shopping assistants use this skill to retrieve Baidu Youjia vehicle pricing, dealer quotes, discounts, total cost estimates, and owner transaction references by model and city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The key acquisition flow sends a user's phone number to Baidu Youjia. <br>
Mitigation: Use the phone verification flow only after the user has reviewed the Baidu Youjia agreement and agrees to share the phone number. <br>
Risk: API keys may be displayed in chat and stored in plaintext local files such as the skill .env file or ~/.youjia/key.json. <br>
Mitigation: Prefer an explicitly supplied key or a secure environment variable, avoid committing .env files, rotate any key exposed in chat, and remove local key files when persistence is no longer wanted. <br>
Risk: Vehicle prices and dealer quotes are market-dependent and can change after retrieval. <br>
Mitigation: Treat returned prices as current references for the selected city and verify important purchase decisions with the dealer or official Baidu Youjia data source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changxueyi/skills/baidu-youjia-car) <br>
- [Agent calling notes](references/agent-notes.md) <br>
- [API key configuration guide](references/apikey-fetch.md) <br>
- [Temporary key guide](tempkey-guide.md) <br>
- [Baidu Youjia car price endpoint](https://youjia.baidu.com/bff-third-api/openapi/v1/clue/askprice/popbefore) <br>
- [Baidu Youjia homepage](https://www.yoojia.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown answers, Python examples, shell commands, and JSON-like API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu Youjia API key; formatted replies may include vehicle details, city, dealer price ranges, discounts, total-cost fields, fees, and owner transaction references.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
