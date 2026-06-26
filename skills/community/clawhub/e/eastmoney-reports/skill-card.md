## Description: <br>
Queries and downloads Dongfang Caifu research reports, including industry, stock, strategy, macro, and broker morning reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manymore13](https://clawhub.ai/user/manymore13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research analysts use this skill to query Eastmoney report listings, find industry codes, export report metadata, and download selected PDFs through command-line or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executable Python code was not included in the scanned package. <br>
Mitigation: Review the external repository and dependencies before installing or running the tool. <br>
Risk: The skill can save many PDF files locally, especially when bulk download options are used. <br>
Mitigation: Use an explicit output directory, start with small download limits, and use bulk downloads only when intentionally saving many reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manymore13/eastmoney-reports) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save CSV/Excel exports and downloaded PDF files to a user-specified local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
