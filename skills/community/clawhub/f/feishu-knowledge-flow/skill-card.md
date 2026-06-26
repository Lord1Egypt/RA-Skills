## Description: <br>
This skill turns article links, pasted text, or chat content into structured summaries and archives them into a user's Feishu knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keson1521](https://clawhub.ai/user/keson1521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and researchers use this skill to capture public articles, drafts, or useful conversation insights as structured Feishu knowledge-base entries. It is designed for automated summarization, classification, document writing, and index updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically upload article summaries or chat-derived content to Feishu without a review step. <br>
Mitigation: Use it only for content you are authorized to store, and add a manual preview or confirmation step before writing sensitive, regulated, confidential, or copyrighted material. <br>
Risk: The workflow fetches web pages and may process content from external URLs. <br>
Mitigation: Avoid internal URLs, credentials, private documents, and confidential chat history unless the environment and destination workspace are approved for that data. <br>
Risk: The local .wiki-config and .wiki-tree files contain Feishu workspace, document, and node identifiers. <br>
Mitigation: Protect those files with normal secret-handling practices and avoid sharing them in public repositories or support logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keson1521/feishu-knowledge-flow) <br>
- [lark-cli](https://github.com/nicepkg/lark-cli) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, setup guidance, shell commands, and Feishu document updates via lark-cli.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public article pages, create temporary image files, update local Feishu configuration files, and write summarized content to the configured Feishu workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
