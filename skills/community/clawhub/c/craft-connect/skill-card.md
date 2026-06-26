## Description: <br>
Read and write Craft documents via the Craft Connect API, including documents, blocks, folders, tasks, collections, comments, and rich formatting through curl-based API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HWnex](https://clawhub.ai/user/HWnex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate on a Craft workspace: discovering content, searching documents, creating and editing notes, managing folders, tasks, collections, comments, uploads, and rich block formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify a user's Craft workspace, including documents, folders, tasks, collections, comments, and uploaded files. <br>
Mitigation: Install only when workspace access is intended, review planned changes before execution, and require explicit confirmation before uploads, schema changes, moves, or deletes. <br>
Risk: CRAFT_API_URL contains an embedded Craft Connect link token that grants access to the connected workspace. <br>
Mitigation: Keep CRAFT_API_URL private, store it in protected secret storage when possible, and avoid committing it into shared notes or repositories. <br>
Risk: Broad document searches and reads may expose more workspace content than needed for a user request. <br>
Mitigation: Review broad searches before running them and narrow search terms, folders, locations, or document IDs whenever possible. <br>
Risk: Some write operations have high impact, including permanent block deletion and collection schema replacement. <br>
Mitigation: Prefer reversible document operations where available, fetch current schemas before collection writes, and confirm destructive block or schema actions explicitly. <br>


## Reference(s): <br>
- [Craft Formatting Cheatsheet](references/formatting-cheatsheet.md) <br>
- [Craft Connect release page](https://clawhub.ai/HWnex/craft-connect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl commands, JSON request bodies, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CRAFT_API_URL with an embedded Craft Connect link token and curl for HTTP requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
