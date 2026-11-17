## Description:

以文言文压缩输出、节省 token。当用户要求文言回复、节省 token、省输出时触发。支持三档：极致(/e/Extreme)、适度(/m/Medium)、轻微(/l/Light)。

This skill is ready for commercial/non-commercial use.

## Publisher:

[u5bf](https://clawhub.ai/user/u5bf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to answer in concise Classical Chinese to reduce output length while preserving technical literals such as code, paths, URLs, logs, numbers, and markup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classical Chinese compression can reduce clarity for safety-critical, legal, medical, financial, or complex troubleshooting tasks.

Mitigation: Avoid using this skill for those tasks, or lower the compression level and ask for clear modern-language detail.

Risk: Compression may omit connective language that helps users follow multi-step reasoning.

Mitigation: Use the Light (/l) level or request a detailed explanation when clarity is more important than token reduction.

## Reference(s):

- [Compression rules](artifact/references/compression_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses, optionally ending with a concise compression note.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports three compression levels: Extreme (/e), Medium (/m, default), and Light (/l).]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
