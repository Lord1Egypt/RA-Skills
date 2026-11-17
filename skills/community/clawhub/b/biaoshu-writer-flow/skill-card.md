## Description:

Helps users process authorized tender and bid files through the Bailian bid-document service for tender interpretation, .docx bid generation, compliance review, and bid-document similarity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement and bidding users use this skill to interpret tender files, generate finished bid documents, review bid compliance, and compare 2-3 bid documents for similarity risks. It is intended for files the user is authorized to upload and process with the vendor service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive procurement files are uploaded to the vendor service and may remain in the vendor account for about 7 days.

Mitigation: Use only files the user is authorized to share, obtain consent before upload, and avoid uploading confidential material outside approved procurement workflows.

Risk: Security evidence says the skill under-enforces local file/output boundaries and stores project metadata outside the disclosed directory.

Mitigation: Review output path constraints and disclose or move the local metadata store before deployment.

Risk: Bid generation, compliance review, and duplicate checking can consume paid account word balance.

Mitigation: Confirm chargeable workflows and expected usage with the user before starting paid actions.

Risk: Security evidence notes a forced channel-tagged platform link and branding.

Mitigation: Make the channel tagging optional or clearly disclose it to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-flow)
- [Open API dispatch reference](artifact/references/api.md)
- [Usage guide](artifact/references/usage.md)
- [API authentication, jobs, and word balance](artifact/references/api-auth.md)
- [Bid workflow API reference](artifact/references/api-bid-workflow.md)
- [Compliance review API reference](artifact/references/api-compliance.md)
- [Duplicate-check API reference](artifact/references/api-duplicate.md)
- [Knowledge fields reference](artifact/references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, CLI progress text, JSON API results, HTML/DOCX reports, and .docx bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files and task results may remain in the vendor account for about 7 days.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
