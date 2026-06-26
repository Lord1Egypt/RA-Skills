## Description: <br>
Interact with the USDA FoodData Central (FDC) API to search for foods and retrieve detailed nutritional information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search USDA FoodData Central by food name, retrieve FDC IDs, and display detailed nutrition information for specific foods. It is useful for nutrition lookup and comparison workflows that can operate against USDA's English-language, US-focused data. <br>

### Deployment Geography for Use: <br>
United States-focused data; global use where USDA FoodData Central coverage is appropriate. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a USDA FDC API key stored in the local OpenClaw environment. <br>
Mitigation: Keep the OpenClaw configuration private, avoid committing or sharing the key, and rotate it if exposed. <br>
Risk: Food lookup results are constrained by USDA FoodData Central's English-language, US-focused coverage and may omit non-US branded products. <br>
Mitigation: Use results with that coverage limitation in mind and verify nutrition data against authoritative sources for regulated, clinical, or high-impact decisions. <br>
Risk: The USDA API enforces request limits and may return rate-limit or authentication errors. <br>
Mitigation: Handle 403, 429, 404, and 400 responses as surfaced by the scripts, and wait before retrying after rate-limit responses. <br>


## Reference(s): <br>
- [USDA FoodData Central API](https://api.nal.usda.gov/fdc/v1) <br>
- [USDA FoodData Central API Key Signup](https://fdc.nal.usda.gov/api-key-signup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown tables and concise command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a user-provided FDC_API_KEY; food detail output limits nutrient rows to keep responses manageable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
