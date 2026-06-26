## Description: <br>
Search markdown knowledge bases efficiently using qmd. Use this when searching Obsidian vaults or markdown collections to find relevant content with minimal token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anshumanbh](https://clawhub.ai/user/anshumanbh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to search local markdown knowledge bases, including Obsidian vaults and markdown collections, and retrieve relevant snippets and file paths without loading full files into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing qmd with a global bun command introduces trust and supply-chain risk from an external CLI repository. <br>
Mitigation: Verify that the qmd GitHub repository and global bun install path are trusted before installing or running setup commands. <br>
Risk: Indexing markdown folders can expose private notes or sensitive local content to future searches. <br>
Mitigation: Add only markdown folders that are appropriate to make searchable, review returned file paths before reading full files, and check qmd documentation for index and embedding storage or deletion behavior. <br>


## Reference(s): <br>
- [qmd GitHub repository](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise search-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relevant snippets, file paths, collection names, and setup steps depending on whether qmd and a collection are already available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
