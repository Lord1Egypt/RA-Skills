## Description: <br>
Framer CRM API helps agents manage Framer CMS content through the Server API, including collection and item CRUD, image uploads, preview publishing, production deployment, and project asset management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berthelol](https://clawhub.ai/user/berthelol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to automate Framer CMS workflows from an agent, including creating or updating content, uploading assets, publishing previews, and deploying approved changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Framer site content, pages, redirects, custom code, publishing state, and deployment state beyond routine CMS edits. <br>
Mitigation: Require explicit user confirmation before deletes, bulk edits, page changes, redirects, code or custom-code changes, publishing, and deployment; show the preview or change summary before production deployment. <br>
Risk: The Framer API key is a sensitive project credential. <br>
Mitigation: Keep FRAMER_API_KEY in an environment variable or ignored .env file, and do not log, commit, screenshot, or share it. <br>
Risk: CMS item field updates can be silently ignored if field values are not wrapped in a fieldData object. <br>
Mitigation: Resolve field IDs before updates, wrap all CMS field values inside fieldData, and verify updated items after write operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/berthelol/framer-crm-api) <br>
- [CMS Operations Reference](references/cms-operations.md) <br>
- [Onboarding Flow](references/onboarding.md) <br>
- [Project Assets & Configuration](references/project-assets.md) <br>
- [Publishing & Deployment](references/publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, FRAMER_PROJECT_URL, and FRAMER_API_KEY; outputs should avoid exposing secrets and should ask for confirmation before destructive or live-site operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
