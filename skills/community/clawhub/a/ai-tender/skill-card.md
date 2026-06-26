## Description: <br>
AI-Tender automates tender document parsing and extracts bid requirements from user-provided tender files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengcheng8632](https://clawhub.ai/user/chengcheng8632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and proposal teams use AI-Tender to parse tender files, classify industry context, extract bid requirements, check completeness and compliance, and generate a previewable PDF result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and local skill files may be exposed by the LAN-accessible preview server. <br>
Mitigation: Run the skill in a restricted environment, disable or contain the preview server for confidential work, and bind preview access to localhost only. <br>
Risk: Tender documents are sent to the user-configured LLM provider for parsing. <br>
Mitigation: Use only approved LLM endpoints and avoid processing confidential bid material unless that provider is authorized for the data. <br>
Risk: API keys configured in env_config.md can be exposed in shared or network-accessible environments. <br>
Mitigation: Protect env_config.md, avoid committing credentials, rotate keys regularly, and keep runtime directories out of shared access paths. <br>
Risk: Unpinned or unreviewed dependencies may introduce production risk. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub AI-Tender release page](https://clawhub.ai/chengcheng8632/ai-tender) <br>
- [Publisher profile](https://clawhub.ai/user/chengcheng8632) <br>
- [Biaoshu Mofang product site](https://biaoshu.supcon.com/?scene=01010040) <br>
- [README](artifact/README.md) <br>
- [Security statement](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, parsed tender analysis, and a generated PDF report or preview URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-configured OpenAI-compatible LLM endpoint and writes a local PDF result.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
