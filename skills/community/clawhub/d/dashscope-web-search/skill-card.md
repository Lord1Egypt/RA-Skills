## Description: <br>
Searches the web in real time with DashScope Qwen, returning cited text results and optional image markdown for current or source-specific queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oreo992](https://clawhub.ai/user/Oreo992) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask agents for current web information, fact checks, source-specific research, recent results, and optional visual references through DashScope Qwen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to DashScope/Qwen under the user's API key. <br>
Mitigation: Do not submit secrets, credentials, private customer data, regulated data, or internal documents unless the query is redacted and explicitly approved. <br>
Risk: Broad automatic-use guidance can trigger external search for more user requests than intended. <br>
Mitigation: Review activation rules before installation and narrow them to the organization's approved web-search use cases. <br>
Risk: Third-party data handling is not fully disclosed in the artifact. <br>
Mitigation: Confirm DashScope/Qwen data handling and credential-scope requirements before using the skill with sensitive or business-critical queries. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Oreo992/dashscope-web-search) <br>
- [Publisher Profile](https://clawhub.ai/user/Oreo992) <br>
- [DashScope](https://dashscope.aliyuncs.com/) <br>
- [DashScope Console](https://dashscope.console.aliyun.com/) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with numbered citations; image mode can include Markdown image links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source lists, numbered citations, optional image links, and optional thinking-tag content returned by DashScope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
