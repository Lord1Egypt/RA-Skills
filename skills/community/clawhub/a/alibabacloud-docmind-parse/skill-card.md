## Description: <br>
Alibaba Cloud DocMind document parsing skill for converting PDFs, Office files, images, and other supported documents into structured Markdown, JSON, or HTML through V2 direct API or Alibaba Cloud POP invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to parse user-provided documents, extract text, tables, images, and layout data, and return the parsed content in Markdown, JSON, or HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive documents to Alibaba Cloud during parsing. <br>
Mitigation: Use it only with documents the user is comfortable sending to Alibaba Cloud and confirm data sensitivity before invoking the parser. <br>
Risk: The default V2 direct endpoint path may use unencrypted HTTP. <br>
Mitigation: Prefer an explicit HTTPS DOCMIND_V2_ENDPOINT before using V2 direct mode. <br>
Risk: Automatic POP routing can use the default Alibaba Cloud credential chain and associated billing account. <br>
Mitigation: Verify the selected credentials and billing account, and use the documented least-privilege RAM policy for DocMind access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-docmind-parse) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Alibaba Cloud DocMind console](https://docmind.console.aliyun.com/doc-overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or HTML document parsing results with optional command-line and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write parsed output to stdout or to a user-specified output file.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
