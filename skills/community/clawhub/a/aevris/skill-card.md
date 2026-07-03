## Description: <br>
Scan every prompt for injection attacks, verify AI outputs for manipulation, intercept agent actions before execution, and detect MCP tool poisoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aevris-ai](https://clawhub.ai/user/aevris-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Aevris to add API-based security checks around user input, model output, tool execution, MCP tool definitions, and document ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes broad agent content, including prompts, outputs, tool metadata, action details, and document text, to a third-party API. <br>
Mitigation: Use it only after reviewing the vendor's privacy, retention, and compliance terms; redact sensitive content and require clear opt-in for confidential or regulated workflows. <br>
Risk: The skill requires the AEVRIS_API_KEY credential. <br>
Mitigation: Store the key in a managed secret store or environment variable, restrict access to trusted runtimes, and rotate it if exposure is suspected. <br>
Risk: Scanning depends on an external API being reachable and trusted at decision time. <br>
Mitigation: Define fail-closed behavior for blocked or unavailable scans in high-risk workflows and monitor API status and quota before relying on the checks. <br>


## Reference(s): <br>
- [Aevris homepage](https://aevris.ai) <br>
- [Aevris API documentation](https://aevris.ai/docs) <br>
- [Aevris comparison](https://aevris.ai/compare) <br>
- [ClawHub release page](https://clawhub.ai/aevris-ai/aevris) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoint descriptions, curl examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEVRIS_API_KEY and sends scanned content to the Aevris API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
