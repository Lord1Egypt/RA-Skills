## Description:

高数题库批量出题工作流：选章→撞车排查→生成→分布校验→双维度去重→入库→复核→归档

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, training teams, and question-bank maintainers use this skill to run a repeatable batch workflow for producing, deduplicating, importing, verifying, and archiving advanced mathematics question-bank updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can import approved batches or update progress records in a local question-bank repository when triggered in the wrong context.

Mitigation: Confirm the target repository path, batch number, chapters, and approval intent before running imports with --approved or updating MEMORY.md.

Risk: Question batches may contain duplicate or mathematically incorrect items if generation output is accepted without the workflow checks.

Mitigation: Run the documented q[:80] and normalized math-signature deduplication checks, verify solution scores sum to 10, and perform the post-import review before archiving a batch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daigxok/skills/gaoshu-questionbank-workflow)
- [ClawHub publisher profile](https://clawhub.ai/user/daigxok)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow instructions for batch generation, deduplication, import, verification, and archival.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
