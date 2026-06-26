## Description: <br>
Cnki is a unified CNKI research workflow for literature search, advanced search, paper detail lookup, downloads, citation export, journal search, and table-of-contents access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to search CNKI, inspect paper metadata, download permitted PDF or CAJ files, and export citations to Zotero, RIS, or GB/T 7714 formats through a Chrome session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a Chrome session that may be logged into CNKI and can interact with private or institution-linked research access. <br>
Mitigation: Use it only in a Chrome profile you are comfortable delegating to the agent, and confirm the active account and access scope before downloads or exports. <br>
Risk: Downloads, RIS files, and Zotero exports can create local files or records outside the chat transcript. <br>
Mitigation: Confirm the browser download location, RIS destination, and Zotero collection or export scope before running batch operations. <br>
Risk: CNKI may require login, download permissions, or manual captcha completion for protected operations. <br>
Mitigation: Complete captcha challenges manually and verify account permissions before retrying failed download or export actions. <br>


## Reference(s): <br>
- [ClawHub Cnki release page](https://clawhub.ai/jirboy/cnki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with structured result lists, browser action guidance, downloaded PDF or CAJ files, RIS files, Zotero exports, and GB/T 7714 citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome with chrome-devtools MCP; CNKI login, download permissions, and manual captcha completion may be required for protected actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
