## Description:

This skill helps B2B, SaaS, customer success, and marketing teams turn authorized customer interviews into customer-case video briefs, testimonial segments, scripts, AI-HIVE generation commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, customer success, SaaS, and B2B teams use this skill to convert authorized interview material, customer background, public facts, brand rules, and channel constraints into reviewable customer-case video plans and assets. Developers and operators can also use its helper scripts to create project blueprints, process video files, query AI-HIVE models, submit generation tasks, poll task status, and download outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real API keys or business media could be exposed or sent to an untrusted service if users set custom endpoints or mishandle credentials.

Mitigation: Use the official AI-HIVE endpoint unless the alternative server is fully trusted, keep API keys out of logs and repositories, and review configuration before uploads.

Risk: Generation tasks may incur costs, upload media without sufficient rights, or overwrite existing output files.

Mitigation: Confirm final parameters and routing before paid calls, upload only media the user is allowed to share, and choose output paths carefully.

Risk: Customer names, logos, claims, or testimonial statements could be misleading if not backed by permission and evidence.

Mitigation: Require authorization for customer material, mark uncertain facts for review, and avoid replacing real customer evidence with generated claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/customer-interview-case-video-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, plus optional JSON files, task records, and downloaded media paths from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default responses present a reviewable plan before potentially billable AI-HIVE generation calls; task records may include routing mode, model, pricing snapshot, taskId, status, and local file paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
