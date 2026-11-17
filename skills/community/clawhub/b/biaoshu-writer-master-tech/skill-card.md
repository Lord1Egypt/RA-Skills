## Description:

全行业标书智能生成大师 helps agents use the 百炼®标书 service to interpret tender files, generate finished bid documents, run bid compliance reviews, and compare bid documents for similarity risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users, procurement teams, and bid-writing teams use this skill to process local tender and bid documents through the 百炼®标书 cloud service. It supports tender interpretation, finished .docx bid generation, compliance review, and bid-document similarity checks before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential tender and bid documents are uploaded to the vendor service under the user's API key.

Mitigation: Use only with documents the user is authorized to process, obtain upload consent before execution, and account for vendor-side retention of task data and outputs.

Risk: API key exposure could permit unauthorized account use or billing-impacting actions.

Mitigation: Keep the API key in the local skill configuration only, do not paste it in chat, and do not forward links or logs that may contain credential-bearing parameters.

Risk: Local output path or basename choices may write files outside the expected workspace until patched.

Mitigation: Use the default output directory or trusted explicit paths, and avoid arbitrary custom output paths or custom basenames.

Risk: Bid generation, review, and similarity results may affect procurement decisions but can still require expert judgment.

Mitigation: Treat generated documents, compliance findings, and similarity checks as drafting and review aids; have qualified reviewers verify final submissions and legal or procurement conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-master-tech)
- [Publisher Profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 Open API Overview](references/api.md)
- [API Authentication, Jobs, and Billing](references/api-auth.md)
- [Tender Interpretation and Bid Generation API](references/api-bid-workflow.md)
- [Bid Compliance Review API](references/api-compliance.md)
- [Bid Similarity Check API](references/api-duplicate.md)
- [Knowledge Base Fields](references/knowledge-fields.md)
- [Execution Usage Guide](references/usage.md)
- [百炼®标书 Service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses, JSON API results, HTML or Word reports, and DOCX bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided 百炼®标书 API key. User-supplied tender and bid documents are uploaded to the vendor service, and task results or generated DOCX outputs may expire after about 7 days.]

## Skill Version(s):

3.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
