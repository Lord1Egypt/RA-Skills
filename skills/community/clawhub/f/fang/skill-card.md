## Description: <br>
Fang audits skill directories for potential environment variable theft using a local static scan and optional OpenAI-compatible LLM review, then reports risk ratings for suspicious files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Fang to audit installed, downloaded, or workspace skill directories for patterns that may expose environment variables or secrets. It helps triage findings with HIGH, MEDIUM, LOW, and CLEAN ratings before a skill is run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM review can send scanned script content to the configured provider or endpoint. <br>
Mitigation: Use the default local static scan for sensitive or proprietary code; enable --llm-key only with a trusted provider or local endpoint and a narrow target directory. <br>


## Reference(s): <br>
- [Fang ClawHub listing](https://clawhub.ai/goog/fang) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown/text threat report with optional raw JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static mode scans Python and shell files locally; optional LLM mode reviews script contents from selected file types and truncates each file to 3000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
