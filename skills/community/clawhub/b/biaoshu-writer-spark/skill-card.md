## Description:

This skill helps agents process tender and bid documents through the BaiLian bidding platform, including structured tender interpretation, generated bid documents, compliance review, and similarity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, bidding, and proposal teams use this skill to interpret authorized tender files, generate draft bid documents, review bid submissions for risk, and compare two or three bid documents for similarity indicators. The skill sends user-provided files to the BaiLian bidding cloud API and requires the user's own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive procurement documents and bid credentials.

Mitigation: Use it only with documents the user is authorized to process, prefer a dedicated revocable API key, and keep the key in the skill-local configuration file rather than in chat.

Risk: Generated bid documents, compliance findings, and similarity findings may influence procurement decisions.

Mitigation: Treat outputs as drafting and review assistance; have qualified users verify legal, commercial, and submission-critical content before use.

Risk: Paid generation, review, or duplicate-check tasks can consume the API key owner's word entitlement.

Mitigation: Confirm billed generation or review actions before submission and make expected consumption clear when the workflow provides an estimate.

Risk: Local persistence may retain tender filename metadata, generated reports, and the skill-local API-key configuration.

Mitigation: Use a controlled output directory, restrict permissions on local configuration, and remove retained artifacts when they are no longer needed.

Risk: Untrusted prompts or document content could try to steer arbitrary local output paths.

Mitigation: Keep reads and writes limited to user-authorized files and the configured skill output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-spark)
- [BaiLian bidding platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API overview](artifact/references/api.md)
- [Authentication, jobs, and word entitlement API](artifact/references/api-auth.md)
- [Tender interpretation and bid-document generation API](artifact/references/api-bid-workflow.md)
- [Bid compliance review API](artifact/references/api-compliance.md)
- [Bid similarity check API](artifact/references/api-duplicate.md)
- [Knowledge-base fields](artifact/references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses, JSON summaries, HTML or Word reports, generated .docx bid documents, and short-lived download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs use Simplified Chinese labels for bidding terminology and may include locally written reports under the skill output directory.]

## Skill Version(s):

1.0.15 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
