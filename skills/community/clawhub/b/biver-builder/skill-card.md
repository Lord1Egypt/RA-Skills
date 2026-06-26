## Description: <br>
Integration skill for the Biver Landing Page Builder API for managing landing pages, domains, products, forms, gallery assets, workspace settings, branding, and AI-generated page or section content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RamaAditya49](https://clawhub.ai/user/RamaAditya49) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through Biver landing page administration, including page creation, publishing, domain setup, product and form management, asset upload, workspace configuration, and AI-assisted page generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through live publishing, deletion, domain changes, gallery deletion, and workspace updates. <br>
Mitigation: Require explicit user confirmation before these operations and use test or read-only API keys until the workflow is reviewed. <br>
Risk: Permission scoping is unclear for some documented Biver operations. <br>
Mitigation: Verify exact API key scopes in the Biver dashboard and grant only the minimum read or write scopes required for the current task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RamaAditya49/biver-builder) <br>
- [Publisher profile](https://clawhub.ai/user/RamaAditya49) <br>
- [Declared repository](https://github.com/RamaAditya49/biver-builder) <br>
- [Biver API base URL](https://api.biver.id) <br>
- [Biver dashboard](https://biver.id/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code examples, API request snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIVER_API_KEY for authenticated Biver operations; BIVER_API_BASE_URL is optional.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
