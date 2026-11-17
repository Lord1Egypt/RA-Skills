## Description:

Pre-publish AI-flavor gatekeeper for Chinese long-form articles (公众号/自媒体评论). Detects and removes AI-writing tells using 1,108 rules that were A/B-validated on 52 real Tencent Zhuque detector-labeled fragments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrestneo](https://clawhub.ai/user/forrestneo)

### License/Terms of Use:

MIT

## Use Case:

Authors, editors, and publishing teams use this skill to check Chinese long-form commentary drafts before publication, identify AI-writing tells, and receive concrete repair guidance. It is scoped to Chinese self-media commentary and is not intended for fiction, academic, legal, or English-language writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is explicitly designed to help Chinese articles pass AI-detection and platform review.

Mitigation: Review before installation and use only for legitimate editing, transparency, factual accuracy, and style quality; do not use it to disguise AI-generated work where disclosure is required.

Risk: The workflow can encourage an external detector pass/fail loop.

Mitigation: Keep detector checks limited to appropriate editorial validation and avoid using them as a way to evade platform, publisher, reader, or reviewer disclosure requirements.

## Reference(s):

- [Server-resolved source repository](https://github.com/forrestneo/anti-ai-foolish)
- [ClawHub skill page](https://clawhub.ai/forrestneo/skills/anti-ai-foolish)
- [English README](README.en.md)
- [Methodology and Evidence Chain](references/方法论与证据链.md)
- [Evaluation Report](references/评测报告.md)
- [Project Roadmap](references/ROADMAP.md)
- [Rule Index](rules/INDEX.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with command-line preflight and scanner guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may recommend iterative article edits and external chunked detector checks for Chinese commentary drafts.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
