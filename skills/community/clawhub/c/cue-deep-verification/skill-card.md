## Description:

Uses Cue's deep verification scene to run multi-source public-data research that checks claims, business records, intellectual property, addresses, financial-statement notes, counterparty qualifications, and research-report credibility, producing source-linked verification notes with evidence chains and red flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Cue deep-research workflows for verification and due-diligence tasks, including fact checks, company records, address validation, financial-note risk review, counterparty qualification checks, and research-report credibility checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to download or update third-party runner code under ~/.cue and execute it with access to a local Cue API key.

Mitigation: Prefer a pinned, preinstalled, audited Cue runner before use, and review any code update path before allowing execution.

Risk: Deep research runs consume Cue credits and may send the user's query to Cue.

Mitigation: Require explicit confirmation for the selected buddy, subject, and credit-consuming run before execution.

Risk: Generated reports may be incomplete and are limited to public data; they do not replace legal, underwriting, or due-diligence review.

Mitigation: Keep source links intact, treat the report as a verification draft, and independently review high-impact findings before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-deep-verification)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [cue-skills runner repository](https://github.com/sensedeal/cue-skills)
- [cue-skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep research runs may take 3-15 minutes, consume Cue credits, and should preserve source links in the final report.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
