## Description:

Uploads tender and bid documents to the 百炼®标书 service to interpret requirements, generate DOCX bid documents, review compliance risks, and compare 2-3 bid files for similarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to analyze procurement documents, prepare bid responses, review generated or existing bids for compliance issues, and check similarity risks across legally held bid files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential tender and bid materials are uploaded to and retained by the 百炼®标书 service.

Mitigation: Use only when the user is authorized to process the files with that service and accepts its server-side retention and account controls.

Risk: The API key controls billable operations tied to the user's account word balance.

Mitigation: Keep the key out of chat, store it only in the skill-local config file with restrictive permissions, and confirm paid generation or review actions before submitting them.

Risk: Security evidence flags under-scoped local write, persistence, path-containment, overwrite, and redirect-handling risks.

Mitigation: Prefer a contained output directory, avoid arbitrary output paths, review existing files before overwriting, and use only official service links until the publisher tightens these behaviors.

Risk: Security evidence flags instruction-priority language that may overreach.

Mitigation: Review the skill before installation and keep platform, system, and organizational policies ahead of the skill's internal operating guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-read-pro)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API dispatch guide](references/api.md)
- [Authentication, jobs, and billing APIs](references/api-auth.md)
- [Interpretation and bid-document workflow API](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid duplicate-check API](references/api-duplicate.md)
- [Usage workflow guide](references/usage.md)
- [Knowledge-base field guide](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, JSON API results, HTML or DOCX reports, and generated DOCX bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided local tender or bid files, a skill-local API key configuration, account word balance for paid operations, and time-limited download links for generated bid documents.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
