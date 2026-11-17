## Description:

Search USDA FoodData Central for foods and retrieve detailed nutrition information using the USDA FDC API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for foods, retrieve FDC IDs, and fetch formatted nutrition details from the USDA FoodData Central database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food search terms and the FDC API key are sent to the USDA FoodData Central API.

Mitigation: Use a dedicated FDC API key and avoid submitting sensitive search terms.

Risk: The database is English-language and US-focused, so non-English searches or international branded foods may return incomplete results.

Mitigation: Use English search terms and verify nutrition details against local product labels when regional accuracy matters.

Risk: USDA API rate limits can interrupt lookups.

Mitigation: Keep request volume within the documented USDA limits and wait before retrying after HTTP 429 responses.

## Reference(s):

- [USDA FoodData Central API](https://api.nal.usda.gov/fdc/v1)
- [USDA FoodData Central API Key Signup](https://fdc.nal.usda.gov/api-key-signup)
- [ClawHub Skill Page](https://clawhub.ai/patello/skills/fdc-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, text status messages, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and FDC_API_KEY; food detail output is capped to the first 50 nutrients unless filtered.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
