## Description:

Generates Chinese weekly technical research reports on LLM and VLM applications in search, advertising, and recommendation systems, with optional synchronization of the Markdown report to an IMA knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fandywang87](https://clawhub.ai/user/fandywang87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical researchers, and product teams use this skill to compile weekly AI search, ads, and recommendation-system research reports, including paper tracking, trend summaries, comparative analysis, and follow-up reading lists. Teams can also upload the generated Markdown report to a configured IMA knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be uploaded on a schedule to a specified IMA knowledge base.

Mitigation: Review each generated report before enabling weekly automation or allowing upload.

Risk: IMA API credentials are stored locally and used for cloud uploads.

Mitigation: Use a least-privilege IMA key and restrict credential file permissions.

Risk: The upload flow invokes an external COS uploader path while using cloud credentials.

Mitigation: Verify or vendor the COS uploader before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fandywang87/skills/ai-recsys-weekly-report)
- [Research Scope](references/research-scope.md)
- [OneTrans](https://arxiv.org/abs/2510.26104)
- [MixFormer](https://arxiv.org/abs/2602.14110)
- [BlossomRec](https://arxiv.org/abs/2512.13368)
- [STRec](https://dl.acm.org/doi/10.1145/3604915.3608779)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated Markdown report and may upload it to a configured IMA knowledge base.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
