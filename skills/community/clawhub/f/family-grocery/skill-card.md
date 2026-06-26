## Description: <br>
Shared family grocery list — multiple members add, remove, and view items organized by store, with admin-managed access and optional web verification for store addresses and item availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adeydas](https://clawhub.ai/user/adeydas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Family members use this skill to maintain a shared grocery list, organize items by store, manage household access, and review change history. An admin configures the shared local data path, users, primary store, fallback order, and category-to-store mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household grocery data is stored in a shared local folder. <br>
Mitigation: Use a dedicated shared folder with appropriate operating-system permissions and avoid sensitive directory paths. <br>
Risk: Access control depends on stored agent name and path values, so a user who can set those values may impersonate a family member. <br>
Mitigation: Have the intended admin perform setup first, register only trusted users, and keep shared-path access limited to the household members who should use the list. <br>
Risk: Web search may not confirm store addresses, hours, or item availability. <br>
Mitigation: Treat web results as optional confirmation, ask the user to verify uncertain store details, and proceed without blocking list actions when search is unavailable. <br>


## Reference(s): <br>
- [Family Grocery ClawHub release](https://clawhub.ai/adeydas/family-grocery) <br>
- [Data file templates](memory-template.md) <br>
- [List operations](lists.md) <br>
- [Store management](stores.md) <br>
- [User management](user-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with occasional shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces grocery-list updates, store and user management guidance, local shared-folder file changes, and concise confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
