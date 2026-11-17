## Description:

English dictionary lookup tool for querying English words to get Chinese definitions and two example sentences for vocabulary learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohaiyan3-tal](https://clawhub.ai/user/mohaiyan3-tal)

### License/Terms of Use:


## Use Case:

External users and language learners use this skill to look up English word meanings in Chinese, review pronunciation and part of speech, and get simple example sentences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Definitions may be incomplete because the bundled word list is small and fallback entries are not authoritative.

Mitigation: Use the skill for lightweight vocabulary assistance and verify important meanings with an authoritative dictionary.

Risk: External dictionary API behavior is outside the bundled local skill and may change when users extend the script.

Mitigation: Review and configure any external API integration separately before relying on it for broad or authoritative dictionary results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohaiyan3-tal/skills/english-dict)
- [Youdao dictionary JSON endpoint](https://dict.youdao.com/jsonresult?q={word})
- [Oxford Dictionaries API](https://developer.oxforddictionaries.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Plain text dictionary output followed by JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes built-in fallback output when a word is not in the small local dictionary.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
