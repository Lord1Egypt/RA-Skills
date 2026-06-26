## Description: <br>
Looks up English words, returns Chinese definitions, phonetics and part of speech, and generates two example sentences for vocabulary learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohaiyan3-tal](https://clawhub.ai/user/mohaiyan3-tal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up English vocabulary, get Chinese meanings, and produce short example sentences for language learning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The built-in word list and template-generated examples are limited and may not be authoritative for important vocabulary decisions. <br>
Mitigation: Treat results as vocabulary-learning assistance and verify meanings or examples against an authoritative dictionary when accuracy matters. <br>
Risk: Future external dictionary API integrations could expose credentials if keys are placed in shared files. <br>
Mitigation: Store API keys in environment variables or secret storage and avoid committing them with the skill files. <br>


## Reference(s): <br>
- [Youdao Dictionary API](https://dict.youdao.com/jsonresult?q={word}) <br>
- [Oxford Dictionaries Developer API](https://developer.oxforddictionaries.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text dictionary output with a JSON block from the CLI script; Markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a small built-in dictionary and template-generated fallback examples for unknown words.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
