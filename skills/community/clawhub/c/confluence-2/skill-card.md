## Description: <br>
Provides Confluence Cloud integration for browsing spaces and pages, managing pages, labels, comments, child pages, and running CQL search through MorphixAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent browse Confluence Cloud spaces, retrieve and manage pages, labels, comments, child pages, and search content with CQL after linking a Confluence account through MorphixAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify content in the linked Confluence workspace. <br>
Mitigation: Install only if you trust the MorphixAI plugin, use the least-privileged account or workspace possible, follow organizational approval rules, and require explicit confirmation before creating, updating, labeling, commenting on, or deleting shared pages. <br>
Risk: The skill requires a MorphixAI API key and a linked Confluence account. <br>
Mitigation: Provide MORPHIXAI_API_KEY through the environment and link only the Confluence account needed for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paul-leo/confluence-2) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with shell commands and YAML-like tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Confluence account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
