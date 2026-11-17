## Description:

Uploads tender and bid documents to 百炼®标书 to interpret tender requirements, generate finished .docx bid documents, review compliance risks, and compare bid files for similarity or duplication risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and bid teams use this skill to analyze tender files, draft bid-response documents, review submissions for disqualification and compliance risks, and compare multiple bid files for similarity concerns before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tender and bid files are uploaded to the vendor cloud service for processing.

Mitigation: Use only files the user is authorized to process, obtain explicit upload consent, and avoid using the skill for material that cannot leave the local environment.

Risk: The Api Key is a full account credential and paid workflows may consume the account's usable word balance.

Mitigation: Use a dedicated key, keep config.json private, never paste the key into chat, and confirm paid generation, compliance review, or duplicate-check steps before submission.

Risk: The security summary flags boundary concerns around local writes and project metadata.

Mitigation: Review configured output paths, avoid untrusted custom report names or paths, and inspect local project metadata if running in a shared environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-swift)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API overview](references/api.md)
- [Authentication and task API](references/api-auth.md)
- [Tender interpretation and bid-document workflow API](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid similarity and duplicate-check API](references/api-duplicate.md)
- [Usage guide](references/usage.md)
- [Knowledge-base field guide](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Conversational guidance plus generated HTML, Word, JSON, and .docx artifacts depending on workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Api Key; paid workflows may consume the account's usable word balance and generated task artifacts may expire after a limited retention period.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
