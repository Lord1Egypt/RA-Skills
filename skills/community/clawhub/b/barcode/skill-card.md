## Description: <br>
按条形码查询商品名称、品牌、规格与产地等。当用户说：扫这个条码是什么商品、690 开头的条码查一下信息，或类似商品条码查询时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up product details from a barcode, including product name, brand, specification, net content, weight, and origin information. The skill is intended for barcode inquiry workflows that can send the queried barcode to JisuAPI under the user's API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Barcode values are sent to JisuAPI under the user's API key, which may reveal purchase, inventory, or personal context. <br>
Mitigation: Use a dedicated API key where possible, monitor quota usage, and avoid querying sensitive barcode values unless the provider is trusted. <br>
Risk: Provider API errors, quota limits, expired keys, or missing records can produce incomplete or failed lookups. <br>
Mitigation: Check the returned JSON error fields before presenting results and communicate when the provider reports no data or an API error. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/barcode) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI Barcode API Documentation](https://www.jisuapi.com/api/barcode2/) <br>
- [JisuAPI Barcode Query Endpoint](https://api.jisuapi.com/barcode2/query) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON returned by a Python command-line script, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; accepts a JSON object with a required barcode string.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
