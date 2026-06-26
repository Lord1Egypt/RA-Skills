## Description: <br>
以文言文压缩输出、节省 token。当用户要求文言回复、节省 token、省输出时触发。支持三档：极致(/e/Extreme)、适度(/m/Medium)、轻微(/l/Light)。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u5bf](https://clawhub.ai/user/u5bf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make agent replies more concise by rewriting suitable responses into compressed Classical Chinese while preserving code, paths, proper nouns, error messages, formulas, numbers, versions, and markup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heavy compression can obscure nuance in medical, legal, financial, safety, debugging, or other clarity-sensitive responses. <br>
Mitigation: Use /l or avoid compression when clarity is more important than saving tokens. <br>
Risk: Classical Chinese rewriting may omit connective detail or alter emphasis in complex explanations. <br>
Mitigation: Lower the compression level for complex logic and preserve technical content such as code, paths, proper nouns, error messages, formulas, numbers, versions, and markup exactly. <br>


## Reference(s): <br>
- [Compression Rules](references/compression_rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/u5bf/classicalchinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text, depending on the agent response being compressed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports three explicit compression levels: /e for extreme, /m for medium, and /l for light; responses may include an estimated character-reduction note.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
