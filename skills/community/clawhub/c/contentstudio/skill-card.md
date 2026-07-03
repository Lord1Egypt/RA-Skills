## Description: <br>
ContentStudio helps agents schedule social-media posts across Facebook, LinkedIn, Twitter/X, Instagram, YouTube, TikTok, Pinterest, Threads, Tumblr, Bluesky, and Google Business Profile, and manage posts, media, workspaces, accounts, campaigns, labels, categories, and team members through the ContentStudio CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contentstudio-official](https://clawhub.ai/user/contentstudio-official) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to automate ContentStudio social-media workflows from the terminal, including listing resources, creating or approving posts, uploading media, connecting accounts, and auditing workspace data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, approve, delete, upload, connect accounts, or delete content from social platforms through a real ContentStudio workspace. <br>
Mitigation: Review dry-run output first, confirm the workspace and target posts or accounts, and require explicit approval before mutating commands. <br>
Risk: Using the wrong active workspace can apply changes to the wrong ContentStudio account or social channels. <br>
Mitigation: Check the active workspace before mutations and ask the user to confirm whether to proceed there or select a different workspace. <br>
Risk: Bulk scripts or delete operations can amplify mistakes across many posts or accounts. <br>
Mitigation: Avoid copying bulk examples without adding a review step, paginate deliberately, and verify each destructive target before execution. <br>


## Reference(s): <br>
- [ContentStudio Skill on ClawHub](https://clawhub.ai/contentstudio-official/skills/contentstudio) <br>
- [ContentStudio API Guide](https://api.contentstudio.io/guide) <br>
- [ContentStudio API Docs](https://api.contentstudio.io/api-docs) <br>
- [contentstudio-cli npm Package](https://www.npmjs.com/package/contentstudio-cli) <br>
- [ContentStudio Website](https://contentstudio.io) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with contentstudio CLI commands and JSON-response handling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the contentstudio CLI and CONTENTSTUDIO_API_KEY. The skill emphasizes --json output, dry-run review for mutations, workspace confirmation, and pagination handling.] <br>

## Skill Version(s): <br>
1.0.10 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
