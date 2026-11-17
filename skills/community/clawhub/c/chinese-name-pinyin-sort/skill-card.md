## Description:

Sorts Chinese names by pinyin using Chinese naming conventions, including surname pronunciation fixes, stroke-count ordering for homophonous names, compound surnames, and ambiguity reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxiaopeng-zgci](https://clawhub.ai/user/zhangxiaopeng-zgci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to sort Chinese person-name lists for rosters, address books, and text-processing workflows where Chinese surname and given-name ordering conventions matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper depends on pypinyin and suggests an unpinned pip install when the dependency is missing.

Mitigation: Install it in a virtual environment and pin the pypinyin version when reproducible runs are required.

Risk: Rare characters can fall back to estimated stroke counts, and names with identical pinyin may remain ambiguous.

Mitigation: Review ambiguity warnings and add project-specific stroke-count or tie-break rules before relying on the ordering for formal records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxiaopeng-zgci/skills/chinese-name-pinyin-sort)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and sorted-name text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include numbering, pinyin annotations, surname grouping, and homophone ambiguity warnings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
