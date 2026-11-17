## Description:

按条形码查询商品名称、品牌、规格与产地等。当用户说：扫这个条码是什么商品、690 开头的条码查一下信息，或类似商品条码查询时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up product details from a supplied EAN8 or EAN13 barcode. It is intended for explicit product barcode inquiries where the user wants a concise summary of fields such as name, brand, specification, weight, and origin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Barcode values and the JISU_API_KEY are sent to JisuAPI for lookup.

Mitigation: Use the skill only for explicit barcode inquiries and configure API keys with appropriate quota, billing, and access controls.

Risk: The skill is limited to product barcode lookup and may return API errors for missing, invalid, unavailable, or unsupported barcodes.

Mitigation: Check the JSON error fields before summarizing results, and avoid using it for barcode generation, QR handling, or general product search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/barcode)
- [JisuAPI barcode inquiry documentation](https://www.jisuapi.com/api/barcode2/)
- [JisuAPI service website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the lookup script, with agent-facing text summaries derived from returned product fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; sends the queried barcode and API key to JisuAPI.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
