## Description:

Helps agents process tender and bid documents by uploading user-authorized files to the Bailian bid-writing service for tender interpretation, bid document generation, compliance review, and similarity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bid teams use this skill to interpret tender requirements, generate draft bid documents, review bid compliance, and compare bid files for similarity before submission. The skill is intended for workflows where the user can authorize cloud processing of confidential tender and bid files under their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential tender and bid documents are uploaded to the vendor service for processing and retained temporarily under the user's API-key account.

Mitigation: Use the skill only after confirming the user has authority to upload the files and accepts the service retention and billing model.

Risk: The API key grants account access for billed operations.

Mitigation: Store the key only in the skill-local config file with restrictive permissions and do not paste, echo, or pass it through chat or command-line arguments.

Risk: Local project metadata may be retained in ~/.zcm/projects.json.

Mitigation: Review or clear that metadata when project names, job IDs, or tender filenames should not remain on the local machine.

Risk: User-supplied output paths could overwrite important local files.

Mitigation: Prefer the skill's default output directory and review explicit output paths before writing generated reports or documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-corp-pro)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [Bailian bid-writing platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [API overview](references/api.md)
- [Authentication, jobs, and billing](references/api-auth.md)
- [Tender interpretation and bid generation API](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid similarity check API](references/api-duplicate.md)
- [Knowledge base field guide](references/knowledge-fields.md)
- [Agent usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, progress/status text, JSON summaries, generated HTML or Word reports, and generated DOCX bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a skill-local API key configuration; generated reports and documents may be written to a local output directory or delivered through short-lived service download links.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
