## Description: <br>
Integrates with Craft.do to automate tasks, manage documents and folders, edit markdown content, and migrate selected Obsidian vault notes through the Craft REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomtanstudio](https://clawhub.ai/user/atomtanstudio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to operate Craft.do through its REST API, automate task and document workflows, and migrate selected Obsidian vault notes into Craft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can erase broad Craft workspace content by deleting user-created folders and moving documents to trash. <br>
Mitigation: Back up Craft first, test in a non-critical workspace, and run cleanup only when the operator explicitly intends to remove workspace content. <br>
Risk: The skill requires a Craft API key and can upload selected vault note content to Craft. <br>
Mitigation: Store the API key securely, scope usage to intended vaults and workspaces, and review notes before migration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/atomtanstudio/craft-do) <br>
- [Craft API Documentation](https://craft.do/api) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Guide](artifact/SKILL.md) <br>
- [Craft API helper script](artifact/craft-api.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and shell script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Craft API credentials in environment variables and may create, update, move, or delete Craft workspace content through API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
