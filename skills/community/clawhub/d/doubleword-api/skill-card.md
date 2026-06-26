## Description: <br>
Create and manage batch inference jobs using the Doubleword API for asynchronous JSONL-based AI inference workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjb157](https://clawhub.ai/user/pjb157) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create JSONL batch request files, upload them to Doubleword, create asynchronous batch jobs, poll progress, retrieve results, and retry failed requests for large or cost-sensitive inference workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch files may contain prompts or request bodies that are sent to the external Doubleword API. <br>
Mitigation: Review and redact JSONL files before upload, and confirm that Doubleword is the intended provider for the workload. <br>
Risk: API-key use and submitted jobs may affect account usage or cost. <br>
Mitigation: Use the intended Doubleword API key, choose the appropriate completion window, and monitor request counts, batch status, and output or error files. <br>
Risk: Invalid or oversized JSONL input can fail validation or require retries. <br>
Mitigation: Validate each JSONL line locally, keep files under the documented 200MB limit, and split large workloads into multiple batches. <br>


## Reference(s): <br>
- [Doubleword Batch API Reference](references/api_reference.md) <br>
- [Doubleword API skill page](https://clawhub.ai/pjb157/doubleword-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with JSON, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on JSONL request files, Doubleword API keys, curl commands, batch IDs, file IDs, and result or error JSONL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
