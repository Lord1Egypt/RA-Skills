## Description:

Helps agents upload tender and bid documents to the 百炼标书 service for AI-assisted tender interpretation, bid-document generation, compliance review, and duplicate-risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate tender requirements, generate bid documents, review bid compliance risks, and compare bid files for similarity before submission. It is intended for workflows where users can provide local tender or bid files and a 百炼标书 API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files may contain confidential business data and are uploaded to the vendor service for processing.

Mitigation: Use the skill only after confirming the user understands and accepts vendor processing and retention terms for the documents.

Risk: The API key is a credential for the user's 百炼标书 account.

Mitigation: Keep config.json private, avoid sharing or echoing the API key in chat, and rotate the key through the service if exposure is suspected.

Risk: Local metadata such as document names, job IDs, and project IDs may remain in ~/.zcm/projects.json.

Mitigation: Review or remove the local metadata file when those identifiers should not persist after use.

Risk: Custom report basenames or output directories can affect local file writes.

Mitigation: Use trusted output paths and avoid untrusted report names or directories.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-read)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API overview](references/api.md)
- [Authentication, jobs, and billing](references/api-auth.md)
- [Tender interpretation and bid-document workflow](references/api-bid-workflow.md)
- [Compliance review API](references/api-compliance.md)
- [Duplicate-risk API](references/api-duplicate.md)
- [Knowledge-base fields](references/knowledge-fields.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, JSON API results, local HTML or Word reports, and generated .docx bid documents or short-lived download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include risk summaries, report file paths, progress updates, account word-balance notices, and credential-setup guidance.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
