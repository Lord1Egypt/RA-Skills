## Description: <br>
Compress academic abstracts to meet strict word limits while preserving key information, scientific accuracy, and readability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, editors, and academic writers use this skill to shorten abstracts for journal submissions, conference applications, and grant proposals while preserving core scientific claims. It can check word counts, apply conservative, balanced, or aggressive trimming, and emit compressed abstracts as JSON, plain text, or a local output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected output paths can overwrite an existing file. <br>
Mitigation: Choose output paths deliberately and avoid pointing the tool at files you do not want replaced. <br>
Risk: Automated abstract compression can remove context or change scientific emphasis. <br>
Mitigation: Review the trimmed abstract against the original before using it in a submission. <br>
Risk: Local file input may expose sensitive draft text to the runtime environment. <br>
Mitigation: Use non-sensitive abstracts when possible and run the script only in trusted local environments. <br>


## Reference(s): <br>
- [Abstract Trimmer Guidelines](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/abstract-trimmer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or plain text, with optional local file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided abstract text or a local text file and may write a user-specified output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
