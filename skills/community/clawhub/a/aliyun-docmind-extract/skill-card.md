## Description: <br>
Use when working with Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results. Designed for Claude Code/Codex document understanding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect agent workflows to Alibaba Cloud Document Mind for asynchronous document parsing, including URL submission, local file upload examples, polling, and result capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses Alibaba Cloud credentials to send selected documents or URLs to DocMind for parsing. <br>
Mitigation: Use limited-scope Alibaba Cloud keys, confirm endpoint and region before use, and submit only documents approved for cloud processing. <br>
Risk: URL-based submission may expose confidential content through public or long-lived document links. <br>
Mitigation: Avoid confidential or long-lived public URLs unless approved; prefer controlled access patterns and remove temporary links when processing is complete. <br>
Risk: Saved outputs can contain private document content. <br>
Mitigation: Review, protect, or delete generated outputs and API response summaries according to the user's data handling requirements. <br>


## Reference(s): <br>
- [Source list](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-docmind-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit user-selected document URLs or file streams to Alibaba Cloud DocMind and save API response summaries or output artifacts when directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
