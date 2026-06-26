## Description: <br>
A native UI asset and color toolset for OpenClaw and other AI Agents. Generate SVG placeholders, animated gradients, theme-based palettes, and perform color conversions without hallucination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douxc](https://clawhub.ai/user/douxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent users use this skill to generate UI placeholder images, animated gradients, curated palettes, random colors, CSS color-name lookups, and color conversions for mockups and frontend workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated color, palette, placeholder, and conversion requests are sent to the third-party colors-cc.top service. <br>
Mitigation: Avoid including secrets, private project names, customer data, or internal labels in placeholder text or URL parameters. <br>
Risk: External SVG placeholder URLs may reveal descriptive text or parameters to the third-party service and to clients that render the URL. <br>
Mitigation: Use generic labels for sensitive or internal mockups, or prefer local and self-hosted assets when privacy matters. <br>
Risk: Malformed color parameters can produce invalid requests or unexpected visual output. <br>
Mitigation: URL-encode hash characters as %23 and keep palette values within the documented 2 to 10 color range. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/douxc/colors-cc-skill) <br>
- [Publisher profile](https://clawhub.ai/user/douxc) <br>
- [Colors CC LLM documentation](https://colors-cc.top/llms.txt) <br>
- [Colors CC OpenAPI specification](https://colors-cc.top/openapi.json) <br>
- [Colors CC live site](https://colors-cc.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, guidance] <br>
**Output Format:** [Markdown or HTML image embeds, API URLs, JavaScript snippets, and JSON color data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses colors-cc.top endpoints; placeholder text is capped at 100 characters, dimensions are clamped from 50 to 4000 pixels, palettes accept 2 to 10 colors, and hash characters in colors must be URL-encoded as %23.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
