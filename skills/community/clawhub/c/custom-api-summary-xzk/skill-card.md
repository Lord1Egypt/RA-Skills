## Description: <br>
调用自定义摘要 API，对用户提供的文本进行处理并返回结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqq-github](https://clawhub.ai/user/heqq-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they explicitly ask an agent to summarize, extract key points from, or otherwise process supplied text through a custom summary API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for summarization is sent to an external API. <br>
Mitigation: Do not submit passwords, API keys, private documents, customer data, regulated information, or proprietary material unless the endpoint operator and its data handling are trusted and approved. <br>
Risk: The external API can be unavailable or return an error. <br>
Mitigation: Surface API failures clearly and avoid inventing a summary when the endpoint does not return a usable result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heqq-github/custom-api-summary-xzk) <br>
- [Custom summary API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON] <br>
**Output Format:** [JSON or plain text returned from the custom summary API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires non-empty user-provided text; external API failures should be surfaced instead of fabricated results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
