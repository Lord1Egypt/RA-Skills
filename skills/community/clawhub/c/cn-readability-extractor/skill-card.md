## Description: <br>
Extracts readable article text, title, and description from a URL while filtering common page chrome such as ads, navigation, scripts, and styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing agents use this skill to fetch a web page by URL and produce a cleaner text representation for summarization, analysis, or downstream extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches arbitrary URLs, so agents may retrieve untrusted or unexpected web content. <br>
Mitigation: Use it with URLs from trusted workflows and review extracted text before relying on it for decisions or downstream automation. <br>
Risk: Extracted page text can omit context or truncate long content. <br>
Mitigation: Check the source page when completeness matters, especially for legal, financial, medical, or policy-sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-readability-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text output with extracted metadata and readable page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches one URL at a time and truncates extracted content above 5000 characters.] <br>

## Skill Version(s): <br>
1.3.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
