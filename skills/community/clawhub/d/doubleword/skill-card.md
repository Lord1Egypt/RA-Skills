## Description: <br>
Submit and manage asynchronous batch AI inference jobs via the Doubleword API, including OpenAI-compatible endpoints, tool calling, structured outputs, and JSONL batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjb157](https://clawhub.ai/user/pjb157) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prepare JSONL request files, submit Doubleword batch jobs, monitor status, and retrieve results for high-volume asynchronous inference workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch JSONL files may contain secrets, regulated data, or other sensitive inputs that will be uploaded to Doubleword. <br>
Mitigation: Review batch files before upload and avoid secrets or regulated data unless the user is authorized to process that data with Doubleword. <br>
Risk: Large batch jobs can spend account credits unexpectedly. <br>
Mitigation: Use the Doubleword cost estimator and check expected token usage before creating large batches. <br>
Risk: API keys can be exposed if pasted into prompts, files, or shell history. <br>
Mitigation: Store DOUBLEWORD_API_KEY securely in an environment variable or secrets manager and do not commit it to source control. <br>
Risk: The optional autobatcher package is a third-party dependency. <br>
Mitigation: Verify and pin the autobatcher dependency before installing it in production environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pjb157/doubleword) <br>
- [Doubleword Batch API Reference](references/api_reference.md) <br>
- [Getting Started with Doubleword Batch API](references/getting_started.md) <br>
- [Doubleword Batch API Pricing](references/pricing.md) <br>
- [Doubleword Console](https://app.doubleword.ai/) <br>
- [Doubleword API base URL](https://api.doubleword.ai/v1) <br>
- [autobatcher](https://github.com/doublewordai/autobatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes JSONL batch file guidance, API request examples, status handling, result parsing, pricing considerations, and optional autobatcher setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
