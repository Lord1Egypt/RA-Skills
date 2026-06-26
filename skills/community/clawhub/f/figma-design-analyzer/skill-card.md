## Description: <br>
Analyzes Figma design files to extract design-system data, export screenshots, and compare implementation files against the design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plume-lj](https://clawhub.ai/user/plume-lj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design engineers use this skill to inspect Figma files, extract colors, typography, spacing, and components, export design screenshots, and compare CSS or code implementations with the source design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Figma access tokens can expose private design files if mishandled. <br>
Mitigation: Keep FIGMA_ACCESS_TOKEN private, avoid committing .env files or shell-profile token changes, use the narrowest practical Figma access, and rotate the token if exposed. <br>
Risk: Generated reports and exported screenshots may contain design details or local implementation content. <br>
Mitigation: Review generated local outputs before sharing them and only compare local files intended to be included in the analysis output. <br>


## Reference(s): <br>
- [Figma API Reference](references/figma-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and shell commands; generated artifacts may include JSON reports, HTML reports, and PNG/JPG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+ and a FIGMA_ACCESS_TOKEN with appropriate Figma file access.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
