## Description: <br>
Guides an AI agent through browser and web-access routing, escalating from WebFetch and OpenCLI adapters to Firecrawl, agent-browser, browser-use, and anti-bot tools when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to choose cost-aware tools for searching, extracting, interacting with, and troubleshooting web pages, including sites that require cookies or JavaScript rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse browser login sessions and may export cookie state. <br>
Mitigation: Use it only for sites and accounts the operator is authorized to access, require confirmation before browser-cookie or internal-site access, and protect or delete exported cookie files after use. <br>
Risk: The skill includes anti-bot, proxy, and browser-fingerprinting guidance. <br>
Mitigation: Avoid anti-bot or proxy workflows unless the operator has permission for the target site and a legitimate testing or access purpose. <br>
Risk: Helper scripts have unsafe input handling according to the authoritative security evidence. <br>
Mitigation: Do not run helper scripts with untrusted URLs, search queries, platform names, or limits until the injection issues are fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/browser-ops) <br>
- [Routing Decision Tree](references/routing.md) <br>
- [Setup](references/setup.md) <br>
- [OpenCLI Usage Guide](references/opencli-usage.md) <br>
- [Cookie and Session State](references/state-management.md) <br>
- [Anti-Detection Strategies](references/anti-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-routing explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the extracted content, the tool path used, and failure reasons or next actions when a task cannot be completed.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
