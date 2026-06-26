## Description: <br>
Extract design information from Figma files, including design tokens, component structure, colors, typography, spacing, and assets for development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-system engineers use this skill to inspect Figma files, extract implementation-ready design tokens, summarize component structure, and export selected visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma personal access token, which may expose private design files available to that token. <br>
Mitigation: Use the least-privileged token available, provide only Figma URLs or node IDs intended for agent access, and revoke the token when the task is complete. <br>


## Reference(s): <br>
- [Figma Bridge on ClawHub](https://clawhub.ai/vanthienha199/figma-bridge) <br>
- [Figma REST API](https://api.figma.com/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CSS, JSON, JavaScript, shell command examples, and exported asset summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Figma REST API using FIGMA_TOKEN and may write exported assets to a local figma-exports directory when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
