## Description: <br>
Ampere AI Agent Marketplace for OpenClaw. Browse and install free & paid agents across developer tools, automation, research, content, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[himanshunextbase](https://clawhub.ai/user/himanshunextbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to search the Ampere marketplace, inspect available free and paid agent skills, preview selected packages, and install approved skills locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to search an external marketplace and install remote ZIP packages into persistent OpenClaw skills. <br>
Mitigation: Install only after user approval, preview the SKILL.md content, review the full archive contents, and extract to a temporary review folder before copying approved files into OpenClaw. <br>
Risk: Marketplace searches and paid-agent downloads may expose search intent or an Ampere API key to the external Ampere API. <br>
Mitigation: Avoid sensitive marketplace searches, protect AMPERE_API_KEY, and send the key only for paid-agent download URL requests. <br>
Risk: Downloaded agent packages may contain behavior that is not visible from the marketplace listing alone. <br>
Mitigation: Review and scan each package before deployment and do not run setup commands automatically. <br>


## Reference(s): <br>
- [Ampere Marketplace Skill Page](https://clawhub.ai/himanshunextbase/ampere) <br>
- [Ampere Marketplace API](https://api.agentplace.sh/marketplace/agents) <br>
- [Publisher Profile](https://clawhub.ai/user/himanshunextbase) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include marketplace result summaries, SKILL.md previews, installation steps, API key setup guidance, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.2.0 and artifact _meta.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
