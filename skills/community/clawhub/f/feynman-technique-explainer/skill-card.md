## Description:

Explain any concept using the Feynman Technique, plain language, a real-world analogy, a concrete example, and a comprehension quiz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and learners use this skill to turn a single concept into a plain-language explanation, analogy, concrete example, and short comprehension quiz. It is best suited for foundational understanding rather than deep technical study or document summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause generic explanation requests to use this simplified teaching format even when the user did not explicitly request the skill.

Mitigation: Enable it when Feynman-style explanations are desired by default, and review trigger behavior in the target agent before release.

Risk: Plain-language simplification can omit technical depth that expert users may expect.

Mitigation: Use it for foundational understanding, and route explicit expert-level, derivation, retrieval, or document-summary requests to a more suitable response mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/feynman-technique-explainer)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with labelled explanation sections and a numbered comprehension quiz]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to stay concise, use plain language, include one analogy limit statement, and withhold quiz answers until the user responds.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
