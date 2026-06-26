## Description: <br>
Guides Chinese writing tasks through setup questions, staged drafting, multi-critic debate, arbitration, and substantive revision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agent users use this skill to produce formal or semi-formal Chinese articles, reports, analyses, proposals, posts, and emails through a structured collaborative drafting workflow. It is most useful when the user wants iterative critique and revision rather than a quick one-shot draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill strongly prefers a full multi-step workflow, which can slow tasks where the user only wants a quick draft. <br>
Mitigation: Enable it for deliberate writing and revision work, and avoid enabling it globally when fast one-shot drafting is the normal expectation. <br>
Risk: The workflow is written for Chinese output and may be a poor fit when users expect non-Chinese writing by default. <br>
Mitigation: Use it for zh-CN writing tasks or explicitly clarify the target language before drafting. <br>
Risk: Persona-based critic debate can make stylized viewpoints sound authoritative. <br>
Mitigation: Treat critic statements as creative writing critique and review factual claims, quotations, and attributions before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/critical-writing) <br>
- [Critic style and debate pairing guide](artifact/references/critics.md) <br>
- [README](artifact/README.md) <br>
- [Test cases](artifact/tests/test-cases.md) <br>
- [Product review example](artifact/examples/example-product-review.md) <br>
- [Debate session example](artifact/examples/example-debate-session.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Chinese Markdown with planning notes, staged draft sections, debate critique, arbitration conclusions, and revised prose.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow prefers full setup, planning, debate, and revision steps, and may be too rigid for quick one-shot drafting.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
