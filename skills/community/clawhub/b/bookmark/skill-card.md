## Description: <br>
Search and browse the Shuqianlan bookmark library by keyword, latest updates, categories, articles, or links in read-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer user requests for Shuqianlan bookmark searches, latest articles, top categories, category articles, and category links. It is intended for users who want read-only bookmark lookup results returned as direct, link-preserving responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user can direct the script to a non-default bookmark source URL, which could send read-only requests to an untrusted or sensitive endpoint. <br>
Mitigation: Use the default Shuqianlan source unless the user explicitly trusts another public URL, and do not point the base URL override at internal or sensitive services. <br>


## Reference(s): <br>
- [Shuqianlan](https://shuqianlan.com) <br>
- [ClawHub Bookmark Skill](https://clawhub.ai/jvy/bookmark) <br>
- [openclaw-server Bookmark Map](references/openclaw-server-bookmark-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with links and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookup output; result count and page can be adjusted with command flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
