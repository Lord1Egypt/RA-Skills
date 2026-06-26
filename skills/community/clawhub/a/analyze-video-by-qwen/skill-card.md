## Description: <br>
Analyzes local or remote videos with Qwen 3.5 Plus using a configurable prompt and frame sampling rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fackee](https://clawhub.ai/user/fackee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run video understanding tasks such as scene description, object and action identification, and video summarization for local files or public video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected videos to Alibaba Cloud DashScope/Qwen for analysis. <br>
Mitigation: Analyze only videos that are approved for that provider, and confirm user consent and data handling requirements before use. <br>
Risk: The bundled local settings allow broad python3 and chmod command execution. <br>
Mitigation: Remove or narrow those permissions before routine installation or deployment. <br>
Risk: The DashScope dependency is unpinned, which can introduce unreviewed dependency changes. <br>
Mitigation: Pin the dashscope package version and review updates before adopting them. <br>
Risk: Provider API use can consume quota or incur charges. <br>
Mitigation: Use a dedicated DashScope key with appropriate quota and spend monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fackee/analyze-video-by-qwen) <br>
- [DashScope API endpoint used by the skill](https://dashscope.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text analysis printed to stdout, with command examples and configuration guidance in Markdown documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a local file path or HTTP(S) URL, an optional prompt, and an optional frame sampling rate.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
