## Description: <br>
Routes Clawpage requests to workflows that create, update, publish, and manage Clawpage pages, dashboards, templates, data, links, blobs, stats, and SDK usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin-zhan](https://clawhub.ai/user/kevin-zhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to turn long or complex content into Clawpage web apps and dashboards, then publish or update those pages and related Clawpage resources. It also guides authenticated management of templates, data tables, short links, blobs, statistics, and browser SDK integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and use persistent Clawpage account credentials stored in keys.local.json. <br>
Mitigation: Confirm initialization before account creation, keep keys.local.json private, and never place sk_* tokens in page HTML or browser JavaScript. <br>
Risk: The skill runs the @clawpage.ai/cli npm runtime, which may be fetched dynamically. <br>
Mitigation: Pin @clawpage.ai/cli to an audited version before production use and trust the Clawpage service and CLI before running commands. <br>
Risk: The skill can publish externally accessible Clawpage content. <br>
Mitigation: Review generated content, page access settings, pagecode protection, and TTL before publishing or updating pages. <br>


## Reference(s): <br>
- [Clawpage Skill on ClawHub](https://clawhub.ai/kevin-zhan/clawpage-skill) <br>
- [Clawpage](https://clawpage.ai) <br>
- [@clawpage.ai/cli](https://www.npmjs.com/package/@clawpage.ai/cli) <br>
- [API quick reference](skills/clawpage-skill/references/api-quickref.md) <br>
- [Design guidelines](skills/clawpage-skill/references/design-guidelines.md) <br>
- [Prompt contracts](skills/clawpage-skill/references/prompt-contracts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with code snippets, CLI commands, local file changes, and structured URL fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishing workflows return URL fields such as publicUrl, rootUrl, accessUrl, pageId, and expiresAt when available.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
