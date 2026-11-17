## Description:

Use when correcting Chinese ill-formed sentences with punctuation-focused errors (comma,顿号,分号,冒号,问号,叹号,引号,书名号,括号,省略号,破折号), including mixed punctuation-and-grammar cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catchfishcat](https://clawhub.ai/user/catchfishcat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content editors use this skill to correct Chinese sentences with punctuation-focused errors while preserving meaning and making only minimal edits. It can return corrected text directly or provide a short issue-by-issue explanation when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chinese punctuation conventions can vary across simplified Chinese, Taiwan, Hong Kong, publication-specific, or custom style guides.

Mitigation: Tell the agent which convention to follow when GB/T-style simplified Chinese punctuation rules should not be the default.

Risk: Punctuation edits in ambiguous sentences can unintentionally alter meaning or tone.

Mitigation: Use minimal edits, preserve original wording where possible, and request explanations or low-confidence notes for uncertain corrections.

## Reference(s):

- [Chinese Punctuation Rules for Sentence Correction](references/punctuation_rules.md)
- [National Language Commission punctuation query system](https://gf.ywky.edu.cn/punctuation_cn_text)
- [ClawHub skill page](https://clawhub.ai/catchfishcat/skills/chinese-punctuation-sentence-correction)
- [ClawHub publisher profile](https://clawhub.ai/user/catchfishcat)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text by default; Markdown explanation when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Corrected Chinese text only by default; explanations use original sentence, issue type, correction, and rationale.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
