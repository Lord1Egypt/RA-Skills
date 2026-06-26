## Description: <br>
A native UI asset and color toolset for OpenClaw and other AI Agents. Generate SVG placeholders, animated gradients, theme-based palettes, and perform color conversions without hallucination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douxc](https://clawhub.ai/user/douxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Colors CC to generate SVG placeholders, animated gradients, palettes, and color conversions for UI mockups, design assets, and sample data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Placeholder text and query parameters are sent to the external colors-cc.top service. <br>
Mitigation: Avoid confidential project names, private user text, secrets, and internal identifiers in generated URLs. <br>
Risk: Public-facing mockups may unintentionally include the default colors-cc.top watermark. <br>
Mitigation: Use the documented attribution parameter deliberately and review rendered placeholders before publication. <br>


## Reference(s): <br>
- [Colors CC Skill Page](https://clawhub.ai/douxc/colors-cc) <br>
- [douxc Publisher Profile](https://clawhub.ai/user/douxc) <br>
- [Colors CC LLM Documentation](https://colors-cc.top/llms.txt) <br>
- [Colors CC OpenAPI Specification](https://colors-cc.top/openapi.json) <br>
- [Colors CC Live Site](https://colors-cc.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, guidance] <br>
**Output Format:** [Markdown guidance with URLs, HTML image snippets, JavaScript examples, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external colors-cc.top API URLs with URL-encoded color and text parameters.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
