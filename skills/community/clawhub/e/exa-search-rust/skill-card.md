## Description: <br>
Exa Search (Rust) lets agents run Exa neural web search, find similar pages, and fetch URL contents through a native Rust binary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Prompt-Surfer](https://clawhub.ai/user/Prompt-Surfer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to search the web, discover similar pages, and retrieve page contents from Exa for research and information-gathering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and requested URLs are sent to Exa. <br>
Mitigation: Use the skill only for inputs suitable for Exa processing and avoid submitting sensitive or restricted information. <br>
Risk: The skill requires an EXA_API_KEY stored in the agent workspace environment. <br>
Mitigation: Use a revocable key, keep the workspace .env file private, and avoid sharing command transcripts that expose environment values. <br>
Risk: The installed skill path must match the expected workspace location before invocation. <br>
Mitigation: Verify the installed path and binary before running the skill, especially after installation or upgrade. <br>


## Reference(s): <br>
- [ClawHub listing for Exa Search (Rust)](https://clawhub.ai/Prompt-Surfer/exa-search-rust) <br>
- [Exa AI](https://exa.ai) <br>
- [Exa Python SDK](https://github.com/exa-labs/exa-py) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw Exa plugin reference](https://github.com/Prompt-Surfer/openclaw-exa-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON on stdout with a formatted Markdown field for search and similar-page results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful responses include ok, action, results, optional cost data, and, for search-style actions, formatted Markdown; errors are emitted to stderr with exit code 1.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
