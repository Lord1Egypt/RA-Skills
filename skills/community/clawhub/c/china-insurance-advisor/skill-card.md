## Description:

China Insurance Advisor is a thin proxy to the remote 中国保险顾问 web chat at whylingxi.cn for insurance planning, product comparison, budget allocation, and insurance Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpb123](https://clawhub.ai/user/lpb123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to forward Chinese insurance planning, product comparison, budget allocation, and Q&A requests to a remote insurance advisor while preserving session continuity when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insurance questions are sent to whylingxi.cn and may include personal, financial, medical, or policy details.

Mitigation: Avoid unnecessary identifiers, policy numbers, payment details, medical documents, and other sensitive personal data.

Risk: Session mode preserves conversation continuity through a local-to-upstream session mapping.

Mitigation: Use reset or avoid session mode when continuity is not needed.

Risk: The remote service can fail, time out, or change its response contract.

Mitigation: Report the remote advisor as temporarily unavailable and do not fabricate product names, prices, or planning results.

## Reference(s):

- [Integration Notes](artifact/integration-notes.md)
- [Remote insurance advisor chat endpoint](https://whylingxi.cn/chat)
- [ClawHub skill page](https://clawhub.ai/lpb123/skills/china-insurance-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown returned from the remote insurance advisor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve upstream tables, product names, prices, links, and session-continuity context.]

## Skill Version(s):

3.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
