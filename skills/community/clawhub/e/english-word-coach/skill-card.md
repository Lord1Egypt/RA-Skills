## Description: <br>
English Word Coach helps users analyze English vocabulary, maintain a local vocabulary library, and run spaced-repetition daily review sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hushenglang](https://clawhub.ai/user/hushenglang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and learners use this skill to collect English words, receive Chinese-language vocabulary explanations with professional example phrases, and review saved words through a simple spaced-repetition workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local Markdown study files in the current working directory. <br>
Mitigation: Use it in a workspace where memory/ENGLISH_WORDS.md and daily review files are expected, and review file changes as part of normal agent output review. <br>
Risk: Vocabulary notes may contain sensitive personal or work-related context if users include it in examples or notes. <br>
Mitigation: Avoid putting sensitive personal information, confidential project names, credentials, or private business details into vocabulary notes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown responses and local Markdown study files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates memory/ENGLISH_WORDS.md and memory/DAILY_REVIEW_YYYYMMDD.md in the current working directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
