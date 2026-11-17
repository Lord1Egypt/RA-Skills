## Description:

Helps agents use the 百炼®标书 cloud service to interpret tender files, generate bid-document drafts, review bid compliance, and compare bid files for duplicate or similarity risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement or bid teams use this skill to process legally held tender and bid documents through the 百炼®标书 service. It supports structured tender interpretation, generated .docx bid drafts, compliance-risk reports, and 2-3 bid-file similarity checks.

### Deployment Geography for Use:

Global; workflow language and report terminology are Simplified Chinese and oriented toward mainland-China procurement conventions.

## Known Risks and Mitigations:

Risk: Tender and bid documents may contain sensitive commercial, pricing, personal, or procurement information and are uploaded to the vendor cloud service for processing.

Mitigation: Use only with documents the user is authorized to process, obtain informed consent before upload, and verify the vendor retention and account-management expectations before deployment.

Risk: The skill relies on a full account API key stored in a local skill-level config file.

Mitigation: Have users create and protect the config file themselves, avoid placing credentials in chat or links, restrict file permissions, and rotate the key if exposure is suspected.

Risk: Bid generation, compliance review, and duplicate checking can consume a paid word balance and may stop when balance is insufficient.

Mitigation: Confirm cost expectations before paid operations, surface balance and partial-output status clearly, and avoid retrying or restarting long jobs without user approval.

Risk: Generated bid drafts, compliance findings, and similarity results can be incomplete, stale, or legally non-determinative.

Mitigation: Require human review before submission, preserve unresolved placeholders for unknown company or bid details, and present duplicate or compliance findings as internal risk signals rather than legal conclusions.

Risk: The release includes vendor-controlled promotional signup and recharge links.

Mitigation: Treat those links as third-party commercial material, do not forward credential-bearing bind links, and disclose the vendor relationship to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-turbo)
- [Publisher Profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 Service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API Overview](references/api.md)
- [Authentication, Jobs, and Word Balance API](references/api-auth.md)
- [Tender Interpretation and Bid Generation API](references/api-bid-workflow.md)
- [Bid Compliance Review API](references/api-compliance.md)
- [Bid Duplicate Check API](references/api-duplicate.md)
- [Knowledge Base Field Reference](references/knowledge-fields.md)
- [Operational Usage Guide](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Conversational text plus generated HTML, Word, JSON, and .docx report or bid-document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local report paths, short-lived download links, risk summaries, progress updates, and generated bid-document drafts.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
