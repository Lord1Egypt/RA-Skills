## Description: <br>
Commerce content generator. Input a product brief, evidence, audience, and channel; output Xiaohongshu notes, Douyin scripts, ad/email/listing variants, and a claims checklist. Evidence-aware: does not invent unsupported claims and flags missing proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, commerce, and content teams use this skill to turn product briefs and supporting evidence into platform-specific commerce drafts for Xiaohongshu, Douyin, live selling, social posts, marketplace listings, and ads. It also produces quality notes that identify unsupported claims, risky phrases, missing evidence, and useful next-iteration data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated marketing copy can still be misleading if the input includes unsupported or regulated claims. <br>
Mitigation: Provide only product facts suitable for marketing use, keep proof points attached to concrete claims, and review outputs before publishing. <br>
Risk: Regulated categories such as health, finance, legal, children, food, or supplements can require stricter claim review. <br>
Mitigation: Use the quality checklist and remove or rewrite claims that lack reliable evidence or domain review. <br>


## Reference(s): <br>
- [Platform Playbook](references/platform-playbook.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON content packs with platform drafts, brief fields, and quality notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content is evidence-aware and may include assumptions, missing fields, risky claim flags, and next-iteration suggestions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence, package.json, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
